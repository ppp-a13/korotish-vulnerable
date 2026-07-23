from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.routes import auth as auth_routes
from app.routes import links as links_routes
from app.routes import pages as pages_routes
from app.routes.api import auth as api_auth_routes

app = FastAPI(title="korotish")

app.include_router(auth_routes.router, tags=["auth-html"])
app.include_router(api_auth_routes.router, prefix="/api/auth", tags=["auth-api"])
app.include_router(pages_routes.router, tags=["pages"])
app.include_router(links_routes.router, tags=["links"])


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/health/db")
async def health_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"db": result.scalar()}
