import logging
from datetime import datetime, timedelta
from typing import Optional

import jwt
from app.auth.schemas.auth import Token
from app.core.config import settings
from fastapi import HTTPException, status
from passlib.context import CryptContext

# Get logger for this module
logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if a plain password matches a hashed password.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except (ValueError, TypeError) as e:
        logger.error(f"Password verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during password verification",
        )


def get_password_hash(password: str) -> str:
    """
    Generate a hashed password from a plain password.
    """
    return pwd_context.hash(password)


def generate_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> Token:
    """
    Generate a JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    try:
        # Generate the JWT token string
        token_string = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
        )

        logger.info(f"Access token generated for user: {data['sub']}")
        # Return as Token object
        return Token(access_token=token_string, token_type="bearer")

    except Exception as e:
        logger.error(f"Error creating access token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating access token",
        )
