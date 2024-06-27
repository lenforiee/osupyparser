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
    # back then osu relied on osu file hash and those can be nullable
    beatmap_id: int = -1
    beatmap_set_id: int = -1
