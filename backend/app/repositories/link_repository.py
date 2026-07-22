from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Link


async def get_link_by_code(db: AsyncSession, code: str) -> Link | None:
    result = await db.execute(select(Link).where(Link.code == code))
    return result.scalar_one_or_none()


async def create_link(
    db: AsyncSession,
    code: str,
    target_url: str,
    owner_id: str | None,
    title: str | None,
    description: str | None,
) -> Link:
    link = Link(
        code=code,
        target_url=target_url,
        owner_id=owner_id,
        title=title,
        description=description,
    )
    db.add(link)
    await db.commit()
    await db.refresh(link)
    return link
