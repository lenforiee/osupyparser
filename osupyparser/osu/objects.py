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
    normal: Optional[str] = ""
    additional: Optional[str] = ""
    custom_sample_index: Optional[int] = ""
    volume: Optional[int] = 0
    filename: Optional[Any] = None

@dataclass
class Edge:
    """A additional class for slider edges."""
    sound_types: List[str]
    additions: Optional[Additions]

@dataclass
class TimingPoint:
    """Represents a standalone timing point."""
    offset: float
    beat_length: float
    time_signature: int
    sample_set_id: int
    custom_sample_index: int
    sample_volume: int
    timing_change: Optional[bool]
    kiai_time_active: Optional[bool]
    velocity: Optional[float] = None
    bpm: Optional[float] = None

@dataclass
class HitObject:
    """Subclass representing standalone hitobject."""
    pos: Position
    start_time: int
    new_combo: bool
    sound_enum: int

@dataclass
class Circle(HitObject):
    """Represents one circle object."""
    # Circle is basically normal hitobject
    # but I wanted it to be its own type.
    additions: Optional[Additions] = None

@dataclass
class Spinner(HitObject):
    """Represents one spinner object."""
    end_time: int
    additions: Optional[Additions] = None

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
    additions: Optional[Additions] = None
