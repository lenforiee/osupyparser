from __future__ import annotations

from pydantic import BaseModel

from osupyparser.osu.models.events.background import Background
from osupyparser.osu.models.events.break_period import BreakPeriod
from osupyparser.osu.models.events.video import Video


class EventsSection(BaseModel):
    background: Background | None = None
    videos: list[Video] = []  # NOTE: Video could have multiple instances
    break_periods: list[BreakPeriod] = []

    # TODO: storyboard stuff
