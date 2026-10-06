from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    id: int | None = None
    email: str | None = None

class LoginRequest(BaseModel):
    email: str
    password: str