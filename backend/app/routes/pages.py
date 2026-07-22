from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.services.link_service import AliasTakenError, create_new_link
from app.templating import templates

router = APIRouter()


@router.get('/')
async def index(request: Request):
    return templates.TemplateResponse(request, 'index.html', {'created_link': None, 'error': None})


@router.post('/')
async def index_shorten(
    request: Request,
    target_url: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    link = await create_new_link(db, target_url=target_url, owner=None)
    return templates.TemplateResponse(request, 'index.html', {'created_link': link, 'error': None})


@router.get('/links/new')
async def new_link_form(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse(request, 'links_new.html', {'error': None})


@router.post('/links/new')
async def new_link_submit(
    request: Request,
    target_url: str = Form(...),
    custom_alias: str = Form(default=''),
    title: str = Form(default=''),
    description: str = Form(default=''),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await create_new_link(
            db,
            target_url=target_url,
            owner=user,
            custom_alias=custom_alias or None,
            title=title or None,
            description=description or None,
        )
    except AliasTakenError:
        return templates.TemplateResponse(
            request, 'links_new.html', {'error': 'This alias is already taken'}, status_code=400
        )
    
    return RedirectResponse(url='/dashboard', status_code=303)
