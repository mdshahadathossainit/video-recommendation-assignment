from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.db.crud import get_or_create_user, save_user_interaction # save_user_interaction এখন এখানে ইমপোর্ট করা হয়েছে
from app.db.models import Video # Video মডেল এখানে ইমপোর্ট করা হয়েছে
from app.api.v1.schemas import InteractionIn # InteractionIn Pydantic মডেলটি schemas.py থেকে আসছে

router = APIRouter()

@router.post("/interactions", summary="Record a user interaction with a video (e.g., WATCHED, LIKED)")
async def record_interaction(
    interaction_data: InteractionIn,
    db: AsyncSession = Depends(get_db)
):
    # 1. ইউজার আইডি খুঁজে বের করা (বা নতুন ইউজার তৈরি করা)
    user = await get_or_create_user(db, username=interaction_data.username)

    # 2. youtube_id ব্যবহার করে ডেটাবেসের ভিডিও ID খুঁজে বের করা
    video_result = await db.execute(select(Video).where(Video.youtube_id == interaction_data.youtube_id))
    video = video_result.scalars().first()

    if not video:
        raise HTTPException(status_code=404, detail=f"Video with youtube_id '{interaction_data.youtube_id}' not found.")

    # 3. ইন্টারেকশন সেভ করা
    await save_user_interaction(
        db,
        user_id=user.id,
        video_id=video.id,
        interaction_type=interaction_data.interaction_type
    )

    return {"message": "Interaction recorded successfully."}