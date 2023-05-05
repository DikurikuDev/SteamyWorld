from abc import ABC, abstractmethod
from logger import Logger


class CompressionHandler(ABC):
    @abstractmethod
    def __iter__(self, path, options):
        pass

    @abstractmethod
    def start(self):
        pass


class Compressor(CompressionHandler):
    def __init__(self, path, options={}):
        self.path = path
        self.logger = options.get("logger", Logger())

    def start(self):
        pass


class Decompressor(CompressionHandler):
    def __init__(self, path, options={}):
        self.path = path
        self.logger = options.get("logger", Logger())

    def start(self):
        pass
