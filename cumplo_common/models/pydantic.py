from cumplo_common.models.base_model import StrEnum


class ValidatorMode(StrEnum):
    BEFORE = "before"
    PLAIN = "plain"
    AFTER = "after"
    WRAP = "wrap"
