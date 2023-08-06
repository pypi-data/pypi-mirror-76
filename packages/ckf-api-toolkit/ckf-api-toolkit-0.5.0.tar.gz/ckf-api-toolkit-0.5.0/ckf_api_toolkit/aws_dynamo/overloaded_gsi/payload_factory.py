from typing import Any, List, Tuple, Optional

from ckf_api_toolkit.aws_dynamo.condition_expression import DynamoConditionExpressionFactory, \
    DynamoConditionExpressionComparisonComparator
from ckf_api_toolkit.aws_dynamo.constants import DynamoReturnValues
from ckf_api_toolkit.aws_dynamo.overloaded_gsi.composite_key_utils import make_composite_key
from ckf_api_toolkit.aws_dynamo.payload_construction import DynamoUpdateItemPayload, DynamoQueryPayload, \
    DynamoGetItemPayload, DynamoQueryKeyCondition, DynamoDeleteItemPayload
from ckf_api_toolkit.aws_dynamo.update_expression import DynamoUpdateExpressionFactory
from ckf_api_toolkit.tools.model import Model


class OverloadedGsiPayloadFactory:
    gsi_key_delimiter: str
    sk_name: str
    pk_name: str
    gsi_key_prefix: str
    table_name: str

    def __init__(self, *, table_name: str, pk_name: str, sk_name: str, gsi_key_prefix: str,
                 gsi_key_delimiter: str = '_'):
        self.gsi_key_delimiter = gsi_key_delimiter
        self.sk_name = sk_name
        self.pk_name = pk_name
        self.gsi_key_prefix = gsi_key_prefix
        self.table_name = table_name

    # TODO: Add functions for salting GSI keys
    def _get_gsi_index_name(self, gsi: int) -> str:
        return self.gsi_key_delimiter.join([self.gsi_key_prefix, str(gsi)])

    def _get_gsi_pk_name(self, gsi: int) -> str:
        return self.gsi_key_delimiter.join([self._get_gsi_index_name(gsi), self.pk_name])

    def _get_gsi_sk_name(self, gsi: int) -> str:
        return self.gsi_key_delimiter.join([self._get_gsi_index_name(gsi), self.sk_name])

    def get_update_payload(self, model_object: Model, *, for_transaction=False,
                           enforce_unique=False) -> DynamoUpdateItemPayload:
        model_dict = model_object.get_dict_for_db()

        payload = DynamoUpdateItemPayload(table_name=self.table_name)
        if not for_transaction:
            payload.set_return_values(DynamoReturnValues.ALL_NEW)

        pk_value = model_dict[self.pk_name]
        payload.add_key_item(self.pk_name, pk_value)
        sk_value = model_dict[self.sk_name]
        payload.add_key_item(self.sk_name, sk_value)

        update_expression = DynamoUpdateExpressionFactory()
        for attribute, value in model_dict.items():
            if attribute not in [self.pk_name, self.sk_name]:
                update_expression.set_path_to_python_value(attribute, value)
        payload.set_update_expression(update_expression)

        # TODO: Look into moving this someplace where it can be used more generically
        if enforce_unique:
            pk_not_exists_expression = DynamoConditionExpressionFactory()
            pk_not_exists_expression.add_comparison(
                DynamoConditionExpressionFactory.get_name_operand(self.pk_name),
                DynamoConditionExpressionComparisonComparator.NOT_EQ,
                DynamoConditionExpressionFactory.get_value_operand(pk_value)
            )

            sk_not_exists_expression = DynamoConditionExpressionFactory()
            sk_not_exists_expression.add_comparison(
                DynamoConditionExpressionFactory.get_name_operand(self.sk_name),
                DynamoConditionExpressionComparisonComparator.NOT_EQ,
                DynamoConditionExpressionFactory.get_value_operand(sk_value)
            )

            enforce_unique_comparison = DynamoConditionExpressionFactory()
            enforce_unique_comparison.add_logical_and(pk_not_exists_expression, sk_not_exists_expression)

            payload.set_condition_expression(enforce_unique_comparison)

        return payload

    def get_read_payload(self, model_object: Model) -> DynamoGetItemPayload:
        model_dict = model_object.get_dict_for_db()

        payload = DynamoGetItemPayload(table_name=self.table_name)
        payload.add_key_item(self.pk_name, model_dict[self.pk_name])
        payload.add_key_item(self.sk_name, model_dict[self.sk_name])

        return payload

    def get_delete_payload(self, model_object: Model) -> DynamoDeleteItemPayload:
        model_dict = model_object.get_dict_for_db()

        payload = DynamoDeleteItemPayload(table_name=self.table_name)
        payload.add_key_item(self.pk_name, model_dict[self.pk_name])
        payload.add_key_item(self.sk_name, model_dict[self.sk_name])

        return payload

    def _get_possible_gsi_payload(self, gsi: int) -> DynamoQueryPayload:
        return DynamoQueryPayload(table_name=self.table_name) if not gsi else DynamoQueryPayload(
            table_name=self.table_name,
            index_name=self._get_gsi_index_name(gsi)
        )

    def _get_possible_gsi_pk_name(self, gsi: int) -> str:
        return self.pk_name if not gsi else self._get_gsi_pk_name(gsi)

    def _get_possible_gsi_sk_name(self, gsi: int) -> str:
        return self.sk_name if not gsi else self._get_gsi_sk_name(gsi)

    def get_explicit_pk_query_payload(self, primary_key_value: Any, *, gsi: int = None) -> DynamoQueryPayload:
        payload = self._get_possible_gsi_payload(gsi)
        primary_key_name = self._get_possible_gsi_pk_name(gsi)
        payload.add_partition_key_eq_condition_expression(primary_key_name, primary_key_value)

        return payload

    def get_sk_begins_with_payload(self, primary_key_value: Any, sort_key_begins_with_value: str, *,
                                   gsi: int = None) -> DynamoQueryPayload:
        payload = self._get_possible_gsi_payload(gsi)
        primary_key_name = self._get_possible_gsi_pk_name(gsi)

        sk_condition = DynamoQueryKeyCondition(self._get_possible_gsi_sk_name(gsi))
        sk_condition.add_key_begins_with(sort_key_begins_with_value)

        payload.add_partition_key_eq_condition_expression(primary_key_name, primary_key_value, sk_condition)

        return payload

    @staticmethod
    def _get_composite_key_components(
            ordered_key_values: List[str], delimiter: Optional[str]
    ) -> Tuple[str, str]:
        composite_key_value = make_composite_key(ordered_key_values, delimiter) if delimiter \
            else make_composite_key(ordered_key_values)
        partition_key_value = ordered_key_values[0]

        return composite_key_value, partition_key_value

    def _get_composite_key_query_components(
            self, ordered_key_values: List[str], delimiter: Optional[str]
    ) -> Tuple[str, str, DynamoQueryKeyCondition, DynamoQueryPayload]:
        composite_key_value, partition_key_value = self._get_composite_key_components(
            ordered_key_values, delimiter)
        return composite_key_value, partition_key_value, DynamoQueryKeyCondition(self.sk_name), DynamoQueryPayload(
            table_name=self.table_name)

    def get_composite_key_read_payload(self, ordered_key_values: List[str], *,
                                       delimiter: str = None) -> DynamoQueryPayload:
        composite_key_value, partition_key_value, range_key_condition, payload = \
            self._get_composite_key_query_components(ordered_key_values, delimiter)

        range_key_condition.add_key_equals(composite_key_value)
        payload.add_partition_key_eq_condition_expression(self.pk_name, partition_key_value, range_key_condition)
        return payload

    def get_composite_key_query_payload(self, ordered_key_values: List[str], *,
                                        delimiter: str = None) -> DynamoQueryPayload:
        composite_key_value, partition_key_value, range_key_condition, payload = \
            self._get_composite_key_query_components(ordered_key_values, delimiter)

        range_key_condition.add_key_begins_with(composite_key_value)
        payload.add_partition_key_eq_condition_expression(self.pk_name, partition_key_value, range_key_condition)
        return payload

    def get_composite_key_delete_payload(self, ordered_key_values: List[str], *,
                                         delimiter: str = None) -> DynamoDeleteItemPayload:
        sk_value, pk_value = self._get_composite_key_components(ordered_key_values, delimiter)
        payload = DynamoDeleteItemPayload(table_name=self.table_name)
        payload.add_key_item(self.pk_name, pk_value)
        payload.add_key_item(self.sk_name, sk_value)
        return payload

# def get_composite_key_query_payload(self, ordered_key_values: List[str], *,
#                                     delimiter: str = None) -> DynamoQueryPayload:
#     composite_key_value, partition_key_value, range_key_condition, payload = self._get_composite_key_components(
#         ordered_key_values, delimiter)
#
#     range_key_condition.add_key_begins_with(composite_key_value)
#     payload.add_partition_key_eq_condition_expression(self.pk_name, partition_key_value, range_key_condition)
#     return payload
