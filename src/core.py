from compression import CompressionHandler, Compressor, Decompressor
from logger import Logger


def __terminalLogging(message):
    print(message)


def main(options):
    logger_options = {
        "run_quietly": options["quiet"],
        "verbosety_level": options["verbose"],
    }
    logger = Logger(logger_options)
    logger.onLog(__terminalLogging)

    compression_options = {"logger": logger}
    compression_path = options["game_directory"]
    compression_handler: CompressionHandler = Decompressor
    if options["action"] == "compress":
        compression_handler = Compressor
    compression = compression_handler(compression_path, compression_options)
    compression.start()
