from __future__ import annotations

import hashlib
import re
from typing import Any
from typing import TypedDict

from osupyparser.constants.effects import Effects
from osupyparser.constants.sample_set import SampleSet
from osupyparser.constants.time_signature import TimeSignature
from osupyparser.osu.models.beatmap import OsuBeatmapFile
from osupyparser.osu.models.sections.colours import ColoursSection
from osupyparser.osu.models.sections.difficulty import DifficultySection
from osupyparser.osu.models.sections.editor import EditorSection
from osupyparser.osu.models.sections.events import EventsSection
from osupyparser.osu.models.sections.general import GeneralSection
from osupyparser.osu.models.sections.metadata import MetadataSection
from osupyparser.osu.models.timing_point import TimingPoint


SECTION_REGEX = re.compile(rb"\[([^\]]+)\]\s*((?:.*?\n)+?)(?=\[|$)")
EARLY_VERSION_TIMING_OFFSET = 24

BytesLike = bytes | bytearray | memoryview


def _split_contents_to_sections(lines: list[bytearray]) -> dict[str, bytearray]:
    sections: dict[str, bytearray] = {}
    match_text = b"\n".join(lines)

    for match_data in SECTION_REGEX.finditer(match_text):
        section_name = _decode_osu_str(match_data.group(1).lower())
        section_contents = bytearray(match_data.group(2).strip())
        sections[section_name] = section_contents

    return sections


def _get_offset_time(offset: int, format_version: int) -> int:
    if format_version < 5:
        return offset + EARLY_VERSION_TIMING_OFFSET

    return offset


def _decode_osu_str(s: bytearray | bytes) -> str:
    return s.decode("utf-8-sig", errors="ignore")


def _parse_value_from_str(s: bytearray) -> str:
    return _decode_osu_str(s.split(b":", 1)[1].strip())


def _clean_file_name(filename: bytearray) -> str:
    return _decode_osu_str(filename.replace(b"\\", b"/").strip(b'"'))


def _parse_general_section(
    section_contents: bytearray, *, format_version: int
) -> GeneralSection:
    general_section: dict[str, Any] = {}
    lines = section_contents.split(b"\n")

    for line in lines:
        if not line:
            continue

        value = _parse_value_from_str(line)

        if line.startswith(b"AudioFilename"):
            general_section["audio_filename"] = value

        elif line.startswith(b"AudioLeadIn"):
            general_section["audio_lead_in"] = int(value)

        elif line.startswith(b"AudioHash"):
            general_section["audio_hash"] = value

        elif line.startswith(b"PreviewTime"):
            time = int(value)
            general_section["preview_time"] = (
                time if time == -1 else _get_offset_time(time, format_version)
            )

        elif line.startswith(b"Countdown"):
            general_section["countdown"] = int(value)

        elif line.startswith(b"SampleSet"):
            general_section["sample_set"] = value

        elif line.startswith(b"SampleVolume"):
            general_section["sample_volume"] = int(value)

        elif line.startswith(b"StackLeniency"):
            general_section["stack_leniency"] = float(value)

        elif line.startswith(b"Mode"):
            general_section["mode"] = int(value)

        elif line.startswith(b"LetterboxInBreaks"):
            general_section["letterbox_in_breaks"] = value == "1"

        elif line.startswith(b"StoryFireInFront"):
            general_section["story_fire_in_front"] = value == "1"

        elif line.startswith(b"UseSkinSprites"):
            general_section["use_skin_sprites"] = value == "1"

        elif line.startswith(b"AlwaysShowPlayfield"):
            general_section["always_show_playfield"] = value == "1"

        elif line.startswith(b"OverlayPosition"):
            general_section["overlay_position"] = value

        elif line.startswith(b"SkinPreference"):
            general_section["skin_preference"] = value

        elif line.startswith(b"EpilepsyWarning"):
            general_section["epilepsy_warning"] = value == "1"

        elif line.startswith(b"CountdownOffset"):
            general_section["countdown_offset"] = int(value)

        elif line.startswith(b"SpecialStyle"):
            general_section["special_style"] = value == "1"

        elif line.startswith(b"WidescreenStoryboard"):
            general_section["widescreen_storyboard"] = value == "1"

        elif line.startswith(b"SamplesMatchPlaybackRate"):
            general_section["samples_match_playback_rate"] = value == "1"

    return GeneralSection(**general_section)


def _parse_editor_section(section_contents: bytearray) -> EditorSection:
    editor_section: dict[str, Any] = {}
    lines = section_contents.split(b"\n")

    for line in lines:
        if not line:
            continue

        value = _parse_value_from_str(line)

        if line.startswith(b"Bookmarks"):
            editor_section["bookmarks"] = [
                int(x) for x in value.split(",") if x.strip()
            ]

        elif line.startswith(b"DistanceSpacing"):
            editor_section["distance_spacing"] = float(value)

        elif line.startswith(b"BeatDivisor"):
            editor_section["beat_divisor"] = int(value)

        elif line.startswith(b"GridSize"):
            editor_section["grid_size"] = int(value)

        elif line.startswith(b"TimelineZoom"):
            editor_section["timeline_zoom"] = float(value)

    return EditorSection(**editor_section)


def _parse_metadata_section(section_contents: bytearray) -> MetadataSection:
    metadata_section: dict[str, Any] = {}
    lines = section_contents.split(b"\n")

    for line in lines:
        if not line:
            continue

        value = _parse_value_from_str(line)

        if line.startswith(b"Title:"):
            metadata_section["title"] = value

        elif line.startswith(b"TitleUnicode"):
            metadata_section["title_unicode"] = value

        elif line.startswith(b"Artist:"):
            metadata_section["artist"] = value

        elif line.startswith(b"ArtistUnicode"):
            metadata_section["artist_unicode"] = value

        elif line.startswith(b"Creator"):
            metadata_section["creator"] = value

        elif line.startswith(b"Version"):
            metadata_section["version"] = value

        elif line.startswith(b"Source"):
            metadata_section["source"] = value

        elif line.startswith(b"Tags"):
            metadata_section["tags"] = [tag for tag in value.split(" ") if tag.strip()]

        elif line.startswith(b"BeatmapID"):
            metadata_section["beatmap_id"] = int(value)

        elif line.startswith(b"BeatmapSetID"):
            metadata_section["beatmap_set_id"] = int(value)

    return MetadataSection(**metadata_section)


def _parse_difficulty_section(section_contents: bytearray) -> DifficultySection:
    difficutly_section: dict[str, Any] = {}
    lines = section_contents.split(b"\n")

    for line in lines:
        if not line:
            continue

        value = _parse_value_from_str(line)
        has_approach_rate = False

        if line.startswith(b"HPDrainRate"):
            difficutly_section["hp_drain_rate"] = float(value)

        elif line.startswith(b"CircleSize"):
            difficutly_section["circle_size"] = float(value)

        elif line.startswith(b"OverallDifficulty"):
            difficutly_section["overall_difficulty"] = float(value)

            if not has_approach_rate:
                difficutly_section["approach_rate"] = float(value)

        elif line.startswith(b"ApproachRate"):
            difficutly_section["approach_rate"] = float(value)
            has_approach_rate = True

        elif line.startswith(b"SliderMultiplier"):
            difficutly_section["slider_multiplier"] = float(value)

        elif line.startswith(b"SliderTickRate"):
            difficutly_section["slider_tick_rate"] = float(value)

    return DifficultySection(**difficutly_section)


def _parse_events_section(
    section_contents: bytearray, *, format_version: int
) -> EventsSection:
    # TODO: storyboard handling
    events_section: dict[str, Any] = {}
    lines = section_contents.split(b"\n")

    videos = []
    break_periods = []
    for line in lines:
        if not line:
            continue

        if line.startswith(b"//"):
            continue

        values = line.split(b",")

        match values[0]:
            case b"0" | b"Background":
                events_section["background"] = {
                    "filename": _clean_file_name(values[2]),
                    "x_offset": 0,
                    "y_offset": 0,
                }

                if len(values) > 3:
                    events_section["background"]["x_offset"] = int(values[3])

                if len(values) > 4:
                    events_section["background"]["y_offset"] = int(values[4])

            case b"1" | b"Video":
                video: dict[str, Any] = {
                    "filename": _clean_file_name(values[2]),
                    "start_time": _get_offset_time(int(values[1]), format_version),
                    "x_offset": 0,
                    "y_offset": 0,
                }

                if len(values) > 3:
                    video["x_offset"] = int(values[3])

                if len(values) > 4:
                    video["y_offset"] = int(values[4])

                videos.append(video)

            case b"2" | b"Break":
                break_periods.append(
                    {
                        "start_time": _get_offset_time(int(values[1]), format_version),
                        "end_time": _get_offset_time(int(values[2]), format_version),
                    },
                )

    if videos:
        events_section["videos"] = videos

    if break_periods:
        events_section["break_periods"] = break_periods

    return EventsSection(**events_section)


def _parse_colours_section(section_contents: bytearray) -> ColoursSection:
    colours_section: dict[str, Any] = {}
    lines = section_contents.split(b"\n")

    custom_combo_colours = []
    for line in lines:
        if not line:
            continue

        values = _parse_value_from_str(line).split(",")

        colour = {
            "red": int(values[0]),
            "green": int(values[1]),
            "blue": int(values[2]),
            "alpha": 255,
        }

        if line.startswith(b"Combo"):
            custom_combo_colours.append(colour)

        elif line.startswith(b"SliderTrackOverride"):
            colours_section["slider_track_override_colour"] = colour

        elif line.startswith(b"SliderBorder"):
            colours_section["slider_border_colour"] = colour

    if custom_combo_colours:
        colours_section["custom_combo_colours"] = custom_combo_colours

    return ColoursSection(**colours_section)


class ParsedTimingPointsData(TypedDict):
    timing_points: list[TimingPoint]
    minimum_bpm: float
    maximum_bpm: float


def _parse_timing_points_section(
    section_contents: bytearray,
    *,
    format_version: int,
    beatmap_sample_set: SampleSet,
    beatmap_sample_volume: int,
) -> ParsedTimingPointsData:

    timing_points = []
    minimum_bpm = float("inf")
    maximum_bpm = float("-inf")

    lines = section_contents.split(b"\n")

    for line in lines:
        if not line:
            continue

        timing_point: dict[str, Any] = {}
        values = line.split(b",")

        timing_point["start_time"] = _get_offset_time(int(values[0]), format_version)
        timing_point["beat_length"] = float(values[1])

        timing_point["slider_velocity"] = (
            100 / -timing_point["beat_length"] if timing_point["beat_length"] < 0 else 1
        )

        time_signature = TimeSignature.SimpleQuadruple()
        if len(values) >= 3:
            time_signature = (
                time_signature
                if values[2] == b"0"
                else TimeSignature(numerator=int(values[2]))
            )
        timing_point["time_signature"] = time_signature

        sample_set = beatmap_sample_set
        if len(values) >= 4:
            sample_set = SampleSet.from_int_enum(int(values[3]))
        timing_point["sample_set"] = sample_set

        custom_sample_bank = 0
        if len(values) >= 5:
            custom_sample_bank = int(values[4])
        timing_point["custom_sample_bank"] = custom_sample_bank

        sample_volume = beatmap_sample_volume
        if len(values) >= 6:
            sample_volume = int(values[5])
        timing_point["sample_volume"] = sample_volume

        timing_change = True
        if len(values) >= 7:  # also known as "uninherited"
            timing_change = values[6] == b"1"
        timing_point["timing_change"] = timing_change

        kiai_mode = False
        omit_first_bar_line = False

        if len(values) >= 8:
            effects = Effects(int(values[7]))
            kiai_mode = effects.has_kiai()
            omit_first_bar_line = effects.has_omit_first_bar_line()

        timing_point["kiai_mode"] = kiai_mode
        timing_point["omit_first_bar_line"] = omit_first_bar_line

        if timing_point["timing_change"]:
            current_bpm = round(60000 / timing_point["beat_length"])
            minimum_bpm = min(minimum_bpm, current_bpm) if minimum_bpm else current_bpm
            maximum_bpm = max(maximum_bpm, current_bpm) if maximum_bpm else current_bpm

        timing_points.append(TimingPoint(**timing_point))

    return ParsedTimingPointsData(
        timing_points=timing_points,
        minimum_bpm=minimum_bpm,
        maximum_bpm=maximum_bpm,
    )


def _parse_hit_objects_section(
    section_contents: bytearray, *, format_version: int
) -> ...:
    ...


def _parse_beatmap_contents(buffer_bytes: bytearray) -> OsuBeatmapFile:
    beatmap: dict[str, Any] = {}
    beatmap["file_hash"] = hashlib.md5(buffer_bytes).hexdigest()

    lines = buffer_bytes.replace(b"\r\n", b"\n").split(b"\n")

    header = lines.pop(0)
    if not header.startswith(b"osu file format v"):
        raise ValueError(
            f"Invalid beatmap file format, expected header: 'osu file format v', got: '{header}'",
        )

    beatmap["format_version"] = int(header.split(b"v")[-1])
    sections = _split_contents_to_sections(lines)

    beatmap["general"] = _parse_general_section(
        sections["general"],
        format_version=beatmap["format_version"],
    )
    beatmap["editor"] = _parse_editor_section(sections["editor"])
    beatmap["metadata"] = _parse_metadata_section(sections["metadata"])
    beatmap["difficulty"] = _parse_difficulty_section(sections["difficulty"])
    beatmap["events"] = _parse_events_section(
        sections["events"],
        format_version=beatmap["format_version"],
    )

    parsed_timing_points_data = _parse_timing_points_section(
        sections["timingpoints"],
        format_version=beatmap["format_version"],
        beatmap_sample_set=beatmap["general"].sample_set,
        beatmap_sample_volume=beatmap["general"].sample_volume,
    )
    beatmap["timing_points"] = parsed_timing_points_data["timing_points"]
    beatmap["minimum_bpm"] = parsed_timing_points_data["minimum_bpm"]
    beatmap["maximum_bpm"] = parsed_timing_points_data["maximum_bpm"]

    beatmap["colours"] = _parse_colours_section(sections["colours"])
    beatmap["hit_objects"] = _parse_hit_objects_section(
        sections["hitobjects"],
        format_version=beatmap["format_version"],
    )

    return OsuBeatmapFile(**beatmap)


def read_osu_file(file_path: str) -> OsuBeatmapFile:
    with open(file_path, "rb") as file_buffer:
        buffer_bytes = bytearray(file_buffer.read())

    return _parse_beatmap_contents(buffer_bytes)


def read_osu_buffer(file_buffer: BytesLike) -> OsuBeatmapFile:
    buffer_bytes = bytearray(file_buffer)

    return _parse_beatmap_contents(buffer_bytes)
