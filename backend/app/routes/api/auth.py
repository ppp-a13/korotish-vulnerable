from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.services.auth_service import (
    EmailAlreadyRegisteredError,
    InvalidCredentialError,
    authenticate_user,
    issue_token_for,
    register_user,
)

router = APIRouter()


@router.post('/register', response_model=TokenResponse)
async def api_register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    try:
        user = await register_user(db, email=payload.email, password=payload.password)
    except EmailAlreadyRegisteredError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')
    
    return TokenResponse(access_token=issue_token_for(user))


@router.post('/login', response_model=TokenResponse)
async def api_login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        user = await authenticate_user(db, email=payload.email, password=payload.password)
    except InvalidCredentialError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')

    return TokenResponse(access_token=issue_token_for(user))
