from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Click, Link


async def get_link_by_code(db: AsyncSession, code: str) -> Link | None:
    result = await db.execute(select(Link).where(Link.code == code))
    return result.scalar_one_or_none()


async def create_link(
    db: AsyncSession,
    code: str,
    target_url: str,
    owner_id: int | None,
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


async def get_link_by_id(db: AsyncSession, link_id: int) -> Link | None:
    result = await db.execute(select(Link).where(Link.id == link_id))
    return result.scalar_one_or_none()


async def list_links_with_click_counts(db: AsyncSession, owner_id: int) -> list[tuple[Link, int]]:
    result = await db.execute(
        select(Link, func.count(Click.id))
        .outerjoin(Click, Click.link_id == Link.id)
        .where(Link.owner_id == owner_id)
        .group_by(Link.id)
        .order_by(Link.created_at.desc())
    )
    return [(link, count) for link, count in result.all()]


async def search_links_by_owner(db: AsyncSession, owner_id: int, query: str) -> list[Link]:
    pattern = f"%{query}%"
    result = await db.execute(
        select(Link)
        .where(Link.owner_id == owner_id)
        .where(or_(Link.title.ilike(pattern), Link.target_url.ilike(pattern)))
        .order_by(Link.created_at.desc())
    )
    return list(result.scalars().all())
