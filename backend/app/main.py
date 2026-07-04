from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

app = FastAPI(title='korotish')


@app.get('/health')
async def health():
    return {'status': 'ok'}

@app.get('/health/db')
async def health_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text('SELECT 1'))
    return {'db': result.scalar()}