from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from osupyparser.constants.grade import Grade
from osupyparser.constants.hit_result import HitResult


# TODO: integrate lazer-like models to work with stable-legacy enums
class OsuReplayLazerMod(BaseModel):
    acronym: str
    settings: dict[str, Any] = {}


class OsuReplayLazerData(BaseModel):
    online_id: int = -1
    mods: list[OsuReplayLazerMod]
    statistics: dict[HitResult, int]
    maximum_statistics: dict[HitResult, int]
    client_version: str
    user_id: int = -1
    rank: Grade | None = None
    total_score_without_mods: int | None = None
