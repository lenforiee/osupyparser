from __future__ import annotations

from pydantic import BaseModel

from osupyparser.osu.models.hit_objects import HitObjectCircle
from osupyparser.osu.models.hit_objects import HitObjectHold
from osupyparser.osu.models.hit_objects import HitObjectSlider
from osupyparser.osu.models.hit_objects import HitObjectSpinner
from osupyparser.osu.models.sections.colours import ColoursSection
from osupyparser.osu.models.sections.difficulty import DifficultySection
from osupyparser.osu.models.sections.editor import EditorSection
from osupyparser.osu.models.sections.events import EventsSection
from osupyparser.osu.models.sections.general import GeneralSection
from osupyparser.osu.models.sections.metadata import MetadataSection
from osupyparser.osu.models.timing_point import TimingPoint


class OsuBeatmapFile(BaseModel):
    format_version: int
    file_hash: str

    general: GeneralSection
    editor: EditorSection
    metadata: MetadataSection
    difficulty: DifficultySection
    events: EventsSection
    timing_points: list[TimingPoint]
    colours: ColoursSection | None = None
    hit_objects: list[
        HitObjectCircle | HitObjectSlider | HitObjectSpinner | HitObjectHold
    ]

    minimum_bpm: float
    maximum_bpm: float

    circle_count: int
    slider_count: int
    spinner_count: int
    hold_count: int

    max_combo: int
    play_time: int
    break_time: int
    drain_time: int
