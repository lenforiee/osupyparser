from __future__ import annotations

from pydantic import BaseModel


# TODO: add some fancy converters for colour format types
class ColourRGBA(BaseModel):
    red: int
    green: int
    blue: int
    alpha: int
