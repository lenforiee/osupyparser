from __future__ import annotations

from osupyparser.constants.mode import Mode


def calculate_accuracy(
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
                ]
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
                ]
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
                ]
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
                ]
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
