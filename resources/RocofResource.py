# schemas/RocofResource.py
from pydantic import BaseModel, Field, ConfigDict, computed_field
from typing import List, Optional, ForwardRef, TYPE_CHECKING
from datetime import datetime

class RocofResource(BaseModel):
    rocof: float
    f: float
    t: str
    createdAt: datetime = Field(..., alias="created_at")

    model_config = ConfigDict(
        from_attributes=True,  # Replaces orm_mode
        populate_by_name=True  # Replaces allow_population_by_field_name
    )

    @computed_field
    @property
    def dateTime(self) -> str:
        """
        Combines the date from created_at with the time from t field.
        Returns format: 'YYYY-MM-DD HH:MM:SS'
        """
        # Extract date part from created_at
        date_part = self.createdAt.strftime("%Y-%m-%d")

        # Combine with time from t field
        return f"{date_part} {self.t}"

