from __future__ import annotations

from enum import Enum
from enum import IntEnum
from enum import IntFlag


class Mode(IntEnum):
    OSU = 0
    TAIKO = 1
    CATCH = 2
    MANIA = 3


class CurveType(Enum):
    CATMULL = "C"
    BEZIER = "B"
    LINEAR = "L"
    PERFECT_CURVE = "P"


class Effects(IntFlag):
    NONE = 0
    KIAI = 1 << 0
    OMIT_FIRST_BAR_LINE = 1 << 3


class HitObjectType(IntFlag):
    CIRCLE = 1 << 0
    SLIDER = 1 << 1
    NEW_COMBO = 1 << 2
    SPINNER = 1 << 3
    COMBO_OFFSET = (1 << 4) | (1 << 5) | (1 << 6)
    HOLD = 1 << 7


class HitSoundType(IntFlag):
    NORMAL = 0
    WHISTLE = 1 << 1
    FINISH = 1 << 2
    CLAP = 1 << 3


class SampleSet(IntEnum):
    NONE = 0
    NORMAL = 1
    SOFT = 2
    DRUM = 3

    def to_str(self) -> str:
        return {
            SampleSet.NONE: "None",
            SampleSet.NORMAL: "Normal",
            SampleSet.SOFT: "Soft",
            SampleSet.DRUM: "Drum",
        }[self]

    @staticmethod
    def from_str(val: str) -> SampleSet:
        return {
            "None": SampleSet.NONE,
            "Normal": SampleSet.NORMAL,
            "Soft": SampleSet.SOFT,
            "Drum": SampleSet.DRUM,
        }[val]


class TaikoColor(IntEnum):
    RED = 0
    BLUE = 1


class TimeSignature(IntEnum):
    SIMPLE_TRIPLE = 3
    SIMPLE_QUADRUPLE = 4


class OverlayPosition(Enum):
    NO_CHANGE = "NoChange"
    BELOW = "Below"
    ABOVE = "Above"
