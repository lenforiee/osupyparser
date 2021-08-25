from dataclasses import dataclass
from enum import IntFlag

class Key(IntFlag):
    M1    = 1 << 0
    M2    = 1 << 1
    K1    = 1 << 2
    K2    = 1 << 3
    SMOKE = 1 << 4

class KeyTaiko(IntFlag):
    LEFT_DON  = 1 << 0
    LEFT_KAT  = 1 << 1
    RIGHT_DON = 1 << 2
    RIGHT_KAT = 1 << 3

class KeyMania(IntFlag):
    K1 = 1 << 0
    K2 = 1 << 1
    K3 = 1 << 2
    K4 = 1 << 3
    K5 = 1 << 4
    K6 = 1 << 5
    K7 = 1 << 6
    K8 = 1 << 7
    K9 = 1 << 8
    K10 = 1 << 9
    K11 = 1 << 10
    K12 = 1 << 11
    K13 = 1 << 12
    K14 = 1 << 13
    K15 = 1 << 14
    K16 = 1 << 15
    K17 = 1 << 16
    K18 = 1 << 17

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