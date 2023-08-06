from enum import Enum


class OverloadedGsiKeys(Enum):
    PK = 'PK'
    SK = 'SK'
    GSI_PREFIX = 'GSI'
    DELIMITER = '_'


def get_gsi_pk(gsi: int) -> str:
    return OverloadedGsiKeys.DELIMITER.value.join(
        [OverloadedGsiKeys.GSI_PREFIX.value, str(gsi), OverloadedGsiKeys.PK.value])


def get_gsi_sk(gsi: int) -> str:
    return OverloadedGsiKeys.DELIMITER.value.join(
        [OverloadedGsiKeys.GSI_PREFIX.value, str(gsi), OverloadedGsiKeys.SK.value])
