from __future__ import annotations

from pydantic import BaseModel


class DifficultySection(BaseModel):
    hp_drain_rate: float
    circle_size: float
    overall_difficulty: float
    approach_rate: float
    slider_multiplier: float
    slider_tick_rate: float
