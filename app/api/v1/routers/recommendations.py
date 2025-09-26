from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from app.db.database import get_db
from app.db.crud import get_or_create_user
from app.services.recommendation_logic import generate_recommendations

router = APIRouter()


@router.get(
    "/recommendations",
    response_model=List[Dict],
    summary="Get personalized video recommendations for a user"
)
async def get_user_recommendations(
        # Query parameter for username (e.g., /recommendations?username=test_user)
        username: str = Query(..., description="The username for whom to generate recommendations."),
        db: AsyncSession = Depends(get_db)
):
    """
    Fetches the most relevant videos for the specified user.

    If the username does not exist, a new user profile is created first.
    """

    # 1. Get or create the user
    user = await get_or_create_user(db, username=username)

    if not user:
        # Should not happen if get_or_create_user works, but good practice
        raise HTTPException(status_code=500, detail="Could not retrieve or create user.")

    # 2. Generate recommendations using the service logic
    recommendations = await generate_recommendations(db, user_id=user.id)

    if not recommendations:
        # If no videos exist in the database, return an error
        raise HTTPException(status_code=404, detail="No videos found to recommend.")

    return recommendations