from fastapi import FastAPI
from pydantic import BaseModel

from agent.memory import load_messages, save_messages
from agent.emotion import detect_emotion
from agent.strategy import choose_strategy
from agent.prompt import build_prompt
from agent.generator import generate_reply
from config import MAX_HISTORY

app = FastAPI()

class AgentRequest(BaseModel):
    session_id: str
    user_text: str

@app.post("/agent/respond")
def respond(req: AgentRequest):
    messages = load_messages(req.session_id)

    messages.append({"role": "user", "content": req.user_text})

    recent = messages[-MAX_HISTORY:]
    history = "\n".join(f"{m['role']}: {m['content']}" for m in recent)

    emotion = detect_emotion(req.user_text)
    strategy = choose_strategy(emotion, len(messages))

    prompt = build_prompt(history, emotion, strategy)
    reply = generate_reply(prompt)

    if strategy == "interrupt":
        reply = "Hey—can I pause you for a second? " + reply

    messages.append({"role": "agent", "content": reply})
    save_messages(req.session_id, messages)

    return {
        "reply": reply,
        "emotion": emotion,
        "strategy": strategy
    }
