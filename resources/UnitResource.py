# schemas/LineResource.py
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, ForwardRef, TYPE_CHECKING
from resources.flats.FlatStationResource import FlatStationResource

class UnitResource(BaseModel):
    tableId: int = Field(..., alias="id")
    id: str = Field(..., alias="identifier")  # map identifier → id
    name: str
    inertia: float
    active: bool
    voltageLevel: Optional[float] = Field(None, alias="voltage_level")
    station: Optional[FlatStationResource] = None  # <-- Optional relationship

    # class Config:
    #     orm_mode = True
    #     allow_population_by_field_name = True
    model_config = ConfigDict(
        from_attributes=True,  # Replaces orm_mode
        populate_by_name=True  # Replaces allow_population_by_field_name
    )

