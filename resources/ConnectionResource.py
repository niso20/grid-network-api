# schemas/LineResource.py
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, ForwardRef, TYPE_CHECKING
from resources.flats.FlatStationResource import FlatStationResource
from resources.flats.FlatLineResource import FlatLineResource

class ConnectionResource(BaseModel):
    tableId: int = Field(..., alias="id")
    id: str = Field(..., alias="identifier")  # map identifier → id
    fromStation: Optional[FlatStationResource] = None  # <-- Optional relationship
    fromLine: Optional[FlatLineResource] = None  # <-- Optional relationship
    fromSide: str = Field(..., alias="from_side")  # map identifier → from_side
    toStation: Optional[FlatStationResource] = None  # <-- Optional relationship
    toLine: Optional[FlatLineResource] = None  # <-- Optional relationship
    toSide: str = Field(..., alias="to_side")  # map identifier → to_side

    # class Config:
    #     orm_mode = True
    #     allow_population_by_field_name = True
    model_config = ConfigDict(
        from_attributes=True,  # Replaces orm_mode
        populate_by_name=True  # Replaces allow_population_by_field_name
    )

# LineResource.update_forward_refs()
