from __future__ import annotations

from enum import IntEnum
from enum import IntFlag


class Mode(IntEnum):
    STANDARD = 0
    TAIKO = 1
    CATCH = 2
    MANIA = 3


class Mods(IntFlag):
    NOMOD = 0
    NOFAIL = 1 << 0
    EASY = 1 << 1
    TOUCHSCREEN = 1 << 2
    HIDDEN = 1 << 3
    HARDROCK = 1 << 4
    SUDDENDEATH = 1 << 5
    DOUBLETIME = 1 << 6
    RELAX = 1 << 7
    HALFTIME = 1 << 8
    NIGHTCORE = 1 << 9
    FLASHLIGHT = 1 << 10
    AUTOPLAY = 1 << 11
    SPUNOUT = 1 << 12
    AUTOPILOT = 1 << 13
    PERFECT = 1 << 14
    KEY4 = 1 << 15
    KEY5 = 1 << 16
    KEY6 = 1 << 17
    KEY7 = 1 << 18
    KEY8 = 1 << 19
    FADEIN = 1 << 20
    RANDOM = 1 << 21
    CINEMA = 1 << 22
    TARGET = 1 << 23
    KEY9 = 1 << 24
    KEYCOOP = 1 << 25
    KEY1 = 1 << 26
    KEY3 = 1 << 27
    KEY2 = 1 << 28
    SCOREV2 = 1 << 29
    MIRROR = 1 << 30

    SPEED_MODS = DOUBLETIME | NIGHTCORE | HALFTIME
    GAME_CHANGING = RELAX | AUTOPILOT


class Keys(IntFlag):
    NONE = 0
    M1 = 1 << 0
    M2 = 1 << 1
    K1 = 1 << 2 + M1
    K2 = 1 << 3 + M2
    SMOKE = 1 << 4


class TaikoKeys(IntFlag):
    NONE = 0
    LEFT_RED = 1 << 0
    LEFT_BLUE = 1 << 1
    RIGHT_RED = 1 << 2
    RIGHT_BLUE = 1 << 3


class CatchKeys(IntFlag):
    NONE = 0
    DASH = 1 << 0


class ManiaKeys(IntFlag):
    NONE = 0
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
