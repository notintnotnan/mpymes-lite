from datetime import datetime

from pydantic import BaseModel

class Tax(BaseModel):
    description:str
    rate:str

class TaxCreate(Tax):
    pass

class TaxRead(Tax):
    id:int
    valid_from:datetime
    valid_until:datetime
    created_at:datetime

class TaxUpdate(Tax):
    valid_from:datetime
    valid_until:datetime

class TaxDelete(BaseModel):
    id:int