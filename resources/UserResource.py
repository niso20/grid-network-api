# schemas/UserResource.py
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, ForwardRef, TYPE_CHECKING
from resources.RoleResource import RoleResource

class UserResource(BaseModel):
    id: int
    firstname: str
    surname: str
    username: str
    role: Optional[RoleResource] = None  # <-- Optional relationship

    # class Config:
    #     orm_mode = True
    #     allow_population_by_field_name = True
    model_config = ConfigDict(
        from_attributes=True,  # Replaces orm_mode
        populate_by_name=True  # Replaces allow_population_by_field_name
    )

# LineResource.update_forward_refs()
