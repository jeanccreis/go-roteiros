from pydantic import BaseModel
from app.schemas.user import UserResponse

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class UserInDB(UserResponse):
    hashed_password: str
