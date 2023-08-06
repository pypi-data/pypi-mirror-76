from enum import Enum
from typing import Any, Union, List

from ckf_api_toolkit.aws_dynamo.condition_expression import DynamoConditionExpressionFactory, \
    DynamoConditionExpressionComparisonComparator
from ckf_api_toolkit.aws_dynamo.constants import DynamoScalarSetDataType, DynamoAttribute, DynamoReturnValues
from ckf_api_toolkit.aws_dynamo.converter import convert_python_data_to_dynamo
from ckf_api_toolkit.aws_dynamo.expression_attributes import DynamoExpressionAttributesNamesObject, \
    DynamoExpressionAttributesValuesObject, ExpressionAttributes
from ckf_api_toolkit.aws_dynamo.update_expression import DynamoUpdateExpressionFactory
from ckf_api_toolkit.tools.general_error import GeneralError

'''
Dynamo Actor Payloads
===========================================================
General
============================
'''


class DynamoKeyTooLong(GeneralError):
    def __init__(self):
        super().__init__(f"DynamoDB keys can only be a maximum of two attributes.")


class DynamoPayload:
    pass


class DynamoTableNamePayload(DynamoPayload):
    TableName: str
    IndexName: str

    def __init__(self, *, table_name: str, index_name: str = None):
        super().__init__()
        self.TableName = table_name
        if index_name:
            self.IndexName = index_name


class DynamoExpressionAttributeNamePayload(DynamoTableNamePayload):
    ExpressionAttributeNames: DynamoExpressionAttributesNamesObject

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ExpressionAttributeNames = {}

    def add_expression_attributes(self, expression_attributes: ExpressionAttributes):
        expression_attributes.merge_expression_attributes(
            expression_attribute_names=self.ExpressionAttributeNames,
        )
        if expression_attributes.expression_attribute_names:
            self.ExpressionAttributeNames = expression_attributes.expression_attribute_names


class DynamoExpressionAttributeValuePayload(DynamoExpressionAttributeNamePayload):
    ExpressionAttributeValues: DynamoExpressionAttributesValuesObject

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ExpressionAttributeValues = {}

    def add_expression_attributes(self, expression_attributes: ExpressionAttributes):
        expression_attributes.merge_expression_attributes(
            expression_attribute_values=self.ExpressionAttributeValues,
            expression_attribute_names=self.ExpressionAttributeNames,
        )
        if expression_attributes.expression_attribute_names:
            self.ExpressionAttributeNames = expression_attributes.expression_attribute_names
        if expression_attributes.expression_attribute_values:
            self.ExpressionAttributeValues = expression_attributes.expression_attribute_values


class DynamoConditionExpressionPayload(DynamoExpressionAttributeValuePayload, DynamoExpressionAttributeNamePayload):
    ConditionExpression: str

    def set_condition_expression(self, condition_expression_factory: DynamoConditionExpressionFactory):
        self.ConditionExpression = condition_expression_factory.condition_expression
        self.add_expression_attributes(condition_expression_factory.expression_attributes)


class DynamoUpdateExpressionPayload(DynamoExpressionAttributeValuePayload, DynamoExpressionAttributeNamePayload):
    UpdateExpression: str

    def set_update_expression(self, update_expression_factory: DynamoUpdateExpressionFactory):
        self.UpdateExpression = update_expression_factory.update_expression
        self.add_expression_attributes(update_expression_factory.expression_attributes)


class DynamoKeyedPayload(DynamoExpressionAttributeNamePayload):
    Key: DynamoAttribute

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Key = {}

    def add_key_item(self, key_name: str, key_value: Any, *,
                     dynamo_set_type: DynamoScalarSetDataType = None):
        if len(self.Key) >= 2:
            raise DynamoKeyTooLong()
        dynamo_value = convert_python_data_to_dynamo(key_value, dynamo_set_type=dynamo_set_type)
        self.Key[key_name] = dynamo_value


class DynamoReturnValuesPayload(DynamoExpressionAttributeNamePayload):
    ReturnValues: str

    def set_return_values(self, return_values: DynamoReturnValues):
        self.ReturnValues = return_values.value


'''
============================
Put Item
============================
'''


class DynamoPutItemPayload(DynamoConditionExpressionPayload, DynamoReturnValuesPayload):
    Item: DynamoAttribute

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Item = {}

    def set_attribute(self, attribute_name: str, attribute_value: Any, *,
                      dynamo_set_type: DynamoScalarSetDataType = None):
        dynamo_value = convert_python_data_to_dynamo(attribute_value, dynamo_set_type=dynamo_set_type)
        self.Item[attribute_name] = dynamo_value


'''
============================
Get Item
============================
'''


class DynamoGetItemPayload(DynamoKeyedPayload):
    pass


'''
============================
Scan
============================
'''


class DynamoScanPayload(DynamoTableNamePayload):
    pass


'''
============================
Query
============================
'''


class DynamoQueryKeyCondition(DynamoConditionExpressionFactory):
    key_name: str

    def __init__(self, key_name: str):
        super().__init__()
        self.key_name = key_name

    def __add_key_comparison(self, comparator: DynamoConditionExpressionComparisonComparator, value: Any):
        self.add_comparison(
            self.get_name_operand(self.key_name),
            comparator,
            self.get_value_operand(value)
        )

    def add_key_equals(self, value: Any):
        self.__add_key_comparison(DynamoConditionExpressionComparisonComparator.EQ, value)

    def add_key_less_than(self, value: Any):
        self.__add_key_comparison(DynamoConditionExpressionComparisonComparator.LT, value)

    def add_key_less_than_equals(self, value: Any):
        self.__add_key_comparison(DynamoConditionExpressionComparisonComparator.LTE, value)

    def add_key_greater_than(self, value: Any):
        self.__add_key_comparison(DynamoConditionExpressionComparisonComparator.GT, value)

    def add_key_greater_than_equals(self, value: Any):
        self.__add_key_comparison(DynamoConditionExpressionComparisonComparator.GTE, value)

    def add_key_between(self, lower_value: Any, upper_value):
        self.add_between(
            self.get_name_operand(self.key_name),
            self.get_value_operand(lower_value),
            self.get_value_operand(upper_value)
        )

    def add_key_begins_with(self, substring: str):
        self.add_begins_with(self.key_name, substring)


class DynamoQueryPayload(DynamoExpressionAttributeValuePayload):
    KeyConditionExpression: str
    ExclusiveStartKey: str
    Limit: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_partition_key_eq_condition_expression(self, partition_key_name: str, partition_key_value: Any,
                                                  sort_condition: DynamoQueryKeyCondition = None):
        key_condition_expression = DynamoConditionExpressionFactory()
        key_condition_expression.add_comparison(
            key_condition_expression.get_name_operand(partition_key_name),
            DynamoConditionExpressionComparisonComparator.EQ,
            key_condition_expression.get_value_operand(partition_key_value)
        )
        if sort_condition:
            key_condition_expression.append_logical_and(sort_condition)

        self.add_expression_attributes(key_condition_expression.expression_attributes)
        self.KeyConditionExpression = key_condition_expression.condition_expression

    def set_page_start_key(self, page_start_key: str):
        self.ExclusiveStartKey = page_start_key

    def set_query_limit(self, limit: int):
        self.Limit = limit


'''
============================
Update Item
============================
Reference:
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html
'''


class DynamoUpdateItemPayload(DynamoUpdateExpressionPayload, DynamoConditionExpressionPayload, DynamoKeyedPayload,
                              DynamoReturnValuesPayload):
    pass


'''
============================
Delete Item
============================
'''


class DynamoDeleteItemPayload(DynamoConditionExpressionPayload, DynamoKeyedPayload):
    pass


'''
============================
Transact Write Items
============================
'''

TransactWriteItemsPayloadType = Union[DynamoPutItemPayload, DynamoUpdateItemPayload, DynamoDeleteItemPayload]


class DynamoTransactItemType(Enum):
    ConditionCheck = 'ConditionCheck'
    Put = 'Put'
    Delete = 'Delete'
    Update = 'Update'


class DynamoTransactWriteItemsConditionCheck(DynamoKeyedPayload, DynamoConditionExpressionPayload):
    pass


class DynamoTransactWriteItemsPayload(DynamoPayload):
    TransactItems: List[dict]

    def __init__(self):
        super().__init__()
        self.TransactItems = []

    def add_item_payload(self, item_payload: TransactWriteItemsPayloadType,
                         # return_values: TransactItemReturnValues = TransactItemReturnValues.Key
                         ):
        transact_item = {}
        payload_type = type(item_payload)

        if payload_type is DynamoPutItemPayload:
            transact_item = {DynamoTransactItemType.Put.value: vars(item_payload)}
        elif payload_type is DynamoUpdateItemPayload:
            transact_item = {DynamoTransactItemType.Update.value: vars(item_payload)}
        elif payload_type is DynamoDeleteItemPayload:
            transact_item = {DynamoTransactItemType.Delete.value: vars(item_payload)}

        if transact_item:
            # transact_item['ReturnValue'] = return_values.value
            self.TransactItems.append(transact_item)

    def add_condition_check(self, condition_check: DynamoTransactWriteItemsConditionCheck):
        self.TransactItems.append({DynamoTransactItemType.ConditionCheck.value: vars(condition_check)})
