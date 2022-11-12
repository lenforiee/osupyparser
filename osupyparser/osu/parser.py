from __future__ import annotations

import hashlib
import logging
import math
from dataclasses import dataclass
from typing import Optional
from typing import Union

from ..shared.maths import calculate_bpm_multiplier
from ..shared.maths import calculate_end_time
from ..shared.maths import get_slider_points
from ..shared.maths import Vector2
from .enums import CurveType
from .enums import EventType
from .enums import Effects
from .enums import HitObjectType
from .enums import HitSoundType
from .enums import Mode
from .enums import OverlayPosition
from .enums import SampleSet
from .enums import TimeSignature
from .models import Background
from .models import BreakEvent
from .models import CatchBananaRain
from .models import CatchFruit
from .models import CatchJuiceStream
from .models import Circle
from .models import Extras
from .models import HitObject
from .models import ManiaHoldNote
from .models import ManiaNote
from .models import RGB
from .models import Slider
from .models import Spinner
from .models import TaikoDrumroll
from .models import TaikoHit
from .models import TaikoSpinner
from .models import TimingPoint
from .models import Video

# storyboard event list.
STORYBOARD_EVENTS = [
    EventType.SPRITE,
    EventType.SAMPLE,
    EventType.ANIMATION,
    EventType.STORYBOARD_COMMAND,
]


def parse_value_from_str(s: str) -> str:
    """Parses a value from a string."""

    return s.split(":", 1)[1].strip()


class OsuBeatmapFile:
    def __init__(self) -> None:

        self.__buffer: list[str] = []
        self._sb_buffer: list[str] = []  # TODO: Storyboard parsing.

        self.file_version: int = 0

        # General
        self.audio_filename: str = ""
        self.audio_lead_in: int = 0
        self.audio_hash: str = ""
        self.preview_time: int = -1
        self.countdown: int = 1
        self.sample_set: SampleSet = SampleSet.NORMAL
        self.stack_leniency: float = 0.7
        self.mode: Mode = Mode.OSU
        self.letterbox_in_breaks: bool = False
        self.story_fire_in_front: bool = True
        self.use_skin_sprites: bool = False
        self.always_show_play_field: bool = False
        self.overlay_position: OverlayPosition = OverlayPosition.NO_CHANGE
        self.skin_preference: str = ""
        self.epilepsy_warning: bool = False
        self.countdown_offset: int = 0
        self.special_style: bool = False
        self.widescreen_storyboard: bool = False
        self.samples_match_playback_rate: bool = False

        # Editor
        self.bookmarks: list[int] = []
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
        self.tags: list[str] = []
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
        self.background: Optional[Background] = None
        self.videos: list[Video] = []  # XXX: There can be few instances of video.
        self.break_times: list[BreakEvent] = []

        # Timing Points
        self.timing_points: list[TimingPoint] = []

        # BPM
        self.min_bpm: float = 0.0
        self.max_bpm: float = 0.0

        # Colours
        self.colour_slider_track_override: Optional[RGB] = None
        self.colour_slider_border: Optional[RGB] = None
        self.combo_colours: dict[str, RGB] = {}

        # Hit Objects
        self.hit_objects: list[HitObject] = []

        # Misc
        self.max_combo: int = 0
        self.beatmap_file_hash: str = ""

        # Stats
        self.ncircles: int = 0
        self.nsliders: int = 0
        self.nspinners: int = 0

        # Times
        self.play_time: int = 0
        self.drain_time: int = 0
        self.break_time: int = 0

    @property
    def nobjects(self) -> int:
        return self.ncircles + self.nsliders + self.nspinners

    @property
    def full_song_name(self) -> str:
        return f"{self.artist} - {self.title} [{self.version}]"

    def __str__(self) -> str:
        return f"<OsuFile: {self.full_song_name} ({self.beatmap_id})>"

    def __ensure_file_type(self) -> None:
        if not self.__buffer:
            raise ValueError("OsuBeatmapFile buffer is empty!")

        header = self.__buffer.pop(0)
        if not header[:17] == "osu file format v":
            raise ValueError("OsuBeatmapFile buffer is not a valid osu file!")

        self.file_version = int(header[17:])

    def __timing_point_at(self, time: int) -> TimingPoint:

        timing_point = 0
        for i, timing in enumerate(self.timing_points):
            if time >= timing.offset:
                timing_point = i

        return self.timing_points[timing_point]

    def __beat_len_at(self, offset: int) -> float:

        if not self.timing_points:
            return 0.0

        timing_point = 0
        sample_point = 0

        for i, timing in enumerate(self.timing_points):
            if timing.offset < offset:
                if timing.inherited:
                    sample_point = i
                else:
                    timing_point = i

        multiplier = 1.0

        if (
            sample_point > timing_point
            and self.timing_points[sample_point].beat_length < 0
        ):
            multiplier = calculate_bpm_multiplier(
                self.timing_points[sample_point].beat_length,
            )

        return self.timing_points[timing_point].beat_length * multiplier

    @classmethod
    def __from_string(cls, buffer: str) -> OsuBeatmapFile:

        self = cls()
        self.__buffer = buffer.split("\n")

        self.__ensure_file_type()
        self.beatmap_file_hash = hashlib.md5(buffer.encode()).hexdigest()

        section_name = ""
        while self.__buffer:  # While loop to flush buffer
            line = self.__buffer.pop(0)

            if not line.strip():
                continue  # Line is empty.

            if line[0] == "[" and line[-1] == "]":
                section_name = line[1:-1].lower()
                continue

            section_parser = getattr(self, f"_{section_name}_section", None)
            if not section_parser:
                continue
            section_parser(line)

        self.__calculate_max_combo()
        self.__calculate_gameplay_times()
        return self

    @staticmethod
    def from_path(path: str) -> OsuBeatmapFile:
        with open(path, encoding="utf-8-sig") as f:
            return OsuBeatmapFile.from_buffer(f.read())

    @staticmethod
    def from_buffer(_buffer: Union[bytes, str]) -> OsuBeatmapFile:
        """Load an osu file from a byte buffer."""
        if not isinstance(_buffer, str):
            buffer = _buffer.decode("utf-8-sig")
        else:
            buffer = _buffer

        return OsuBeatmapFile.__from_string(buffer)

    def _general_section(self, line: str) -> None:
        """
        Reference: https://osu.ppy.sh/wiki/en/Client/File_formats/Osu_(file_format)#general
        """
        if ":" not in line:
            return

        value = parse_value_from_str(line)

        if line.startswith("AudioFilename"):
            self.audio_filename = value

        elif line.startswith("AudioLeadIn"):
            self.audio_lead_in = int(value)

        elif line.startswith("AudioHash"):
            self.audio_hash = value  # Deprecated.

        elif line.startswith("PreviewTime"):
            self.preview_time = int(value)

        elif line.startswith("Countdown"):
            self.countdown = int(value)

        elif line.startswith("SampleSet"):
            self.sample_set = SampleSet.from_str(value)

        elif line.startswith("SampleVolume"):
            self.sample_volume = int(value)

        elif line.startswith("StackLeniency"):
            self.stack_leniency = float(value)

        elif line.startswith("Mode"):
            self.mode = Mode(int(value))

        elif line.startswith("LetterboxInBreaks"):
            self.letterbox_in_breaks = value == "1"  # Cast it to bool.

        elif line.startswith("StoryFireInFront"):
            self.story_fire_in_front = value == "1"

        elif line.startswith("UseSkinSprites"):
            self.use_skin_sprites = value == "1"

        elif line.startswith("AlwaysShowPlayfield"):
            self.always_show_play_field = value == "1"  # Deprecated.

        elif line.startswith("OverlayPosition"):
            self.overlay_position = OverlayPosition(value)

        elif line.startswith("SkinPreference"):
            self.skin_preference = value

        elif line.startswith("EpilepsyWarning"):
            self.epilepsy_warning = value == "1"

        elif line.startswith("CountdownOffset"):
            self.countdown_offset = int(value)

        elif line.startswith("SpecialStyle"):
            self.special_style = value == "1"

        elif line.startswith("WidescreenStoryboard"):
            self.widescreen_storyboard = value == "1"

        elif line.startswith("SamplesMatchPlaybackRate"):
            self.samples_match_playback_rate = value == "1"

    def _editor_section(self, line: str) -> None:
        """
        Reference: https://osu.ppy.sh/wiki/en/Client/File_formats/Osu_(file_format)#editor
        """
        if ":" not in line:
            return

        value = parse_value_from_str(line)

        if line.startswith("Bookmarks"):
            self.bookmarks = [int(x) for x in value.split(",") if x != ""]

        elif line.startswith("DistanceSpacing"):
            self.distance_spacing = float(value)

        elif line.startswith("BeatDivisor"):
            self.beat_divisor = float(value)

        elif line.startswith("GridSize"):
            self.grid_size = int(value)

        elif line.startswith("TimelineZoom"):
            self.timeline_zoom = float(value)

    def _metadata_section(self, line: str) -> None:
        """
        Reference: https://osu.ppy.sh/wiki/en/Client/File_formats/Osu_(file_format)#metadata
        """
        if ":" not in line:
            return

        value = parse_value_from_str(line)

        if line.startswith("Title:"):
            self.title = value

        elif line.startswith("TitleUnicode"):
            self.title_unicode = value

        elif line.startswith("Artist:"):
            self.artist = value

        elif line.startswith("ArtistUnicode:"):
            self.artist_unicode = value

        elif line.startswith("Creator"):
            self.creator = value

        elif line.startswith("Version"):
            self.version = value

        elif line.startswith("Source"):
            self.source = value

        elif line.startswith("Tags"):
            self.tags = value.split(" ")

        elif line.startswith("BeatmapID"):
            self.beatmap_id = int(value)

        elif line.startswith("BeatmapSetID"):
            self.beatmap_set_id = int(value)

    def _difficulty_section(self, line: str) -> None:
        """
        Reference: https://osu.ppy.sh/wiki/en/Client/File_formats/Osu_(file_format)#difficulty
        """
        if ":" not in line:
            return

        value = parse_value_from_str(line)

        if line.startswith("HPDrainRate"):
            self.hp = float(value)

        elif line.startswith("CircleSize"):
            self.cs = float(value)

        elif line.startswith("OverallDifficulty"):
            self.od = float(value)

        elif line.startswith("ApproachRate"):
            self.ar = float(value)

        elif line.startswith("SliderMultiplier"):
            self.slider_multiplier = float(value)

        elif line.startswith("SliderTickRate"):
            self.slider_tick_rate = float(value)

    def _events_section(self, line: str) -> None:
        """
        Reference: https://osu.ppy.sh/wiki/en/Client/File_formats/Osu_(file_format)#events
        """
        if line.startswith("//"):
            return

        content = line.split(",")

        if line.startswith(" ") or line.startswith("_"):
            event_type = EventType.STORYBOARD_COMMAND
        else:
            event_type = EventType.from_str(content[0])

        if event_type is None:
            logging.warn(
                f"[OsuBeatmapFile:_events_section] Silently ignoring invalid event: {line!r}"
            )
            return

        print(event_type)

        if event_type in STORYBOARD_EVENTS:
            self._sb_buffer.append(line)  # Its most likely a storyboard event.
            return

        data = {
            "filename": content[2].strip('"'),
            "x_offset": 0,
            "y_offset": 0,
        }

        if len(content) > 3:
            data["x_offset"] = int(content[3])

        if len(content) > 4:
            data["y_offset"] = int(content[4])

        if event_type == EventType.BACKGROUND:
            self.background = Background(**data)

        elif event_type == EventType.VIDEO:
            data["start_time"] = int(content[1])
            self.videos.append(Video(**data))

        elif event_type == EventType.BREAK:
            start_time = int(content[1])
            end_time = int(content[2])
            self.break_times.append(BreakEvent(start_time, end_time))

    def _timingpoints_section(self, line: str) -> None:
        """
        Knowledge Reference:
        https://osu.ppy.sh/wiki/en/Client/File_formats/Osu_(file_format)#timing-points,

        Code Reference:
        https://github.com/mrflashstudio/OsuParsers/blob/master/OsuParsers/Decoders/BeatmapDecoder.cs#L293L335
        """

        content = line.split(",")
        if not content:
            return

        offset = int(content[0])
        beat_length = float(content[1])
        time_signature = TimeSignature.SIMPLE_QUADRUPLE
        sample_set = SampleSet.NONE
        custom_sample_set = 0
        volume = 100
        inherited = True
        effects = Effects.NONE

        if len(content) >= 3:
            time_signature = TimeSignature(int(content[2]))

        if len(content) >= 4:
            sample_set = SampleSet(int(content[3]))

        if len(content) >= 5:
            custom_sample_set = int(content[4])

        if len(content) >= 6:
            volume = int(content[5])

        if len(content) >= 7:
            inherited = int(content[6]) == 1

        if len(content) >= 8:
            effects = Effects(int(content[7]))

        bpm = velocity = 0
        if inherited:
            bpm = round(60000 / beat_length)
            self.min_bpm = min(self.min_bpm, bpm) if self.min_bpm else bpm
            self.max_bpm = max(self.max_bpm, bpm) if self.max_bpm else bpm
        else:
            velocity = abs(100 / beat_length)

        self.timing_points.append(
            TimingPoint(
                offset=offset,
                beat_length=beat_length,
                time_signature=time_signature,
                sample_set=sample_set,
                custom_sample_set=custom_sample_set,
                volume=volume,
                inherited=inherited,
                effects=effects,
                bpm=bpm,
                velocity=velocity,
            ),
        )

    def _colours_section(self, line: str) -> None:
        """
        Reference: https://osu.ppy.sh/wiki/en/Client/File_formats/Osu_(file_format)
        """

        colour_type, rgb_colours = line.split(" : ")
        rgb = rgb_colours.split(",")

        colour = RGB(
            r=int(rgb[0]),
            g=int(rgb[1]),
            b=int(rgb[2]),
        )

        if colour_type == "SliderTrackOverride":
            self.colour_slider_track_override = colour
        elif colour_type == "SliderBorder":
            self.colour_slider_border = colour
        else:
            self.combo_colours[colour_type] = colour

    def _hitobjects_section(self, line: str) -> None:
        """
        Knowledge Reference:
        https://osu.ppy.sh/wiki/en/Client/File_formats/Osu_%28file_format%29#hit-objects,

        Code Reference:
        https://github.com/mrflashstudio/OsuParsers/blob/master/OsuParsers/Decoders/BeatmapDecoder.cs#L293L335
        """

        content = line.split(",")

        position = Vector2(float(content[0]), float(content[1]))
        start_time = int(content[2])
        hit_type = HitObjectType(int(content[3]))

        combo_offset = int((hit_type & HitObjectType.COMBO_OFFSET) >> 4)
        hit_type = HitObjectType(hit_type & ~HitObjectType.COMBO_OFFSET)

        is_new_combo = bool(hit_type & HitObjectType.NEW_COMBO)
        hit_type = HitObjectType(hit_type & ~HitObjectType.NEW_COMBO)

        hit_sound = HitSoundType(int(content[4]))

        offset = 1 if hit_type & HitObjectType.HOLD else 0
        extras_data = content[-1].split(":")[offset:]

        extras = None
        if ":" in content[-1]:

            data = {
                "sample_set": SampleSet(int(extras_data[0])),
                "addition_set": SampleSet(int(extras_data[1])),
                "custom_index": 0,
                "volume": 0,
                "sample_filename": "",
            }

            if len(extras_data) > 2:
                data["custom_index"] = int(extras_data[2])

            if len(extras_data) > 3:
                data["volume"] = int(extras_data[3])

            if len(extras_data) > 4:
                data["sample_filename"] = extras_data[4]

            extras = Extras(**data)

        hit_object = None
        if hit_type == HitObjectType.CIRCLE:

            self.ncircles += 1

            args = {
                "position": position,
                "start_time": start_time,
                "end_time": start_time,
                "hit_sound": hit_sound,
                "extras": extras,
                "is_new_combo": is_new_combo,
                "combo_offset": combo_offset,
            }

            if self.mode == Mode.OSU:
                hit_object = Circle(**args)
            elif self.mode == Mode.TAIKO:
                hit_object = TaikoHit(**args)
            elif self.mode == Mode.CATCH:
                hit_object = CatchFruit(**args)
            elif self.mode == Mode.MANIA:
                hit_object = ManiaNote(**args)

        elif hit_type == HitObjectType.SPINNER:

            self.nspinners += 1

            end_time = int(content[5])

            args = {
                "position": position,
                "start_time": start_time,
                "end_time": end_time,
                "hit_sound": hit_sound,
                "extras": extras,
                "is_new_combo": is_new_combo,
                "combo_offset": combo_offset,
            }

            if self.mode == Mode.OSU:
                hit_object = Spinner(**args)
            elif self.mode == Mode.TAIKO:
                hit_object = TaikoSpinner(**args)
            elif self.mode == Mode.CATCH:
                hit_object = CatchBananaRain(**args)

        elif hit_type == HitObjectType.HOLD:

            self.nsliders += 1

            additions = content[5].split(":")
            end_time = int(additions[0])

            args = {
                "position": position,
                "start_time": start_time,
                "end_time": end_time,
                "hit_sound": hit_sound,
                "extras": extras,
                "is_new_combo": is_new_combo,
                "combo_offset": combo_offset,
            }

            hit_object = ManiaHoldNote(**args)

        elif hit_type == HitObjectType.SLIDER:

            self.nsliders += 1

            curve_type = CurveType(content[5].split("|")[0][0])
            slider_points = get_slider_points(content[5].split("|"))

            repeats = int(content[6])
            pixel_length = float(content[7])

            end_time = calculate_end_time(
                start_time,
                repeats,
                pixel_length,
                self.slider_multiplier,
                self.__beat_len_at(start_time),
            )

            edge_hit_sounds = None
            if len(content) > 8 and len(content[8]) > 0:
                edge_hit_sounds = []
                for hitsound in content[8].split("|"):
                    edge_hit_sounds.append(HitSoundType(int(hitsound)))

            edge_additions = None
            if len(content) > 9 and len(content[9]) > 0:
                edge_additions = []
                for addiction in content[9].split("|"):
                    samples = addiction.split(":")
                    edge_additions.append(
                        (SampleSet(int(samples[0])), SampleSet(int(samples[1]))),
                    )

            args = {
                "position": position,
                "start_time": start_time,
                "end_time": end_time,
                "hit_sound": hit_sound,
                "extras": extras,
                "is_new_combo": is_new_combo,
                "combo_offset": combo_offset,
            }

            if self.mode != Mode.MANIA:
                args |= {
                    "curve_type": curve_type,
                    "slider_points": slider_points,
                    "repeats": repeats,
                    "pixel_length": pixel_length,
                    "edge_hitsounds": edge_hit_sounds,
                    "edge_additions": edge_additions,
                }

            if self.mode == Mode.OSU:
                hit_object = Slider(**args)
            elif self.mode == Mode.TAIKO:
                hit_object = TaikoDrumroll(**args)
            elif self.mode == Mode.CATCH:
                hit_object = CatchJuiceStream(**args)
            elif self.mode == Mode.MANIA:
                hit_object = ManiaHoldNote(**args)

        if not hit_object:
            return

        self.hit_objects.append(hit_object)

    def __calculate_max_combo(self) -> None:
        """
        Edited pyttanko max combo calculation.
        Reference: https://github.com/Francesco149/pyttanko/blob/master/pyttanko.py#L265
        """
        combo_val = 0
        for hit_object in self.hit_objects:

            if not isinstance(hit_object, Slider):
                combo_val += 1
                continue

            timing_point = self.__timing_point_at(hit_object.start_time)
            sv_multiplier = 1.0

            if not timing_point.inherited and timing_point.beat_length < 0:
                sv_multiplier = -100.0 / timing_point.beat_length

            px_per_beat = self.slider_multiplier * 100.0 * sv_multiplier
            if self.file_version < 8:
                px_per_beat /= sv_multiplier

            num_beats = (hit_object.pixel_length * hit_object.repeats) / px_per_beat

            ticks = math.ceil(
                (num_beats - 0.1) / hit_object.repeats * self.slider_tick_rate,
            )

            ticks = ((ticks - 1) * hit_object.repeats) + hit_object.repeats + 1

            combo_val += max(0, ticks)

        self.max_combo = combo_val

    def __calculate_gameplay_times(self) -> None:

        first_obj = self.hit_objects[0]
        last_obj = self.hit_objects[-1]

        # XXX: All times are in seconds.
        for break_time in self.break_times:
            self.break_time += math.floor(
                (break_time.end_time - break_time.start_time) / 1000,
            )

        if first_obj and last_obj:
            self.play_time = math.floor(
                (last_obj.end_time - first_obj.start_time) / 1000,
            )
            self.drain_time = math.floor(
                (last_obj.end_time - first_obj.start_time) / 1000 - self.break_time,
            )
