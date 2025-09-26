from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.db.base import Base

class Video(Base):
    """
    SQLAlchemy model for storing video data.
    """
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=True)
    channel_title = Column(String, nullable=True)
    category = Column(String, nullable=True)
    tags = Column(JSON, nullable=True)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)

    def __repr__(self):
        return f"<Video(title='{self.title}', external_id='{self.external_id}')>"
