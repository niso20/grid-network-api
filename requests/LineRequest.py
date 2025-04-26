from pydantic import BaseModel, Field
from typing import Optional

class CreateLine(BaseModel):
    name: str = Field(min_length=1)
    identifier: str = Field(min_length=1)
    stationId: int
    voltageLevel: Optional[float] = None


class UpdateLine(BaseModel):
    name: Optional[str] = None
    identifier: Optional[str] = None
    stationId: Optional[int] = None
    voltageLevel: Optional[float] = None
    x: Optional[int] = None
    y: Optional[int] = None
