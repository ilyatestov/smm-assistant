from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated

from models.user import User
from api.v1.schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from core.security import get_password_hash, verify_password, create_access_token, decode_access_token
from utils.dependencies import get_db
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


async def get_current_user(
    token: str,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    """Dependency to get current authenticated user from JWT token."""
    payload = decode_access_token(token)
    
    if payload is None:
        logger.warning("Invalid or expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserResponse:
    """
    Register a new user.
    
    - **email**: Valid email address
    - **password**: Password (min 8 characters)
    """
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        logger.warning("Registration attempt with existing email", email=user_data.email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        role="user",
        subscription_tier="free"
    )
    
    db.add(new_user)
    await db.flush()  # Get the ID before commit
    await db.refresh(new_user)
    
    logger.info("New user registered", user_id=new_user.id, email=new_user.email)
    
    return UserResponse.model_validate(new_user)


@router.post("/login", response_model=TokenResponse)
async def login_user(
    credentials: UserLogin,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> TokenResponse:
    """
    Login user and return JWT token.
    
    - **email**: User email
    - **password**: User password
    """
    # Find user
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        logger.warning("Failed login attempt", email=credentials.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    
    logger.info("User logged in", user_id=user.id, email=user.email)
    
    return TokenResponse(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserResponse:
    """
    Get current authenticated user profile.
    
    Protected endpoint - requires valid JWT token.
    """
    logger.info("User profile accessed", user_id=current_user.id)
    return UserResponse.model_validate(current_user)
