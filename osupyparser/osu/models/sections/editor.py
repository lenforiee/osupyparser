from __future__ import annotations

from pydantic import BaseModel


class EditorSection(BaseModel):
    bookmarks: list[int]
    distance_spacing: float
    beat_divisor: int
    grid_size: int
    timeline_zoom: float
