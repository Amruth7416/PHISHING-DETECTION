# model.py

def analyze_text(text, mode):
    """
    Analyzes text based on the selected mode.
    """
    if mode == "website":
        return detect_suspicious_website(text)
    elif mode == "phishing_phrases":
        return detect_phishing_phrases(text)
    elif mode == "email":
        return detect_suspicious_email(text)
    else:
        return "low"  # Default risk level

# Placeholder functions for detection logic
def detect_suspicious_website(text):
    """
    Detects suspicious patterns in website URLs.
    """
    suspicious_patterns = [
        r"https?://(?:www\.)?([a-zA-Z0-9-]+)\.(?:tk|ml|ga|cf|gq)",  # Suspicious TLDs
        r"https?://(?:www\.)?([a-zA-Z0-9-]+)\.(?:xyz|info|biz)",  # Less common TLDs
    ]
    return "high" if any(re.search(pattern, text) for pattern in suspicious_patterns) else "low"

def detect_phishing_phrases(text):
    """
    Detects common phishing phrases in text.
    """
    phishing_phrases = [
        "urgent action required", "verify your account", "click the link below",
        "your account has been compromised", "password reset required",
    ]
    return "high" if any(phrase in text.lower() for phrase in phishing_phrases) else "low"

def detect_suspicious_email(text):
    """
    Detects suspicious patterns in email text.
    """
    suspicious_patterns = [
        "urgent", "password", "verify", "account", "suspended",
        "click here", "immediately", "security", "login", "credentials"
    ]
    return "high" if any(pattern in text.lower() for pattern in suspicious_patterns) else "low"