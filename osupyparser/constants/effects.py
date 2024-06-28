from __future__ import annotations

from enum import IntFlag


class Effects(IntFlag):
    NONE = 0
    KIAI = 1
    OMIT_FIRST_BAR_LINE = 8

    def has_kiai(self) -> bool:
        return bool(self & Effects.KIAI)

    def has_omit_first_bar_line(self) -> bool:
        return bool(self & Effects.OMIT_FIRST_BAR_LINE)
