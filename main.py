import json
from subprocess import run
from sys import argv
from typing import Any, List, Optional


class TmuxPane:
    cmds: Optional[List[str]]

    def __init__(self, cmds={}):
        cmds = cmds.get("cmds")
        self.cmds = cmds

    def __repr__(self):
        return f"TmuxPane({self.cmds})"

    def setup(self):
        """
        TODO.
        Run commands if any.
        """
        pass


class TmuxWindow:
    name: str
    panes: List[TmuxPane]

    def __init__(self, name: str, panes=None):
        self.name = name
        self.panes = [TmuxPane(i) for i in panes] if panes is not None else [TmuxPane()]

    def __repr__(self):
        return f"TmuxWindow('{self.name}', {self.panes})"

    def setup(self, session_name: str, idx: int, rename: bool = False):
        """
        Run the commands to setup window
        """
        if rename:
            run(["tmux", "rename-window", "-t", f"{session_name}:{idx}", self.name])
        else:
            run(["tmux", "new-window", "-t", f"{session_name}:{idx}", "-n", self.name])

        for pane in self.panes:
            pane.setup()


class TmuxSession:
    name: str
    windows: List[TmuxWindow]

    def __init__(self, name: str, windows: Any):
        self.name = name
        self.windows = [TmuxWindow(**i) for i in windows]

    def __repr__(self):
        return f"TmuxSession({self.name}, {self.windows})"

    def setup(self):
        """
        Setup the entire session.
        """
        run(["tmux", "new-session", "-d", "-s", self.name])
        for idx, window in enumerate(self.windows):
            if idx == 0:
                window.setup(self.name, rename=True, idx=idx)
                continue
            window.setup(self.name, idx=idx)


# python main.py ~/path/to/config.json
if __name__ == "__main__":
    file_path = argv[1]
    with open(file_path) as f:
        sessions = json.load(f)
        for session in sessions:
            tmux_session = TmuxSession(**session)
            tmux_session.setup()
            print(tmux_session)
