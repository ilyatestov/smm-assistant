from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# Request schemas
class UserRegister(BaseModel):
    """Schema for user registration request."""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")


class UserLogin(BaseModel):
    """Schema for user login request."""
    email: EmailStr
    password: str


# Response schemas
class UserResponse(BaseModel):
    """Schema for user response (without sensitive data)."""
    id: int
    email: EmailStr
    role: str
    subscription_tier: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str = "bearer"
