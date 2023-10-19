import json
from subprocess import run
from sys import argv
from typing import List, Optional


class TmuxPane:
    name: str

    def __init__(self, name: str = "zsh"):
        self.name = name

    def __repr__(self):
        return f"TmuxPane('{self.name}')"

    def setup(self, idx: int):
        if idx == 0:
            pass


class TmuxWindow:
    name: str
    panes: List[TmuxPane]

    def __init__(self, name: str, panes: Optional[List[TmuxPane]] = None):
        self.name = name
        self.panes = panes if panes is not None else [TmuxPane()]

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
            for idx, pane in enumerate(self.panes):
                pane.setup(idx)


class TmuxSession:
    name: str
    windows: List[TmuxWindow]

    def __init__(self, name: str, windows: List[TmuxWindow]):
        self.name = name
        self.windows = windows

    def __repr__(self):
        return f"TmuxSession({self.name}, {self.windows})"

    def setup(self):
        """
        Setup the entire session.
        """
        # create session
        run(["tmux", "new-session", "-d", "-s", self.name])

        # setup session windows
        for idx, window in enumerate(self.windows):
            if idx == 0:
                window.setup(self.name, rename=True, idx=idx)
                continue
            window.setup(self.name, idx=idx)


# python main.py ~/path/to/config.json
if __name__ == "__main__":
    file_path = argv[1]
    with open(file_path) as f:
        sessions = json.load(f)  # expect array of tmux-session objects
        for session in sessions:
            tmux_session = TmuxSession(**session)
