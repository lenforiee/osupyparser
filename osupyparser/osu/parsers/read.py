from __future__ import annotations

import hashlib
import re
from typing import Any
from typing import TextIO
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


SECTION_REGEX = re.compile(r"\[([^\]]+)\]\s*((?:.*?\n)+?)(?=\[|$)")
EARLY_VERSION_TIMING_OFFSET = 24


def _split_contents_to_sections(lines: list[str]) -> dict[str, str]:
    sections: dict[str, str] = {}
    match_text = "\n".join(lines)

    for match_data in SECTION_REGEX.finditer(match_text):
        section_name = match_data.group(1).lower()
        section_contents = match_data.group(2).strip()
        sections[section_name] = section_contents

    return sections


def _get_offset_time(offset: int, format_version: int) -> int:
    if format_version < 5:
        return offset + EARLY_VERSION_TIMING_OFFSET

    return offset


def _parse_value_from_str(s: str) -> str:
    """Parses a value from a string."""

    return s.split(":", 1)[1].strip()


def _clean_file_name(filename: str) -> str:
    return filename.replace("\\", "/").strip('"')


def _parse_general_section(
    section_contents: str, *, format_version: int
) -> GeneralSection:
    general_section: dict[str, Any] = {}
    lines = section_contents.split("\n")

    for line in lines:
        if not line:
            continue

        value = _parse_value_from_str(line)

        if line.startswith("AudioFilename"):
            general_section["audio_filename"] = value

        elif line.startswith("AudioLeadIn"):
            general_section["audio_lead_in"] = int(value)

        elif line.startswith("AudioHash"):
            general_section["audio_hash"] = value

        elif line.startswith("PreviewTime"):
            time = int(value)
            general_section["preview_time"] = (
                time if time == -1 else _get_offset_time(time, format_version)
            )

        elif line.startswith("Countdown"):
            general_section["countdown"] = int(value)

        elif line.startswith("SampleSet"):
            general_section["sample_set"] = value

        elif line.startswith("SampleVolume"):
            general_section["sample_volume"] = int(value)

        elif line.startswith("StackLeniency"):
            general_section["stack_leniency"] = float(value)

        elif line.startswith("Mode"):
            general_section["mode"] = int(value)

        elif line.startswith("LetterboxInBreaks"):
            general_section["letterbox_in_breaks"] = value == "1"

        elif line.startswith("StoryFireInFront"):
            general_section["story_fire_in_front"] = value == "1"

        elif line.startswith("UseSkinSprites"):
            general_section["use_skin_sprites"] = value == "1"

        elif line.startswith("AlwaysShowPlayfield"):
            general_section["always_show_playfield"] = value == "1"

        elif line.startswith("OverlayPosition"):
            general_section["overlay_position"] = value

        elif line.startswith("SkinPreference"):
            general_section["skin_preference"] = value

        elif line.startswith("EpilepsyWarning"):
            general_section["epilepsy_warning"] = value == "1"

        elif line.startswith("CountdownOffset"):
            general_section["countdown_offset"] = int(value)

        elif line.startswith("SpecialStyle"):
            general_section["special_style"] = value == "1"

        elif line.startswith("WidescreenStoryboard"):
            general_section["widescreen_storyboard"] = value == "1"

        elif line.startswith("SamplesMatchPlaybackRate"):
            general_section["samples_match_playback_rate"] = value == "1"

    return GeneralSection(**general_section)


def _parse_editor_section(section_contents: str) -> EditorSection:
    editor_section: dict[str, Any] = {}
    lines = section_contents.split("\n")

    for line in lines:
        if not line:
            continue

        value = _parse_value_from_str(line)

        if line.startswith("Bookmarks"):
            editor_section["bookmarks"] = [
                int(x) for x in value.split(",") if x.strip()
            ]

        elif line.startswith("DistanceSpacing"):
            editor_section["distance_spacing"] = float(value)

        elif line.startswith("BeatDivisor"):
            editor_section["beat_divisor"] = int(value)

        elif line.startswith("GridSize"):
            editor_section["grid_size"] = int(value)

        elif line.startswith("TimelineZoom"):
            editor_section["timeline_zoom"] = float(value)

    return EditorSection(**editor_section)


def _parse_metadata_section(section_contents: str) -> MetadataSection:
    metadata_section: dict[str, Any] = {}
    lines = section_contents.split("\n")

    for line in lines:
        if not line:
            continue

        value = _parse_value_from_str(line)

        if line.startswith("Title:"):
            metadata_section["title"] = value

        elif line.startswith("TitleUnicode"):
            metadata_section["title_unicode"] = value

        elif line.startswith("Artist:"):
            metadata_section["artist"] = value

        elif line.startswith("ArtistUnicode"):
            metadata_section["artist_unicode"] = value

        elif line.startswith("Creator"):
            metadata_section["creator"] = value

        elif line.startswith("Version"):
            metadata_section["version"] = value

        elif line.startswith("Source"):
            metadata_section["source"] = value

        elif line.startswith("Tags"):
            metadata_section["tags"] = [tag for tag in value.split(" ") if tag.strip()]

        elif line.startswith("BeatmapID"):
            metadata_section["beatmap_id"] = int(value)

        elif line.startswith("BeatmapSetID"):
            metadata_section["beatmap_set_id"] = int(value)

    return MetadataSection(**metadata_section)


def _parse_difficulty_section(section_contents: str) -> DifficultySection:
    difficutly_section: dict[str, Any] = {}
    lines = section_contents.split("\n")

    for line in lines:
        if not line:
            continue

        value = _parse_value_from_str(line)
        has_approach_rate = False

        if line.startswith("HPDrainRate"):
            difficutly_section["hp_drain_rate"] = float(value)

        elif line.startswith("CircleSize"):
            difficutly_section["circle_size"] = float(value)

        elif line.startswith("OverallDifficulty"):
            difficutly_section["overall_difficulty"] = float(value)

            if not has_approach_rate:
                difficutly_section["approach_rate"] = float(value)

        elif line.startswith("ApproachRate"):
            difficutly_section["approach_rate"] = float(value)
            has_approach_rate = True

        elif line.startswith("SliderMultiplier"):
            difficutly_section["slider_multiplier"] = float(value)

        elif line.startswith("SliderTickRate"):
            difficutly_section["slider_tick_rate"] = float(value)

    return DifficultySection(**difficutly_section)


def _parse_events_section(
    section_contents: str, *, format_version: int
) -> EventsSection:
    # TODO: storyboard handling
    events_section: dict[str, Any] = {}
    lines = section_contents.split("\n")

    videos = []
    break_periods = []
    for line in lines:
        if not line:
            continue

        if line.startswith("//"):
            continue

        values = line.split(",")

        match values[0]:
            case "0" | "Background":
                events_section["background"] = {
                    "filename": _clean_file_name(values[2]),
                    "x_offset": int(values[3]),
                    "y_offset": int(values[4]),
                }
            case "1" | "Video":
                videos.append(
                    {
                        "filename": _clean_file_name(values[2]),
                        "start_time": _get_offset_time(int(values[1]), format_version),
                        "x_offset": int(values[3]),
                        "y_offset": int(values[4]),
                    },
                )
            case "2" | "Break":
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


def _parse_colours_section(section_contents: str) -> ColoursSection:
    colours_section: dict[str, Any] = {}
    lines = section_contents.split("\n")

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
            # NOTE: it seems like lazer might support alpha in near future but for now it doesn't
        }

        if line.startswith("Combo"):
            custom_combo_colours.append(colour)

        elif line.startswith("SliderTrackOverride"):
            colours_section["slider_track_override_colour"] = colour

        elif line.startswith("SliderBorder"):
            colours_section["slider_border_colour"] = colour

    if custom_combo_colours:
        colours_section["custom_combo_colours"] = custom_combo_colours

    return ColoursSection(**colours_section)


class ParsedTimingPointsData(TypedDict):
    timing_points: list[TimingPoint]
    minimum_bpm: float
    maximum_bpm: float


def _parse_timing_points_section(
    section_contents: str,
    *,
    format_version: int,
    beatmap_sample_set: SampleSet,
    beatmap_sample_volume: int,
) -> ParsedTimingPointsData:

    timing_points = []
    minimum_bpm = float("inf")
    maximum_bpm = float("-inf")

    lines = section_contents.split("\n")

    for line in lines:
        if not line:
            continue

        timing_point: dict[str, Any] = {}
        values = line.split(",")

        timing_point["start_time"] = _get_offset_time(int(values[0]), format_version)
        timing_point["beat_length"] = float(values[1])

        timing_point["slider_velocity"] = (
            100 / -timing_point["beat_length"] if timing_point["beat_length"] < 0 else 1
        )

        time_signature = TimeSignature.SimpleQuadruple()
        if len(values) >= 3:
            time_signature = (
                time_signature
                if values[2] == "0"
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
            timing_change = values[6] == "1"
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


def _parse_hit_objects_section(section_contents: str, *, format_version: int) -> ...:
    ...


def _parse_beatmap_contents(lines: list[str]) -> OsuBeatmapFile:
    beatmap: dict[str, Any] = {}
    beatmap["file_hash"] = hashlib.md5("\n".join(lines).encode()).hexdigest()

    header = lines.pop(0)
    if not header.startswith("osu file format v"):
        raise ValueError(
            f"Invalid beatmap file format, expected header: 'osu file format v', got: '{header}'",
        )

    beatmap["format_version"] = int(header.split("v")[-1])
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
    with open(file_path, encoding="utf-8-sig", errors="ignore") as file_buffer:
        lines = file_buffer.readlines()

    return _parse_beatmap_contents(lines)


def read_osu_buffer(file_buffer: TextIO) -> OsuBeatmapFile:
    lines = file_buffer.readlines()
    return _parse_beatmap_contents(lines)
