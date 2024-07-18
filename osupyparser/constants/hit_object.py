from __future__ import annotations

from enum import IntFlag


class HitObject(IntFlag):
    CIRCLE = 1
    SLIDER = 1 << 1
    NEW_COMBO = 1 << 2
    SPINNER = 1 << 3
    COMBO_OFFSET = (1 << 4) | (1 << 5) | (1 << 6)
    HOLD = 1 << 7

    def is_circle(self) -> bool:
        return bool(self & HitObject.CIRCLE)

    def is_slider(self) -> bool:
        return bool(self & HitObject.SLIDER)

    def is_spinner(self) -> bool:
        return bool(self & HitObject.SPINNER)

    def is_hold(self) -> bool:
        return bool(self & HitObject.HOLD)

    def has_new_combo(self) -> bool:
        return bool(self & HitObject.NEW_COMBO)
