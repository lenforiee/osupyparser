from __future__ import annotations

from pydantic import BaseModel


class EditorSection(BaseModel):
    distance_spacing: float
    beat_divisor: int
    grid_size: int

    bookmarks: list[int] | None = None
    timeline_zoom: float = 1.0  # can be null
