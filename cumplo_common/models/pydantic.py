from cumplo_common.models import StrEnum


class ValidatorMode(StrEnum):
    BEFORE = "before"
    PLAIN = "plain"
    AFTER = "after"
    WRAP = "wrap"
