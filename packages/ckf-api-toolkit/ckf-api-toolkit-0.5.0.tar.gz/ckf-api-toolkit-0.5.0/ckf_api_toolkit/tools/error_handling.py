from traceback import format_exc
from typing import Callable, NamedTuple, List, Union

from ckf_api_toolkit.tools.logger import Logger, LogLevel


def get_trace() -> str:
    return format_exc()


ErrorParser = Callable[[type(Exception)], Union[type(Exception), Union[Callable, bool]]]


class ErrorConversion(NamedTuple):
    incoming_error: type(Exception)
    outgoing_error: type(Exception)
    error_parsers: List[ErrorParser] = []


class ErrorConverter:
    error_conversions: List[ErrorConversion]

    def __init__(self):
        self.error_conversions = []

    def add_error_conversion(self, incoming_error: type(Exception), outgoing_error: type(Exception),
                             error_parsers: List[ErrorParser] = None):
        self.error_conversions.append(
            ErrorConversion(incoming_error=incoming_error, outgoing_error=outgoing_error,
                            error_parsers=error_parsers if error_parsers else []))

    def handle_error(self, error: type(Exception)):
        Logger().log(LogLevel.debug, error, title=f"Error Handler - Error Class: {type(error)}")
        current_error = error
        for conversion in self.error_conversions:
            Logger().log(LogLevel.debug, (
                f"Incoming error type: {conversion.incoming_error}\n"
                f"Outgoing error type: {conversion.outgoing_error}"
            ), title=f"Error Handler - Converter")
            if isinstance(current_error, conversion.incoming_error):
                incoming_error = current_error
                Logger().log(LogLevel.debug, conversion.outgoing_error, title="Error Handler - Conversion Matched")
                current_error = conversion.outgoing_error()
                for error_parser in conversion.error_parsers:
                    parsed_error = error_parser(incoming_error)
                    if parsed_error:
                        Logger().log(LogLevel.debug, parsed_error, title="Error Handler - Parsed Error")
                        current_error = parsed_error()
        raise current_error
