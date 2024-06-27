from __future__ import annotations

from pydantic import BaseModel


class MetadataSection(BaseModel):
    title: str
    title_unicode: str
    artist: str
    artist_unicode: str
    creator: str
    version: str
    source: str
    tags: list[str]
    beatmap_id: int
    beatmap_set_id: int
