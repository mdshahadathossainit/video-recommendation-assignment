from fastapi import FastAPI
from app.api.v1.routers import feed, youtube, fetch, recommendations, interactions


app = FastAPI(title="Video Recommendation Engine")

# Include routers for the API endpoints
app.include_router(feed.router, prefix="/api/v1")
app.include_router(youtube.router, prefix="/api/v1")
app.include_router(fetch.router, prefix="/api/v1")
app.include_router(recommendations.router, prefix="/api/v1")
app.include_router(interactions.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """
    Application startup event.
    Note: We are no longer using `Base.metadata.create_all` here,
    as Alembic handles database migrations.
    """
    # Placeholder for any future startup logic
    pass

@app.get("/health")
async def health():
    return {"status": "ok"}