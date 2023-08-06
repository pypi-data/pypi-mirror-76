from functools import wraps
from json import dumps, loads
from typing import Callable, Union

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from ckf_api_toolkit.aws_s3.s3_constants import S3GetObjectResponse
from ckf_api_toolkit.aws_s3.s3_payload_construction import S3Payload, S3GetObjectPayload, S3PutObjectPayload, \
    S3DeleteObjectPayload
from ckf_api_toolkit.core import ActionType, Instruction, Client, Repository
from ckf_api_toolkit.tools.logger import Logger, LogLevel

'''
S3 Actor Models
===========================================================

S3 specific versions of the classes used by an Actor.
'''


class S3ActionType(ActionType):
    READ_OBJECT = "READ_OBJECT"
    WRITE_OBJECT = "WRITE_OBJECT"
    DELETE_OBJECT = "DELETE_OBJECT"


class S3Instruction(Instruction):
    def __init__(self, action_type: S3ActionType, payload: S3Payload, parser: Callable):
        super().__init__(action_type, payload, parser)


def _log_s3_payload(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload_dict = vars(args[1])
        try:
            Logger().log(LogLevel.debug, payload_dict, title=f"S3 Payload for: {func.__name__}", pretty_json=True)
        except TypeError:
            Logger().log(LogLevel.debug, 'Payload contents were not JSON serializable',
                         title=f"S3 Payload for: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


class S3Client(Client):
    __client: BaseClient

    def __init__(self):
        super().__init__()
        self.__client = boto3.client('s3')
        self.add_action_type(S3ActionType.WRITE_OBJECT, self.__write_object)
        self.add_action_type(S3ActionType.READ_OBJECT, self.__read_object)
        self.add_action_type(S3ActionType.DELETE_OBJECT, self.__delete_object)

    @_log_s3_payload
    def __read_object(self, payload: S3GetObjectPayload) -> S3GetObjectResponse:
        return S3GetObjectResponse(**self.__client.get_object(**vars(payload)))

    @_log_s3_payload
    def __write_object(self, payload: S3PutObjectPayload):
        return self.__client.put_object(**vars(payload))

    @_log_s3_payload
    def __delete_object(self, payload: S3DeleteObjectPayload):
        return self.__client.delete_object(**vars(payload))


ENCODING: str = 'utf-8'


class S3ItemNotFound(Exception):
    pass


class S3Repository(Repository):
    def __init__(self):
        super().__init__()
        self.add_error_conversion(ClientError, S3ItemNotFound, [self.__not_found_error_parser])

    @staticmethod
    def __not_found_error_parser(error: ClientError) -> Union[S3ItemNotFound, bool]:
        return S3ItemNotFound if error.response['Error']['Code'] == 'NoSuchKey' else False

    @staticmethod
    def _convert_item_to_bytes(event_item: dict) -> bytes:
        return dumps(event_item).encode(ENCODING)

    @staticmethod
    def __parse_item(bytes_response: bytes) -> dict:
        event_item = loads(bytes_response.decode(ENCODING), encoding=ENCODING)
        Logger().log(LogLevel.debug, event_item, title="S3 Item", pretty_json=True)
        return event_item

    @staticmethod
    def __get_data_from_get_response(get_object_response: S3GetObjectResponse) -> bytes:
        try:
            data = get_object_response.Body.read()
        finally:
            get_object_response.Body.close()

        return data

    def _get_item_parser(self, s3_response: S3GetObjectResponse) -> dict:
        return self.__parse_item(self.__get_data_from_get_response(s3_response))
