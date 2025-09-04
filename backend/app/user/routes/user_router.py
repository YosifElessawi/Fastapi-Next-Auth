from typing import List

from app.auth.deps.auth_deps import get_current_user
from app.core.database import get_db
from app.user.models.user import User as UserModel
from app.user.schemas.user import UserCreate, UserInDB, UserUpdate
from app.user.services.user_service import UserService
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])


# Module-level variable for Depends(get_db)
db_dependency = Depends(get_db)

# Module-level variable for Depends(get_current_user)
authentication = Depends(get_current_user)


@router.get("/me", response_model=UserInDB)
async def read_users_me(
    request: Request, current_user: UserModel = authentication
) -> UserInDB:
    return current_user


@router.get("/", response_model=List[UserInDB])
async def read_users(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = db_dependency,
    current_user: UserModel = authentication,
) -> List[UserInDB]:
    users = UserService.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserInDB)
async def read_user_by_id(
    request: Request,
    user_id: int,
    db: Session = db_dependency,
    current_user: UserModel = authentication,
) -> UserInDB:
    db_user = UserService.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: Request,
    user: UserCreate,
    db: Session = db_dependency,
) -> UserInDB:
    return UserService.create_user(db=db, user=user)


@router.put("/{user_id}", response_model=UserInDB)
async def update_user(
    request: Request,
    user_id: int,
    user_update: UserUpdate,
    db: Session = db_dependency,
    current_user: UserModel = authentication,
) -> UserInDB:
    db_user = UserService.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return UserService.update_user(db=db, db_user=db_user, user_update=user_update)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    request: Request,
    user_id: int,
    db: Session = db_dependency,
    current_user: UserModel = authentication,
) -> None:
    db_user = UserService.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    UserService.delete_user(db=db, user_id=user_id)
    return None
