# tests/test_feed.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_feed_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/feed", params={"username": "testuser", "page": 1, "page_size": 3})
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) == 3
