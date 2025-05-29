from pydantic import BaseModel, Field
from typing import Optional, Any
from enums.PowerUnit import PowerUnit

class SaveTransformer(BaseModel):
    name: str = Field(min_length=1)
    manufacturerId: int
    serialNo: Optional[str] = None
    powerRating: int
    powerRatingUnit: PowerUnit
    typeOfCooling: Optional[str]
    voltageRating: str
    manufactureYear: Optional[int]
    installationYear: Optional[int]
    stationId: Optional[int] = None


class UpdateTransformer(BaseModel):
    name: Optional[str] = None
    manufacturerId: Optional[int] = None
    serialNo: Optional[str] = None
    powerRating: Optional[int] = None
    powerRatingUnit: Optional[PowerUnit] = None
    typeOfCooling: Optional[str] = None
    voltageRating: Optional[str] = None
    manufactureYear: Optional[int] = None
    installationYear: Optional[int] = None
    stationId: Optional[int] = None
