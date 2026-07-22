from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Click


async def create_click(db: AsyncSession, link_id: int, ip: str, user_agent: str | None) -> Click:
    click = Click(link_id=link_id, ip=ip, user_agent=user_agent)
    db.add(click)
    await db.commit()
    return click
