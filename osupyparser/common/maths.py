from __future__ import annotations

from pydantic import BaseModel


class Vector2(BaseModel):
    x: float
    y: float

    def __sub__(self, pos: Vector2) -> Vector2:
        return Vector2(
            x=self.x - pos.x,
            y=self.y - pos.y,
        )

    def __isub__(self, pos: Vector2) -> Vector2:
        self.x -= pos.x
        self.y -= pos.x

        return self

    def __add__(self, pos: Vector2) -> Vector2:
        return Vector2(
            x=self.x + pos.x,
            y=self.y + pos.y,
        )

    def __iadd__(self, pos: Vector2) -> Vector2:
        self.x += pos.x
        self.y += pos.x

        return self

    def __mul__(self, pos: Vector2) -> Vector2:
        return Vector2(
            x=self.x * pos.x,
            y=self.y * pos.y,
        )

    def __imul__(self, pos: Vector2) -> Vector2:
        self.x *= pos.x
        self.y *= pos.y

        return self

    def __div__(self, pos: Vector2) -> Vector2:
        return Vector2(
            x=self.x / pos.x,
            y=self.y / pos.y,
        )

    def __idiv__(self, pos: Vector2) -> Vector2:
        self.x /= pos.x
        self.y /= pos.y

        return self

    def distance(self, pos: Vector2) -> float:
        difference = self - pos
        return (difference.x**2 + difference.y**2) ** 0.5
