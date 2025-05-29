from pydantic import BaseModel, Field
from typing import Optional, Any

class SaveManufacturer(BaseModel):
    name: str = Field(min_length=1)


class UpdateManufacturer(BaseModel):
    name: Optional[str] = None
