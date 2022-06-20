from __future__ import annotations

from typing import Union


BUFFER_LIKE = Union[bytes, bytearray, memoryview, str]


class OsuFile:
    def __init__(self) -> None:

        self.__buffer = None

        self.file_version: int = 0

        # General
        self.audio_filename: str = ""
        self.audio_lead_in: int = 0
        self.audio_hash: str = ""
        self.preview_time: int = -1
        self.countdown: int = 1
        self.sample_set: str = "Normal"
        self.stack_leniency: float = 0.7
        self.mode: int = 0
        self.letterbox_in_breaks: bool = False
        self.story_fire_in_front: bool = True
        self.use_skin_sprites: bool = False
        self.always_show_play_field: bool = False
        self.overlay_position: str = "NoChange"
        self.skin_preference: str = ""
        self.epilepsy_warning: bool = False
        self.countdown_offset: int = 0
        self.special_style: bool = False
        self.widescreen_storyboard: bool = False
        self.samples_match_playback_rate: bool = False

        # Editor
        self.bookmarks: list = []
        self.distance_spacing: float = 0.0
        self.beat_divisor: float = 0.0
        self.grid_size: int = 0
        self.timeline_zoom: float = 0.0

        # Metadata
        self.title: str = ""
        self.title_unicode: str = ""
        self.artist: str = ""
        self.artist_unicode: str = ""
        self.creator: str = ""
        self.version: str = ""
        self.source: str = ""
        self.tags: str = ""
        self.beatmap_id: int = -1
        self.beatmap_set_id: int = -1

        # Difficulty
        self.hp: float = 0.0
        self.cs: float = 0.0
        self.od: float = 0.0
        self.ar: float = 0.0
        self.slider_multiplier: float = 0.0
        self.slider_tick_rate: float = 0.0

        # Events
        self.background = None
        self.video = None
        self.break_times: list = []

    @property
    def full_song_name(self) -> str:
        return f"{self.artist} - {self.title} [{self.version}]"

    def __str__(self) -> str:
        return "<OsuFile: {self.full_song_name} ({self.beatmap_id})>"

    def __from_string(self, buffer: BUFFER_LIKE) -> OsuFile:
        self.__buffer = buffer
        ...

    @staticmethod
    def from_path(path: str) -> OsuFile:
        with open(path) as f:
            return OsuFile.from_buffer(f.read())

    @staticmethod
    def from_buffer(buffer: BUFFER_LIKE) -> OsuFile:
        if not isinstance(buffer, str):
            buffer = buffer.decode("utf-8")
        return OsuFile.__from_string(buffer)
