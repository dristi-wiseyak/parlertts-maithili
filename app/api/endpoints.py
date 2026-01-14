from fastapi import APIRouter, HTTPException, Form, Query
from fastapi.responses import StreamingResponse

from app.services.tts_service import tts_service
from app.core import constants as log_msg
from app.core.logging import logger
from app.core.enums import Language
from app.core.prompts import LANGUAGE_DESCRIPTIONS

router = APIRouter()

@router.post("/generate", summary="Generate TTS", description="Generate audio from text using Wise multilingual TTS")
async def generate_tts(
    text: str = Form(..., description="Text to synthesize"),
    language: str = Form(..., description="Language (e.g. maithili, nepali, english, hindi)")
):
    """
    Generate audio from text for the specified language.
    """
    normalized_lang = language.lower().strip()
    logger.info(log_msg.LOG_ENTRY.format("generate_tts", f"text_len={len(text)} lang={normalized_lang}"))
    
    try:
        # Validate and get description
        try:
            # Convert string input to Enum to lookup description
            lang_enum = Language(normalized_lang)
            description = LANGUAGE_DESCRIPTIONS[lang_enum]
        except ValueError:
            supported = ", ".join([l.value for l in Language])
            raise HTTPException(status_code=400, detail=f"Unsupported language: {language}. Supported: {supported}")

        audio_buffer = tts_service.generate_audio(text, description)
        
        return StreamingResponse(
            audio_buffer, 
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=output.wav"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(log_msg.LOG_ERROR.format("generate_tts", str(e)))
        raise HTTPException(status_code=500, detail=log_msg.ERR_INTERNAL_PROCESSING)

@router.get("/info", summary="System Information", description="Get available languages and model info")
async def get_info():
    return {
        "service": "Wise multilingual TTS",
        "languages": [lang.value for lang in Language],
        "descriptions": LANGUAGE_DESCRIPTIONS
    }

@router.get("/health", summary="Health Check")
async def health_check():
    return {"status": "ok", "message": "Service is running"}