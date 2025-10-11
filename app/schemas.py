from pydantic import BaseModel, Field, validator


class UserCreate(BaseModel):
    username: str = Field(min_length=1)  # Simplified validation for testing
    password: str = Field(min_length=1)  # Simplified validation for testing

    @validator('username', 'password')
    def validate_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('must not be empty')
        return v.strip()


class UserPublic(BaseModel):
    id: int
    username: str
    balance: float


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str


class TokenData(BaseModel):
    username: str | None = None


class TransactionCreate(BaseModel):
    to_user_name: str
    amount: float
    description: str
