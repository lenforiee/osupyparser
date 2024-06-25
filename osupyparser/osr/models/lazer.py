from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from osupyparser.constants.grade import Grade


# TODO: integrate lazer-like models to work with stable-legacy enums
class OsuReplayLazerMod(BaseModel):
    acronym: str
    settings: dict[str, Any] = {}


# TODO: work out which of these doesn't have to be nullable
class OsuReplayLazerStatistics(BaseModel):
    miss: int | None = None
    meh: int | None = None
    ok: int | None = None
    good: int | None = None
    great: int | None = None
    perfect: int | None = None
    small_tick_miss: int | None = None
    small_tick_hit: int | None = None
    large_tick_miss: int | None = None
    large_tick_hit: int | None = None
    small_bonus: int | None = None
    large_bonus: int | None = None
    ignore_miss: int | None = None
    ignore_hit: int | None = None
    combo_break: int | None = None
    slider_tail_hit: int | None = None
    legacy_combo_increase: int | None = None


class OsuReplayLazerData(BaseModel):
    online_id: int = -1
    mods: list[OsuReplayLazerMod]
    statistics: OsuReplayLazerStatistics
    maximum_statistics: OsuReplayLazerStatistics
    client_version: str
    user_id: int = -1
    rank: Grade | None = None
    total_score_without_mods: int | None = None
