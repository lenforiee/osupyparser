from __future__ import annotations

from pydantic import BaseModel


class ReplayStatistics(BaseModel):
    count_300: int
    count_100: int
    count_50: int
    count_geki: int
    count_katu: int
    count_miss: int
