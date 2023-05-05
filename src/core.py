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
    compression: CompressionHandler = None
    if options["action"] == "compress":
        compression = Compressor(options["path"], compression_options)
    else:
        compression = Decompressor(options["path"], compression_options)

    compression.start()
