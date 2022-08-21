from pydantic import BaseModel, Field

class User(BaseModel):
    first_name = Field(example="Ezio", min_length=3, default=None)
    last_name = Field(example="Auditore", min_length=3, default=None)
    nickname = Field(..., example="ezaud", min_length=3)
