from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from resources.flats.FlatTransformerResource import FlatTransformerResource


class ManufacturerResource(BaseModel):
    id: int
    name: str
    transformers: Optional[List[FlatTransformerResource]] = None  # optional!