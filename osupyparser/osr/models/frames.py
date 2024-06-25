from __future__ import annotations

from pydantic import BaseModel

from osupyparser.common.maths import Vector2
from osupyparser.constants.keys import Keys


class LifeBarGraphFrame(BaseModel):
    time: int
    percentage: float


class ReplayFrame(BaseModel):
    absolute_time: int  # time since replay start
    delta_time: int  # time since last action
    position: Vector2
    keys: Keys
