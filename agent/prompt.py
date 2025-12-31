from agent.emotion import ALLOWED_EMOTIONS
from agent.persona import PersonaProfile


# ============================
# SYSTEM PROMPT BUILDER
# ============================

def build_system_prompt(persona: PersonaProfile) -> str:
    """
    Builds the system-level instruction for the LLM.
    This defines WHO the AI is and HOW it should speak.
    """

    return f"""
You are a voice-first conversational AI.

Persona:
- Name: {persona.name}
- Description: {persona.description}
- Base tone: {persona.base_tone}
- Vocabulary style: {persona.vocabulary_style}

Rules:
- Speak naturally, as if talking to a human.
- Use spoken language, not text-chat language.
- Keep responses concise and clear.
- Never mention persona, emotions, or internal reasoning.
- Never include markdown, bullet points, or emojis.
"""


# ============================
# USER PROMPT BUILDER (STRICT JSON)
# ============================

def build_user_prompt(user_text: str) -> str:
    """
    Instructs the LLM to:
    1. Infer emotional need from text
    2. Select ONE emotion from whitelist
    3. Respond in STRICT JSON only
    """

    return f"""
User message:
"{user_text}"

Task:
1. Understand the user's intent and emotional need.
2. Choose ONE emotion strictly from this list:
{ALLOWED_EMOTIONS}

3. Write a natural spoken reply.

Output format:
Return ONLY valid JSON.
Do NOT include explanations, markdown, or extra text.

STRICT JSON SCHEMA:
{{
  "reply": "<spoken response>",
  "emotion": "<one emotion from the allowed list>"
}}
"""


# ============================
# FULL PROMPT ASSEMBLER
# ============================

def build_full_prompt(user_text: str, persona: PersonaProfile) -> dict:
    """
    Returns a prompt object compatible with LLM APIs.
    """

    return {
        "system": build_system_prompt(persona),
        "user": build_user_prompt(user_text)
    }

# ============================
# MAIN PROMPT ENTRY POINT
# ============================

def build_prompt(
    user_text: str,
    context: str = "",
    persona_name: str = "mentor",
    emotion_name: str = "neutral_balanced"
) -> str:
    """
    Builds the final prompt sent to the language model.
    Minimal safe implementation.
    """

    prompt_parts = []

    if persona_name:
        prompt_parts.append(f"Persona: {persona_name}")

    if emotion_name:
        prompt_parts.append(f"Emotion: {emotion_name}")

    if context:
        prompt_parts.append("Conversation context:")
        prompt_parts.append(context)

    prompt_parts.append("User:")
    prompt_parts.append(user_text)

    prompt_parts.append("AI:")

    return "\n".join(prompt_parts)
