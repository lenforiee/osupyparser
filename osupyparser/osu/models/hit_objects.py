from __future__ import annotations

from pydantic import BaseModel

from osupyparser.common.vector import Vector2
from osupyparser.constants.curve_type import CurveType
from osupyparser.constants.hit_object import HitObject
from osupyparser.constants.hit_sound import HitSound
from osupyparser.constants.sample_set import SampleSet


class CustomHitSample(BaseModel):
    normal_set: SampleSet = SampleSet.NONE
    addition_set: SampleSet = SampleSet.NONE
    sample_index: int = 0
    sample_volume: int = 0
    sample_filename: str = ""
    is_beatmap_sample: bool = False


class EdgeSampleBank(BaseModel):
    hit_sound_type: HitSound
    normal_set: SampleSet = SampleSet.NONE
    addition_set: SampleSet = SampleSet.NONE


class HitObjectBase(BaseModel):
    position: Vector2
    start_time: int
    hit_object_type: HitObject
    hit_sound_type: HitSound
    combo_color_offset: int
    is_new_combo: bool
    hit_sample: CustomHitSample = CustomHitSample()


class HitObjectCircle(HitObjectBase):
    pass


class HitObjectSlider(HitObjectBase):
    curve_type: CurveType
    curve_points: list[Vector2]
    slides: int  # also known as `repeat count + 1`
    repeat_count: int
    pixel_length: float
    end_time: int

    bezier_degree: int | None = None
    # edge_sample_banks: list[EdgeSampleBank] | None = None


class HitObjectSpinner(HitObjectBase):
    end_time: int


class HitObjectHold(HitObjectBase):
    end_time: int
