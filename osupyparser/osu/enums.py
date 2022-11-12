from __future__ import annotations

from enum import Enum
from enum import IntEnum
from enum import IntFlag
from typing import Optional


class Mode(IntEnum):
    OSU = 0
    TAIKO = 1
    CATCH = 2
    MANIA = 3


class EventType(IntEnum):
    BACKGROUND = 0
    VIDEO = 1
    BREAK = 2
    COLOUR = 3
    SPRITE = 4
    SAMPLE = 5
    ANIMATION = 6
    STORYBOARD_COMMAND = 7

    @staticmethod
    def from_str(value: str) -> Optional[EventType]:

        if value.isdigit():
            return EventType(int(value))

        if value.upper() not in EventType.__members__:
            return

        return EventType[value.upper()]


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


class ITimeSignature:
    def __init__(self, numerator: int):

        if numerator < 1:
            raise ValueError("The numerator of a time signature must be positive.")

        self.numerator = numerator

    def __str__(self):
        return self.to_str()

    def to_str(self) -> str:
        return f"{self.numerator}/4"

    @staticmethod
    def from_str(value: str) -> ITimeSignature:
        return ITimeSignature(int(value))


class TimeSignature:
    SIMPLE_TRIPLE = ITimeSignature(3)
    SIMPLE_QUADRUPLE = ITimeSignature(4)

    def __new__(cls, numerator: int):
        if numerator == 3:
            return TimeSignature.SIMPLE_TRIPLE

        if numerator == 4:
            return TimeSignature.SIMPLE_QUADRUPLE

        return ITimeSignature(numerator)


class OverlayPosition(Enum):
    NO_CHANGE = "NoChange"
    BELOW = "Below"
    ABOVE = "Above"
