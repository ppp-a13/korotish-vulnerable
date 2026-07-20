from datetime import datetime


from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column


from app.database import Base


class Click(Base):
    __tablename__ = 'clicks'

    id: Mapped[int] = mapped_column(primary_key=True)
    link_id: Mapped[int] = mapped_column(ForeignKey('links.id'), index=True)
    ip: Mapped[str] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())