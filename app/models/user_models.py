from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    """User login model."""
    email: EmailStr
    password: str

class UserInDB(UserBase):
    """User model for database storage."""
    id: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime

class Token(BaseModel):
    """JWT token model."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """JWT token data model."""
    email: Optional[str] = None
    user_id: Optional[str] = None 