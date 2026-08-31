from datetime import datetime

from pydantic import BaseModel, ConfigDict

class Tax(BaseModel):
    description:str
    rate:float

class TaxCreate(Tax):
    valid_from:datetime

class TaxRead(Tax):
    id:int
    valid_from:datetime
    valid_until:datetime|None = None
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)

class TaxUpdate(Tax):
    id:int
    valid_from:datetime
    valid_until:datetime

class TaxDelete(BaseModel):
    id:int