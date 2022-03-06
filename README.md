[![PyPI version](https://badge.fury.io/py/OsuPyParser.svg)](https://badge.fury.io/py/OsuPyParser.svg)
## OsuPyParser 
A powerful package for parsing .osu and .osr (replay) extention files.

### What's this?
OsuPyParser is my 2nd implementation of osu file and osr (replay) file parser.

It doesn't use any external packages so you don't need to install anything else!

## Example
Parsing osu files is simple as never.

### .osu file

```py
from osupyparser import OsuFile

data = OsuFile("test.osu").parse_file()
info = data.__dict__
for d, e in info.items():
    print(f"{d}: {e}") # Prints all members of the class.
```

### .osr file
```py
from osupyparser import ReplayFile

data = ReplayFile.from_file("test.osr")
info = data.__dict__
# pure_lzma = ReplayFile.from_file("test.osr", pure_lzma= True) This will return only lzma content.
# data = ReplayFile.from_bytes(replay_files) you can also use pure bytes.
for d, e in info.items():
    print(f"{d}: {e}") # Prints members of class.
```
## Testing
To run unittests type the following command to terminal in main directory:

`python3 -m unittest tests/test_beatmap.py tests/test_replay.py`

## Contribution
If you spot any issue/bug, don't heaste to open issue/make pull request.

I'll try to review it in free time :)

