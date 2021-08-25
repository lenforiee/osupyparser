from dataclasses import dataclass

@dataclass
class ReplayFrame:
    delta: int

@dataclass
class OsuReplayFrame(ReplayFrame):
    x: int
    y: int
    keys: int

@dataclass
class TaikoReplayFrame(ReplayFrame):
    x: int
    keys: int

@dataclass
class CatchReplayFrame(ReplayFrame):
    x: int
    dashing: bool

@dataclass
class ManiaReplayFrame(ReplayFrame):
    keys: int