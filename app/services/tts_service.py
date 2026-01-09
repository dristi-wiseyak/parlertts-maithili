import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import io
import numpy as np
from app.core.config import settings
from app.core import constants as log_msg
from app.core.logging import logger


class TTSService:
    def __init__(self):
        self.device = settings.DEVICE
        self.model = None
        self.tokenizer = None
        self.description_tokenizer = None
        
        # Lazy loading: Model is NOT loaded here. It creates the service quickly.
        # It will be loaded on the first request.
        logger.info("TTSService initialized. Model will be loaded lazily on first request.")

    def _load_model(self):
        """
        Loads the model. Safe to call multiple times (checks if already loaded).
        Tries to load from local cache first to support offline/cached usage.
        """
        if self.model is not None:
            return

        try:
            logger.info(log_msg.TTS_MODEL_LOAD_START)
            logger.info(log_msg.TTS_MODEL_INIT.format(settings.MODEL_ID, self.device))
            
            # 1. OPTIMIZATION: Try loading from local files first
            # This ensures we don't ping Hugging Face if we have the model "on device"
            try:
                logger.info("Attempting to load model from local cache...")
                self.model = ParlerTTSForConditionalGeneration.from_pretrained(
                    settings.MODEL_ID, 
                    local_files_only=True
                ).to(self.device)
                
                self.tokenizer = AutoTokenizer.from_pretrained(
                    settings.MODEL_ID, 
                    local_files_only=True
                )
                
                # Load description tokenizer from the internal config path
                self.description_tokenizer = AutoTokenizer.from_pretrained(
                    self.model.config.text_encoder._name_or_path, 
                    local_files_only=True
                )
                logger.info("Model loaded successfully from local cache.")

            except Exception as e:
                logger.info(f"Local load failed ({str(e)}). Downloading from Hugging Face Hub... (One-time process)")
                
                # 2. Fallback: Download from Hub (cache it for next time)
                self.model = ParlerTTSForConditionalGeneration.from_pretrained(
                    settings.MODEL_ID, 
                    use_auth_token=settings.HF_TOKEN
                ).to(self.device)
                
                self.tokenizer = AutoTokenizer.from_pretrained(
                    settings.MODEL_ID, 
                    use_auth_token=settings.HF_TOKEN
                )
                
                self.description_tokenizer = AutoTokenizer.from_pretrained(
                    self.model.config.text_encoder._name_or_path, 
                    use_auth_token=settings.HF_TOKEN
                )
                logger.info(log_msg.TTS_MODEL_LOAD_SUCCESS)

            self.model.eval()
            
        except Exception as e:
            logger.error(log_msg.TTS_MODEL_LOAD_FAIL.format(str(e)))
            # If loading fails, ensure we reset to None so we can retry later if needed
            self.model = None
            raise e

    def generate_audio(self, text: str, description: str) -> io.BytesIO:
        """
        Generates audio for the given text using the provided description.
        Automatically loads the model if it's the first request (Lazy Loading).
        """
        # Ensure model is loaded (Lazy check)
        if self.model is None:
            self._load_model()
            
        logger.info(log_msg.TTS_PROCESSING_START.format(text[:50]))
        
        if not text:
             logger.warning(log_msg.WARN_EMPTY_TEXT)
             raise ValueError("Text cannot be empty")

        try:
            # Tokenize description
            description_inputs = self.description_tokenizer(
                description, 
                return_tensors="pt"
            ).to(self.device)

            # Tokenize text
            prompt_inputs = self.tokenizer(
                text, 
                return_tensors="pt"
            ).to(self.device)

            # Generate audio
            with torch.no_grad():
                generation = self.model.generate(
                    input_ids=description_inputs.input_ids,
                    attention_mask=description_inputs.attention_mask,
                    prompt_input_ids=prompt_inputs.input_ids,
                    prompt_attention_mask=prompt_inputs.attention_mask,
                )
            
            audio_arr = generation.cpu().numpy().squeeze()
            
            # Save to BytesIO buffer
            buffer = io.BytesIO()
            sf.write(buffer, audio_arr, self.model.config.sampling_rate, format='WAV')
            buffer.seek(0)
            
            logger.info(log_msg.LOG_EXIT.format("generate_audio"))
            return buffer
        except Exception as e:
            logger.error(log_msg.TTS_INFERENCE_FAIL.format(str(e)))
            raise e

# Singleton instance
tts_service = TTSService()