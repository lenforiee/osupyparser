from __future__ import annotations

import lzma
from datetime import datetime

from ..shared.maths import Vector2
from .binary import BinaryReader
from .enums import CatchKeys
from .enums import Keys
from .enums import ManiaKeys
from .enums import Mode
from .enums import Mods
from .enums import TaikoKeys
from .models import LifeBarFrame
from .models import ReplayFrame


class OsuReplayFile:
    def __init__(self):

        self.__buffer: BinaryReader = BinaryReader()

        self.mode: Mode = Mode.STANDARD
        self.osu_version: int = 0

        self.beatmap_md5: str = ""
        self.player_name: str = ""
        self.replay_md5: str = ""

        self.n300: int = 0
        self.n100: int = 0
        self.n50: int = 0
        self.ngeki: int = 0
        self.nkatu: int = 0
        self.nmiss: int = 0

        self.score: int = 0
        self.max_combo: int = 0
        self.perfect: bool = False
        self.mods: Mods = Mods.NOMOD

        self.life_graph: list[LifeBarFrame] = []
        self.timestamp: datetime = datetime.now()
        self.online_score_id: int = 0
        self.rng_seed: int = 0
        self.target_practice_hits: float = 0.0

        self.skip_offset: int = 0
        self.frames: list[ReplayFrame] = []
        self.keypresses: list[ReplayFrame] = []

    def __str__(self) -> str:
        return f"<ReplayFile: {self.player_name} ({self.beatmap_md5})>"

    def __ensure_file_type(self) -> None:
        if not self.__buffer:
            raise ValueError("OsuReplayFile buffer is empty!")

    def __parse_lzma_content(self, length: int = -1) -> None:
        data = lzma.decompress(  # type: ignore
            self.__buffer.read(length),
            format=lzma.FORMAT_AUTO,
        ).decode("ascii")

        last_time = 0
        prev_keys = 0
        for frame in data.split(","):
            if not frame:
                continue

            split = frame.split("|")

            if split[0] != "-1":
                self.skip_offset = int(split[0])

                if self.mods & Mods.AUTOPLAY:
                    self.skip_offset -= 100000

                if self.skip_offset > 0:
                    last_time = self.skip_offset

                continue

            if len(split) < 4:
                continue

            if self.osu_version >= 20130319 and split[0] == "-12345":
                # After 20130319 replays started to have seeds.
                self.rng_seed = int(split[3])
                continue

            delta = int(split[0])
            time = delta + last_time
            position = Vector2(float(split[1]), float(split[2]))
            replay_frame = ReplayFrame(
                position=position,
                delta=delta,
                time=time,
            )

            if self.mode == Mode.STANDARD:
                replay_frame.osu_keys = Keys(int(split[3]))

                if (replay_frame.osu_keys & Keys.M1 and not prev_keys & Keys.M1) or (
                    replay_frame.osu_keys & Keys.M2 and not prev_keys & Keys.M2
                ):
                    self.keypresses.append(replay_frame)

                prev_keys = replay_frame.osu_keys
            elif self.mode == Mode.TAIKO:
                replay_frame.taiko_keys = TaikoKeys(int(split[3]))

                # TODO: Add keypresses for taiko
                prev_keys = replay_frame.taiko_keys
            elif self.mode == Mode.CATCH:
                replay_frame.catch_keys = CatchKeys(int(split[3]))

                # TODO: Add keypresses for catch
                prev_keys = replay_frame.catch_keys
            elif self.mode == Mode.MANIA:
                replay_frame.mania_keys = ManiaKeys(position.x)

                # TODO: Add keypresses for mania
                prev_keys = replay_frame.mania_keys

            self.frames.append(replay_frame)
            last_time = time

    @classmethod
    def __from_bytes(cls, buffer: bytes, pure_lzma: bool = False) -> OsuReplayFile:

        self = cls()
        self.__buffer += buffer

        self.__ensure_file_type()

        if pure_lzma:
            self.__parse_lzma_content()
            return self

        self.mode = Mode(self.__buffer.read_u8())
        self.osu_version = self.__buffer.read_i32()

        self.beatmap_md5 = self.__buffer.read_string()
        self.player_name = self.__buffer.read_string()
        self.replay_md5 = self.__buffer.read_string()

        self.n300 = self.__buffer.read_u16()
        self.n100 = self.__buffer.read_u16()
        self.n50 = self.__buffer.read_u16()
        self.ngeki = self.__buffer.read_u16()
        self.nkatu = self.__buffer.read_u16()
        self.nmiss = self.__buffer.read_u16()

        self.score = self.__buffer.read_u32()
        self.max_combo = self.__buffer.read_u16()
        self.perfect = self.__buffer.read_u8() == 1
        self.mods = Mods(self.__buffer.read_u32())

        life_graph_data = self.__buffer.read_string()
        if life_graph_data:
            for life_bar in life_graph_data.split(","):

                split = life_bar.split("|")
                if len(split) != 2:
                    continue

                self.life_graph.append(
                    LifeBarFrame(time=int(split[0]), percentage=float(split[1])),
                )

        self.timestamp = self.__buffer.read_datetime()

        replay_frames_len = self.__buffer.read_i32()
        if replay_frames_len > 0:
            self.__parse_lzma_content(replay_frames_len)

        # Reference:
        # https://github.com/ppy/osu/blob/84e1ff79a0736aa6c7a44804b585ab1c54a84399/osu.Game/Scoring/Legacy/LegacyScoreDecoder.cs#L78-L81
        if self.osu_version >= 20140721:
            self.online_score_id = self.__buffer.read_i64()
        elif self.osu_version >= 20121008:
            self.online_score_id = self.__buffer.read_i32()

        if self.mods & Mods.TARGET:
            self.target_practice_hits = self.__buffer.read_f64()

        return self

    @staticmethod
    def from_path(path: str, pure_lzma: bool = False) -> OsuReplayFile:
        with open(path, "rb") as f:
            return OsuReplayFile.from_buffer(f.read(), pure_lzma)

    @staticmethod
    def from_buffer(buffer: bytes, pure_lzma: bool = False) -> OsuReplayFile:
        if isinstance(buffer, str):
            raise ValueError(f"Buffer must be bytes-like, got {type(buffer)}.")

        return OsuReplayFile.__from_bytes(buffer, pure_lzma)
