import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    full_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password must be at least 8 characters long",
    )

    @field_validator("username")
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_-]{3,20}$", v):
            raise ValueError(
                "Username must be 3-20 characters long and contain only "
                "letters, numbers, underscores, or hyphens"
            )
        return v

    @field_validator("password")
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        # Add more password strength requirements if needed
        # Example: require at least one number and one special character
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number")
        if not any(char in "!@#$%^&*" for char in v):
            raise ValueError(
                "Password must contain at least one special character " "(!@#$%^&*)"
            )
        return v


class UserInDB(UserBase):
    """Schema for user data stored in the database."""

    id: int
    is_active: bool = True
    is_superuser: bool = False

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user information."""

    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
