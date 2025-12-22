from fastapi import FastAPI
from pydantic import BaseModel

from config import MAX_HISTORY, DEFAULT_PERSONA
from agent.memory import load_session, save_session
from agent.emotion import detect_emotion
from agent.strategy import choose_strategy
from agent.persona import detect_persona_switch
from agent.prompt import build_prompt
from agent.generator import generate_reply
from agent.voice import shape_for_voice

app = FastAPI()

class AgentRequest(BaseModel):
    session_id: str
    user_text: str

@app.post("/agent/respond")
def respond(req: AgentRequest):
    session = load_session(req.session_id)
    messages = session["messages"]
    persona = session["persona"] or DEFAULT_PERSONA

    # Persona switch detection
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

    # Normal agent flow
    messages.append({"role": "user", "content": req.user_text})
    recent = messages[-MAX_HISTORY:]
    history = "\n".join(f"{m['role']}: {m['content']}" for m in recent)

    emotion = detect_emotion(req.user_text)
    strategy = choose_strategy(emotion, len(messages))

    prompt = build_prompt(history, emotion, strategy, persona)
    reply = shape_for_voice(generate_reply(prompt))

    if strategy == "interrupt":
        reply = "Hey—can I pause you for a second? " + reply

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
