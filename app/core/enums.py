from enum import Enum

class AccountTypes(Enum):
    CASH = "cash"
    CREDIT = "credit"
    DEBIT = "debit"

class MovementTypes(Enum):
    CREDIT = "credit"
    DEBIT = "debit"