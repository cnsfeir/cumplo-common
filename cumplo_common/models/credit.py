from cumplo_common.models.base_model import StrEnum


class CreditType(StrEnum):
    WORKING_CAPITAL = "WORKING CAPITAL"
    STATE_SUBSIDY = "STATE SUBSIDY"
    BULLET_LOAN = "BULLET LOAN"
    FACTORING = "FACTORING"
