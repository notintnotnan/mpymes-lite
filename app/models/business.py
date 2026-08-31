from datetime import datetime

from pydantic import BaseModel, ConfigDict

class Business(BaseModel):
    name:str
    identifier:str|None = None

class BusinessCreate(Business):
    pass

class BusinessRead(Business):
    id:int
    created_at:datetime
    updated_at:datetime|None = None

    model_config = ConfigDict(from_attributes=True)

class BusinessUpdate(Business):
    id:int

class BusinessDelete(BaseModel):
    id:int
