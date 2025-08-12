import re

EXTENSIONS = ["iso", "zip", "7z", "rar", "img", "bin"]


def parse_intent(text: str):
    lower = text.lower()
    ext = None
    for candidate in EXTENSIONS:
        if re.search(rf"\b{re.escape(candidate)}\b", lower) or re.search(
            rf"\*\.{candidate}\b", lower
        ):
            ext = candidate
            break
    if not ext:
        return None
    dest_match = re.search(r"\bto\s+([^\s]+)", text, re.IGNORECASE)
    if dest_match:
        return {
            "type": "move_by_extension",
            "extension": ext,
            "destination": dest_match.group(1),
        }
    return {"type": "find_by_extension", "extension": ext}
