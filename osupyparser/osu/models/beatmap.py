from __future__ import annotations

from pydantic import BaseModel

from osupyparser.osu.models.sections.difficulty import DifficultySection
from osupyparser.osu.models.sections.editor import EditorSection
from osupyparser.osu.models.sections.events import EventsSection
from osupyparser.osu.models.sections.general import GeneralSection
from osupyparser.osu.models.sections.metadata import MetadataSection


class OsuBeatmapFile(BaseModel):
    format_version: int

    general: GeneralSection
    editor: EditorSection
    metadata: MetadataSection
    difficulty: DifficultySection
    # events: EventsSection
    # timing_points: ...
    # colours: ...
    # hit_objects: ...

    # TODO: add custom extras
