from __future__ import annotations

from enum import Enum


class SampleSet(Enum):
    NONE = "None"
    NORMAL = "Normal"
    SOFT = "Soft"
    DRUM = "Drum"

    @property
    def int_enum(self) -> int:
        return _sample_set_int_enum[self]

    @staticmethod
    def from_int_enum(value: int) -> SampleSet:
        return _sample_set_from_int_enum[value]


_sample_set_int_enum = {
    SampleSet.NONE: 0,
    SampleSet.NORMAL: 1,
    SampleSet.SOFT: 2,
    SampleSet.DRUM: 3,
}

_sample_set_from_int_enum = {
    0: SampleSet.NONE,
    1: SampleSet.NORMAL,
    2: SampleSet.SOFT,
    3: SampleSet.DRUM,
}
