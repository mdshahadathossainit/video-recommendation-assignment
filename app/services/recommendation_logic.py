from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from app.db.crud import get_popular_videos, get_user_preferred_categories
from app.db.models import Video
from typing import List, Dict


async def get_videos_by_categories(db: AsyncSession, categories: List[str], limit: int = 15) -> List[Video]:
    if not categories:
        return []

    result = await db.execute(
        select(Video)
        .where(Video.category.in_(categories))
        .order_by(desc(Video.view_count))
        .limit(limit)
    )
    return result.scalars().all()


async def generate_recommendations(db: AsyncSession, user_id: int) -> List[Dict]:
    RECOMMENDATION_LIMIT = 20

    # 1. ইউজার প্রিফারেন্স বের করা
    preferred_categories: List[str] = await get_user_preferred_categories(db, user_id, limit=3)

    if preferred_categories:
        # 2. Content-Based Logic: ইউজার পছন্দ করেন এমন ক্যাটাগরির ভিডিওগুলি আনা
        videos: List[Video] = await get_videos_by_categories(
            db,
            categories=preferred_categories,
            limit=RECOMMENDATION_LIMIT
        )

        # যদি ক্যাটাগরি অনুসারে কোনো ভিডিও না পাওয়া যায়, তবে fallback করুন
        if not videos:
            videos = await get_popular_videos(db, limit=RECOMMENDATION_LIMIT)

    else:
        # 3. Fallback to Popularity: ইউজার নতুন হলে বা কোনো watch history না থাকলে
        videos = await get_popular_videos(db, limit=RECOMMENDATION_LIMIT)

    recommendations = []
    for video in videos:
        recommendations.append({
            "id": video.id,
            "youtube_id": video.youtube_id,
            "title": video.title,
            "channel_title": video.channel_title,
            "view_count": video.view_count,
            "category": video.category,
            "score": video.view_count
        })

    return recommendations