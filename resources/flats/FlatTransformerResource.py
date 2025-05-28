from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from resources.flats.FlatConnectionResource import FlatConnectionResource

class FlatLineResource(BaseModel):
    tableId: int = Field(..., alias="id")
    id: str = Field(..., alias="identifier")
    name: str
    x: int
    y: int
    outgoingConnections: Optional[List[FlatConnectionResource]] = None
    incomingConnections: Optional[List[FlatConnectionResource]] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )