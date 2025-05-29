from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from resources.flats.FlatStationResource import FlatStationResource

class FlatTransformerResource(BaseModel):
    id: int
    name: str
    serialNo: str = Field(..., alias="serial_no")
    powerRating: int = Field(..., alias="power_rating")
    powerRatingUnit: str = Field(..., alias="power_rating_unit")
    typeOfCooling: str = Field(..., alias="type_of_cooling")
    voltageRating: str = Field(..., alias="voltage_rating")
    manufactureYear: int = Field(..., alias="manufacture_year")
    installationYear: int = Field(..., alias="installation_year")
    station: FlatStationResource

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )