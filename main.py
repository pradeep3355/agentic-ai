from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api import chat

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n\nStarting app...\n\n")
    yield
    print("\n\nShutting down app...\n\n")


app = FastAPI(tittle=settings.PROJECT_NAME, version=settings.VERSION, lifespan=lifespan)


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
