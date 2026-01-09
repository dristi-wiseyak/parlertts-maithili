from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import StreamingResponse

from app.services.tts_service import tts_service
from app.core import constants as log_msg
from app.core.logging import logger

router = APIRouter()

@router.post("/tts", summary="Generate TTS", description="Generate audio from text using Indic Parler TTS (Maithili)")
async def generate_tts(text: str = Form(..., description="Text to synthesize in Maithili")):
    """
    Generate audio from text.
    """
    logger.info(log_msg.LOG_ENTRY.format("generate_tts", f"text_len={len(text)}"))
    try:
        audio_buffer = tts_service.generate_audio(text)
        
        return StreamingResponse(
            audio_buffer, 
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=output.wav"}
        )
    except Exception as e:
        logger.error(log_msg.LOG_ERROR.format("generate_tts", str(e)))
        raise HTTPException(status_code=500, detail=log_msg.ERR_INTERNAL_PROCESSING)

@router.get("/health", summary="Health Check")
async def health_check():
    return {"status": "ok", "message": "Service is running"}
