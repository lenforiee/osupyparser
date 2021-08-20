class ObjectType:
  CIRCLE = 1 << 0
  SLIDER =  1 << 1
  SPINNER = 1 << 3

OSU_FILE_HEADER = "osu file format v"
CURVE_TYPES = {
    "C": "Catmull",
    "B": "Bezier",
    "L": "Linear",
    "P": "Pass-Through"
}