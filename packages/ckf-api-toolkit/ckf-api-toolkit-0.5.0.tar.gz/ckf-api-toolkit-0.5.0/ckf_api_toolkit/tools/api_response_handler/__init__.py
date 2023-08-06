from abc import ABC, abstractmethod
from enum import Enum
from json import dumps
from typing import NamedTuple, Any, Union
from ckf_api_toolkit.core import Actor, UseCase
from ckf_api_toolkit.tools.error_handling import get_trace
from ckf_api_toolkit.tools.logger import Logger, LogLevel


class ResponseCode(Enum):
    OK = 200
    REDIRECT = 300
    REDIRECT_PERMANENT = 301
    REDIRECT_TEMP = 302
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    ALREADY_EXISTS = 409
    ERROR = 500
    NOT_IMPLEMENTED = 501


class ApiResponseException(Exception):
    status_code: ResponseCode
    message: str

    def __init__(self, status_code: ResponseCode, message: str):
        self.status_code = status_code
        self.message = message


class ApiSuccessResponseBody(NamedTuple):
    data: dict = {}
    message: str = None

    def append_data(self, data: Any, data_key: str):
        self.data[data_key] = data


class ApiErrorResponseBody(NamedTuple):
    error: str


class ApiResponseFactory(ABC):
    return_trace: bool
    status_code: int
    body: Union[ApiSuccessResponseBody, ApiErrorResponseBody]

    def __init__(self, *, return_trace=False):
        self.return_trace = return_trace
        self.body = ApiSuccessResponseBody()

    @abstractmethod
    def get_response(self) -> dict:
        pass

    @property
    def is_error(self) -> bool:
        return type(self.body) is ApiErrorResponseBody

    def set_error(self, error_code: ResponseCode, message: str):
        self.body = ApiErrorResponseBody(message)
        self.status_code = error_code.value

    def set_exception(self, error: Union[Exception, ApiResponseException]):
        if self.return_trace:
            trace = get_trace()
            Logger().log(LogLevel.debug, trace, title="Returning Exception Trace in Response")
            error_object = {
                'trace': trace,
                'error': str(error),
            }
            message = dumps(error_object)
        else:
            message = "Internal server error."

        if isinstance(error, ApiResponseException):
            self.set_error(error.status_code, error.message)
        else:
            self.set_error(ResponseCode.ERROR, message)

    def set_success(self, operation_name: str, *, response_code: ResponseCode = ResponseCode.OK):
        self.body = ApiSuccessResponseBody(
            message=f"Operation successful: {operation_name}.",
        )
        self.status_code = response_code.value

    def add_to_response_data(self, data: Any, data_key: str):
        if type(self.body) is ApiSuccessResponseBody:
            self.body.append_data(data, data_key)

    def set_response_from_actor(self, actor: Actor, use_case: UseCase, data_key: str, *, suppress_data=False):
        data = actor.run_use_case(use_case)
        self.set_success(use_case.name)
        if not suppress_data:
            self.add_to_response_data(data, data_key)
