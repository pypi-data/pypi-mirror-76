from enum import Enum
from typing import NewType, NamedTuple, Union, List, Any

from ckf_api_toolkit.aws_dynamo.constants import DynamoValue, DynamoScalarStringDataType, DynamoDataType
from ckf_api_toolkit.aws_dynamo.converter import convert_python_data_to_dynamo
from ckf_api_toolkit.aws_dynamo.expression_attributes import ExpressionAttributes
from ckf_api_toolkit.tools.general_error import GeneralError

'''
Condition Expression Factory
===========================================================
references: 
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.OperatorsAndFunctions.html
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html
'''


class DynamoConditionExpressionFunction(Enum):
    ATTRIBUTE_EXISTS = "attribute_exists"
    ATTRIBUTE_NOT_EXISTS = "attribute_not_exists"
    ATTRIBUTE_TYPE = "attribute_type"
    BEGINS_WITH = "begins_with"
    CONTAINS = "contains"
    SIZE = "size"


class DynamoConditionExpressionComparisonComparator(Enum):
    EQ = "="
    NOT_EQ = "<>"
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="


class DynamoConditionExpressionComparisonKeyword(Enum):
    BETWEEN = "BETWEEN"
    IN = "IN"


class DynamoConditionExpressionLogicalOperator(Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


AttributeNameOperand = NewType("AttributeNameOperand", str)
AttributeValueOperand = NewType("AttributeValueOperand", DynamoValue)


class ConditionOperandType(Enum):
    NAME = 'name'
    VALUE = 'value'


class ConditionOperand(NamedTuple):
    type: ConditionOperandType
    value: Union[AttributeValueOperand, AttributeNameOperand]


class ConditionExpressionObject(NamedTuple):
    ConditionExpression: str


class DynamoConditionExpressionEmptyOperandList(GeneralError):
    def __init__(self):
        super().__init__(f"An empty operand list was used to create an IN ConditionExpression")


class DynamoConditionExpressionFactory:
    expression_attributes: ExpressionAttributes
    condition_expression: str

    def __init__(self):
        self.expression_attributes = ExpressionAttributes()
        self.condition_expression = ""

    @staticmethod
    def get_value_operand(value: Any) -> ConditionOperand:
        return ConditionOperand(ConditionOperandType.VALUE, AttributeValueOperand(convert_python_data_to_dynamo(value)))

    @staticmethod
    def get_name_operand(name: str) -> ConditionOperand:
        return ConditionOperand(ConditionOperandType.NAME, AttributeNameOperand(name))

    def __add_to_condition_expression(self, new_expression: str):
        # Safe whitespace
        self.condition_expression += f" {new_expression}"
        self.condition_expression = self.condition_expression.strip()

    def __set_operand_to_expression_attributes(self, operand: ConditionOperand) -> str:
        if operand.type == ConditionOperandType.NAME:
            return self.expression_attributes.set_expression_attribute_name(operand.value)
        elif operand.type == ConditionOperandType.VALUE:
            return self.expression_attributes.set_expression_attribute_value(operand.value)

    def add_string(self, expression: str):
        self.__add_to_condition_expression(expression)

    def add_comparison(
            self, operand1: ConditionOperand, comparator: DynamoConditionExpressionComparisonComparator,
            operand2: ConditionOperand
    ):
        operand1_expression_string = self.__set_operand_to_expression_attributes(operand1)
        operand2_expression_string = self.__set_operand_to_expression_attributes(operand2)
        self.__add_to_condition_expression(
            f"{operand1_expression_string} {comparator.value} {operand2_expression_string}"
        )

    def add_between(
            self, between_operand: ConditionOperand, lower_operand: ConditionOperand, upper_operand: ConditionOperand
    ):
        between_operand_expression_string = self.__set_operand_to_expression_attributes(between_operand)
        lower_operand_expression_string = self.__set_operand_to_expression_attributes(lower_operand)
        upper_operand_expression_string = self.__set_operand_to_expression_attributes(upper_operand)
        self.__add_to_condition_expression(
            f"{between_operand_expression_string} {DynamoConditionExpressionComparisonKeyword.BETWEEN.value} "
            f"{lower_operand_expression_string} {DynamoConditionExpressionLogicalOperator.AND.value} "
            f"{upper_operand_expression_string}"
        )

    def add_in(self, operand: ConditionOperand, in_list: List[ConditionOperand]):
        if len(in_list) < 1:
            raise DynamoConditionExpressionEmptyOperandList()
        operand_expression_string = self.__set_operand_to_expression_attributes(operand)
        in_expression_string = " ("
        for current_operand in in_list:
            current_operand_expression_string = self.__set_operand_to_expression_attributes(current_operand)
            in_expression_string += f"{current_operand_expression_string}, "
        self.__add_to_condition_expression(
            f"{operand_expression_string} {DynamoConditionExpressionComparisonKeyword.IN.value} "
            f"{in_expression_string[:-2]})"
        )

    def add_expression_in_parenthesis(
            self, expression: str, expression_attributes: ExpressionAttributes = ExpressionAttributes()
    ):
        self.expression_attributes.merge_expression_attributes(**vars(expression_attributes))
        self.__add_to_condition_expression(f"({expression})")

    def __parse_condition(self, condition: Union[str, 'DynamoConditionExpressionFactory']) -> str:
        if isinstance(condition, DynamoConditionExpressionFactory):
            self.expression_attributes.merge_expression_attributes(
                expression_attribute_names=condition.expression_attributes.expression_attribute_names,
                expression_attribute_values=condition.expression_attributes.expression_attribute_values,
            )
            return condition.condition_expression
        else:
            return condition

    def __add_logical(self, *,
                      condition_1: Union[str, 'DynamoConditionExpressionFactory'] = "",
                      operator: DynamoConditionExpressionLogicalOperator,
                      condition_2: Union[str, 'DynamoConditionExpressionFactory']
                      ):
        condition_1_str = self.__parse_condition(condition_1)
        condition_2_str = self.__parse_condition(condition_2)
        self.__add_to_condition_expression(f"({condition_1_str}) {operator.value} ({condition_2_str})")

    def __append_logical(self, *, operator: DynamoConditionExpressionLogicalOperator,
                         condition: Union[str, 'DynamoConditionExpressionFactory']):
        condition_str = self.__parse_condition(condition)
        self.__add_to_condition_expression(f" {operator.value} ({condition_str})")

    def add_logical_and(self, condition_1: Union[str, 'DynamoConditionExpressionFactory'],
                        condition_2: Union[str, 'DynamoConditionExpressionFactory']):
        self.__add_logical(
            condition_1=condition_1, operator=DynamoConditionExpressionLogicalOperator.AND, condition_2=condition_2
        )

    def add_logical_or(self, condition_1: Union[str, 'DynamoConditionExpressionFactory'],
                       condition_2: Union[str, 'DynamoConditionExpressionFactory']):
        self.__add_logical(
            condition_1=condition_1, operator=DynamoConditionExpressionLogicalOperator.OR, condition_2=condition_2
        )

    def add_logical_not(self, condition: Union[str, 'DynamoConditionExpressionFactory']):
        self.__add_logical(condition_2=condition, operator=DynamoConditionExpressionLogicalOperator.NOT)

    def append_logical_and(self, condition: Union[str, 'DynamoConditionExpressionFactory']):
        self.__append_logical(operator=DynamoConditionExpressionLogicalOperator.AND, condition=condition)

    def append_logical_or(self, condition: Union[str, 'DynamoConditionExpressionFactory']):
        self.__append_logical(operator=DynamoConditionExpressionLogicalOperator.OR, condition=condition)

    def append_logical_not(self, condition: Union[str, 'DynamoConditionExpressionFactory']):
        self.__append_logical(operator=DynamoConditionExpressionLogicalOperator.NOT, condition=condition)

    def __add_path_only_function(self, *, path_name: str, function: DynamoConditionExpressionFunction):
        path_expression_attribute_name = self.expression_attributes.set_expression_attribute_name(path_name)
        self.__add_to_condition_expression(f"{function.value}({path_expression_attribute_name})")

    def add_attribute_exists(self, attribute_path: str):
        self.__add_path_only_function(path_name=attribute_path,
                                      function=DynamoConditionExpressionFunction.ATTRIBUTE_EXISTS)

    def add_attribute_not_exists(self, attribute_path: str):
        self.__add_path_only_function(path_name=attribute_path,
                                      function=DynamoConditionExpressionFunction.ATTRIBUTE_NOT_EXISTS)

    def add_size(self, attribute_path: str):
        self.__add_path_only_function(path_name=attribute_path,
                                      function=DynamoConditionExpressionFunction.SIZE)

    def __add_function_with_string_arg(self, *,
                                       attribute_path: str, function: DynamoConditionExpressionFunction, arg_str: str
                                       ):
        path_expression_attribute_name = self.expression_attributes.set_expression_attribute_name(attribute_path)
        arg_str_scalar_string_value = {DynamoScalarStringDataType.STRING.value: arg_str}
        arg_str_expression_attribute_value = self.expression_attributes.set_expression_attribute_value(
            arg_str_scalar_string_value
        )
        self.__add_to_condition_expression(
            f"{function.value}({path_expression_attribute_name}, {arg_str_expression_attribute_value})"
        )

    def add_attribute_type(self, attribute_path: str, data_type: DynamoDataType):
        self.__add_function_with_string_arg(
            attribute_path=attribute_path, function=DynamoConditionExpressionFunction.ATTRIBUTE_TYPE,
            arg_str=data_type.value
        )

    def add_begins_with(self, attribute_path: str, substring: str):
        self.__add_function_with_string_arg(
            attribute_path=attribute_path, function=DynamoConditionExpressionFunction.BEGINS_WITH, arg_str=substring
        )

    def add_contains(self, attribute_path: str, operand: str):
        self.__add_function_with_string_arg(
            attribute_path=attribute_path, function=DynamoConditionExpressionFunction.CONTAINS, arg_str=operand
        )
