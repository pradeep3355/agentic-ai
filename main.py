from fastapi import FastAPI, status
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api import chat


# Keep one FastAPI instance
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n\nStarting app with Gunicorn and Uvicorn workers...\n")
    print(f"Database connection: {settings.DATABASE_URL}")
    yield
    print("\n\nShutting down app...\n")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# Health check endpoint


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint that includes container information"""
    import os

    container_id = os.environ.get("HOSTNAME", "unknown")
    container_name = os.environ.get("CONTAINER_NAME", "unknown")

    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "container": {
            "id": container_id,
            "name": container_name,
        },
    }


app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["Chat"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        reload=settings.RELOAD,
    )
