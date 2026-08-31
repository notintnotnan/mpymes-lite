from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict

from app.core.enums import AccountTypes

if TYPE_CHECKING:
    from app.models.business import BusinessRead
    from app.models.movement import MovementRead

class Account(BaseModel):
    number:str

class AccountCreate(Account):
    business_id:int
    account_type:AccountTypes

class AccountRead(Account):
    id:int
    business_id:int
    account_type:AccountTypes
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)

class AccountDetailRead(AccountRead):
    business: Optional["BusinessRead"] = None
    movements: List["MovementRead"] = []

class AccountUpdate(Account):
    id:int

class AccountDelete(BaseModel):
    id:int
