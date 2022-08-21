from typing import List, Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    first_name: Optional[str] = Field(example="Ezio", min_length=3, default=None)
    last_name: Optional[str] = Field(example="Auditore", min_length=3, default=None)
    nickname: str = Field(..., example="ezaud", min_length=3)

class Users(BaseModel):
    users: List[str] = Field(...)