from __future__ import annotations

import re
from typing import Any
from typing import TextIO

from osupyparser.osu.models.beatmap import OsuBeatmapFile
from osupyparser.osu.models.sections.colours import ColoursSection
from osupyparser.osu.models.sections.difficulty import DifficultySection
from osupyparser.osu.models.sections.editor import EditorSection
from osupyparser.osu.models.sections.events import EventsSection
from osupyparser.osu.models.sections.general import GeneralSection
from osupyparser.osu.models.sections.metadata import MetadataSection

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


def _parse_beatmap_contents(lines: list[str]) -> OsuBeatmapFile:
    beatmap: dict[str, Any] = {}

    header = lines.pop(0)
    if not header.startswith("osu file format v"):
        raise ValueError("Invalid file format")

    beatmap["format_version"] = int(header.split("osu file format v")[-1])
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
    beatmap["colours"] = _parse_colours_section(sections["colours"])

    return OsuBeatmapFile(**beatmap)


def read_osu_file(file_path: str) -> OsuBeatmapFile:
    with open(file_path, encoding="utf-8-sig", errors="ignore") as file_buffer:
        lines = file_buffer.readlines()

    return _parse_beatmap_contents(lines)


def read_osu_buffer(file_buffer: TextIO) -> OsuBeatmapFile:
    lines = file_buffer.readlines()
    return _parse_beatmap_contents(lines)
