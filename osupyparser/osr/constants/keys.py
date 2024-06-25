from __future__ import annotations

from enum import IntFlag


class Keys(IntFlag):
    M1 = 1 << 0
    M2 = 1 << 1
    K1 = 1 << 2 + M1
    K2 = 1 << 3 + M2
    SMOKE = 1 << 4
