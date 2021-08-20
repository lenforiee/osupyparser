from osupyparser import OsuFile
import time

start = time.perf_counter()
data = OsuFile("test.osu").parse_file()
end = time.perf_counter()
info = data.__dict__
for d, e in info.items():
    print(f"{d}: {e}")
print(f"Parsed in {round((end - start) * 1000, 2)}ms")