# app/db/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# ❌ DELETE: from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_settings


# Settings লোড করুন
settings = get_settings()





# 2. Database Engine:
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
)


# 3. Session Local:
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# 4. Dependency:
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session