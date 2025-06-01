from pydantic import BaseModel, Field
from typing import Optional

class Login(BaseModel):
    username: str = Field(
                            min_length=1,
                            description="Username is required and cannot be empty",
                            json_schema_extra={"error_msg": "Username is required"}
                          )
    password: str = Field(
        min_length=1,
        description="Password is required and cannot be empty",
        json_schema_extra={"error_msg": "Password is required"}
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "your_username",
                "password": "your_password"
            }
        }
    }
