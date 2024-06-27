from __future__ import annotations

from osupyparser.constants.hit_result import HitResult
from osupyparser.constants.mode import Mode


def calculate_accuracy_legacy(
    statistics: dict[str, int],
    *,
    mode: Mode,
) -> float:
    match mode:
        case Mode.STANDARD:
            total_hits = sum(
                [
                    statistics["count_300"],
                    statistics["count_100"],
                    statistics["count_50"],
                    statistics["count_miss"],
                ],
            )

            if total_hits > 0:
                return (
                    statistics["count_300"] * 300
                    + statistics["count_100"] * 100
                    + statistics["count_50"] * 50
                ) / (total_hits * 300)

            return 1.0

        case Mode.TAIKO:
            total_hits = sum(
                [
                    statistics["count_300"],
                    statistics["count_100"],
                    statistics["count_50"],
                    statistics["count_miss"],
                ],
            )

            if total_hits > 0:
                return (
                    statistics["count_300"] * 300 + statistics["count_100"] * 150
                ) / (total_hits * 300)

            return 1.0

        case Mode.CATCH:
            total_hits = sum(
                [
                    statistics["count_300"],
                    statistics["count_100"],
                    statistics["count_50"],
                    statistics["count_miss"],
                    statistics["count_katu"],
                ],
            )

            if total_hits > 0:
                return (
                    statistics["count_300"]
                    + statistics["count_100"]
                    + statistics["count_50"]
                ) / total_hits

            return 1.0

        case Mode.MANIA:
            total_hits = sum(
                [
                    statistics["count_300"],
                    statistics["count_100"],
                    statistics["count_50"],
                    statistics["count_miss"],
                    statistics["count_geki"],
                    statistics["count_katu"],
                ],
            )

            if total_hits > 0:
                return (
                    (statistics["count_300"] + statistics["count_geki"]) * 300
                    + statistics["count_katu"] * 200
                    + statistics["count_100"] * 100
                    + statistics["count_50"] * 50
                ) / (total_hits * 300)

            return 1.0

        case _:
            raise ValueError(f"Unreachable mode: {mode}")


def calculate_accuracy_lazer(
    statistics: dict[HitResult, int],
    maximum_statistics: dict[HitResult, int],
    *,
    mode: Mode,
) -> float:
    base_score = sum(
        hit_result.get_base_score(mode) * count
        for hit_result, count in statistics.items()
        if hit_result.affects_accuracy()
    )

    maximum_base_score = sum(
        hit_result.get_base_score(mode) * count
        for hit_result, count in maximum_statistics.items()
        if hit_result.affects_accuracy()
    )

    if maximum_base_score == 0:
        return 1.0
    else:
        return base_score / maximum_base_score
