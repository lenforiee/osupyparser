from __future__ import annotations

from enum import Enum


class CurveType(Enum):
    BEZIER = "B"
    CATMULL = "C"
    LINEAR = "L"
    PERFECT = "P"
