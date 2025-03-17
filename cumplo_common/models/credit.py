from .utils import StrEnum


class CreditType(StrEnum):
    HUD_SUBSIDY = "HOUSING & URBAN DEVELOPMENT SUBSIDY"
    TREASURY_SUBSIDY = "TREASURY SUBSIDY"
    WORKING_CAPITAL = "WORKING CAPITAL"
    FACTORING = "FACTORING"
