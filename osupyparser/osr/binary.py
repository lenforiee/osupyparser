from __future__ import annotations

import struct
from datetime import datetime
from datetime import timedelta
from datetime import timezone


class BinaryReader:
    """A binary-deserialisation class managing a buffer of bytes. Tailored for
    usage within osu's binary formats, such as Bancho packets and replays."""

    __slots__ = (
        "buffer",
        "offset",
    )

    def __init__(self, data: bytes = b"") -> None:
        self.buffer: bytearray = bytearray(data)
        self.offset: int = 0

    def __iadd__(self, other: bytes) -> BinaryReader:
        self.buffer += other
        return self

    def __len__(self) -> int:
        return len(self.buffer)

    def read(self, offset: int = -1) -> bytes:
        """Reads offseted data."""

        if offset < 0:
            offset = len(self.buffer) - self.offset

        data = self.buffer[self.offset : self.offset + offset]
        self.offset += offset
        return data

    def read_int(self, size: int, signed: bool) -> int:
        """Read a int."""
        return int.from_bytes(
            self.read(size),
            byteorder="little",
            signed=signed,
        )

    def read_u8(self) -> int:
        return self.read_int(1, False)

    def read_u16(self) -> int:
        return self.read_int(2, False)

    def read_i16(self) -> int:
        return self.read_int(2, True)

    def read_u32(self) -> int:
        return self.read_int(4, False)

    def read_i32(self) -> int:
        return self.read_int(4, True)

    def read_u64(self) -> int:
        return self.read_int(8, False)

    def read_i64(self) -> int:
        return self.read_int(8, True)

    def read_f32(self) -> float:
        return struct.unpack("<f", self.read(4))[0]

    def read_f64(self) -> float:
        return struct.unpack("<f", self.read(8))[0]

    def read_uleb128(self) -> int:
        """Reads a uleb bytes into int."""
        if self.read_u8() != 0x0B:
            return 0

        val = shift = 0
        while True:
            b = self.read_u8()
            val |= (b & 0b01111111) << shift
            if (b & 0b10000000) == 0:
                break
            shift += 7
        return val

    def read_string(self) -> str:
        """Read string."""
        s_len = self.read_uleb128()
        return self.read(s_len).decode()

    def read_datetime(self) -> datetime:
        """Read datetime."""
        ticks = self.read_i64()

        if ticks < 0 or ticks > 3155378975999999999:
            ticks = 0

        timestamp = datetime.min + timedelta(microseconds=ticks / 10)
        timestamp = timestamp.replace(tzinfo=timezone.utc)
        return timestamp
