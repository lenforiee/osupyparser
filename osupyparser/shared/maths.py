from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Vector2:
    x: float
    y: float

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __getitem__(self, key: int) -> float:
        return self.y if key else self.x

    def __setitem__(self, key: int, value: float) -> None:
        if key:
            self.y = value
        else:
            self.x = value

    def __delitem__(self, key: int) -> None:
        if key:
            del self.y
        else:
            del self.x

    def __sub__(self, v: Vector2) -> Vector2:
        return Vector2(self.x - v.x, self.y - v.y)

    def __isub__(self, v: Vector2) -> Vector2:
        self.x -= v.x
        self.y -= v.x

        return self

    def __add__(self, v: Vector2) -> Vector2:
        return Vector2(self.x + v.x, self.y + v.y)

    def __iadd__(self, v: Vector2) -> Vector2:
        self.x += v.x
        self.y += v.x

        return self

    def __mul__(self, v: float) -> Vector2:
        return Vector2(self.x * v, self.y * v)

    def __imul__(self, v: float) -> Vector2:
        self.x *= v
        self.y *= v

        return self

    def distance(self, v: Vector2) -> float:
        subtracted = self - v
        return (subtracted.x**2 + subtracted.y**2) ** 0.5


def clamp(value: float, min: float, max: float) -> float:
    if value > max:
        return max

    if value < min:
        return min

    return value


def calculate_bpm_multiplier(beat_len: float) -> float:
    if beat_len >= 0.0:
        return 1.0

    return clamp(float(-beat_len), 10.0, 1000.0) / 100.0


def get_slider_points(lines: list[str]) -> list[Vector2]:

    points = []

    for line in lines[1:]:
        pos = line.split(":")
        if len(pos) == 2:
            points.append(Vector2(int(pos[0]), int(pos[1])))

    return points


def calculate_end_time(
    start_time: int,
    repeats: int,
    pixel_len: float,
    slider_multi: float,
    beat_len: float,
) -> int:
    duration = int(pixel_len / (100.0 * slider_multi) * repeats * beat_len)
    return start_time + duration
