
class Position:
    """A (x, y) coordinates class."""
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

class HitObject:
    """Subclass representing standalone hitobject."""
    def __init__(self, x: int, y: int, start: int, new_combo: bool):
        self.pos = Position(x, y)
        self.start_time = start
        self.new_combo = new_combo
        self.sound_types = []
        self.additions = None

class Circle(HitObject):
    """Represents one circle object."""
    def __init__(self, x: int, y: int, start: int, new_combo: bool):
        super().__init__(x, y, start, new_combo)

class Spinner(HitObject):
    """Represents one spinner object."""
    def __init__(self, x: int, y: int, start: int, new_combo: bool):
        self.end_time: int = 0
        super().__init__(x, y, start, new_combo)

class Slider(HitObject):
    """Represents one slider object."""
    def __init__(self, x: int, y: int, start: int, new_combo: bool):
        self.repeat_count = 0
        self.pixel_length = 0
        self.edges = []
        self.points = [Position(x, y)]
        self.duration = 0
        self.end_time = 0
        self.curve_type = ""
        self.end_position = None
        super().__init__(x, y, start, new_combo)