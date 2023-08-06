from enum import Enum
from typing import Any, Callable, Dict, List

from ckf_api_toolkit.tools.error_handling import ErrorConverter, ErrorParser

'''
Generics
============================
These can be adapted to support different DB connections by inheriting these to DB specific versions. Use these generics
in your use cases to decouple use cases from specific DB requirements.
'''


class ActionType(Enum):
    # Inherit, then define DB specific action types. E.x. C, R, U, D
    pass


class Instruction:
    # Used by actor to determine specific client methods if required. E.x. requests.get()
    action_type: ActionType
    # Used by actor to give instructions to the client. Can be any kind of required object.
    payload: Any
    # Parser function will be used to parse return values to the actor. Use for additional logic and formatting.
    parser: Callable

    def __init__(self, action_type: ActionType, payload: Any, parser: Callable):
        self.parser = parser
        self.payload = payload
        self.action_type = action_type


class UseCase:
    name: str


class Repository:
    # Inherit, then define specific Instance state required for specific connections.
    use_cases: Dict[str, Callable[[UseCase], Any]]
    error_converter: ErrorConverter

    def __init__(self):
        self.use_cases = {}
        self.error_converter = ErrorConverter()

    def add_use_case(self, use_case: type(UseCase), function: Callable[[Any], Instruction]):
        self.use_cases[use_case.name] = function

    def get_instruction(self, use_case: UseCase) -> Instruction:
        return self.use_cases[use_case.name](use_case)

    def add_error_conversion(self, incoming_error: type(Exception), outgoing_error: type(Exception),
                             error_parsers: List[ErrorParser] = None):
        self.error_converter.add_error_conversion(incoming_error, outgoing_error, error_parsers)


class Client:
    action_types: Dict[ActionType, Callable]

    # Inherit, then define client specific initialization logic, and handling for action types.
    def __init__(self):
        self.action_types = {}

    def add_action_type(self, action_type: ActionType, payload_handler: Callable):
        self.action_types[action_type] = payload_handler

    def handle_action_type(self, action_type: ActionType, payload: Any) -> Any:
        return self.action_types[action_type](payload)


'''
Actor
===========================================================
This actor executes defined use cases, and returns parsed values based on instances of the generic model classes.
'''


class Actor:
    repository: Repository
    client: Client

    def __init__(self, client: Client, repository: Repository):
        self.repository = repository
        self.client = client

    def run_use_case(self, use_case: UseCase) -> Any:
        instruction = self.repository.get_instruction(use_case)
        # noinspection PyBroadException
        try:
            return instruction.parser(
                self.client.handle_action_type(instruction.action_type, instruction.payload)
            )
        except Exception as error:
            self.repository.error_converter.handle_error(error)
