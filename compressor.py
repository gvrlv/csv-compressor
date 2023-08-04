#!/usr/bin/env python
import abc
import bz2
import gzip
import json
import pathlib
import argparse
import typing as tp


class Compressor(abc.ABC):
    @abc.abstractmethod
    def compress(data: str) -> bytes:
        pass

    @abc.abstractmethod
    def get_suffix(self) -> str:
        pass


class Encryptor(abc.ABC):
    @abc.abstractmethod
    def encrypt(data: str) -> bytes:
        pass


class GzipCompressor(Compressor):
    def __init__(self, level: int) -> None:
        self.level = level

    def compress(self, data: str) -> bytes:
        return gzip.compress(data.encode(), self.level)

    def get_suffix(self) -> str:
        return '.gzip'


class BZ2Compressor(Compressor):
    def __init__(self, level: int) -> None:
        self.level = level

    def compress(self, data: str) -> bytes:
        return bz2.compress(data.encode(), self.level)

    def get_suffix(self) -> str:
        return '.bz2'


class NoCompressionCompressor(Compressor):
    def compress(self, data: str) -> bytes:
        return data.encode()

    def get_suffix(self) -> str:
        return ''


class FileManager:
    def __init__(
        self, filename: str, compressor: tp.Optional[Compressor]
    ) -> None:
        self.path = pathlib.Path(filename)
        self.compressor = compressor

    def read(self) -> str:
        data = []
        with self.path.open() as _file:
            for line in _file:
                key, value = line.split(',', 2)
                data.append({'key': key, 'value': value.strip()})
        return json.dumps(data)

    def write(self, filename: pathlib.Path, data: str) -> None:
        filename.write_bytes(self.compressor.compress(data))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, required=True)
    parser.add_argument(
        '--compress-with', type=str, required=False, choices=['gzip', 'bz2']
    )
    parser.add_argument('--compress-level', type=int, required=False, default=9)

    return parser.parse_args()


def main():
    args = parse_args()
    filename = pathlib.Path(args.filename)
    compressor = NoCompressionCompressor()
    if args.compress_with == 'gzip':
        compressor = GzipCompressor(args.compress_level)
    if args.compress_with == 'bz2':
        compressor = BZ2Compressor(args.compress_level)

    manager = FileManager(filename, compressor)
    data = manager.read()
    manager.write(filename.with_suffix(compressor.get_suffix()), data)


if __name__ == '__main__':
    main()
