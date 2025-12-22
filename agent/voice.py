def shape_for_voice(text: str) -> str:
    text = text.replace("\n", " ")
    text = text.replace("...", "…")
    text = text.replace("  ", " ")
    return text.strip()
