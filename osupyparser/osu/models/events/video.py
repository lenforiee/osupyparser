from __future__ import annotations

from pydantic import BaseModel


class Video(BaseModel):
    filename: str
    start_time: int
    x_offset: int
    y_offset: int
