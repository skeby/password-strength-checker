import math
import re
from collections import Counter

from zxcvbn import zxcvbn


def _entropy_bits(password: str) -> float:
    if not password:
        return 0.0
    counts = Counter(password)
    length = len(password)
    entropy = 0.0
    for count in counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    return entropy


def extract_features(password: str) -> list[float]:
    zx = zxcvbn(password)
    sequence = zx.get("sequence", [])

    has_uppercase = 1.0 if re.search(r"[A-Z]", password) else 0.0
    has_lowercase = 1.0 if re.search(r"[a-z]", password) else 0.0
    has_digits = 1.0 if re.search(r"\d", password) else 0.0
    has_special = 1.0 if re.search(r"[^A-Za-z0-9]", password) else 0.0

    unique_char_ratio = (len(set(password)) / len(password)) if password else 0.0
    char_class_count = has_uppercase + has_lowercase + has_digits + has_special

    has_dictionary_match = 1.0 if any(item.get("pattern") == "dictionary" for item in sequence) else 0.0
    has_l33t_sub = 1.0 if any(item.get("l33t") is True for item in sequence) else 0.0
    has_keyboard_pattern = 1.0 if any(item.get("pattern") == "spatial" for item in sequence) else 0.0
    has_date_pattern = 1.0 if any(item.get("pattern") == "date" for item in sequence) else 0.0
    has_repeat = 1.0 if any(item.get("pattern") == "repeat" for item in sequence) else 0.0
    has_sequence = 1.0 if any(item.get("pattern") == "sequence" for item in sequence) else 0.0

    return [
        float(len(password)),
        float(_entropy_bits(password)),
        has_uppercase,
        has_lowercase,
        has_digits,
        has_special,
        float(unique_char_ratio),
        float(char_class_count),
        float(zx.get("score", 0)),
        float(zx.get("guesses_log10", 0.0)),
        has_dictionary_match,
        has_l33t_sub,
        has_keyboard_pattern,
        has_date_pattern,
        has_repeat,
        has_sequence,
    ]
