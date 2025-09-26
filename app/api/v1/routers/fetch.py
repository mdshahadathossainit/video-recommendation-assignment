from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.fetcher import save_videos_to_db

from app.db.database import get_db as get_async_db
from app.services.external_api import fetch_most_popular_videos
import logging
from typing import Any  # Add Any for type hint flexibility

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/fetch-videos")
# Note: The router function remains 'async' because database operations are async.
async def fetch_videos(db: AsyncSession = Depends(get_async_db)) -> dict[str, Any]:
    """
    API endpoint to manually trigger the fetching and saving of popular YouTube videos.
    """
    try:
        logger.info("Starting video fetching process...")


        videos_data = fetch_most_popular_videos()

        # Check for error (videos_data will be a dict if an error occurred)
        if isinstance(videos_data, dict) and "error" in videos_data:
            logger.error(f"Error fetching videos from YouTube API: {videos_data['error']}")
            return {"message": "Error fetching videos from YouTube API.", "error": videos_data["error"]}

        # Check for empty list (videos_data will be a list if successful but empty)
        if not videos_data:
            logger.info("No videos returned from API. Nothing to save.")
            return {"message": "No videos found to save."}

        # save_videos_to_db is an async function, so 'await' is mandatory here.
        result = await save_videos_to_db(db, videos_data)
        return result
    except Exception as e:
        logger.error(f"An unexpected error occurred during fetch process: {e}")
        return {"message": "An unexpected error occurred.", "error": str(e)}