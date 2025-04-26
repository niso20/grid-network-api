# schemas/LineResource.py
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, ForwardRef, TYPE_CHECKING

class FlatConnectionResource(BaseModel):
    tableId: int = Field(..., alias="id")
    id: str = Field(..., alias="identifier")  # map identifier → id
    fromSide: str = Field(..., alias="from_side")  # map identifier → to_side
    toSide: str = Field(..., alias="to_side")  # map identifier → to_side

    # class Config:
    #     orm_mode = True
    #     allow_population_by_field_name = True
    model_config = ConfigDict(
        from_attributes=True,  # Replaces orm_mode
        populate_by_name=True  # Replaces allow_population_by_field_name
    )
