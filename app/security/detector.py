import re

def detect_prompt_injection(text: str) -> bool:
    risky_patterns = [
        r"ignore (all|any) previous instructions",
        r"reveal system prompt",
        r"bypass safety",
    ]
    for pattern in risky_patterns:
        if re.search(pattern, text.lower()):
            return True
    return False
