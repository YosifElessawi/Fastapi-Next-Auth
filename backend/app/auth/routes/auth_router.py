from app.auth.schemas.auth import AuthResponse
from app.auth.services.auth_service import AuthService
from app.core.database import get_db
from app.user.schemas.user import UserCreate
from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

# Create router with auth prefix and consistent tags
router = APIRouter(prefix="/auth", tags=["auth"])

# Module-level variable for Depends(get_db)
db_dependency = Depends(get_db)

# Module-level variable for Depends(OAuth2PasswordRequestForm)
form_dependency = Depends(OAuth2PasswordRequestForm)


@router.post(
    "/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    user: UserCreate, request: Request, db: Session = db_dependency
) -> AuthResponse:
    return AuthService.register_user(db=db, user_data=user, request=request)


@router.post(
    "/login",
    response_model=AuthResponse,
    dependencies=[Depends(RateLimiter(times=3, seconds=60))],
)
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = form_dependency,
    db: Session = db_dependency,
) -> AuthResponse:
    return AuthService.login_user(
        db=db, username=form_data.username, password=form_data.password, request=request
    )
