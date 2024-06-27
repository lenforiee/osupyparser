from __future__ import annotations

from typing import TextIO

from osupyparser.osu.models.beatmap import OsuBeatmapFile


def _parse_beatmap_contents(lines: list[str]) -> OsuBeatmapFile:
    ...


def read_osu_file(file_path: str) -> OsuBeatmapFile:
    with open(file_path, encoding="utf-8-sig", errors="ignore") as file_buffer:
        lines = file_buffer.readlines()

    return _parse_beatmap_contents(lines)


def read_osu_buffer(file_buffer: TextIO) -> OsuBeatmapFile:
    lines = file_buffer.readlines()
    return _parse_beatmap_contents(lines)
