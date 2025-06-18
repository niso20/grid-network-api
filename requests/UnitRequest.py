from pydantic import BaseModel, Field
from typing import Optional

class CreateUnit(BaseModel):
    name: str = Field(min_length=1)
    identifier: str = Field(min_length=1)
    stationId: int
    voltageLevel: Optional[float] = None
    inertia: float
    active: Optional[bool]


class UpdateUnit(BaseModel):
    name: Optional[str] = None
    identifier: Optional[str] = None
    stationId: Optional[int] = None
    voltageLevel: Optional[float] = None
    inertia: Optional[float]
    active: Optional[bool]
