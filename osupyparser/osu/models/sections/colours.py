from __future__ import annotations

from pydantic import BaseModel

from osupyparser.common.colours import ColourRGBA


class ColoursSection(BaseModel):
    custom_combo_colours: list[ColourRGBA] | None = None
    slider_track_override_colour: ColourRGBA | None = None
    slider_border_colour: ColourRGBA | None = None
