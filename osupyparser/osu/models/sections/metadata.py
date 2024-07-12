from __future__ import annotations

from pydantic import BaseModel


class MetadataSection(BaseModel):
    title: str
    artist: str
    creator: str
    version: str
    source: str
    tags: list[str]

    # unicode can be missing
    title_unicode: str | None = None
    artist_unicode: str | None = None

    # back then osu relied on osu file hash and those can be nullable
    beatmap_id: int = -1
    beatmap_set_id: int = -1
