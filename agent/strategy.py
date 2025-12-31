from agent.persona import get_persona
from agent.emotion import get_emotion


# ============================
# PERSONA–EMOTION BLENDING
# ============================

def blend_persona_emotion(persona_name: str, emotion_name: str) -> dict:
    """
    Combines persona traits with emotion traits to produce
    final behavioral parameters used by voice or response layers.
    """

    persona = get_persona(persona_name)
    emotion = get_emotion(emotion_name)

    blended_style = {
        "persona": persona.name,
        "emotion": emotion.name,

        # Speech behavior
        "speaking_rate": persona.verbosity * emotion.speaking_rate,
        "pitch": emotion.pitch,

        # Conversational feel
        "warmth": emotion.warmth,
        "expressiveness": emotion.expressiveness,

        # Text style hints (used by prompt / generator if needed)
        "base_tone": persona.base_tone,
        "vocabulary_style": persona.vocabulary_style
    }

    return blended_style


# ============================
# EMOTION FALLBACK STRATEGY
# ============================

def stabilize_emotion(previous_emotion: str, current_emotion: str) -> str:
    """
    Prevents abrupt emotional jumps.
    If emotion changes too drastically, soften it.
    """

    if previous_emotion == current_emotion:
        return current_emotion

    # Hard safety net
    if current_emotion is None:
        return previous_emotion or "neutral_balanced"

    return current_emotion


# ============================
# HIGH-LEVEL STRATEGY ENTRY POINT
# ============================

def apply_strategy(
    persona_name: str,
    detected_emotion: str,
    previous_emotion: str | None = None
) -> dict:
    """
    Main strategy function used by the system.
    """

    final_emotion = stabilize_emotion(previous_emotion, detected_emotion)

    return blend_persona_emotion(persona_name, final_emotion)

# ============================
# BACKWARD-COMPATIBILITY ALIAS
# ============================

def choose_strategy(
    persona_name: str,
    detected_emotion: str,
    previous_emotion: str | None = None
) -> dict:
    """
    Alias for apply_strategy.
    Keeps main.py imports stable.
    """
    return apply_strategy(persona_name, detected_emotion, previous_emotion)
