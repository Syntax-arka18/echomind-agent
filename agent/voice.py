import os
import requests
from pathlib import Path
from datetime import datetime

from agent.strategy import apply_strategy

AUDIO_OUTPUT_DIR = Path("audio")
AUDIO_OUTPUT_DIR.mkdir(exist_ok=True)

# THIS voice is public + guaranteed
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

ELEVEN_TTS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

def speak(text: str, persona_name: str, detected_emotion: str, previous_emotion=None) -> Path:
    api_key = os.getenv("ELEVENLABS_API_KEY")

    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY missing")

    text = text.strip()
    if not text:
        raise RuntimeError("Empty text cannot be spoken")

    style = apply_strategy(
        persona_name=persona_name,
        detected_emotion=detected_emotion,
        previous_emotion=previous_emotion
    )

    payload = {
        "text": text[:4500],
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.6
        }
    }

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    r = requests.post(
        ELEVEN_TTS_URL,
        json=payload,
        headers=headers,
        timeout=30
    )

    if r.status_code != 200:
        raise RuntimeError(f"ElevenLabs error {r.status_code}: {r.text}")

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    output_file = AUDIO_OUTPUT_DIR / f"response_{timestamp}.mp3"

    with open(output_file, "wb") as f:
        f.write(r.content)

    return output_file
