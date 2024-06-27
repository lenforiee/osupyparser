from __future__ import annotations

from pydantic import BaseModel


class BreakPeriod(BaseModel):
    start_time: int
    end_time: int
