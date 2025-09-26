# app/services/recommender.py

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession  # ✅ FIX: ডেটাবেস সেশনের জন্য ইমপোর্ট
from app.api.v1.schemas import VideoOut  # ✅ FIX: আপনার schemas ইমপোর্ট করুন
from app.db.crud import get_or_create_user  # ✅ FIX: ইউজার CRUD ইমপোর্ট করুন
from app.db.models import Video  # ✅ FIX: মডেল ইমপোর্ট করুন
from app.services.recommendation_logic import generate_recommendations  # ✅ FIX: আসল রেকমেন্ডেশন লজিক


# Note: configuration (get_settings) is typically passed via dependency injection (Depends)
# or imported elsewhere, not generally at the top level here unless necessary.

# Load the settings object (If needed later)
# settings = get_settings()


async def get_personalized_feed(db: AsyncSession, username: str, page: int, page_size: int) -> List[VideoOut]:
    """
    This function provides a personalized video feed for the user
    by calling the core recommendation logic and applying pagination.
    """

    # 1. Get the user (or create if not exists)
    user = await get_or_create_user(db, username=username)

    # 2. Get the core recommendations (e.g., top 50 popular videos)
    # Note: generate_recommendations should return Video model objects or similar structure
    recommendations_list = await generate_recommendations(db, user_id=user.id)

    # 3. Apply Pagination
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    paginated_videos = recommendations_list[start_index:end_index]

    # 4. Map the database results to the Pydantic schema

    return [
        VideoOut(
            id=v["id"],
            external_id=v["youtube_id"],
            title=v["title"],
            description="",
            category=""
            # অন্যান্য ফিল্ড...
        )
        for v in paginated_videos
    ]

