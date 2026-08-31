from datetime import datetime

from pydantic import BaseModel

class Account(BaseModel):
    number:str

class AccountCreated(Account):
    business_id:int
    account_type:str

class AccountRead(Account):
    id:int
    business_id:int
    account_type:str
    created_at:datetime

class AccountUpdate(Account):
    id:int

class AccountDelete(BaseModel):
    id:int
