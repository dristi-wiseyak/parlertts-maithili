from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.endpoints import router as api_router
from app.core.config import settings
from app.core import constants as log_msg
from app.core.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(log_msg.SERVER_STARTUP)
    yield
    logger.info(log_msg.SERVER_SHUTDOWN)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for converting text to speech using Wise multilingual TTS (Supports Maithili, Nepali, English, Hindi)",
    lifespan=lifespan
)

app.include_router(api_router, prefix="")

@app.get("/", include_in_schema=False)
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "message": "Welcome to Wise multilingual TTS API. See /docs for usage."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=5555, reload=True)