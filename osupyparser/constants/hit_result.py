from __future__ import annotations

from enum import Enum

from osupyparser.constants.mode import Mode


class HitResult(Enum):
    NONE = "none"
    MISS = "miss"
    MEH = "meh"
    OK = "ok"
    GOOD = "good"
    GREAT = "great"
    PERFECT = "perfect"
    SMALL_TICK_MISS = "small_tick_miss"
    SMALL_TICK_HIT = "small_tick_hit"
    LARGE_TICK_MISS = "large_tick_miss"
    LARGE_TICK_HIT = "large_tick_hit"
    SMALL_BONUS = "small_bonus"
    LARGE_BONUS = "large_bonus"
    IGNORE_MISS = "ignore_miss"
    IGNORE_HIT = "ignore_hit"
    COMBO_BREAK = "combo_break"
    SLIDER_TAIL_HIT = "slider_tail_hit"
    LEGACY_COMBO_INCREASE = "legacy_combo_increase"

    @property
    def int_value(self) -> int:
        return _hit_result_int_value[self]

    def get_base_score(self, mode: Mode) -> int:
        match mode:
            case Mode.TAIKO:
                if self == HitResult.OK:
                    return 150

                return _hit_result_base_score.get(self, 0)

            case Mode.CATCH:
                if (
                    self == HitResult.GREAT
                    or self == HitResult.LARGE_TICK_HIT
                    or self == HitResult.SMALL_TICK_HIT
                ):
                    return 300

                if self == HitResult.LARGE_BONUS:
                    return 200

                return _hit_result_base_score.get(self, 0)

            case Mode.MANIA:
                if self == HitResult.PERFECT:
                    return 305

                return _hit_result_base_score.get(self, 0)

            case _:
                return _hit_result_base_score.get(self, 0)

    def affects_accuracy(self) -> bool:
        match self:
            case HitResult.LEGACY_COMBO_INCREASE | HitResult.COMBO_BREAK:
                return False

            case _:
                return self.is_scorable() and not self.is_bonus()

    def is_bonus(self) -> bool:
        match self:
            case HitResult.LARGE_BONUS | HitResult.SMALL_BONUS:
                return True

            case _:
                return False

    def is_scorable(self) -> bool:
        match self:
            case (
                HitResult.LEGACY_COMBO_INCREASE
                | HitResult.COMBO_BREAK
                | HitResult.SLIDER_TAIL_HIT
            ):
                return True

            case _:
                return (
                    self.int_value >= HitResult.MISS.int_value
                    and self.int_value < HitResult.IGNORE_MISS.int_value
                )


_hit_result_int_value = {
    HitResult.NONE: 0,
    HitResult.MISS: 1,
    HitResult.MEH: 2,
    HitResult.OK: 3,
    HitResult.GOOD: 4,
    HitResult.GREAT: 5,
    HitResult.PERFECT: 6,
    HitResult.SMALL_TICK_MISS: 7,
    HitResult.SMALL_TICK_HIT: 8,
    HitResult.LARGE_TICK_MISS: 9,
    HitResult.LARGE_TICK_HIT: 10,
    HitResult.SMALL_BONUS: 11,
    HitResult.LARGE_BONUS: 12,
    HitResult.IGNORE_MISS: 13,
    HitResult.IGNORE_HIT: 14,
    HitResult.COMBO_BREAK: 15,
    HitResult.SLIDER_TAIL_HIT: 16,
    HitResult.LEGACY_COMBO_INCREASE: 99,
}

_hit_result_base_score = {
    HitResult.SMALL_TICK_HIT: 10,
    HitResult.LARGE_TICK_HIT: 30,
    HitResult.SLIDER_TAIL_HIT: 150,
    HitResult.MEH: 50,
    HitResult.OK: 100,
    HitResult.GOOD: 200,
    HitResult.GREAT: 300,
    HitResult.PERFECT: 300,
    HitResult.SMALL_BONUS: 10,
    HitResult.LARGE_BONUS: 50,
}
