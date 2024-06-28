from __future__ import annotations

from pydantic import BaseModel


# This constant can be fixed therefore we can't define literal enums
class TimeSignature(BaseModel):
    numerator: int

    def __str__(self):
        return f"{self.numerator}/4"

    @staticmethod
    def SimpleTriple():
        return TimeSignature(numerator=3)

    @staticmethod
    def SimpleQuadruple():
        return TimeSignature(numerator=4)

    def __eq__(self, other):
        if not isinstance(other, TimeSignature):
            return False
        return self.numerator == other.numerator

    def __hash__(self):
        return self.numerator
