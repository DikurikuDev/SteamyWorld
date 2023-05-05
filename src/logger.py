class Logger:
    def __init__(self, options={}):
        self.callbacks = []
        self.run_quietly = options.get("run_quietly", False)

        # 0  - just warning
        # 1  - warning and info
        # 2+ - warning, info and debug
        self.verbosety_level = options.get("verbosety_level", 0)

    def __log(self, message):
        for callback in self.callbacks:
            callback(message)

    def warning(self, message):
        if not self.run_quietly:
            self.__log("WARNING: " + str(message))

    def info(self, message):
        if self.verbosety_level >= 1 and not self.run_quietly:
            self.__log("INFO: " + str(message))

    def debug(self, message):
        if self.verbosety_level >= 2 and not self.run_quietly:
            self.__log("DEBUG: " + str(message))

    def onLog(self, callback):
        if callback not in self.callbacks:
            self.callbacks.append(callback)
