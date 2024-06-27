from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from osupyparser.constants.grade import Grade
from osupyparser.constants.mode import Mode
from osupyparser.constants.mods import Mods
from osupyparser.osr.models.frames import LifeBarGraphFrame
from osupyparser.osr.models.frames import ReplayFrame
from osupyparser.osr.models.lazer import OsuReplayLazerData
from osupyparser.osr.models.statistics import ReplayStatistics


class OsuReplayFileLzma(BaseModel):
    frames: list[ReplayFrame]
    skip_offset: int
    rng_seed: int | None = None


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

    legacy_grade: Grade
    legacy_accuracy: float

    # Can be only calculated if the replay has lazer data
    lazer_grade: Grade | None = None
    lazer_accuracy: float | None = None

    online_score_id: int | None = None

    rng_seed: int | None = None
    target_practice_hits: float | None = None

    lazer_data: OsuReplayLazerData | None = None
