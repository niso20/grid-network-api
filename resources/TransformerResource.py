# schemas/LineResource.py
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, ForwardRef, TYPE_CHECKING
from resources.flats.FlatStationResource import FlatStationResource
from resources.flats.FlatManufacturerResource import FlatManufacturerResource

class TransformerResource(BaseModel):
    id: int
    name: str
    serialNo: str = Field(..., alias="serial_no")
    powerRating: int = Field(..., alias="power_rating")
    powerRatingUnit: str = Field(..., alias="power_rating_unit")
    typeOfCooling: str = Field(..., alias="type_of_cooling")
    voltageRating: str = Field(..., alias="voltage_rating")
    manufactureYear: int = Field(..., alias="manufacture_year")
    installationYear: int = Field(..., alias="installation_year")
    station: Optional[FlatStationResource] = None  # <-- Optional relationship
    manufacturer: Optional[FlatManufacturerResource] = None

    # class Config:
    #     orm_mode = True
    #     allow_population_by_field_name = True
    model_config = ConfigDict(
        from_attributes=True,  # Replaces orm_mode
        populate_by_name=True  # Replaces allow_population_by_field_name
    )

# LineResource.update_forward_refs()
