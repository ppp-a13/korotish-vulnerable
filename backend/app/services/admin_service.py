from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.click_repository import count_clicks
from app.repositories.link_repository import count_links, list_all_links_with_click_counts
from app.repositories.user_repository import count_users, list_all_users


async def get_admin_overview(db: AsyncSession) -> dict:
    return {
        'users': await list_all_users(db),
        'links_with_counts': await list_all_links_with_click_counts(db),
        'total_users': await count_users(db),
        'total_links': await count_links(db),
        'total_clicks': await count_clicks(db),
    }
