def choose_strategy(emotion: str, history_len: int) -> str:
    if emotion == "anxious":
        return "slow_reflect"
    if emotion == "confused":
        return "clarify"
    if emotion == "overwhelmed":
        return "interrupt"
    if history_len > 6:
        return "deepen"
    return "explore"
