from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..shared.maths import Vector2
from .enums import CatchKeys
from .enums import Keys
from .enums import ManiaKeys
from .enums import TaikoKeys


@dataclass
class LifeBarFrame:
    time: int
    percentage: float


@dataclass
class ReplayFrame:
    position: Vector2
    delta: int
    time: int
    osu_keys: Optional[Keys] = None
    taiko_keys: Optional[TaikoKeys] = None
    catch_keys: Optional[CatchKeys] = None
    mania_keys: Optional[ManiaKeys] = None
