# agent/generator.py

import json
from agent.prompt import build_full_prompt
from agent.persona import get_persona
from agent.emotion import ALLOWED_EMOTIONS


# ============================
# SAFE MOCK LLM (REPLACE LATER)
# ============================

def call_llm(system_prompt: str, user_prompt: str) -> str:
    """
    TEMP SAFE MOCK.
    Must return JSON string.
    """

    return json.dumps({
        "reply": "I’m here with you. Take a slow breath. You don’t have to rush.",
        "emotion": "reassuring_calm"
    })


# ============================
# JSON PARSER
# ============================

def parse_llm_output(raw_output: str) -> tuple[str, str]:
    try:
        data = json.loads(raw_output)

        reply = data.get("reply", "").strip()
        emotion = data.get("emotion", "").strip()

        if not reply:
            raise ValueError("Empty reply")

        if emotion not in ALLOWED_EMOTIONS:
            emotion = "neutral_balanced"

        return reply, emotion

    except Exception:
        return (
            "I’m here with you. Let’s take this step by step.",
            "neutral_balanced"
        )


# ============================
# FULL RESPONSE PIPELINE
# ============================

def generate_response(user_text: str, persona_name: str) -> tuple[str, str]:
    persona = get_persona(persona_name)

    prompt = build_full_prompt(user_text, persona)

    raw_output = call_llm(
        system_prompt=prompt["system"],
        user_prompt=prompt["user"]
    )

    return parse_llm_output(raw_output)


# ============================
# 🔥 FUNCTION USED BY main.py
# ============================

def generate_reply(prompt: str) -> str:
    """
    This is what main.py expects.
    It MUST return ONLY clean text for ElevenLabs.
    """

    reply, _ = parse_llm_output(call_llm("", prompt))
    return reply
