from osupyparser import OsuFile
import time
import unittest


class TestBeatmap(unittest.TestCase):
    def test_basic_functionality(self):
        start = time.perf_counter()
        data = OsuFile("tests//testv2.osu").parse_file()
        end = time.perf_counter()
        self.assertTrue(data.__dict__)
        info = data.__dict__
        for d, e in info.items():
            print(f"{d}: {e}")
        print(f"Parsed in {round((end - start) * 1000, 2)}ms")

    def test_nested_tag(self):
        data = OsuFile("tests//testVersionInTag.osu").parse_file()
        self.assertTrue(data.__dict__)


if __name__ == '__main__':
    unittest.main()
