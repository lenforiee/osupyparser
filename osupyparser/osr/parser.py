from __future__ import annotations

from typing import Union

from binary import BinaryReader

BUFFER_LIKE = Union[bytes, bytearray, memoryview]


class ReplayFile:
    def __init__(self):

        self.__buffer: BinaryReader = BinaryReader()

        self.mode: int = 0
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
        self.full_combo: bool = False
        self.mods: int = 0  # TODO: Make it mods class
        self.life_graph: str = ""
        self.timestamp: int = 0
        self.online_score_id: int = 0
        self.seed: int = 0
        self.target_practice_hits: float = 0.0

        self.frames: list = []

    def __str__(self) -> str:
        return "<ReplayFile: {self.player_name} ({self.beatmap_md5})>"

    def __from_bytes(self, buffer: BUFFER_LIKE) -> ReplayFile:
        self.__buffer += buffer
        ...

    @staticmethod
    def from_path(path: str) -> ReplayFile:
        with open(path, "rb") as f:
            return ReplayFile.from_buffer(f.read())

    @staticmethod
    def from_buffer(buffer: BUFFER_LIKE) -> ReplayFile:
        if isinstance(buffer, str):
            raise ValueError("Buffer must be bytes-like.")

        return ReplayFile.__from_bytes(buffer)
