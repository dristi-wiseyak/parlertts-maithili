
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
# git is needed for pip install git+...
# build-essential for compiling some python extensions
# ffmpeg might be needed by soundfile/audiotools
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Create a non-root user (optional but good practice, skipping for simplicity in ML containers sometimes, but let's stick to root for now unless requested otherwise to avoid permission issues with model cache directories)
# To avoid permission issues with HuggingFace cache, we can set the transformers cache dir
ENV HF_HOME=/tmp/huggingface

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
