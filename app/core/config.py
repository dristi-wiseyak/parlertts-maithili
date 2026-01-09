
import os
import torch
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Maithili Parler TTS API"
    VERSION: str = "1.0.0"
    MODEL_ID: str = "ai4bharat/indic-parler-tts"
    # Robust device detection
    DEVICE: str = "cuda:0" if torch.cuda.is_available() else "cpu"
    # Hardcoded description as requested
    DESCRIPTION: str = "A Maithili female speaker speaks Maithili delivers a slightly expressive speech with a fast speed and pitch."

    class Config:
        env_file = ".env"

settings = Settings()
