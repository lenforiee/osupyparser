# -*- coding: utf-8 -*-
from typing import List
from typing import Optional
from typing import Any
from dataclasses import dataclass

@dataclass
class Position:
    """A (x, y) coordinates class."""
    x: int
    y: int

@dataclass
class Additions:
    """Represents a additions to hitobject class."""
    sample: Optional[str] = ""
    additional_sample: Optional[str] = ""
    custom_sample_index: Optional[int] = ""
    hitsound_volume: Optional[int] = 0
    hitsound: Optional[Any] = None

@dataclass
class Edge:
    """A additional class for slider edges."""
    sound_types: List[str]
    additions: Additions

@dataclass
class TimingPoint:
    """Represents a standalone timing point."""
    offset: int
    beat_length: float
    velocity: Optional[float]
    bpm: Optional[float]
    time_signature: int
    sample_set_id: int
    custom_sample_index: int
    sample_volume: int
    timing_change: bool
    kiai_time_active: Optional[bool]

@dataclass
class HitObject:
    """Subclass representing standalone hitobject."""
    pos: Position
    start_time: int
    new_combo: bool
    sound_types: List[str]
    additions: Optional[Additions]

@dataclass
class Circle(HitObject):
    """Represents one circle object."""
    # Circle is basically normal hitobject
    # but I wanted it to be its own type.

@dataclass
class Spinner(HitObject):
    """Represents one spinner object."""
    end_time: int

@dataclass
class Slider(HitObject):
    """Represents one slider object."""
    repeat_count: int
    pixel_length: int
    edges: list[Edge]
    points: List[Position]
    duration: int
    end_time: int
    curve_type: str
    end_position: Optional[Position]
