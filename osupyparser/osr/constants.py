from dataclasses import dataclass

@dataclass
class ReplayFrame:
    delta: int

@dataclass
class OsuReplayFrame(ReplayFrame):
    x: int
    y: int
    keys: Key

@dataclass
class TaikoReplayFrame(ReplayFrame):
    x: int
    keys: KeyTaiko

@dataclass
class CatchReplayFrame(ReplayFrame):
    x: int
    dashing: bool

@dataclass
class ManiaReplayFrame(ReplayFrame):
    keys: KeyMania