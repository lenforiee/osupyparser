from __future__ import annotations

from pydantic import BaseModel

from osupyparser.constants.sample_set import SampleSet
from osupyparser.constants.time_signature import TimeSignature


class TimingPoint(BaseModel):
    start_time: int
    beat_length: float
    time_signature: TimeSignature
    sample_set: SampleSet
    custom_sample_bank: int
    sample_volume: int
    timing_change: bool

    slider_velocity: float

    kiai_mode: bool
    omit_first_bar_line: bool
