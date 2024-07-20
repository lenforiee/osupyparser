from __future__ import annotations

import math

from osupyparser.helpers import algorithms
from osupyparser.osu.models.events.break_period import BreakPeriod
from osupyparser.osu.models.hit_objects import HitObjectCircle
from osupyparser.osu.models.hit_objects import HitObjectHold
from osupyparser.osu.models.hit_objects import HitObjectSlider
from osupyparser.osu.models.hit_objects import HitObjectSpinner
from osupyparser.osu.models.timing_point import TimingPoint


def calculate_slider_end_time(
    start_time: int,
    slides: int,
    pixel_length: float,
    slider_multiplier: float,
    slider_velocity: float,
    timing_beat_len: float,
) -> int:

    return round(
        start_time
        + slides
        * pixel_length
        / ((100 * slider_multiplier * slider_velocity) / timing_beat_len),
    )


def calculate_play_time(
    hit_objects: list[
        HitObjectCircle | HitObjectSlider | HitObjectSpinner | HitObjectHold
    ],
) -> int:
    if not hit_objects:
        return 0

    first_object = hit_objects[0]
    last_object = hit_objects[-1]

    if isinstance(last_object, HitObjectCircle):
        end_time = last_object.start_time
    else:
        end_time = last_object.end_time

    return math.floor((end_time - first_object.start_time) / 1000)


def calculate_break_time(break_periods: list[BreakPeriod] | None) -> int:
    if break_periods is None:
        return 0

    break_time = 0

    for break_period in break_periods:
        break_time += break_period.end_time - break_period.start_time

    return math.floor(break_time / 1000)


def calculate_drain_time(
    play_time: int,
    break_time: int,
) -> int:
    return play_time - break_time


# TODO: those calculations are +/-3 off for catch and taiko
def calculate_maximum_beatmap_combo(
    hit_objects: list[
        HitObjectCircle | HitObjectSlider | HitObjectSpinner | HitObjectHold
    ],
    timing_points: list[TimingPoint],
    slider_multiplier: float,
    slider_tick_rate: float,
    file_version: int,
) -> int:
    computed_maximum_combo = 0

    for hit_object in hit_objects:
        if not isinstance(hit_object, HitObjectSlider):
            computed_maximum_combo += 1
            continue

        timing_point = algorithms.timing_points_binary_search(
            timing_points,
            hit_object.start_time,
        )
        sv_multiplier = 1.0

        if timing_point is not None:
            sv_multiplier = timing_point.slider_velocity

        px_per_beat = slider_multiplier * 100.0 * sv_multiplier
        if file_version < 8:
            px_per_beat /= sv_multiplier

        num_beats = (hit_object.pixel_length * hit_object.slides) / px_per_beat

        ticks = math.ceil(
            (num_beats - 0.1) / hit_object.slides * slider_tick_rate,
        )

        ticks = ((ticks - 1) * hit_object.slides) + hit_object.slides + 1

        computed_maximum_combo += max(0, ticks)

    return computed_maximum_combo
