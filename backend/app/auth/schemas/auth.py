from typing import Any, Dict, Generic, Optional, Type, TypeVar

from pydantic import BaseModel

# Create a generic type variable for the user model
UserModel = TypeVar("UserModel")


class TokenData(BaseModel):
    """Token data model for JWT payload."""

    username: Optional[str] = None


class Token(BaseModel):
    """Token model."""

    access_token: str
    token_type: str = "bearer"


class AuthResponse(BaseModel, Generic[UserModel]):
    """Authentication response model containing user and token information.

    This is the standard response format for authentication endpoints (login/register).
    """

    user: UserModel
    token: Token

    class Config:
        arbitrary_types_allowed = True  # Required for generic model support
        json_encoders: Dict[Type[Any], Any] = {
            # Add any custom JSON encoders if needed for the UserModel
        }
