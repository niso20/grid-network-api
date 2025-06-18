# schemas/LineResource.py
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, ForwardRef, TYPE_CHECKING

class FlatStationResource(BaseModel):
    tableId: int = Field(..., alias="id")
    id: str = Field(..., alias="identifier")
    name: str
    voltageLevel: Optional[float] = Field(None, alias="voltage_level")
    display: bool
    type: str
    x: int
    y: int
    width: int
    height: int

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )