from __future__ import annotations

import json
import lzma
from typing import Any
from typing import BinaryIO

from osupyparser.common.binary import BinaryReader
from osupyparser.constants.hit_result import HitResult
from osupyparser.constants.mode import Mode
from osupyparser.constants.mods import Mods
from osupyparser.helpers import accuracy
from osupyparser.helpers import grade
from osupyparser.osr.models.lazer import OsuReplayLazerData
from osupyparser.osr.models.replay import OsuReplayFile
from osupyparser.osr.models.replay import OsuReplayFileLzma


def _parse_replay_contents_lzma(
    reader: BinaryReader,
    *,
    length: int = -1,
    mods: int = 0,
) -> OsuReplayFileLzma:
    lzma_data: dict[str, Any] = {}

    data = lzma.decompress(
        reader.read(length),
        format=lzma.FORMAT_AUTO,
    ).decode("ascii")

    lzma_data["frames"] = []
    lzma_data["skip_offset"] = 0
    absolute_frame_time = 0

    for idx, frame in enumerate(data.split(",")):
        if not frame:
            continue

        frame_data = frame.split("|")
        if len(frame_data) != 4:
            continue

        if frame_data[0] == "-12345":
            # After 2013.03.19 replays started to have seeds.
            lzma_data["rng_seed"] = int(frame_data[3])
            continue

        delta_time = int(frame_data[0])
        absolute_frame_time += delta_time

        if idx == 2:  # first is time = 0, second is skip boundary
            lzma_data["skip_offset"] = delta_time

            if mods & Mods.AUTOPLAY.value:
                lzma_data["skip_offset"] -= 100000

        position = {
            "x": float(frame_data[1]),
            "y": float(frame_data[2]),
        }

        keys = int(frame_data[3])
        lzma_data["frames"].append(
            {
                "absolute_time": absolute_frame_time,
                "delta_time": delta_time,
                "position": position,
                "keys": keys,
            },
        )

    return OsuReplayFileLzma(**lzma_data)


def _parse_replay_contents_lazer(
    reader: BinaryReader, *, length: int
) -> OsuReplayLazerData:
    data = lzma.decompress(
        reader.read(length),
        format=lzma.FORMAT_AUTO,
    ).decode("ascii")

    lazer_data = json.loads(data)
    return OsuReplayLazerData(**lazer_data)


def _parse_replay_contents(reader: BinaryReader) -> OsuReplayFile:
    replay: dict[str, Any] = {}
    statistics: dict[str, int] = {}

    replay["mode"] = Mode(reader.read_u8())
    replay["osu_version"] = reader.read_i32()

    replay["beatmap_md5"] = reader.read_string()
    replay["player_name"] = reader.read_string()
    replay["replay_md5"] = reader.read_string()

    statistics["count_300"] = reader.read_u16()
    statistics["count_100"] = reader.read_u16()
    statistics["count_50"] = reader.read_u16()
    statistics["count_geki"] = reader.read_u16()
    statistics["count_katu"] = reader.read_u16()
    statistics["count_miss"] = reader.read_u16()

    replay["score"] = reader.read_u32()
    replay["max_combo"] = reader.read_u16()
    replay["full_combo"] = reader.read_u8() == 1
    replay["mods"] = Mods(reader.read_u32())

    replay["life_bar_graph"] = []
    life_bar_graph_data = reader.read_string()

    for frame in life_bar_graph_data.split(","):
        frame_data = frame.split("|")

        if len(frame_data) != 2:
            continue

        replay["life_bar_graph"].append(
            {
                "time": int(frame_data[0]),
                "percentage": float(frame_data[1]),
            },
        )

    replay["timestamp"] = reader.read_datetime()

    replay["frames"] = []
    replay_frames_len = reader.read_i32()
    if replay_frames_len > 0:
        lzma_data = _parse_replay_contents_lzma(
            reader,
            length=replay_frames_len,
            mods=replay["mods"],
        )

        replay["frames"] = lzma_data.frames
        replay["rng_seed"] = lzma_data.rng_seed
        replay["skip_offset"] = lzma_data.skip_offset

    if replay["osu_version"] >= 2014_07_21:
        replay["online_score_id"] = reader.read_i64()
    elif replay["osu_version"] >= 2012_10_08:
        replay["online_score_id"] = reader.read_i32()

    if replay["mods"] & Mods.TARGET:
        replay["target_practice_hits"] = reader.read_f64()

    replay_accuracy = accuracy.calculate_accuracy_legacy(
        statistics,
        mode=replay["mode"],
    )
    replay_grade = grade.calculate_grade_legacy(
        statistics,
        accuracy=replay_accuracy,
        mode=replay["mode"],
        mods=replay["mods"],
    )

    replay["legacy_accuracy"] = round(replay_accuracy * 100, 4)
    replay["legacy_grade"] = replay_grade
    replay["statistics"] = statistics

    if replay["osu_version"] >= 30000001:
        replay_lazer_data_len = reader.read_i32()
        replay_lazer_data = _parse_replay_contents_lazer(
            reader,
            length=replay_lazer_data_len,
        )

        replay_accuracy_lazer = accuracy.calculate_accuracy_lazer(
            replay_lazer_data.statistics,
            replay_lazer_data.maximum_statistics,
            mode=replay["mode"],
        )

        miss_count = replay_lazer_data.statistics.get(HitResult.MISS, 0)
        replay_grade_lazer = grade.calculate_grade_lazer(
            replay_accuracy_lazer,
            misses=miss_count,
            mode=replay["mode"],
            mods=replay_lazer_data.mods,
        )

        replay["lazer_accuracy"] = round(replay_accuracy_lazer * 100, 4)
        replay["lazer_grade"] = replay_grade_lazer
        replay["lazer_data"] = replay_lazer_data

    return OsuReplayFile(**replay)


def read_osr_file(file_path: str) -> OsuReplayFile:
    with open(file_path, "rb") as file_buffer:
        reader = BinaryReader(file_buffer.read())

    return _parse_replay_contents(reader)


def read_osr_file_lzma(file_path: str) -> OsuReplayFileLzma:
    with open(file_path, "rb") as file_buffer:
        reader = BinaryReader(file_buffer.read())

    return _parse_replay_contents_lzma(reader)


def read_osr_buffer(file_buffer: BinaryIO) -> OsuReplayFile:
    reader = BinaryReader(file_buffer.read())
    return _parse_replay_contents(reader)


def read_osr_buffer_lzma(file_buffer: BinaryIO) -> OsuReplayFileLzma:
    reader = BinaryReader(file_buffer.read())
    return _parse_replay_contents_lzma(reader)
