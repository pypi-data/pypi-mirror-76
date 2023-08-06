from ckf_api_toolkit.tools.logger import Logger, LogLevel


class GeneralError(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message
        self.log()

    def log(self):
        Logger().log(LogLevel.error, self.message, title="Exception")
