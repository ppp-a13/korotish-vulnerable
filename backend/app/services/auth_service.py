from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repositories.user_repository import create_user, get_user_by_email
from app.services.security import create_access_token, hash_password, verify_password


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialError(Exception):
    pass


async def register_user(db: AsyncSession, email: str, password: str) -> User:
    existing = await get_user_by_email(db, email)
    if existing is not None:
        raise EmailAlreadyRegisteredError()

    password_hash = hash_password(password)
    return await create_user(db, email=email, password_hash=password_hash)


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    user = await get_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        raise InvalidCredentialError()

    return user


def issue_token_for(user: User) -> str:
    return create_access_token(user_id=user.id, is_admin=user.is_admin)
