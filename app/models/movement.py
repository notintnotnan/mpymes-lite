from typing import List, Optional

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import MovementTypes

from app.models.tax import TaxRead

class MovementTax(BaseModel):
    tax_id:int
    movement_id:int

class MovementTaxCreate(MovementTax):
    pass

class MovementTaxRead(MovementTax):
    id:int
    rate:float
    description:str

    model_config = ConfigDict(from_attributes=True)

class MovementTaxUpdate(MovementTax):
    pass

class MovementTaxDelete(BaseModel):
    id:int

class MovementCategory(BaseModel):
    description:str
    movement_type:MovementTypes

class MovementCategoryCreate(MovementCategory):
    pass

class MovementCategoryRead(MovementCategory):
    id:int

    model_config = ConfigDict(from_attributes=True)

class MovementCategoryUpdate(MovementCategory):
    pass

class MovementCategoryDelete(BaseModel):
    id:int

class Movement(BaseModel):
    base_value:float
    movement_type:MovementTypes
    movement_category_id:int

class MovementCreate(Movement):
    account_id:int
    taxes:Optional[List[int]] = None

class MovementRead(Movement):
    id:int
    account_id:int
    taxes:List[TaxRead]
    total_value:float
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)

class MovementUpdate(Movement):
    account_id:int
    taxes:List[MovementTaxCreate|MovementTaxUpdate]

class MovementDelete(BaseModel):
    id:int
