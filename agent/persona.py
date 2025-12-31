from dataclasses import dataclass
from typing import Optional

# ============================
# Persona Profile Definition
# ============================

@dataclass(frozen=True)
class PersonaProfile:
    name: str
    base_tone: str
    vocabulary_style: str
    verbosity: float
    default_emotion: str
    description: str


# ============================
# Final Persona Set (Source of Truth)
# ============================

PERSONAS = {

    "mentor": PersonaProfile(
        name="mentor",
        base_tone="calm_authoritative",
        vocabulary_style="clear_structured",
        verbosity=0.85,
        default_emotion="confident_guide",
        description="A knowledgeable mentor who explains patiently and clearly"
    ),

    "friend": PersonaProfile(
        name="friend",
        base_tone="warm_casual",
        vocabulary_style="simple_friendly",
        verbosity=1.1,
        default_emotion="reassuring_calm",
        description="A friendly peer who listens, supports, and reassures"
    ),

    "coach": PersonaProfile(
        name="coach",
        base_tone="energetic_motivational",
        vocabulary_style="direct_action_oriented",
        verbosity=0.9,
        default_emotion="encouraging_motivator",
        description="A motivating coach who pushes the user toward action"
    ),

    "expert": PersonaProfile(
        name="expert",
        base_tone="precise_professional",
        vocabulary_style="technical_concise",
        verbosity=0.75,
        default_emotion="focused_problem_solver",
        description="An expert who provides accurate, efficient, factual answers"
    ),

    "listener": PersonaProfile(
        name="listener",
        base_tone="soft_supportive",
        vocabulary_style="minimal_validating",
        verbosity=0.6,
        default_emotion="empathetic_listener",
        description="A quiet listener who validates feelings without directing"
    ),

    "storyteller": PersonaProfile(
        name="storyteller",
        base_tone="expressive_engaging",
        vocabulary_style="illustrative_narrative",
        verbosity=1.2,
        default_emotion="excited_discovery",
        description="An engaging storyteller who explains ideas through examples"
    )
}


# ============================
# Allowed Personas (Whitelist)
# ============================

ALLOWED_PERSONAS = list(PERSONAS.keys())


# ============================
# Safe Persona Access
# ============================

def get_persona(persona_name: str) -> PersonaProfile:
    """
    Safely retrieve a persona profile.
    Falls back to mentor if invalid.
    """
    return PERSONAS.get(persona_name, PERSONAS["mentor"])


# ============================
# Optional Debug Helper
# ============================

def list_personas():
    return [
        {
            "name": p.name,
            "description": p.description
        }
        for p in PERSONAS.values()
    ]


# ============================
# Emotion → Persona Alignment
# ============================

EMOTION_TO_PERSONA = {
    "confident_guide": "mentor",
    "reassuring_calm": "friend",
    "encouraging_motivator": "coach",
    "focused_problem_solver": "expert",
    "empathetic_listener": "listener",
    "excited_discovery": "storyteller",
}


# ============================
# BACKWARD-COMPATIBLE PERSONA SWITCH
# ============================

def detect_persona_switch(
    user_text: str,
    current_persona: str = "mentor",
    detected_emotion: Optional[str] = None
) -> str:
    """
    Detects whether persona should switch based on emotion or user intent.
    Safe, rule-based, backward compatible.
    """

    # 0. Emotion-driven persona (if emotion system is active)
    if detected_emotion in EMOTION_TO_PERSONA:
        return EMOTION_TO_PERSONA[detected_emotion]

    text = user_text.lower()

    # 1. Strong emotional distress → listener
    distress_keywords = [
        "anxious", "overwhelmed", "sad", "stressed", "worried",
        "depressed", "nervous", "afraid", "panic", "burned out"
    ]
    if any(word in text for word in distress_keywords):
        return "listener"

    # 2. Motivation / pushing forward → coach
    coach_keywords = [
        "motivate", "push me", "discipline", "goals", "routine",
        "improve myself", "be productive"
    ]
    if any(word in text for word in coach_keywords):
        return "coach"

    # 3. Technical / deep accuracy → expert
    expert_keywords = [
        "exactly", "technically", "in detail", "precisely",
        "architecture", "optimize", "best practice"
    ]
    if any(word in text for word in expert_keywords):
        return "expert"

    # 4. Casual / friendly conversation → friend
    friend_keywords = [
        "chat", "talk", "hey", "how are you", "casual", "just talking"
    ]
    if any(word in text for word in friend_keywords):
        return "friend"

    # 5. Stories / explanations with examples → storyteller
    storyteller_keywords = [
        "story", "example", "explain like", "walk me through"
    ]
    if any(word in text for word in storyteller_keywords):
        return "storyteller"

    # Default: keep current persona
    return current_persona
