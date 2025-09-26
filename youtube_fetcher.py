import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import json

# Load environment variables from .env file
load_dotenv()

# Get the YouTube API key from environment variables
api_key = os.getenv("YOUTUBE_API_KEY")

if not api_key:
    raise ValueError("YOUTUBE_API_KEY is not set in the .env file")

# Define the YouTube API service name and version
api_service_name = "youtube"
api_version = "v3"


def get_youtube_client():
    """
    Creates and returns a YouTube API client.
    Returns:
        googleapiclient.discovery.Resource: A YouTube API resource object.
    """
    try:
        youtube_client = build(
            api_service_name,
            api_version,
            developerKey=api_key
        )
        return youtube_client
    except Exception as e:
        print(f"Error creating YouTube API client: {e}")
        return None


def fetch_popular_videos(region_code="US", max_results=10):
    """
    Fetches a list of popular videos for a given region.

    Args:
        region_code (str): The two-letter country code for the region.
        max_results (int): The maximum number of videos to return.

    Returns:
        list: A list of dictionaries, where each dictionary contains video data.
    """
    youtube_client = get_youtube_client()
    if not youtube_client:
        return []

    try:
        request = youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=max_results
        )
        response = request.execute()

        videos_data = []
        for item in response.get("items", []):
            video_info = {
                "youtube_id": item["id"],
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "published_at": item["snippet"]["publishedAt"],
                "channel_id": item["snippet"]["channelId"],
                "channel_title": item["snippet"]["channelTitle"],
                "view_count": item["statistics"].get("viewCount", 0),
                "like_count": item["statistics"].get("likeCount", 0),
                "comment_count": item["statistics"].get("commentCount", 0)
            }
            videos_data.append(video_info)

        return videos_data

    except Exception as e:
        print(f"An error occurred while fetching popular videos: {e}")
        return []


if __name__ == "__main__":
    # Example usage
    print("Fetching top 10 popular videos from the US...")
    popular_videos = fetch_popular_videos(region_code="US", max_results=10)

    if popular_videos:
        print(f"Successfully fetched {len(popular_videos)} videos.")
        # Print the data in a human-readable format
        print(json.dumps(popular_videos, indent=4))
    else:
        print("Failed to fetch videos.")
