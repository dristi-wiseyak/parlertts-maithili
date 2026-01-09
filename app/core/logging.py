import logging
import sys
from typing import Any

class CustomFormatter(logging.Formatter):
    """
    Custom formatter to output logs in a clean format.
    """
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    def format(self, record: Any) -> str:
        log_fmt = self.format_str
        if record.levelno == logging.DEBUG:
            log_fmt = self.grey + self.format_str + self.reset
        elif record.levelno == logging.INFO:
            log_fmt = self.grey + self.format_str + self.reset
        elif record.levelno == logging.WARNING:
            log_fmt = self.yellow + self.format_str + self.reset
        elif record.levelno == logging.ERROR:
            log_fmt = self.red + self.format_str + self.reset
        elif record.levelno == logging.CRITICAL:
            log_fmt = self.bold_red + self.format_str + self.reset
        
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logging():
    """
    Setup logging configuration.
    """
    logger = logging.getLogger("maithili_tts")
    logger.setLevel(logging.DEBUG)
    
    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    
    # Avoid adding multiple handlers if setup is called multiple times
    if not logger.handlers:
        logger.addHandler(ch)

    # Silence noisy libraries
    logging.getLogger("transformers").setLevel(logging.ERROR)
    
    return logger

logger = setup_logging()