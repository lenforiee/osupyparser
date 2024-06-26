from __future__ import annotations

from osupyparser.constants.grade import Grade
from osupyparser.constants.mode import Mode
from osupyparser.constants.mods import Mods


def calculate_grade_legacy(
    statistics: dict[str, int],
    *,
    accuracy: float,
    mode: Mode,
    mods: Mods,
) -> Grade:
    is_silver_grade = mods & Mods.HIDDEN or mods & Mods.FLASHLIGHT
    match mode:
        case Mode.STANDARD | Mode.TAIKO:
            total_hits = sum(
                [
                    statistics["count_300"],
                    statistics["count_100"],
                    statistics["count_50"],
                    statistics["count_miss"],
                ]
            )

            ratio_300 = statistics["count_300"] / total_hits
            ratio_50 = statistics["count_50"] / total_hits

            if ratio_300 == 1.0:
                return Grade.XH if is_silver_grade else Grade.X
            elif ratio_300 > 0.9 and ratio_50 <= 0.01 and statistics["count_miss"] == 0:
                return Grade.SH if is_silver_grade else Grade.S
            elif (ratio_300 > 0.8 and statistics["count_miss"] == 0) or ratio_300 > 0.9:
                return Grade.A
            elif (ratio_300 > 0.7 and statistics["count_miss"] == 0) or ratio_300 > 0.8:
                return Grade.B
            elif ratio_300 > 0.6:
                return Grade.C
            else:
                return Grade.D

        case Mode.CATCH:
            if accuracy == 1.0:
                return Grade.XH if is_silver_grade else Grade.X
            elif accuracy > 0.98:
                return Grade.SH if is_silver_grade else Grade.S
            elif accuracy > 0.94:
                return Grade.A
            elif accuracy > 0.9:
                return Grade.B
            elif accuracy > 0.85:
                return Grade.C
            else:
                return Grade.D

        case Mode.MANIA:
            if accuracy == 1.0:
                return Grade.XH if is_silver_grade else Grade.X
            elif accuracy > 0.95:
                return Grade.SH if is_silver_grade else Grade.S
            elif accuracy > 0.9:
                return Grade.A
            elif accuracy > 0.8:
                return Grade.B
            elif accuracy > 0.7:
                return Grade.C
            else:
                return Grade.D

        case _:
            raise ValueError(f"Unreachable mode: {mode}")
