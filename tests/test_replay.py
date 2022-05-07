from osupyparser import ReplayFile
import unittest
import time


class TestReplay(unittest.TestCase):
    def test_basic_functionality(self):
        start = time.perf_counter()
        data = ReplayFile.from_file("tests//test.osr")
        end = time.perf_counter()
        self.assertTrue(data.__dict__)
        info = data.__dict__
        for d, e in info.items():
            print(f"{d}: {e}")
        print(f"Parsed in {round((end - start) * 1000, 2)}ms")


if __name__ == '__main__':
    unittest.main()
