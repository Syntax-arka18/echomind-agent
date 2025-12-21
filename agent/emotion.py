def detect_emotion(text: str) -> str:
    text = text.lower()

    if any(w in text for w in ["stressed", "anxious", "worried", "panic"]):
        return "anxious"
    if any(w in text for w in ["confused", "lost", "stuck", "unsure"]):
        return "confused"
    if any(w in text for w in ["excited", "happy", "motivated"]):
        return "positive"
    if len(text.split()) > 40:
        return "overwhelmed"

    return "neutral"
