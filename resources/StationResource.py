from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from resources.flats.FlatLineResource import FlatLineResource
from resources.flats.FlatTransformerResource import FlatTransformerResource

class StationResource(BaseModel):
    tableId: int = Field(..., alias="id")
    id: str = Field(..., alias="identifier")  # map identifier → id
    name: str
    voltageLevel: Optional[float] = Field(None, alias="voltage_level")  # rename in response
    display: bool
    x: int
    y: int
    width: int
    height: int
    lines: Optional[List[FlatLineResource]] = None  # optional!
    transformers: Optional[List[FlatTransformerResource]] = None
    # lines: List[LineResource] = []

    # class Config:
    #     # orm_mode = True
    #     from_attributes = True
    #     # allow_population_by_field_name = True  # allows using "id" in output
    #     populate_by_name = True
    model_config = ConfigDict(
        from_attributes=True,  # Replaces orm_mode
        populate_by_name=True  # Replaces allow_population_by_field_name
    )