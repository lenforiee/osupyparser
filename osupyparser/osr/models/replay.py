from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from osupyparser.common.constants.mode import Mode
from osupyparser.common.constants.mods import Mods

from osupyparser.osr.models.statistics import ReplayStatistics
from osupyparser.osr.models.frames import ReplayFrame
from osupyparser.osr.models.frames import LifeBarGraphFrame


class OsuReplayFile(BaseModel):
    mode: Mode
    osu_version: int

    beatmap_md5: str
    player_name: str
    replay_md5: str

    statistics: ReplayStatistics

    score: int
    max_combo: int
    full_combo: bool
    mods: Mods

    life_bar_graph: list[LifeBarGraphFrame]
    timestamp: datetime
    online_score_id: int

    frames: list[ReplayFrame]

    rng_seed: Optional[int] = None
    target_practice_hits: Optional[float] = None
