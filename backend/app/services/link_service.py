import secrets
import string

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Link, User
from app.repositories.link_repository import create_link, get_link_by_code
from app.repositories.click_repository import create_click

CODE_ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 7


class AliasTakenError(Exception):
    pass

class LinkNotFoundError(Exception):
    pass


async def _generate_unique_code(db: AsyncSession) -> str:
    for _ in (5):
        candidate = ''.join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))
        if await get_link_by_code(db, candidate) is None:
            return candidate
    raise RuntimeError('Could not generate a unique code, try again')


async def create_new_link(
    db: AsyncSession,
    target_url: str,
    owner: User | None,
    custom_alias: str | None = None,
    title: str | None = None,
    description: str | None = None,
) -> Link:
    if custom_alias:
        if await get_link_by_code(db, custom_alias) is not None:
            raise AliasTakenError()
        code = custom_alias
    else:
        code = await _generate_unique_code(db)

    return await create_link(
        db,
        code=code,
        target_url=target_url,
        owner_id=owner.id if owner else None,
        title=title,
        description=description,
    )


async def resolve_link(db: AsyncSession, code: str, ip: str, user_agent: str | None) -> Link:
    link = await get_link_by_code(db, code)
    if link is None:
        raise LinkNotFoundError()

    await create_click(db, link_id=link.id, ip=ip, user_agent=user_agent)
    return link
