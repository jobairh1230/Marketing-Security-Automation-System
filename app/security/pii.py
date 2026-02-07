import re

def redact_pii(text: str) -> str:
    patterns = [
        r"\b\d{16}\b",  # Credit card pattern
        r"\b\d{3}-\d{2}-\d{4}\b",  # Social Security Number (SSN)
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",  # Email pattern
    ]
    for pattern in patterns:
        text = re.sub(pattern, "[REDACTED]", text)
    return text
