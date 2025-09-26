from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List

class VideoOut(BaseModel):
    id: int
    external_id: str
    title: str
    description: Optional[str]
    category: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class InteractionIn(BaseModel):
    username: str = Field(..., example="test_user", description="The username performing the interaction.")
    youtube_id: str = Field(..., example="Ma1x7ikpid8", description="The YouTube ID of the video being interacted with.")
    interaction_type: str = Field("WATCHED", example="WATCHED", description="Type of interaction (e.g., WATCHED, LIKED).")