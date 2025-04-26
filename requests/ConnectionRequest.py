from pydantic import BaseModel, Field
from typing import Optional

class CreateConnection(BaseModel):
    identifier: str = Field(min_length=1)
    fromStationId: int
    fromLineId: int
    fromSide: Optional[str] = None
    toStationId: int
    toLineId: int
    toSide: Optional[str] = None


class UpdateConnection(BaseModel):
    identifier: Optional[str] = None
    fromStationId: Optional[int] = None
    fromLineId: Optional[int] = None
    fromSide: Optional[str] = None
    toStationId: Optional[int] = None
    toLineId: Optional[int] = None
    toSide: Optional[str] = None
