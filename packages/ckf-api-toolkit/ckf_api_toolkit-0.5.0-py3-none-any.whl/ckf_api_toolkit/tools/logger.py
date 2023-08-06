import json
from enum import Enum
from os import environ


class LogLevel(Enum):
    debug = 0
    info = 1
    warn = 2
    error = 3


LOG_LEVEL_TEXT = {
    LogLevel.debug: "DEBUG",
    LogLevel.info: "INFO",
    LogLevel.warn: "WARNING",
    LogLevel.error: "ERROR",
}

FORMAT_LOGGING_ENV_VAR = 'FORMAT_LOGGING'


class Logger(object):
    __instance = None
    log_level: LogLevel

    # Singleton
    def __new__(cls, log_level: LogLevel = LogLevel.error):
        if Logger.__instance is None:
            Logger.__instance = object.__new__(cls)
            Logger.__instance.log_level = log_level
        return Logger.__instance

    def __should_log_at_this_level(self, level: LogLevel) -> bool:
        return level.value >= self.log_level.value

    def log(self, level: LogLevel, message: object, *, title: str = '', pretty_json: bool = False):
        if self.__should_log_at_this_level(level):
            if pretty_json:
                if FORMAT_LOGGING_ENV_VAR in environ and environ[FORMAT_LOGGING_ENV_VAR] == 'True':
                    # Will try to pretty the data - may be limited by environment deserializer for large data sets
                    print_message = json.dumps(message, indent=4, sort_keys=True)
                else:
                    print_message = json.dumps(message)
            else:
                print_message = str(message)
            log_message = (f"\n"
                           f"=================================================\n"
                           f"* {LOG_LEVEL_TEXT[level]}: {title}\n"
                           f"=================================================\n"
                           f"{print_message}\n"
                           f"=================================================\n"
                           )

            print(log_message)
