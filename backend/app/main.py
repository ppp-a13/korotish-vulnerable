from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.routes import auth as auth_routes
from app.routes.api import auth as api_auth_routes

app = FastAPI(title='korotish')

app.include_router(auth_routes.router, tags=['auth-html'])
app.include_router(api_auth_routes.router, prefix='/api/auth', tags=['auth-api'])


@app.get('/health')
async def health():
    return {'status': 'ok'}

@app.get('/health/db')
async def health_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text('SELECT 1'))
    return {'db': result.scalar()}