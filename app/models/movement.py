from typing import List

from datetime import datetime

from pydantic import BaseModel

from app.core.enums import MovementTypes

class Movement(BaseModel):
    base_value:float
    movement_type:MovementTypes
    category_id:int

class MovementCreate(Movement):
    account_id:int
    taxes:List[int|None]

class MovementRead(Movement):
    id:int
    account_id:int
    taxes:List[MovementTaxRead]
    total_value:float
    created_at:datetime

class MovementUpdate(Movement):
    account_id:int
    taxes:List[MovementTaxCreate|MovementTaxUpdate]

class MovementDelete(Movement):
    id:int

class MovementTax(BaseModel):
    tax_id:int
    movement_id:int

class MovementTaxCreate(MovementTax):
    pass

class MovementTaxRead(MovementTax):
    id:int
    rate:float
    description:str

class MovementTaxUpdate(MovementTax):
    pass

class MovementTaxDelete(MovementTax):
    id:int

class MovementCategory(BaseModel):
    description:str
    category_id:int

class MovementCategoryCreate(MovementCategory):
    pass

class MovmentCategoryRead(MovementCategory):
    id:int

class MovementCategoryUpdate(MovementCategory):
    pass

class MovementCategoryDelete(MovementCategory):
    id:int
