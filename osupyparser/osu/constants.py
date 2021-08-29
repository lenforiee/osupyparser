class ObjectType:
  CIRCLE = 1
  SLIDER = 1 << 1
  NEW_COMBO = 1 << 2
  SPINNER = 1 << 3
  COMBO_OFFSET = (1 << 4) | (1 << 5) | (1 << 6)
  HOLD = 1 << 7

OSU_FILE_HEADER = "osu file format v"
CURVE_TYPES = {
    "C": "Catmull",
    "B": "Bezier",
    "L": "Linear",
    "P": "Pass-Through"
}