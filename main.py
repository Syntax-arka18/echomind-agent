from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path

from config import MAX_HISTORY, DEFAULT_PERSONA
from agent.memory import load_session, save_session
from agent.emotion import detect_emotion
from agent.strategy import choose_strategy
from agent.persona import detect_persona_switch
from agent.prompt import build_prompt
from agent.generator import generate_reply
from agent.voice import speak

# =========================
# APP SETUP
# =========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ABSOLUTE AUDIO PATH (SINGLE SOURCE OF TRUTH)
# =========================
BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "audio"
AUDIO_DIR.mkdir(exist_ok=True)

# =========================
# REQUEST MODELS
# =========================
class AgentRequest(BaseModel):
    session_id: str
    user_text: str

class FrontendRequest(BaseModel):
    text: str
    persona: str | None = None

# =========================
# CORE AGENT ENDPOINT
# =========================
@app.post("/agent/respond")
def respond(req: AgentRequest):
    session = load_session(req.session_id)
    messages = session["messages"]
    persona = session["persona"] or DEFAULT_PERSONA

    new_persona = detect_persona_switch(req.user_text)
    if new_persona:
        persona = new_persona
        reply = f"Got it. I’ll speak to you like a {persona} now."

        messages.append({"role": "agent", "content": reply})
        session["persona"] = persona
        session["messages"] = messages
        save_session(req.session_id, session)

        return {
            "reply": reply,
            "persona": persona,
            "strategy": "switch"
        }

    messages.append({"role": "user", "content": req.user_text})

    recent = messages[-MAX_HISTORY:]
    history = "\n".join(f"{m['role']}: {m['content']}" for m in recent)

    emotion = detect_emotion(req.user_text)
    strategy = choose_strategy(emotion, len(messages))

    prompt = build_prompt(history, emotion, strategy, persona)
    reply = generate_reply(prompt)

    if not reply or not reply.strip():
        reply = "I’m listening. Please continue."

    messages.append({"role": "agent", "content": reply})

    session["messages"] = messages
    session["persona"] = persona
    save_session(req.session_id, session)

    return {
        "reply": reply,
        "emotion": emotion,
        "strategy": strategy,
        "persona": persona
    }

# =========================
# CHAT + VOICE ENDPOINT (FIXED)
# =========================
@app.post("/chat")
def chat(req: FrontendRequest):
    session_id = "frontend-demo"

    session = load_session(session_id)
    messages = session["messages"]
    persona = req.persona or session["persona"] or DEFAULT_PERSONA

    messages.append({"role": "user", "content": req.text})

    recent = messages[-MAX_HISTORY:]
    history = "\n".join(f"{m['role']}: {m['content']}" for m in recent)

    emotion = detect_emotion(req.text)
    strategy = choose_strategy(emotion, len(messages))

    prompt = build_prompt(history, emotion, strategy, persona)
    reply = generate_reply(prompt)

    if not reply or not reply.strip():
        reply = "I’m here with you. Please continue."

    audio_path = speak(
        text=reply,
        persona_name=persona,
        detected_emotion=emotion,
        previous_emotion=None
    )

    messages.append({"role": "agent", "content": reply})

    session["messages"] = messages
    session["persona"] = persona
    save_session(session_id, session)

    return {
        "reply": reply,
        "emotion": emotion,
        "persona": persona,
        # ✅ SAFE AUDIO URL
        "audio_url": f"/audio/{audio_path.name}" if audio_path else None
    }

# =========================
# AUDIO SERVING
# =========================
@app.get("/audio/{filename}")
def get_audio(filename: str):
    file_path = AUDIO_DIR / filename

    if not file_path.exists():
        return {"error": "Audio file not found"}

    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename=filename
    )
