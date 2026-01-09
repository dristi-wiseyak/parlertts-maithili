# Log Messages
SERVER_STARTUP = "Server starting up..."
SERVER_SHUTDOWN = "Server shutting down..."
STARTUP_FAILURE = "Startup failure: {}"

# TTS (Adapted from ASR templates provided)
TTS_MODEL_INIT = "Initializing model: {} on device: {}"
TTS_MODEL_LOAD_START = "Loading model (this might trigger internal download)..."
TTS_MODEL_LOAD_SUCCESS = "Model loaded successfully."
TTS_MODEL_LOAD_FAIL = "Failed to load model: {}"
TTS_PROCESSING_START = "Processing text: {}"
TTS_INFERENCE_FAIL = "Inference failed: {}"

# API Errors
ERR_TTS_MODEL_NOT_FOUND = "TTS Model requested but not found in registry."
ERR_INTERNAL_PROCESSING = "Internal processing error."

# Metrics
WARN_EMPTY_TEXT = "Received empty text. Returning error."

# Generic Entry/Exit
LOG_ENTRY = "Entry: {} | Args: {}"
LOG_EXIT = "Exit: {} | Success"
LOG_ERROR = "Error: {} | Message: {}"