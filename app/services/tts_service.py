
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
        
        logger.info(log_msg.TTS_MODEL_INIT.format(settings.MODEL_ID, self.device))
        self._load_model()

    def _load_model(self):
        try:
            logger.info(log_msg.TTS_MODEL_LOAD_START)
            
            self.model = ParlerTTSForConditionalGeneration.from_pretrained(settings.MODEL_ID).to(self.device)
            self.tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_ID)
            
            # As per user snippet, getting tokenizer for description from model config
            self.description_tokenizer = AutoTokenizer.from_pretrained(self.model.config.text_encoder._name_or_path)
            
            self.model.eval() # Set to eval mode as per snippet
            
            logger.info(log_msg.TTS_MODEL_LOAD_SUCCESS)
        except Exception as e:
            logger.error(log_msg.TTS_MODEL_LOAD_FAIL.format(str(e)))
            raise e

    def generate_audio(self, text: str) -> io.BytesIO:
        """
        Generates audio for the given text using the hardcoded description from settings.
        
        Args:
            text (str): The input text to synthesize.
            
        Returns:
            io.BytesIO: A buffer containing the generated WAV audio.
            
        Raises:
            ValueError: If text is empty.
            Exception: If generation fails.
        """
        logger.info(log_msg.TTS_PROCESSING_START.format(text[:50]))
        
        if not text:
             logger.warning(log_msg.WARN_EMPTY_TEXT)
             raise ValueError("Text cannot be empty")

        try:
            description = settings.DESCRIPTION
            
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
