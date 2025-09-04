"""
User service module for handling all user-related business logic.

This module provides CRUD operations for user management.
"""

import logging
from datetime import datetime
from typing import List, Optional

from app.auth.utils import get_password_hash
from app.user.models.user import User
from app.user.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

# Get logger for this module
logger = logging.getLogger(__name__)


class UserService:

    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        try:
            return db.query(User).filter(User.id == user_id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving user",
            )

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        try:
            return db.query(User).filter(User.email == email).first()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving user by email {email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving user by email",
            )

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        try:
            return db.query(User).filter(User.username == username).first()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving user by username {username}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving user by username",
            )

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        try:
            return db.query(User).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving users: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving users",
            )

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        try:
            # Check if email already exists
            db_user = UserService.get_user_by_email(db, email=user.email)
            if db_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

            # Check if username already exists
            db_user = UserService.get_user_by_username(db, username=user.username)
            if db_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken",
                )

            # Hash the password
            hashed_password = get_password_hash(user.password)

            # Create new user
            db_user = User(
                email=user.email,
                username=user.username,
                hashed_password=hashed_password,
                full_name=user.full_name,
                is_active=True,
                is_superuser=False,
            )

            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user

        except IntegrityError as e:
            db.rollback()
            logger.error(f"Integrity error creating user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not create user due to data integrity error",
            )
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating user",
            )

    @staticmethod
    def update_user(db: Session, db_user: User, user_update: UserUpdate) -> User:
        try:
            update_data = user_update.dict(exclude_unset=True)

            # If password is being updated, hash the new password
            if "password" in update_data:
                hashed_password = get_password_hash(update_data["password"])
                del update_data["password"]
                update_data["hashed_password"] = hashed_password

            # Update user fields
            for field, value in update_data.items():
                setattr(db_user, field, value)

            db_user.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(db_user)
            return db_user

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error updating user {db_user.id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating user",
            )

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        try:
            db_user = UserService.get_user(db, user_id)
            if not db_user:
                return False

            db.delete(db_user)
            db.commit()
            logger.info(f"User {user_id} deleted successfully")
            return True

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error deleting user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting user",
            )

    @staticmethod
    def is_active(user: User) -> bool:
        return user.is_active

    @staticmethod
    def is_superuser(user: User) -> bool:
        return user.is_superuser
