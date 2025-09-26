import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Video
from datetime import datetime



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# helper function to safely convert string to int
def safe_int_conversion(value):
    """Safely converts a string value to an integer, returning 0 on failure."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


# helper function to convert YouTube's ISO string to datetime object
def convert_published_at(datetime_str):
    """Converts YouTube's ISO 8601 string to a Python datetime object."""
    if not datetime_str:
        return None
    try:
        # YouTube uses 'Z' for UTC. Replacing it with '+00:00' for standard ISO format parsing.
        datetime_str = datetime_str.replace('Z', '+00:00')
        return datetime.fromisoformat(datetime_str)
    except ValueError as e:
        logger.error(f"Failed to convert datetime string '{datetime_str}': {e}")
        return None


async def save_videos_to_db(db: AsyncSession, videos_data: list):
    if not videos_data:
        logger.info("No videos to save. Exiting.")
        return {"message": "No new videos to save."}

    new_video_count = 0

    for video_info in videos_data:
        # সমস্ত আইডি সোর্স থেকে youtube_id বের করে নিচ্ছি
        youtube_id = video_info.get("id") or video_info.get("youtube_id") or video_info.get("external_id")

        if not youtube_id:
            logger.warning("Skipping video without ID.")
            continue

        # Check if exists
        result = await db.execute(select(Video).where(Video.youtube_id == youtube_id))
        existing_video = result.scalars().first()

        if existing_video:
            logger.info(f"Video '{video_info.get('snippet', {}).get('title')}' already exists. Skipping.")
            continue

        # Snippet এবং Statistics ডেটা সহজেই অ্যাক্সেস করার জন্য
        snippet = video_info.get("snippet", {})
        statistics = video_info.get("statistics", {})

        try:

            new_video = Video(
                youtube_id=youtube_id,
                title=snippet.get("title", "Untitled"),
                description=snippet.get("description", ""),

                # 🛠️ publishedAt স্ট্রিং কে datetime অবজেক্টে কনভার্ট করা হলো
                published_at=convert_published_at(snippet.get("publishedAt")),

                channel_title=snippet.get("channelTitle"),
                category=snippet.get("categoryId"),

                # 🛠️ Statistics স্ট্রিং কে Integer এ কনভার্ট করা হলো
                view_count=safe_int_conversion(statistics.get("viewCount")),
                like_count=safe_int_conversion(statistics.get("likeCount")),
                comment_count=safe_int_conversion(statistics.get("commentCount")),
            )

            db.add(new_video)
            new_video_count += 1
            logger.info(f"Adding video: {new_video.title}")

        except Exception as e:
            logger.error(f"Error creating video object for {snippet.get('title')}: {e}")
            continue

    try:
        await db.commit()
        logger.info(f"Successfully saved {new_video_count} new videos to the database.")
        return {"message": f"{new_video_count} videos saved successfully."}
    except Exception as e:
        await db.rollback()
        logger.error(f"An error occurred during commit: {e}")
        # এইখানে error return করা হলো
        return {"message": "Failed to save videos to the database.", "error": str(e)}