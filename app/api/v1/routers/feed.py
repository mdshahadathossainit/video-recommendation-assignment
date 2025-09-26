# app/api/v1/routers/feed.py
import logging
from fastapi import APIRouter, Depends, Query, Header, HTTPException
from typing import Optional, List
from app.api.v1.schemas import VideoOut
from app.services.recommender import get_personalized_feed
from app.config import get_settings, Settings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/feed", response_model=List[VideoOut])
async def feed(
    settings: Settings = Depends(get_settings),
    username: str = Query(..., min_length=1),
    project_code: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    flic_token: Optional[str] = Header(None, convert_underscores=False)
):
    if settings.FLIC_TOKEN and not flic_token:
        raise HTTPException(status_code=401, detail="Flic-Token header missing")

    results = await get_personalized_feed(username=username, project_code=project_code, page=page, page_size=page_size)
    return results
