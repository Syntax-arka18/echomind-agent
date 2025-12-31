from dataclasses import dataclass

# ============================
# Emotion Profile Definition
# ============================

@dataclass(frozen=True)
class EmotionProfile:
    name: str
    speaking_rate: float
    pitch: float
    warmth: float
    expressiveness: float
    description: str


# ============================
# Final Emotion Set (Source of Truth)
# ============================

EMOTIONS = {

    "neutral_balanced": EmotionProfile(
        name="neutral_balanced",
        speaking_rate=1.0,
        pitch=1.0,
        warmth=0.5,
        expressiveness=0.5,
        description="Calm, neutral, default conversational tone"
    ),

    "reassuring_calm": EmotionProfile(
        name="reassuring_calm",
        speaking_rate=0.9,
        pitch=0.95,
        warmth=0.85,
        expressiveness=0.4,
        description="Used when user is anxious or uncertain"
    ),

    "empathetic_listener": EmotionProfile(
        name="empathetic_listener",
        speaking_rate=0.85,
        pitch=0.9,
        warmth=0.9,
        expressiveness=0.35,
        description="Validates emotions, listens more than speaks"
    ),

    "curious_thinking": EmotionProfile(
        name="curious_thinking",
        speaking_rate=0.95,
        pitch=1.05,
        warmth=0.6,
        expressiveness=0.7,
        description="AI is reasoning out loud and exploring ideas"
    ),

    "confident_guide": EmotionProfile(
        name="confident_guide",
        speaking_rate=1.05,
        pitch=1.1,
        warmth=0.6,
        expressiveness=0.6,
        description="Clear, authoritative, guiding the user"
    ),

    "focused_problem_solver": EmotionProfile(
        name="focused_problem_solver",
        speaking_rate=1.1,
        pitch=1.0,
        warmth=0.45,
        expressiveness=0.4,
        description="Task-oriented, logical, efficient"
    ),

    "encouraging_motivator": EmotionProfile(
        name="encouraging_motivator",
        speaking_rate=1.1,
        pitch=1.15,
        warmth=0.85,
        expressiveness=0.75,
        description="Boosts confidence and motivation"
    ),

    "excited_discovery": EmotionProfile(
        name="excited_discovery",
        speaking_rate=1.15,
        pitch=1.2,
        warmth=0.75,
        expressiveness=0.9,
        description="Celebrating insight or discovery"
    ),

    "gentle_correction": EmotionProfile(
        name="gentle_correction",
        speaking_rate=0.95,
        pitch=0.98,
        warmth=0.7,
        expressiveness=0.45,
        description="Corrects mistakes without discouragement"
    ),

    "reflective_thoughtful": EmotionProfile(
        name="reflective_thoughtful",
        speaking_rate=0.85,
        pitch=0.92,
        warmth=0.65,
        expressiveness=0.3,
        description="Used for introspection and deeper reasoning"
    )
}


# ============================
# Allowed Emotions (Whitelist)
# ============================

ALLOWED_EMOTIONS = list(EMOTIONS.keys())


# ============================
# Safe Emotion Access
# ============================

def get_emotion(emotion_name: str) -> EmotionProfile:
    """
    Safely retrieve an emotion profile.
    Falls back to neutral if invalid.
    """
    return EMOTIONS.get(emotion_name, EMOTIONS["neutral_balanced"])


# ============================
# Emotion Detection (REQUIRED)
# ============================

def detect_emotion(text: str) -> str:
    """
    Maps raw user text to a high-level emotion category.
    Keeps logic lightweight and deterministic.
    """

    t = text.lower()

    if any(word in t for word in ["worried", "nervous", "scared", "anxious"]):
        return "reassuring_calm"

    if any(word in t for word in ["sad", "lonely", "depressed", "cry"]):
        return "empathetic_listener"

    if any(word in t for word in ["confused", "thinking", "why", "how"]):
        return "curious_thinking"

    if any(word in t for word in ["guide", "teach", "help me"]):
        return "confident_guide"

    if any(word in t for word in ["fix", "solve", "error", "bug"]):
        return "focused_problem_solver"

    if any(word in t for word in ["motivate", "encourage", "confidence"]):
        return "encouraging_motivator"

    if any(word in t for word in ["wow", "amazing", "awesome"]):
        return "excited_discovery"

    if any(word in t for word in ["wrong", "mistake"]):
        return "gentle_correction"

    if any(word in t for word in ["reflect", "think deeply"]):
        return "reflective_thoughtful"

    return "neutral_balanced"


# ============================
# Optional Debug Helper
# ============================

def list_emotions():
    return [
        {
            "name": e.name,
            "description": e.description
        }
        for e in EMOTIONS.values()
    ]
