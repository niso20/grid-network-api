# schemas/LineResource.py
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, ForwardRef, TYPE_CHECKING
from resources.flats.FlatStationResource import FlatStationResource
from resources.flats.FlatConnectionResource import FlatConnectionResource

class LineResource(BaseModel):
    tableId: int = Field(..., alias="id")
    id: str = Field(..., alias="identifier")  # map identifier → id
    name: str
    x: int
    y: int
    station: Optional[FlatStationResource] = None  # <-- Optional relationship
    outgoingConnections: Optional[List[FlatConnectionResource]] = None
    incomingConnections: Optional[List[FlatConnectionResource]] = None

    # class Config:
    #     orm_mode = True
    #     allow_population_by_field_name = True
    model_config = ConfigDict(
        from_attributes=True,  # Replaces orm_mode
        populate_by_name=True  # Replaces allow_population_by_field_name
    )

# LineResource.update_forward_refs()
