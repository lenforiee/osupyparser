from __future__ import annotations

from pydantic import BaseModel


class Background(BaseModel):
    filename: str
    x_offset: int
    y_offset: int
