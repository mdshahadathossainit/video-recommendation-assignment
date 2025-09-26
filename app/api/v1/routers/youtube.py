# app/api/v1/routers/youtube.py
import logging
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.api.v1.schemas import VideoOut
from app.services.external_api import fetch_most_popular_videos
from app.db.database import get_db  # unified db dependency
from app.db.fetcher import save_videos_to_db
from app.config import get_settings, Settings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/youtube/most-popular", response_model=List[VideoOut])
async def fetch_and_save_videos(
        db: AsyncSession = Depends(get_db),
        settings: Settings = Depends(get_settings),
        flic_token: Optional[str] = Header(None, convert_underscores=False)
):
    if settings.FLIC_TOKEN and not flic_token:
        raise HTTPException(status_code=401, detail="Flic-Token header missing")

    videos_data = await fetch_most_popular_videos()
    if isinstance(videos_data, dict) and "error" in videos_data:
        raise HTTPException(status_code=502, detail="Error fetching videos from YouTube API")

    if not videos_data:
        raise HTTPException(status_code=404, detail="No videos found from API")

    result = await save_videos_to_db(db, videos_data)
    return {"message": "Videos fetched and saved successfully.", "result": result}
