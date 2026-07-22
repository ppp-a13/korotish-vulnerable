from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.link_service import LinkNotFoundError, resolve_link

router = APIRouter()


@router.get('/l/{code}')
async def redirect_link(code: str, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        link = await resolve_link(
            db,
            code=code,
            ip=request.client.host if request.client else 'unknown',
            user_agent=request.headers.get('user-agent')
        )
    except LinkNotFoundError:
        raise HTTPException(status_code=404, detail='Link not found')

    return RedirectResponse(url=link.target_url, status_code=302)
