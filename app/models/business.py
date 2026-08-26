from datetime import datetime

from pydantic import BaseModel

class Business(BaseModel):
    name:str
    identifier:str

class BusinessCreate(Business):
    pass

class BusinessRead(Business):
    id:int
    created_at:datetime
    updated_at:datetime

class BusinessUpdate(Business):
    id:int

class BusinessDelete(BaseModel):
    id:int
