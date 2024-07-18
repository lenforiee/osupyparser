from __future__ import annotations

from enum import IntFlag


class HitSound(IntFlag):
    NONE = 0
    NORMAL = 1
    WHISTLE = 2
    FINISH = 4
    CLAP = 8
