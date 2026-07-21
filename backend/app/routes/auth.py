from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.services.auth_service import (
    EmailAlreadyRegisteredError,
    InvalidCredentialError,
    authenticate_user,
    issue_token_for,
    register_user,
)
from app.templating import templates

router = APIRouter()


def _set_auth_cookie(response, token: str) -> None:
    response.set_cookie(
        key='access_token',
        value=token,
        httponly=True,
        samesite='lax',
        max_age=60 * 60,
    )


@router.get('/register')
async def register_form(request: Request):
    return templates.TemplateResponse(request, 'register.html', {'error': None})


@router.post('/register')
async def register_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await register_user(db, email=email, password=password)
    except EmailAlreadyRegisteredError:
        return templates.TemplateResponse(
            request, 'register.html', {'error': 'Email already registered'}, status_code=400
        )
    
    response = RedirectResponse(url='/dashboard', status_code=303)
    _set_auth_cookie(response, issue_token_for(user))
    return response


@router.get('/login')
async def login_form(request: Request):
    return templates.TemplateResponse(request, 'login.html', {'error': None})


@router.post('/login')
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await authenticate_user(db, email=email, password=password)
    except InvalidCredentialError:
        return templates.TemplateResponse(
            request, 'login.html', {'error': 'Invalid email or password'}, status_code=400
        )
    
    response = RedirectResponse(url='/dashboard', status_code=303)
    _set_auth_cookie(response, issue_token_for(user))
    return response


@router.post('/logout')
async def logout(user: User = Depends(get_current_user)):
    response = RedirectResponse(url='/', status_code=303)
    response.delete_cookie('access_token')
    return response
