import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc, func
from app.db.models import User, Video, Recommendation, UserInteraction
from typing import List
from datetime import datetime

logger = logging.getLogger(__name__)


# --- User CRUD ---
async def get_or_create_user(db: AsyncSession, username: str) -> User:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    if user is None:
        user = User(username=username)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Created new user: {username}")

    return user


# --- Recommendation/Video CRUD ---

async def get_popular_videos(db: AsyncSession, limit: int = 10) -> List[Video]:
    result = await db.execute(
        select(Video)
        .order_by(desc(Video.view_count))
        .limit(limit)
    )
    return result.scalars().all()


async def get_video_by_id(db: AsyncSession, video_id: int) -> Video | None:
    result = await db.execute(select(Video).where(Video.id == video_id))
    return result.scalars().first()


async def save_user_interaction(db: AsyncSession, user_id: int, video_id: int, interaction_type: str = "WATCHED") -> UserInteraction:
    interaction = UserInteraction(
        user_id=user_id,
        video_id=video_id,
        interaction_type=interaction_type,
        timestamp=datetime.utcnow()
    )
    db.add(interaction)
    await db.commit()
    await db.refresh(interaction)
    logger.info(f"User {user_id} saved interaction '{interaction_type}' for video {video_id}")
    return interaction



async def get_user_preferred_categories(db: AsyncSession, user_id: int, limit: int = 5) -> List[str]:
    result = await db.execute(
        select(Video.category, func.count(UserInteraction.id).label('interaction_count'))
        .join(UserInteraction, UserInteraction.video_id == Video.id)
        .where(UserInteraction.user_id == user_id)
        .group_by(Video.category)
        .order_by(desc('interaction_count'))
        .limit(limit)
    )
    return [row[0] for row in result.all() if row[0]]