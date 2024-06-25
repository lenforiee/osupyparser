from __future__ import annotations

from typing import BinaryIO

from osupyparser.common.binary import BinaryReader


def _parse_replay_contents_lzma(reader: BinaryReader, length: int = -1) -> ...: ...


def _parse_replay_contents(reader: BinaryReader) -> ...: ...


def read_osr_file(file_path: str) -> ...:
    with open(file_path, "rb") as file_binary:
        reader = BinaryReader(file_binary.read())

    return _parse_replay_contents(reader)


def read_osr_file_lzma(file_path: str) -> ...:
    with open(file_path, "rb") as file_binary:
        reader = BinaryReader(file_binary.read())

    return _parse_replay_contents_lzma(reader)


def read_osr_binary(file_binary: BinaryIO) -> ...:
    reader = BinaryReader(file_binary.read())
    return _parse_replay_contents(reader)


def read_osr_binary_lzma(file_binary: BinaryIO) -> ...:
    reader = BinaryReader(file_binary.read())
    return _parse_replay_contents_lzma(reader)
