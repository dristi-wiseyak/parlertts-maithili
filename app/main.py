from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.core.config import settings
from app.core import constants as log_msg
from app.core.logging import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for converting text to speech using Indic Parler TTS (Maithili)"
)

app.include_router(api_router, prefix="")

@app.on_event("startup")
async def startup_event():
    logger.info(log_msg.SERVER_STARTUP)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(log_msg.SERVER_SHUTDOWN)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=5555, reload=True)
