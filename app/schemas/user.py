from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    # Syntax: EmailStr  validates proper email formatting
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
