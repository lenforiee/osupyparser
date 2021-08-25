from .iobytes import BinaryRotator
from .constants import OsuReplayFrame
from .constants import CatchReplayFrame
from .constants import ManiaReplayFrame
from .constants import TaikoReplayFrame
import lzma

class ReplayFile:
	"""A class representing replay file data."""
	
	def __init__(self) -> None:
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
		self.target_practice_hits: float = 0.0

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

	def parse_lzma(self) -> None:
		"""Parses only lzma data from replay."""
		data = lzma.decompress(self.__reader.buffer, format= lzma.FORMAT_AUTO).decode("ascii")
		frames = [ frame.split("|") for frame in data.split(",")[:-1] ]

		for action in frames:
			if self.osu_version >= 20130319 and action[0] == "-12345":
				# After 20130319 replays started to have seeds.
				self.seed = int(action[3])
				continue

			# We dont know what mode is it so we assume its standard.
			frame = OsuReplayFrame(int(action[0]), float(action[1]), float(action[2]), int(action[3]))
			self.frames.append(frame)
	
	def parse_data(self, only_lzma: bool):
		"""Parses all replay data."""
		if only_lzma:
			self.parse_lzma(self)
			return self
		
		self.mode = self.__reader.read_u8()
		self.osu_version = self.__reader.read_i32()
		self.map_md5 = self.__reader.read_string()
		self.player_name = self.__reader.read_string()
		self.replay_md5 = self.__reader.read_string()
		self.n300 = self.__reader.read_u16()
		self.n100 = self.__reader.read_u16()
		self.n50 = self.__reader.read_u16()
		self.ngeki = self.__reader.read_u16()
		self.nkatu = self.__reader.read_u16()
		self.nmiss = self.__reader.read_u16()
		self.score = self.__reader.read_i32()
		self.max_combo = self.__reader.read_u16()
		self.perfect = self.__reader.read_u8() == 1
		self.mods = self.__reader.read_i32()
		self.life_graph = self.__reader.read_string()
		self.timestamp = self.__reader.read_i64()

		lzma_len = self.__reader.read_i32()
		lzma_data = self.__reader.read(lzma_len)

		data = lzma.decompress(lzma_data, format= lzma.FORMAT_AUTO).decode("ascii")
		frames = [ frame.split("|") for frame in data.split(",")[:-1] ]

		for action in frames:
			if self.osu_version >= 20130319 and action[0] == "-12345":
				# After 20130319 replays started to have seeds.
				self.seed = int(action[3])
				continue

			if self.mode == 0:
				frame = OsuReplayFrame(int(action[0]), float(action[1]), float(action[2]), int(action[3]))
			elif self.mode == 1:
				frame = TaikoReplayFrame(int(action[0]), float(action[1]), int(action[3]))
			elif self.mode == 2:
				frame = CatchReplayFrame(int(action[0]), float(action[1]), action[3] == "1")
			elif self.mode == 3:
				frame = ManiaReplayFrame(int(action[0]), int(action[1]))
			
			self.frames.append(frame)

		# Reference: https://github.com/ppy/osu/blob/84e1ff79a0736aa6c7a44804b585ab1c54a84399/osu.Game/Scoring/Legacy/LegacyScoreDecoder.cs#L78-L81
		if self.osu_version >= 20140721:
			self.score_id = self.__reader.read_i64()
		elif self.osu_version >= 20121008:
			self.score_id = self.__reader.read_i32()

		if self.mods & 8388608:
			self.target_practice_hits = self.__reader.read_f64()

		return self