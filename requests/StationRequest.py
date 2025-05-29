from pydantic import BaseModel, Field
from typing import Optional, Any
from enums.StationType import StationType

class CreateStation(BaseModel):
    name: str = Field(min_length=1)
    identifier: str = Field(min_length=1)
    type: StationType
    voltageLevel: Optional[float] = None
    display: Optional[bool] = None


class UpdateStation(BaseModel):
    name: Optional[str] = None
    identifier: Optional[str] = None
    type: Optional[StationType] = None
    voltageLevel: Optional[float] = None
    x: Optional[int] = None
    y: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    display: Optional[bool] = None
    lines: Optional[list[Any]] = None
