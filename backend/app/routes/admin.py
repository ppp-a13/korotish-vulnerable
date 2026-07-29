from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_admin
from app.models import User
from app.services.admin_service import get_admin_overview
from app.templating import templates

router = APIRouter()


@router.get('/admin')
async def admin_dashboard(
    request: Request,
    user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    overview = await get_admin_overview(db)
    return templates.TemplateResponse(request, 'admin.html', overview)
