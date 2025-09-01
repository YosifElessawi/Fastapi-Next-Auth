import logging
from datetime import timedelta

from app.auth.schemas.auth import AuthResponse
from app.auth.utils import generate_access_token, verify_password
from app.core.config import settings
from app.user.schemas.user import UserCreate, UserInDB
from app.user.services.user_service import UserService
from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

# Get logger for this module
logger = logging.getLogger(__name__)


class AuthService:

    def register_user(
        db: Session, user_data: UserCreate, request: Request
    ) -> AuthResponse[UserInDB]:
        try:
            # Create new user using UserService
            user = UserService.create_user(db, user_data)

            logger.info(f"New user registered: {user_data.username}")

            # Generate access token
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = generate_access_token(
                data={"sub": user_data.username}, expires_delta=access_token_expires
            )

            # Convert user to Pydantic model for response
            user_in_db = UserInDB.from_orm(user)

            return AuthResponse(user=user_in_db, token=access_token)

        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as e:
            logger.error(f"Unexpected error during registration: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred during registration",
            )

    def login_user(
        db: Session, username: str, password: str, request: Request
    ) -> AuthResponse[UserInDB]:
        try:
            # Input validation
            if not username or not password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username and password are required",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Get user from database using UserService
            user = UserService.get_user_by_username(db, username=username)

            # Check if user exists and is active
            if not user or not verify_password(password, user.hashed_password):
                logger.warning(f"Failed login attempt for user: {username}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if not user.is_active:
                logger.warning(f"Login attempt for inactive user: {user.username}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
                )

            # Generate access token
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = generate_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )

            logger.info(f"User logged in: {user.username}")

            # Convert user to Pydantic model for response
            user_in_db = UserInDB.from_orm(user)

            return AuthResponse(user=user_in_db, token=access_token)

        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred during login",
            )
