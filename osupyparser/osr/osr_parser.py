from .iobytes import BinaryRotator
from .constants import OsuReplayFrame, CatchReplayFrame, ManiaReplayFrame, TaikoReplayFrame, Key, KeyTaiko, KeyMania
import lzma

class ReplayFile:
    """A class representing replay file data."""
    
    def __init__(self):
        self.__reader = None

        self.mode: int = 0
        self.osu_version: int = 0
        self.map_md5: str = ""
        self.player_name: str = ""
        self.replay_md5: str = ""
        self.n300: int = 0
        self.n100: int = 0
        self.n50: int = 0
        self.ngeki: int = 0
        self.nkatu: int = 0
        self.nmiss: int = 0
        self.score: int = 0
        self.max_combo: int = 0
        self.perfect: bool = False
        self.mods: int = 0
        self.life_graph: str = ""
        self.timestamp: int = 0
        self.frames: list = []
        self.score_id: int = 0
        self.seed: int = 0

    @classmethod
    def from_bytes(cls, bytedata: bytes, pure_lzma: bool = False):
        """Parses replay from bytes data."""
        cls.__init__(cls)

        cls.__reader = BinaryRotator(bytedata)
        return cls.parse_data(cls, pure_lzma)
    
    @classmethod
    def from_file(cls, file_path: str, pure_lzma: bool = False):
        """Parses replay from file path."""
        cls.__init__(cls)

        with open(file_path, "rb") as stream:
            cls.__reader = BinaryRotator(stream.read())
        return cls.parse_data(cls, pure_lzma)

    def parse_lzma(self):
        """Parses only lzma data from replay."""
        decompressed = lzma.decompress(self.__reader.data, format= lzma.FORMAT_AUTO).decode('ascii')[:-1]
        for action in decompressed.split(","):
            split = action.split("|")
            if split[0] != "-12345":
                frame = OsuReplayFrame(int(split[0]), float(split[1]), float(split[2]), Key(int(split[3])))
                self.frames.append(frame)
            else:
                self.seed = int(split[3])
    
    def parse_data(self, only_lzma: bool):
        """Parses all replay data."""
        if only_lzma:
            self.parse_lzma()
            return self
        
        self.mode = self.__reader.read_u8()
        self.osu_version = self.__reader.read_i32()
        self.map_md5 = self.__reader.read_string()
        self.player_name = self.__reader.read_string()
        self.replay_md5 = self.__reader.read_string()
        self.n300 = self.__reader.read_i16()
        self.n100 = self.__reader.read_i16()
        self.n50 = self.__reader.read_i16()
        self.ngeki = self.__reader.read_i16()
        self.nkatu = self.__reader.read_i16()
        self.nmiss = self.__reader.read_i16()
        self.score = self.__reader.read_i32()
        self.max_combo = self.__reader.read_i16()
        self.perfect = self.__reader.read_u8() == 1
        self.mods = self.__reader.read_i32()
        self.life_graph = self.__reader.read_string()
        self.timestamp = self.__reader.read_i64()

        lzma_len = self.__reader.read_i32()
        lzma_data = self.__reader.read(lzma_len)

        decompressed = lzma.decompress(lzma_data, format= lzma.FORMAT_AUTO).decode('ascii')[:-1]
        for action in decompressed.split(","):
            split = action.split("|")
            if split[0] != "-12345":
                if self.mode == 1:
                    frame = TaikoReplayFrame(int(split[0]), float(split[1]), KeyTaiko(int(split[3])))
                elif self.mode == 2:
                    frame = CatchReplayFrame(int(split[0]), float(split[1]), split[3] == "1")
                elif self.mode == 3:
                    frame = ManiaReplayFrame(int(split[0]), KeyMania(int(split[1])))
                else:
                    frame = OsuReplayFrame(int(split[0]), float(split[1]), float(split[2]), Key(int(split[3])))
                self.frames.append(frame)
            else:
                self.seed = int(split[3])
            
        if self.osu_version <= 20121008: self.score_id = self.__reader.read_i32()
        else: self.score_id = self.__reader.read_i64()

        return self