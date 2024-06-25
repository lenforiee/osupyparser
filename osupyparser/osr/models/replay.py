from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from osupyparser.constants.grade import Grade
from osupyparser.constants.mode import Mode
from osupyparser.constants.mods import Mods

from osupyparser.osr.models.statistics import ReplayStatistics
from osupyparser.osr.models.frames import ReplayFrame
from osupyparser.osr.models.frames import LifeBarGraphFrame


class OsuReplayFileLzma(BaseModel):
    frames: list[ReplayFrame]
    skip_offset: int
    rng_seed: Optional[int] = None


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

    frames: list[ReplayFrame]
    skip_offset: int

    grade: Grade
    accuracy: float

    online_score_id: Optional[int] = None

    rng_seed: Optional[int] = None
    target_practice_hits: Optional[float] = None
