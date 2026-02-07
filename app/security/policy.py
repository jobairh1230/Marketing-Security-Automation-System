def policy_check(text: str) -> bool:
    blocked_patterns = ["password", "api key", "token"]
    for word in blocked_patterns:
        if word in text.lower():
            return False
    return True
