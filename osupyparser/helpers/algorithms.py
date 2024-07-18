from __future__ import annotations

from osupyparser.osu.models.timing_point import TimingPoint


def timing_points_binary_search(
    timing_points: list[TimingPoint],
    time: int,
) -> TimingPoint | None:
    if not timing_points:
        return None

    if time < timing_points[0].start_time:
        return None

    if time >= timing_points[-1].start_time:
        return timing_points[-1]

    left = 0
    right = len(timing_points) - 2
    while left <= right:
        pivot = left + ((right - left) >> 1)

        if timing_points[pivot].start_time < time:
            left = pivot + 1
        elif timing_points[pivot].start_time > time:
            right = pivot - 1
        else:
            return timing_points[pivot]

    return timing_points[left - 1]
