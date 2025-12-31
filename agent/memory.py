from collections import deque
from dataclasses import dataclass
from typing import Optional
import json
import os


# ============================
# MEMORY RECORD STRUCTURE
# ============================

@dataclass
class MemoryTurn:
    user_text: str
    ai_reply: str
    emotion: str


# ============================
# CONVERSATION MEMORY
# ============================

class ConversationMemory:
    """
    Stores short-term conversational memory.
    """

    def __init__(self, max_turns: int = 6):
        self.max_turns = max_turns
        self.turns = deque(maxlen=max_turns)

    def add_turn(self, user_text: str, ai_reply: str, emotion: str):
        self.turns.append(
            MemoryTurn(
                user_text=user_text,
                ai_reply=ai_reply,
                emotion=emotion
            )
        )

    def get_recent_context(self) -> str:
        """
        Returns a compact text summary of recent conversation.
        Used to maintain continuity.
        """
        context = []
        for turn in self.turns:
            context.append(
                f"User: {turn.user_text}\nAI: {turn.ai_reply}"
            )
        return "\n".join(context)

    def get_last_emotion(self) -> Optional[str]:
        if not self.turns:
            return None
        return self.turns[-1].emotion

    def clear(self):
        self.turns.clear()


# ============================
# EMOTIONAL TREND MEMORY
# ============================

class EmotionalMemory:
    """
    Tracks emotional patterns across conversation.
    """

    def __init__(self):
        self.emotion_counts = {}

    def record_emotion(self, emotion: str):
        self.emotion_counts[emotion] = self.emotion_counts.get(emotion, 0) + 1

    def dominant_emotion(self) -> Optional[str]:
        if not self.emotion_counts:
            return None
        return max(self.emotion_counts, key=self.emotion_counts.get)

    def reset(self):
        self.emotion_counts.clear()


# ============================
# MEMORY MANAGER (RUNTIME)
# ============================

class MemoryManager:
    """
    Unified interface for runtime conversational memory.
    """

    def __init__(self):
        self.conversation = ConversationMemory()
        self.emotional = EmotionalMemory()

    def add_interaction(self, user_text: str, ai_reply: str, emotion: str):
        self.conversation.add_turn(user_text, ai_reply, emotion)
        self.emotional.record_emotion(emotion)

    def get_context(self) -> str:
        return self.conversation.get_recent_context()

    def get_previous_emotion(self) -> Optional[str]:
        return self.conversation.get_last_emotion()

    def get_emotional_trend(self) -> Optional[str]:
        return self.emotional.dominant_emotion()

    def reset(self):
        self.conversation.clear()
        self.emotional.reset()


# ============================
# SESSION MEMORY (PERSISTENT)
# REQUIRED BY main.py
# ============================

SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

def load_session(session_id: str):
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")

    if not os.path.exists(path):
        return {
            "messages": [],
            "persona": None
        }

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_session(session_id: str, session: dict):
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(session, f, ensure_ascii=False, indent=2)
