from __future__ import annotations

from pydantic import BaseModel

from osupyparser.constants.countdown import Countdown
from osupyparser.constants.mode import Mode
from osupyparser.constants.overlay_position import OverlayPosition
from osupyparser.constants.sample_set import SampleSet


# NOTE: This section out of all of them seem to have default values
class GeneralSection(BaseModel):
    audio_filename: str = ""
    audio_lead_in: int = 0
    audio_hash: str = ""  # Deprecated
    preview_time: int = -1
    countdown: Countdown = Countdown.NORMAL
    sample_set: SampleSet = SampleSet.NORMAL
    sample_volume: int = 100
    stack_leniency: float = 0.7
    mode: Mode = Mode.STANDARD
    letterbox_in_breaks: bool = False
    story_fire_in_front: bool = True  # Deprecated
    use_skin_sprites: bool = False
    always_show_playfield: bool = False  # Deprecated
    overlay_position: OverlayPosition = OverlayPosition.NO_CHANGE
    skin_preference: str = ""
    epilepsy_warning: bool = False
    countdown_offset: int = 0
    special_style: bool = False
    widescreen_storyboard: bool = False
    samples_match_playback_rate: bool = False
