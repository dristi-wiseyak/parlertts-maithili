import os
import torch
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Wise TTS API"
    VERSION: str = "1.0.0"
    MODEL_ID: str = "ai4bharat/indic-parler-tts"
    DEVICE: str = "cuda:0" if torch.cuda.is_available() else "cpu"
    DESCRIPTION: str = "A Maithili female speaker speaks Maithili delivers a slightly expressive speech with a fast speed and pitch."
    HF_TOKEN: str | None = None  
    HF_HOME: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()