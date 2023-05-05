from abc import ABC, abstractmethod
from glob import glob
from os import listdir, remove
from os.path import basename, dirname, getsize, join
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

    def __impak(self, paths):
        for path in paths:
            dir = dirname(path)
            inpak_path = path[:-5]
            with open(path, "r") as lock:
                file_paths = lock.readlines()
                self.logger.info(f"compressing {inpak_path}...")
                with ZipFile(inpak_path, "w") as impak_file:
                    for file_path in file_paths:
                        relative_path = file_path.strip()
                        absolute_path = join(dir, relative_path)
                        self.logger.debug(f"adding {relative_path}...")
                        impak_file.write(absolute_path, relative_path)
                        self.logger.debug(f"removing {absolute_path}...")
                        remove(absolute_path)
                        self.logger.debug(f"removing folder (if empty)...")
                        _remove_folder_if_empty(dirname(absolute_path))

            self.logger.debug(f"removing {path}...")
            remove(path)

            self.logger.debug("done!")

    def __z(self, paths):
        for path in paths:
            dir = dirname(path)
            with open(path, "r") as lock:
                file_paths = lock.readlines()
                for file_path in file_paths:
                    original_path = join(dir, file_path.strip())
                    relative_path = f"{file_path.strip()}.z"
                    absolute_path = join(dir, relative_path)

                    self.logger.info(f"compressing {absolute_path}...")
                    with open(absolute_path, "wb") as zfile:
                        # adding header        
                        file_size = _get_file_size(original_path)
                        file_size_as_bytes = file_size.to_bytes(4, "little")
                        zfile.write(file_size_as_bytes)
                        with open(original_path, "rb") as file:
                            # adding file
                            uncompressed_data = file.read()
                            compressed_data = zlib.compress(uncompressed_data)            
                            zfile.write(compressed_data)
                    
                    self.logger.debug(f"removing {original_path}...")
                    remove(original_path)
            
            self.logger.debug(f"removing {file_path}...")
            remove(path)

            self.logger.debug("done!")

    def start(self):
        self.logger.info(f"at folder {self.path}:")
        self.logger.info("starting compression...")
        self.logger.debug("searching .z.lock files...")
        paths = _find_all_files(self.path, "z.lock")
        self.logger.debug(f"found {len(paths)} file(s)!")
        self.logger.debug("searching .impak.lock files...")
        self.__z(paths)
        paths = _find_all_files(self.path, "*.impak.lock")
        self.logger.debug(f"found {len(paths)} file(s)!")
        self.__impak(paths)
        self.logger.info("compression done!")


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
        paths = _find_all_files(self.path, "*.z")
        self.logger.debug(f"found {len(paths)} file(s)!")
        self.logger.debug("searching .impak files...")
        self.__z(paths)
        paths = _find_all_files(self.path, "*.impak")
        self.logger.debug(f"found {len(paths)} file(s)!")
        self.__impak(paths)
        self.logger.info("decompression done!")


def _find_all_files(path, filename_pattern):
    return glob(f"{path}/**/{filename_pattern}", recursive=True)

def _get_file_size(path):
    return getsize(path)

def _remove_folder_if_empty(path):
    if not listdir(path):
        remove(path)