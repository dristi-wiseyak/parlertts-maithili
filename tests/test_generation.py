
import requests
import json
import time

def test_health():
    print("Testing Health Endpoint...")
    try:
        response = requests.get("http://localhost:8000/v1/health")
        if response.status_code == 200:
            print("Health check passed!")
            return True
        else:
            print(f"Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"Health check failed with error: {e}")
        return False

def test_tts():
    print("Testing TTS Endpoint...")
    url = "http://localhost:8000/v1/tts"
    payload = {
        "text": "अहां केना छी?",
        "description": "A female speaker speaks Maithili in a normal voice."
    }
    try:
        start_time = time.time()
        response = requests.post(url, json=payload, stream=True)
        if response.status_code == 200:
            with open("test_output.wav", "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f"TTS generation passed! Audio saved to test_output.wav. Time taken: {time.time() - start_time:.2f}s")
            return True
        else:
            print(f"TTS generation failed: {response.text}")
            return False
    except Exception as e:
        print(f"TTS generation failed with error: {e}")
        return False

if __name__ == "__main__":
    if test_health():
        test_tts()
