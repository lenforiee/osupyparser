# -*- coding: utf-8 -*-
import hashlib
import math
from typing import List
from typing import Dict
from typing import Optional
from .objects import Position
from .objects import Circle
from .objects import Slider
from .objects import Spinner
from .objects import HitObject
from .objects import Additions
from .objects import Edge
from .objects import TimingPoint
from .constants import ObjectType
from .constants import OSU_FILE_HEADER
from .constants import CURVE_TYPES

class OsuFile:
    """A class representing all data from .osu file."""

    def __init__(self, file_path: str):
        self.__file_path: str = file_path

        # Header of file.
        self.file_version: int = 0

        # General section.
        self.audio_filename: str = ""
        self.audio_lead_in: int = 0
        self.preview_time: int = 0
        self.countdown: int = 0
        self.sample_set: str = ""
        self.stack_leniency: float = 0.0
        self.mode: int = 0
        self.letterbox_in_breaks: bool = False
        self.widescreen_storyboard: bool = False
        
        # Editor section.
        self.distance_spacing: float = 0.0
        self.beat_divisor: int = 0
        self.grid_size: int = 0
        self.timeline_zoom: float = 0.0

        # Metadata section.
        self.title: str = ""
        self.title_unicode: str = ""
        self.artist: str = ""
        self.artist_unicode: str = ""
        self.creator: str = ""
        self.version: str = ""
        self.source: str = ""
        self.tags: str = ""
        self.beatmap_id: int = 0
        self.beatmap_set_id: int = 0

        # Difficulty section.
        self.hp: float = 0.0
        self.cs: float = 0.0
        self.od: float = 0.0
        self.ar: float = 0.0
        self.slider_multiplier: float = 0.0
        self.slider_tick_rate: int = 0

        # Events section.
        self.has_video: bool = False
        self.video_file: str = ""
        self.background_file: str = ""
        self.break_times: List[List[int, int]] = []
        self.break_time: int = 0
        self.storyboards: list = []

        # TimingPoints section.
        self.timing_points: List[TimingPoint] = []

        # Colours section.
        self.colours: Dict[str, tuple] = {}

        # HitObjects section.
        self.hit_objects: List[HitObject] = []

        # External data.
        self.md5: str = ""
        self.max_combo: int = 0
        self.bpm: int = -1
        self.total_hits: int = 0
        self.play_time: float = 0.0
        self.drain_time: float = 0.0
        self.ncircles: int = 0
        self.nsliders: int = 0
        self.nspinners: int = 0

    def parse_file(self):
        """Parses sections and set them to class variables."""

        with open(self.__file_path, "rb") as stream:
            buffer = stream.read()
        lines = list(map(lambda x: x.strip(), buffer.decode("utf-8").split("\n"))) # Strip lines.
        self.md5 = hashlib.md5(buffer).digest().hex()

        if not lines[0].startswith(OSU_FILE_HEADER):
            # First line should have osu special header.
            raise ValueError(f"Unknown file error! Excepted: {OSU_FILE_HEADER}, got {lines[0]}")
        self.file_version = int(lines[0][len(OSU_FILE_HEADER):])

        section_name = ""
        for line in lines[1:]:
            if not line: continue # Just continue looping.

            if line[0] == "[" and line[-1] == "]":
                section_name = line[1:-1].lower()
                continue
            
            # Call parser to take care of it.
            section_parser = getattr(self, f"{section_name}_parser", None)
            if not section_parser: continue
            section_parser(line)

        self.calculate_minor_things()
        self.calculate_max_combo()
        return self # Return self as some people would want to make one line parsing.

    def general_parser(self, line: str) -> None:
        """Parses [General] header data."""
        if "AudioFilename" in line:
            self.audio_filename = line.split("AudioFilename: ")[1]
        elif "AudioLeadIn" in line:
            self.audio_lead_in = int(line.split("AudioLeadIn: ")[1])
        elif "PreviewTime" in line:
            self.preview_time = int(line.split("PreviewTime: ")[1])
        elif "Countdown" in line:
            self.countdown = int(line.split("Countdown: ")[1])
        elif "SampleSet" in line:
            self.sample_set = line.split("SampleSet: ")[1]
        elif "StackLeniency" in line:
            self.stack_leniency = float(line.split("StackLeniency: ")[1])
        elif "Mode" in line:
            self.mode = int(line.split("Mode: ")[1])
        elif "LetterboxInBreaks" in line: # Making it bool.
            self.letterbox_in_breaks = "1" == line.split("LetterboxInBreaks: ")[1]
        elif "WidescreenStoryboard" in line: # Same here.
            self.widescreen_storyboard = "1" == line.split("WidescreenStoryboard: ")[1]
    
    def editor_parser(self, line: str) -> None:
        """Parses [Editor] header data."""
        if "DistanceSpacing" in line:
            self.distance_spacing = float(line.split("DistanceSpacing: ")[1])
        elif "BeatDivisor" in line:
            self.beat_divisor = int(line.split("BeatDivisor: ")[1])
        elif "GridSize" in line:
            self.grid_size = int(line.split("GridSize: ")[1])
        elif "TimelineZoom" in line:
            self.timeline_zoom = float(line.split("TimelineZoom: ")[1])

    def metadata_parser(self, line: str) -> None:
        """Parses [Metadata] header data."""
        if "Title:" in line:
            self.title = line.split("Title:")[1]
        elif "TitleUnicode" in line:
            self.title_unicode = line.split("TitleUnicode:")[1]
        elif "Artist:" in line:
            self.artist = line.split("Artist:")[1]
        elif "ArtistUnicode" in line:
            self.artist_unicode = line.split("ArtistUnicode:")[1]
        elif "Creator" in line:
            self.creator = line.split("Creator:")[1]
        elif "Version" in line:
            self.version = line.split("Version:")[1]
        elif "Source" in line:
            self.source = line.split("Source:")[1]
        elif "Tags" in line:
            self.tags = line.split("Tags:")[1]
        elif "BeatmapID" in line:
            self.beatmap_id = int(line.split("BeatmapID:")[1])
        elif "BeatmapSetID" in line:
            self.beatmap_set_id = int(line.split("BeatmapSetID:")[1])
    
    def difficulty_parser(self, line: str) -> None:
        """Parses [Difficulty] header data."""
        if "HPDrainRate" in line:
            self.hp = float(line.split("HPDrainRate:")[1])
        elif "CircleSize" in line:
            self.cs = float(line.split("CircleSize:")[1])
        elif "OverallDifficulty" in line:
            self.od = float(line.split("OverallDifficulty:")[1])
        elif "ApproachRate" in line:
            self.ar = float(line.split("ApproachRate:")[1])
        elif "SliderMultiplier" in line:
            self.slider_multiplier = float(line.split("SliderMultiplier:")[1])
        elif "SliderTickRate" in line:
            self.slider_tick_rate = float(line.split("SliderTickRate:")[1])
    
    def events_parser(self, line: str) -> None:
        """Parses [Events] header data."""
        if not "//" in line:
            data = line.split(",")

            if data and data[0] == "Video":
                self.has_video = True
                self.video_file = data[2]
                if data[2][0] == '"':
                    self.video_file = data[2][1:-1]

            elif data and data[0] == "0" and data[1] == "0":
                # Its most likely background.
                self.background_file = data[2]
                if data[2][0] == '"': # Fix it then.
                    self.background_file = data[2][1:-1]
            
            elif data and data[0] == "2":
                self.break_times.append([int(data[1]), int(data[2])])
    
    # Taken from https://github.com/nojhamster/osu-parser/blob/539b73e087d46de7aa7159476c7ea6ac50983c97/index.js#L99
    def timingpoints_parser(self, line: str) -> None:
        """Parses [TimingPoints] header data."""
        data = line.split(",")
        point = TimingPoint(
            offset= int(data[0]),
            beat_length= float(data[1]),
            velocity= 1,
            bpm= -1,
            time_signature= int(data[2]),
            sample_set_id= int(data[3]),
            custom_sample_index= int(data[4]),
            sample_volume= int(data[5]),
            timing_change= '1' == data[6],
            kiai_time_active= None if not len(data) > 6 else '1' == data[7]
        )

        if point.beat_length:
            if point.beat_length > 0:
                # If positive, beat_length is the length of a beat in milliseconds.
                self.bpm = point.bpm = round(60000 / point.beat_length)
            else:
                # If negative, beat_length is a velocity factor.
                point.velocity = abs(100 / point.beat_length)
        
        self.timing_points.append(point)
    
    def colours_parser(self, line: str) -> None:
        """Parses [Colours] header data."""
        name, rgb_colours = line.split(" : ")
        rgb = rgb_colours.split(",")

        self.colours |= {name: (int(rgb[0]), int(rgb[1]), int(rgb[2]))}

    # Also taken from https://github.com/nojhamster/osu-parser/blob/539b73e087d46de7aa7159476c7ea6ac50983c97/index.js#L134
    def hitobjects_parser(self, line: str) -> None:
        """Parses [HitObjects] header data."""
        data = line.split(",")

        hit_type = int(data[3])
        sound_type = int(data[4])
        new_combo = (hit_type & 4) == 4

        hitsounds_types = []
        if sound_type & 2: hitsounds_types.append("Whistle")
        if sound_type & 4: hitsounds_types.append("Finish")
        if sound_type & 8: hitsounds_types.append("Clap")
        else: hitsounds_types.append("Normal")

        if hit_type & ObjectType.CIRCLE:
            self.ncircles += 1
            hitobject = Circle(
                pos= Position(int(data[0]), int(data[1])),
                start_time= int(data[2]),
                new_combo = new_combo,
                sound_types= hitsounds_types,
                additions= self.parse_addition(data[5])
            )
        elif hit_type & ObjectType.SPINNER:
            self.nspinners += 1
            hitobject = Spinner(
                pos= Position(int(data[0]), int(data[1])),
                start_time= int(data[2]),
                new_combo= new_combo,
                sound_types= hitsounds_types,
                additions= self.parse_addition(data[6]),
                end_time= int(data[5])
            )
        elif hit_type & ObjectType.SLIDER:
            # Hell comes...
            self.nsliders += 1
            duration = 0
            curve_type = ""
            points_list = []
            edges = []

            timing = self.get_timing_point(int(data[2]))
            if timing:
                px_per_beat = self.slider_multiplier * 100 * timing.velocity
                beats_count = (float(data[7]) * int(data[6])) / px_per_beat
                duration = math.ceil(beats_count * timing.beat_length)
            
            points = ('' if len(data) < 5 else data[5]).split("|")
            if points:
                curve_type = CURVE_TYPES.get(points[0])
                for point in points[1:]:
                    x, y = point.split(":")
                    points_list.append(Position(int(x), int(y)))

            edge_sounds = []
            edge_additions = []
            if len(data) > 8: edge_sounds = data[8].split('|')
            if len(data) > 9: edge_additions = data[9].split('|')

            for i in range(0, int(data[6]) + 1):
                additions = self.parse_addition(edge_additions[i])
                sound_edge_types = []

                if edge_sounds and len(edge_sounds) > i:
                    sound = int(edge_sounds[i])
                    if sound & 2: sound_edge_types.append("Whistle")
                    if sound & 4: sound_edge_types.append("Finish")
                    if sound & 8: sound_edge_types.append("Clap")
                    if not len(sound_edge_types): sound_edge_types.append("Normal")
                else:
                    sound_edge_types.append("Normal")

                edges.append(Edge(sound_edge_types, additions))

            hitobject = Slider(
                pos= Position(int(data[0]), int(data[1])),
                start_time= int(data[2]),
                new_combo= new_combo,
                sound_types= hitsounds_types,
                additions= self.parse_addition(data[10]),
                repeat_count= int(data[6]),
                pixel_length= float(data[7]),
                edges= edges,
                points= points_list,
                duration= duration,
                end_time= (int(data[2]) + duration),
                curve_type= curve_type,
                end_position= points_list[-1]
            )
        else:
            # Might be some hitobject I dont know about..
            hitobject = HitObject(
                pos= Position(int(data[0]), int(data[1])),
                start_time= int(data[2]),
                new_combo= new_combo,
                sound_types= hitsounds_types
            )

        self.total_hits += 1
        self.hit_objects.append(hitobject)
    
    def parse_addition(self, line: str) -> Optional[Additions]:
        """Parses addictional hitobject data."""
        if not line: return None

        samples = {
            "1": 'Normal',
            "2": "Soft",
            "3": "Drum"
        }
        data = line.split(":")
        addition = {}
        if not data: return None
        if len(data) > 0: addition['sample'] = samples.get(data[0], None)
        if len(data) > 1: addition['additional_sample'] = samples.get(data[1], None)
        if len(data) > 2: addition['custom_sample_index'] = int(data[2])
        if len(data) > 3: addition['hitsound_volume'] = int(data[3])
        if len(data) > 4: addition['hitsound'] = data[4]

        additional = Additions(**addition)
        return additional

    def get_timing_point(self, offset: int) -> TimingPoint:
        """Finds a timing point with given offset."""
        for timing in self.timing_points:
            if timing.offset <= offset: return timing
        
        return self.timing_points[0]

    # Reference https://github.com/Francesco149/pyttanko/blob/master/pyttanko.py#L265
    def calculate_max_combo(self) -> None:
        """Calculates a combo for map."""
        combo = 0
        timings = self.timing_points
        index = -1
        px_per_beat = None
        next_offset = -float("inf")

        for hitobject in self.hit_objects:
            if not isinstance(hitobject, Slider):
                combo += 1
                continue

            while next_offset != None and hitobject.start_time >= next_offset:
                index += 1
                if len(timings) > index + 1:
                    next_offset = timings[index + 1].offset
                else:
                    next_offset = None
                
                timing = timings[index]
                sv_multiplier = 1.0

                if not timing.timing_change and timing.beat_length < 0:
                    sv_multiplier = (-100.0 / timing.beat_length)
                
                px_per_beat = self.slider_multiplier * 100.0 * sv_multiplier
                if self.file_version < 8:
                    px_per_beat /= sv_multiplier
            
            num_beats = (
                (hitobject.pixel_length * hitobject.repeat_count) / px_per_beat
            )

            ticks = int(
                math.ceil(
                    (num_beats - 0.1) /
                    hitobject.repeat_count * self.slider_tick_rate
                )
            )

            ticks -= 1
            ticks *= hitobject.repeat_count
            ticks += hitobject.repeat_count + 1

            combo += max(0, ticks)

        self.max_combo = combo

    def calculate_minor_things(self) -> None:
        """Calculates rest of minor things."""
        first_obj = self.hit_objects[0]
        last_obj = self.hit_objects[-1]

        for break_time in self.break_times:
            self.break_time += (break_time[1] - break_time[0])
        
        if first_obj and last_obj:
            self.play_time = math.floor(last_obj.start_time / 1000)
            self.drain_time = math.floor((last_obj.start_time - first_obj.start_time - self.break_time) / 1000)
