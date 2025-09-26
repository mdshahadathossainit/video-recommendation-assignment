# alembic/env.py

import sys
import os
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

# ========================
# Project path setup
# ========================
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

# ========================
# Import Base and Settings
# ========================
# ❌ DELETE: from app.db.database import Base
# ✅ FIX: Base এখন app/db/base.py তে আছে, তাই সেখান থেকে ইমপোর্ট করুন।
from app.db.base import Base

from app.config import get_settings
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get application settings
settings = get_settings()

# ✅ FIX: আপনার models ফাইলগুলি লোড করুন যাতে Base.metadata সব টেবিল জানে।
# এই কাজটি database.py তে করলেও Alembic এর জন্য এখানে নিশ্চিত করা ভালো।
from app.db import models


# ========================
# Alembic Config
# ========================
config = context.config

# Logging configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata = Base.metadata


# ========================
# Database URL
# ========================
def get_url():
    """
    Retrieves the DATABASE_URL from application settings and strips the
    async driver (+aiosqlite) when running synchronous Alembic operations.
    This guarantees path consistency with the application.
    """

    url = settings.DATABASE_URL


    if url and "+" in url:
        # Split the driver part (e.g., 'sqlite+aiosqlite') from the rest of the URL.
        driver_part, rest_of_url = url.split("://", 1)
        base_driver = driver_part.split("+")[0]
        return f"{base_driver}://{rest_of_url}"

    return url


# ========================
# Offline migrations
# ========================
def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ========================
# Online migrations
# ========================
def run_migrations_online():
    # create_engine is synchronous, so we use the modified URL from get_url()
    connectable = create_engine(
        get_url(),
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# ========================
# Run migrations
# ========================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()