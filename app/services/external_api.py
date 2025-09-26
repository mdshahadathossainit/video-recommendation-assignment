# app/services/external_api.py
from googleapiclient.discovery import build
from app.config import get_settings
import logging

settings = get_settings()
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

logger = logging.getLogger(__name__)

def get_youtube_client():
    try:
        if not settings.YOUTUBE_API_KEY:
            logger.error("YouTube API key is not set. Please check your .env file.")
            return None
        return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=settings.YOUTUBE_API_KEY)
    except Exception as e:
        logger.error(f"Error creating YouTube client: {e}")
        return None

def fetch_most_popular_videos(max_results: int = 50, region_code: str = "US"):
    youtube = get_youtube_client()
    if not youtube:
        return {"error": "YouTube client could not be created. API key might be missing or invalid."}
    try:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=max_results
        )
        response = request.execute()
        return response.get("items", [])
    except Exception as e:
        logger.error(f"Error fetching most popular videos: {e}")
        return {"error": str(e)}
