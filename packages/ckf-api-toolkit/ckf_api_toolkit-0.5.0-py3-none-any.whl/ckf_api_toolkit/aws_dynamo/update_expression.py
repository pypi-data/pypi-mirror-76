from enum import Enum
from typing import Any, NamedTuple

from ckf_api_toolkit.aws_dynamo.constants import DynamoScalarSetDataType
from ckf_api_toolkit.aws_dynamo.expression_attributes import ExpressionAttributes
from ckf_api_toolkit.aws_dynamo.converter import convert_python_data_to_dynamo
from ckf_api_toolkit.tools.general_error import GeneralError

'''
Update Expression Factory
===========================================================
references: 
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html

Multiple types of updates can be included in one expression, as long as all expressions of that type follow the
keyword for that update type. 

E.g.
SET #name = :val, #name2 = :val2 REMOVE #name3, #name4 DELETE #name5 :val3, #name6 :val4

Constants
============================
'''


class DynamoUpdateTypeKeyword(Enum):
    ADD = "ADD"  # NOTE: Not recommended, and therefore not currently implemented - Use SET
    DELETE = "DELETE"  # Only for Set data types - removes elements
    SET = "SET"  # Set an attribute to a value or another attribute's value
    REMOVE = "REMOVE"  # Remove item attribute, or remove property from Map


class DynamoUpdateSetFunction(Enum):
    LIST_APPEND = "list_append"
    IF_NOT_EXISTS = "if_not_exists"


class DynamoUpdateSetOperator(Enum):
    EQ = "="
    ADD = "+"
    SUB = "-"


'''
============================
Helper functions
============================
'''


def _get_safe_string(string: str) -> str:
    # Only single whitespace and trimmed
    return " ".join(f"{string}".split())


'''
============================
Set value class
============================
Per reference:

- The path element is the document path to the item.
- An operand element can be either a document path to an item or a function.

set-action ::=
    path = value

value ::=
    operand 
    | operand '+' operand 
    | operand '-' operand
 
operand ::=
    path | function
'''


class InvalidModificationToDynamoUpdateExpressionSetActionValue(GeneralError):
    def __init__(self):
        super().__init__("Attempt to modify set action value was not valid.")


class DynamoUpdateExpressionSetActionValueObject(NamedTuple):
    expression_attributes: ExpressionAttributes
    operand_expression: str


class DynamoUpdateExpressionSetActionValueFactory:
    expression_attributes: ExpressionAttributes
    __operand_expression: str
    __modified: bool

    def __init__(self):
        self.expression_attributes = ExpressionAttributes()
        self.__operand_expression = ""
        self.__modified = False

    @property
    def operand_expression(self):
        return _get_safe_string(self.__operand_expression)

    def get_set_action_value_object(self) -> DynamoUpdateExpressionSetActionValueObject:
        return DynamoUpdateExpressionSetActionValueObject(
            expression_attributes=self.expression_attributes,
            operand_expression=self.operand_expression,
        )

    def __error_if_modified(self):
        if self.__modified:
            raise InvalidModificationToDynamoUpdateExpressionSetActionValue()

    def __set_modified(self):
        self.__modified = True

    def set_to_python_value(self, value: Any, *, dynamo_set_type: DynamoScalarSetDataType = None):
        self.__error_if_modified()
        dynamo_value = convert_python_data_to_dynamo(value, dynamo_set_type=dynamo_set_type)
        self.__operand_expression = self.expression_attributes.set_expression_attribute_value(dynamo_value)
        self.__set_modified()

    def __merge_expression_attributes(self, value: DynamoUpdateExpressionSetActionValueObject):
        self.expression_attributes.merge_expression_attributes(**vars(value.expression_attributes))

    def set_if_not_exists(self, path: str, value: DynamoUpdateExpressionSetActionValueObject):
        self.__error_if_modified()
        self.__merge_expression_attributes(value)
        exp_attr_str = self.expression_attributes.set_expression_attribute_name(path)
        self.__operand_expression = (
            f"{DynamoUpdateSetFunction.IF_NOT_EXISTS.value}({exp_attr_str}, {value.operand_expression})"
        )
        self.__set_modified()

    def set_list_append(self,
                        list_appended_to: DynamoUpdateExpressionSetActionValueObject,
                        list_to_append: DynamoUpdateExpressionSetActionValueObject,
                        ):
        self.__error_if_modified()
        self.__merge_expression_attributes(list_appended_to)
        self.__merge_expression_attributes(list_to_append)
        self.__operand_expression = (
            f"{DynamoUpdateSetFunction.LIST_APPEND.value}({list_appended_to}, {list_to_append})"
        )
        self.__set_modified()

    def __arithmetic_by_expression_value(self, value: DynamoUpdateExpressionSetActionValueObject,
                                         operator: DynamoUpdateSetOperator):
        self.__merge_expression_attributes(value)
        self.__operand_expression += f" {operator.value} {value.operand_expression}"
        self.__set_modified()

    def add_by_expression_value(self, value: DynamoUpdateExpressionSetActionValueObject):
        self.__arithmetic_by_expression_value(value, DynamoUpdateSetOperator.ADD)

    def subtract_by_expression_value(self, value: DynamoUpdateExpressionSetActionValueObject):
        self.__arithmetic_by_expression_value(value, DynamoUpdateSetOperator.SUB)

    def __arithmetic_by_python_value(self, value: Any, operator: DynamoUpdateSetOperator, *,
                                     dynamo_set_type: DynamoScalarSetDataType = None):
        dynamo_value = convert_python_data_to_dynamo(value, dynamo_set_type=dynamo_set_type)
        exp_attr_value = self.expression_attributes.set_expression_attribute_value(dynamo_value)
        self.__operand_expression += f" {operator.value} {exp_attr_value}"
        self.__set_modified()

    def add_by_python_value(self, value: Any, *, dynamo_set_type: DynamoScalarSetDataType = None):
        self.__arithmetic_by_python_value(value, DynamoUpdateSetOperator.ADD, dynamo_set_type=dynamo_set_type)

    def subtract_by_python_value(self, value: Any, *, dynamo_set_type: DynamoScalarSetDataType = None):
        self.__arithmetic_by_python_value(value, DynamoUpdateSetOperator.SUB, dynamo_set_type=dynamo_set_type)


'''
============================
Update expression class
============================
'''


class DynamoUpdateExpressionFactory:
    __current_set_expression: str
    __current_delete_expression: str
    __current_remove_expression: str
    expression_attributes: ExpressionAttributes

    def __init__(self):
        self.__current_delete_expression = ""
        self.__current_set_expression = ""
        self.__current_remove_expression = ""
        self.expression_attributes = ExpressionAttributes()

    @property
    def update_expression(self):
        return _get_safe_string(
            f"{self.__current_set_expression} {self.__current_delete_expression} {self.__current_remove_expression}"
        )

    def add_set_expression(self, path: str, value_obj: DynamoUpdateExpressionSetActionValueObject):
        self.expression_attributes.merge_expression_attributes(**vars(value_obj.expression_attributes))
        path_exp_attr_str = self.expression_attributes.set_expression_attribute_name(path)
        if not self.__current_set_expression:
            self.__current_set_expression = f"{DynamoUpdateTypeKeyword.SET.value} "
        else:
            self.__current_set_expression += ", "
        self.__current_set_expression += (
            f"{path_exp_attr_str} {DynamoUpdateSetOperator.EQ.value} {value_obj.operand_expression}"
        )

    def set_path_to_python_value(self, path: str, value: Any, *, dynamo_set_type: DynamoScalarSetDataType = None):
        set_action_value_obj = DynamoUpdateExpressionSetActionValueFactory()
        set_action_value_obj.set_to_python_value(value, dynamo_set_type=dynamo_set_type)
        self.add_set_expression(path, set_action_value_obj.get_set_action_value_object())

    def remove_path(self, path: str):
        if not self.__current_remove_expression:
            self.__current_remove_expression = f"{DynamoUpdateTypeKeyword.REMOVE.value} "
        else:
            self.__current_remove_expression += ", "
        self.__current_remove_expression += self.expression_attributes.set_expression_attribute_name(path)

    def __delete_from_set(self, path: str, value: Any, dynamo_set_type: DynamoScalarSetDataType = None):
        if not self.__current_delete_expression:
            self.__current_delete_expression = f"{DynamoUpdateTypeKeyword.DELETE.value} "
        else:
            self.__current_delete_expression += ", "
        exp_attr_name_str = self.expression_attributes.set_expression_attribute_name(path)
        dynamo_value = convert_python_data_to_dynamo(value, dynamo_set_type=dynamo_set_type)
        exp_attr_value_str = self.expression_attributes.set_expression_attribute_value(dynamo_value)
        self.__current_delete_expression += f"{exp_attr_name_str} {exp_attr_value_str}"

    def delete_set_from_set(self, path: str, set_to_delete: set, dynamo_set_type: DynamoScalarSetDataType):
        self.__delete_from_set(path, set_to_delete, dynamo_set_type)

    def delete_python_value_from_set(self, path: str, value: Any):
        self.__delete_from_set(path, value)
