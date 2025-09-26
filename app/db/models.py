from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

    recommendations = relationship(
        "Recommendation",
        back_populates="user"
    )

    interactions = relationship("UserInteraction", back_populates="user")


class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)

    youtube_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=True)
    channel_title = Column(String, nullable=True)
    category = Column(String, nullable=True)
    tags = Column(JSON, nullable=True)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)

    recommendations = relationship("Recommendation", back_populates="video")

    interactions = relationship("UserInteraction", back_populates="video")

    def __repr__(self):
        return f"<Video(title='{self.title}', youtube_id='{self.youtube_id}')>"


class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)

    score = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="recommendations")
    video = relationship("Video", back_populates="recommendations")

    def __repr__(self):
        return f"<Recommendation(user_id={self.user_id}, video_id={self.video_id}, score={self.score})>"



class UserInteraction(Base):
    __tablename__ = "user_interactions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    video_id = Column(Integer, ForeignKey("videos.id"), index=True, nullable=False)

    # Interaction type, e.g., 'WATCHED', 'LIKED', 'DISLIKED'
    interaction_type = Column(String, default="WATCHED")

    # When the interaction occurred
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="interactions")
    video = relationship("Video", back_populates="interactions")