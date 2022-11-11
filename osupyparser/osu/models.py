from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

from ..shared.maths import Vector2
from .enums import CurveType
from .enums import Effects
from .enums import HitSoundType
from .enums import SampleSet
from .enums import TaikoColor
from .enums import TimeSignature


@dataclass
class RGB:
    r: int
    g: int
    b: int


@dataclass
class BreakEvent:
    start_time: int
    end_time: int


@dataclass
class Background:
    filename: str
    x_offset: int
    y_offset: int


@dataclass
class Video:
    start_time: int
    filename: str
    x_offset: int
    y_offset: int


@dataclass
class TimingPoint:
    offset: int
    beat_length: float
    time_signature: TimeSignature
    sample_set: SampleSet
    custom_sample_set: int
    volume: int
    inherited: bool
    effects: Effects
    bpm: float
    velocity: float


@dataclass
class Extras:
    sample_set: SampleSet
    addition_set: SampleSet
    custom_index: int
    volume: int
    sample_filename: str


@dataclass
class HitObject:
    position: Vector2
    start_time: int
    end_time: int
    hit_sound: HitSoundType
    extras: Optional[Extras]
    is_new_combo: bool
    combo_offset: int

    def distance_from(self, other: HitObject) -> float:
        return self.position.distance(other.position)


### osu!standard hitobjects ###
class Circle(HitObject):
    pass


class Spinner(HitObject):
    pass


@dataclass
class Slider(HitObject):
    curve_type: CurveType
    slider_points: list[Vector2]
    repeats: int
    pixel_length: float
    edge_hitsounds: Optional[list[HitSoundType]]
    edge_additions: Optional[list[tuple[SampleSet, SampleSet]]]


### osu!taiko hitobjects ###
class TaikoDrumroll(Slider):
    @property
    def is_big(self) -> bool:
        return bool(self.hit_sound & HitSoundType.FINISH)


class TaikoHit(Circle):
    @property
    def is_big(self) -> bool:
        return bool(self.hit_sound & HitSoundType.FINISH)

    @property
    def color(self) -> TaikoColor:
        if (
            self.hit_sound & HitSoundType.WHISTLE  # type: ignore
            or self.hit_sound & HitSoundType.CLAP
        ):
            return TaikoColor.BLUE

        return TaikoColor.RED


class TaikoSpinner(Spinner):
    pass


### osu!catch hitobjects ###
class CatchBananaRain(Spinner):
    pass


class CatchFruit(Circle):
    pass


class CatchJuiceStream(Slider):
    pass


### osu!mania hitobjects ###
class ManiaNote(Circle):
    def set_column(self, count: int, column: int):
        width = 512.0 / count
        x = int(math.floor(column * width))
        self.position = Vector2(x, 0)

    def get_column(self, count: int) -> int:
        width = 512.0 / count
        return int(math.floor(self.position.x / width))


class ManiaHoldNote(ManiaNote):
    pass
