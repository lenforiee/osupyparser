from osupyparser import OsuFile

data = OsuFile("test.osu").parse_file()
info = data.__dict__
for d, e in info.items():
    print(f"{d}: {e}")