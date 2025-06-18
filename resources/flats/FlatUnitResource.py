from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class FlatUnitResource(BaseModel):
    tableId: int = Field(..., alias="id")
    id: str = Field(..., alias="identifier")
    name: str
    inertia: float
    active: bool
    voltageLevel: Optional[float] = Field(None, alias="voltage_level")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )