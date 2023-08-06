from enum import Enum
from typing import List, Optional

KEY_DELIMITER = '#'


def make_composite_key(ordered_key_values: List[str], key_delimiter=KEY_DELIMITER, *, append_delimiter=False) -> str:
    return key_delimiter.join(ordered_key_values) if not append_delimiter \
        else key_delimiter.join(ordered_key_values) + key_delimiter


def parse_composite_key(composite_key: str, key_delimiter=KEY_DELIMITER) -> List[str]:
    return composite_key.split(key_delimiter)


def get_dict_with_model_keys(original_dict: dict, composite_key_name: str,
                             ordered_component_key_names: List[str], key_delimiter: Optional[str] = None) -> dict:
    if not key_delimiter:
        key_delimiter = KEY_DELIMITER
    composite_key: str = original_dict[composite_key_name]
    key_value_list = parse_composite_key(composite_key, key_delimiter)

    return {
        **{k: v for k, v in original_dict.items() if k != composite_key_name},
        **{component_key: key_value_list[index] for index, component_key in enumerate(ordered_component_key_names)}
    }


def get_dict_with_composite_key(original_dict: dict, composite_key_name: str,
                                ordered_component_key_names: List[str], key_delimiter: Optional[str] = None) -> dict:
    if not key_delimiter:
        key_delimiter = KEY_DELIMITER
    composite_key = make_composite_key(
        [key_value for key_value in [original_dict[key_name] for key_name in ordered_component_key_names]],
        key_delimiter,
    )

    return {
        **{k: v for k, v in original_dict.items() if k not in ordered_component_key_names},
        composite_key_name: composite_key,
    }
