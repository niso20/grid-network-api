# schemas/LineResource.py
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, ForwardRef, TYPE_CHECKING

class FlatManufacturerResource(BaseModel):
    id: int
    name: str