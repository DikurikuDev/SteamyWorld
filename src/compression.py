from abc import ABC, abstractmethod
from glob import glob
from os import remove
from os.path import basename, dirname, join
from zipfile import ZipFile
import zlib
from logger import Logger


class CompressionHandler(ABC):
    @abstractmethod
    def __init__(self, path, options):
        pass

    @abstractmethod
    def start(self):
        pass


class Compressor(CompressionHandler):
    def __init__(self, path, options={}):
        self.path = path
        self.logger = options.get("logger", Logger())

    def __impak(self):
        pass

    def __z(self):
        pass

    def start(self):
        pass


class Decompressor(CompressionHandler):
    def __init__(self, path, options={}):
        self.path = path
        self.logger: Logger = options.get("logger", Logger())

    def __impak(self, paths):
        for path in paths:
            lock_path = f"{path}.lock"
            dir = dirname(path)

            with ZipFile(path, "r") as file:
                self.logger.debug(f"creating {lock_path}...")
                with open(lock_path, "w") as lock:
                    for name in file.namelist():
                        lock.write(f"{name}\r\n")

                self.logger.info(f"decompressing {path}...")
                file.extractall(dir)

            self.logger.debug(f"removing {path}...")
            remove(path)

            self.logger.debug("done!")

    def __z(self, paths):
        for path in paths:
            dir = dirname(path)
            output_name = basename(path[:-2])
            output_path = join(dir, output_name)
            lock_path = join(dir, "z.lock")

            self.logger.debug(f"creating {lock_path}...")
            with open(lock_path, "a") as lock:
                lock.write(f"{output_name}\r\n")

            self.logger.info(f"decompressing {path}...")
            with open(path, "rb") as compressed_file:
                with open(output_path, "wb") as file:
                    # skipping header
                    compressed_file.seek(4)
                    compressed_data = compressed_file.read()
                    decompressed_data = zlib.decompress(compressed_data)
                    file.write(decompressed_data)

            self.logger.debug(f"removing {path}...")
            remove(path)

            self.logger.debug("done!")

    def start(self):
        self.logger.info(f"at folder {self.path}:")
        self.logger.info("starting decompression...")
        self.logger.debug("searching .z files...")
        paths = _find_all_files_with_extension(self.path, "z")
        self.logger.debug(f"found {len(paths)} file(s)!")
        self.logger.debug("searching .impak files...")
        self.__z(paths)
        paths = _find_all_files_with_extension(self.path, "impak")
        self.logger.debug(f"found {len(paths)} file(s)!")
        self.__impak(paths)
        self.logger.info("decompression done!")


def _find_all_files_with_extension(path, extension):
    return glob(f"{path}/**/*.{extension}", recursive=True)
