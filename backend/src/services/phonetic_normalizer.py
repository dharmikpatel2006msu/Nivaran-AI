"""Phonetic Text Normalizer module for Voice Assistant in Nivaran AI.

Solves acoustic and phonetic errors from Automatic Speech Recognition (ASR):
1. Phonetic matching via Soundex & Metaphone algorithms.
2. Homophone disambiguation ("by" -> "buy", "peace" -> "piece", "sail" -> "sale").
3. Spoken alphanumeric & Order ID normalization ("O R D dash 1 2 3 4" -> "ORD-1234").
4. Spoken number & currency normalization ("twenty dollars" -> "$20").
5. Colloquial Indic/Hinglish/Gujlish intent normalization ("paise wapas" -> "refund", "kyan chhe" -> "where is").
6. Brand & canonical product entity normalization ("shop nest" -> "ShopNest", "ear birds" -> "earbuds").
"""

import re
import logging
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)

# --- 1. Soundex Phonetic Encoding ---
_SOUNDEX_MAPPING = {
    'b': '1', 'f': '1', 'p': '1', 'v': '1',
    'c': '2', 'g': '2', 'j': '2', 'k': '2', 'q': '2', 's': '2', 'x': '2', 'z': '2',
    'd': '3', 't': '3',
    'l': '4',
    'm': '5', 'n': '5',
    'r': '6'
}


def soundex(word: str) -> str:
    """Computes the 4-character Soundex phonetic code for a word."""
    clean_word = re.sub(r'[^a-zA-Z]', '', word).lower()
    if not clean_word:
        return "0000"

    first_letter = clean_word[0].upper()
    encoded = [first_letter]

    prev_code = _SOUNDEX_MAPPING.get(clean_word[0], '0')

    for char in clean_word[1:]:
        curr_code = _SOUNDEX_MAPPING.get(char, '0')
        if curr_code != '0':
            if curr_code != prev_code:
                encoded.append(curr_code)
                prev_code = curr_code
        else:
            prev_code = '0'

    # Pad with zeros or truncate to length 4
    code_str = "".join(encoded)
    return (code_str + "0000")[:4]


# --- 2. Metaphone Phonetic Encoding ---
def metaphone(word: str) -> str:
    """Computes the Metaphone phonetic code for a word."""
    clean = re.sub(r'[^a-zA-Z]', '', word).upper()
    if not clean:
        return ""

    # Initial letter transformations
    if clean.startswith(('KN', 'GN', 'PN', 'AE', 'WR')):
        clean = clean[1:]
    elif clean.startswith('X'):
        clean = 'S' + clean[1:]
    elif clean.startswith('WH'):
        clean = 'W' + clean[2:]

    result = []
    i = 0
    length = len(clean)

    while i < length:
        ch = clean[i]
        next_ch = clean[i + 1] if i + 1 < length else ''
        prev_ch = clean[i - 1] if i > 0 else ''

        # Skip duplicate consonants except 'C'
        if ch == prev_ch and ch != 'C':
            i += 1
            continue

        if ch in ('A', 'E', 'I', 'O', 'U'):
            if i == 0:
                result.append(ch)
        elif ch == 'B':
            if not (i == length - 1 and prev_ch == 'M'):
                result.append('B')
        elif ch == 'C':
            if i + 1 < length and next_ch == 'H':
                result.append('X')
                i += 1
            elif i + 1 < length and next_ch in ('I', 'E', 'Y'):
                result.append('S')
            else:
                result.append('K')
        elif ch == 'D':
            if i + 2 < length and clean[i:i + 2] == 'GE':
                result.append('J')
                i += 1
            else:
                result.append('T')
        elif ch == 'F':
            result.append('F')
        elif ch == 'G':
            if i + 1 < length and next_ch == 'H' and i + 2 == length:
                pass  # Silent GH at end
            elif i + 1 < length and next_ch in ('I', 'E', 'Y'):
                result.append('J')
            else:
                result.append('K')
        elif ch == 'H':
            if (i == 0 or prev_ch in ('A', 'E', 'I', 'O', 'U')) and next_ch in ('A', 'E', 'I', 'O', 'U'):
                result.append('H')
        elif ch in ('J', 'K'):
            result.append(ch)
        elif ch == 'L':
            result.append('L')
        elif ch == 'M':
            result.append('M')
        elif ch == 'N':
            result.append('N')
        elif ch == 'P':
            if i + 1 < length and next_ch == 'H':
                result.append('F')
                i += 1
            else:
                result.append('P')
        elif ch == 'Q':
            result.append('K')
        elif ch == 'R':
            result.append('R')
        elif ch == 'S':
            if i + 1 < length and next_ch == 'H':
                result.append('X')
                i += 1
            else:
                result.append('S')
        elif ch == 'T':
            if i + 1 < length and next_ch == 'H':
                result.append('0')
                i += 1
            elif i + 2 < length and clean[i:i + 3] == 'TIA':
                result.append('X')
            else:
                result.append('T')
        elif ch == 'V':
            result.append('F')
        elif ch in ('W', 'Y'):
            if i + 1 < length and next_ch in ('A', 'E', 'I', 'O', 'U'):
                result.append(ch)
        elif ch == 'Z':
            result.append('S')

        i += 1

    return "".join(result)


# --- 3. Canonical Domain Vocabulary & Phonetic Index ---
CANONICAL_DOMAIN_TERMS = [
    "refund", "return", "cancel", "cancellation", "replacement", "exchange",
    "warranty", "guarantee", "shipping", "delivery", "delivered", "shipped",
    "tracking", "status", "damaged", "broken", "defective", "receipt", "invoice",
    "headphones", "earbuds", "smartwatch", "charger", "bluetooth", "wireless",
    "ShopNest", "support", "ticket", "escalation", "product", "order"
]

_DOMAIN_PHONETIC_INDEX: Dict[str, str] = {}
for term in CANONICAL_DOMAIN_TERMS:
    _DOMAIN_PHONETIC_INDEX[metaphone(term)] = term


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculates Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


# --- 4. Acoustic & ASR Homophone Replacement Map ---
HOMOPHONE_MAP = {
    # Voice ASR acoustic confusions in e-commerce contexts
    r"\bby\b(?=\s+(?:headphones|earbuds|smartwatch|charger|items?|products?|one|now|this|that))": "buy",
    r"\bbye\b(?=\s+(?:headphones|earbuds|smartwatch|charger|items?|products?|one|now|this|that))": "buy",
    r"\bwon\b(?=\s+(?:item|piece|unit|product|pair|order))": "one",
    r"\b(damaged|broken|missing)\s+peace\b": r"\1 piece",
    r"\bon\s+sail\b": "on sale",
    r"\bpackage\s+wait\b": "package weight",
    r"\bhere\s+from\s+you\b": "hear from you",
    r"\bcancell\b": "cancel",
    r"\bcouncel\b": "cancel",
    r"\breffund\b": "refund",
    r"\brefun\b": "refund",
    r"\bretun\b": "return",
    r"\bwarenty\b": "warranty",
    r"\bwaranty\b": "warranty",
    r"\bshippin\b": "shipping",
    r"\bdelivary\b": "delivery",
    r"\bdeliverd\b": "delivered",
    r"\bdefective\s+peace\b": "defective piece",
    r"\btracking\s+statues\b": "tracking status",
    # Brand and Product phonetic ASR mishearings
    r"\b(?:chop\s*nest|sharp\s*nest|shop\s*next|shop\s*net|sharp\s*next)\b": "ShopNest",
    r"\bshop\s*nest\b": "ShopNest",
    r"\b(?:ear\s*birds?|air\s*buds?|ear\s*bods?)\b": "earbuds",
    r"\b(?:blue\s*tooth|blootooth|bluetoth)\b": "bluetooth",
    r"\b(?:smart\s*watch)\b": "smartwatch",
    r"\b(?:head\s*phones?)\b": "headphones"
}

# --- 5. Indic & Colloquial Voice Intent Map ---
# Normalizes spoken Hindi/Gujarati/Hinglish terms to standard e-commerce domain terms
INDIC_VOICE_INTENT_MAP = {
    # Refund & Money back
    r"\b(?:paise\s*wapas|paisa\s*vapas|paisa\s*wapas|paise\s*pachha|paise\s*vapis|rupaye\s*wapas)\b": "refund",
    # Returns & Replacement
    r"\b(?:badalvu\s*chhe|badli\s*karo|palatna\s*hai|vapas\s*karna\s*hai|pachhu\s*apvu\s*chhe)\b": "return exchange",
    # Order Tracking / Where is it
    r"\b(?:kahan\s*hai|kaha\s*hai|kyan\s*chhe|kya\s*che|kithe\s*hai)\b": "where is",
    r"\b(?:kab\s*aayega|kab\s*tak\s*aayega|kyare\s*aavshe|kyare\s*pochshe)\b": "when will it be delivered",
    # Damage / Broken item
    r"\b(?:tuti\s*gayu|kharab\s*chhe|tut\s*gaya|damage\s*chhe|bigdi\s*gayu)\b": "damaged defective",
    # Cancellation
    r"\b(?:cancel\s*karvu\s*chhe|radd\s*karo|band\s*karo\s*order)\b": "cancel order"
}

# --- 6. Spoken Numbers & Currency Normalization ---
NUMBER_WORDS = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
    "ten": "10", "eleven": "11", "twelve": "12", "twenty": "20",
    "thirty": "30", "forty": "40", "fifty": "50", "hundred": "100"
}


def normalize_spoken_order_id(text: str) -> str:
    """Normalizes spoken spelled-out Order IDs from ASR transcripts.

    Examples:
    - "order O R D dash 9 9 2 1" -> "order ORD-9921"
    - "O R D 1 2 3 4" -> "ORD-1234"
    - "order number O-R-D-456" -> "order ORD-456"
    - "O.R.D. 8812" -> "ORD-8812"
    """
    # Replace phonetic letter-by-letter "O R D", "O - R - D", or "O.R.D."
    # (?!\w) ensures "order" is not matched since 'd' is followed by 'e'
    pattern_letters = re.compile(
        r'\b(?:O\s*[\.\-]?\s*R\s*[\.\-]?\s*D\.?)(?!\w)\s*(?:dash|hyphen|-|#|number|no\.?|num)?\s*([0-9A-Za-z](?:\s+[0-9A-Za-z]){1,7}|[0-9A-Za-z]{3,8})\b',
        re.IGNORECASE
    )

    def _replace_order(match):
        raw_tail = match.group(1)
        # Collapse spaces between spoken digits/letters
        clean_tail = re.sub(r'[\s\-]+', '', raw_tail).upper()
        return f"ORD-{clean_tail}"

    normalized = pattern_letters.sub(_replace_order, text)

    # Normalize standalone "order number 1234" -> "order ORD-1234"
    normalized = re.sub(
        r'\border\s+(?:number|no\.?|#|id)\s*([0-9]{3,6})\b',
        r'order ORD-\1',
        normalized,
        flags=re.IGNORECASE
    )

    # Clean redundant dashes or double hashes
    normalized = re.sub(r'ORD\s*[-–—:]\s*', 'ORD-', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'#+\s*(ORD-[A-Za-z0-9]+)', r'\1', normalized, flags=re.IGNORECASE)

    return normalized


def normalize_spoken_currency_and_numbers(text: str) -> str:
    """Converts spoken numbers and currency phrases to standard representations."""
    # Complex multi-word numbers for currency
    text = re.sub(r'\bfive\s+hundred\s*(?:rupees?|rs\.?|inr)\b', r'₹500', text, flags=re.IGNORECASE)
    text = re.sub(r'\bfive\s+hundred\s*(?:dollars?|bucks?)\b', r'$500', text, flags=re.IGNORECASE)

    # Convert spoken word currency (e.g. "twenty dollars" -> "$20")
    for word, digit in NUMBER_WORDS.items():
        text = re.sub(rf'\b{word}\s*(?:dollars?|bucks?)\b', f"${digit}", text, flags=re.IGNORECASE)
        text = re.sub(rf'\b{word}\s*(?:rupees?|rs\.?|inr)\b', f"₹{digit}", text, flags=re.IGNORECASE)

    # Convert numeric currency (e.g. "20 dollars" -> "$20")
    text = re.sub(r'(\d+)\s*(?:dollars?|bucks?)\b', r'$\1', text, flags=re.IGNORECASE)
    text = re.sub(r'(\d+)\s*(?:rupees?|rs\.?|inr)\b', r'₹\1', text, flags=re.IGNORECASE)

    # Normalize standalone spoken digits (e.g., "quantity two" -> "quantity 2")
    for word, digit in NUMBER_WORDS.items():
        text = re.sub(rf'\b(?:quantity|qty|number)\s+{word}\b', f"quantity {digit}", text, flags=re.IGNORECASE)

    return text


def phonetic_correction_word(word: str) -> str:
    """Corrects an individual misspelled word using Soundex and Metaphone domain matching."""
    if len(word) < 4:
        return word

    clean_w = word.lower()

    # 1. Direct Metaphone match
    m_code = metaphone(clean_w)
    if m_code in _DOMAIN_PHONETIC_INDEX:
        canonical = _DOMAIN_PHONETIC_INDEX[m_code]
        # Only accept if Levenshtein distance is small (to avoid over-aggressive collisions)
        if levenshtein_distance(clean_w, canonical.lower()) <= 2:
            return canonical

    # 2. Soundex & Fuzzy Metaphone match against canonical domain vocabulary
    s_code = soundex(clean_w)
    for term in CANONICAL_DOMAIN_TERMS:
        term_s = soundex(term)
        term_m = metaphone(term)
        if term_s == s_code or term_m == m_code or (term_s[:3] == s_code[:3] and abs(len(clean_w) - len(term)) <= 2):
            if levenshtein_distance(clean_w, term.lower()) <= 2:
                return term

    return word


def normalize_voice_transcript(text: str) -> str:
    """Main entrypoint: normalizes a raw voice ASR transcript into clean canonical text.

    Pipeline:
    1. Spoken Order ID & Alphanumeric normalization
    2. Spoken numbers and currency normalization
    3. Indic/Hinglish intent & slang mapping
    4. Homophone & acoustic confusion regex replacement
    5. Phonetic token-level correction via Metaphone/Soundex
    6. Whitespace and punctuation cleanup

    Args:
        text: Raw transcript string from ASR (Whisper or Web Speech).

    Returns:
        Cleaned and phonetically normalized text string.
    """
    if not text or not text.strip():
        return ""

    normalized = text.strip()

    # 1. Normalize Spoken Order IDs
    normalized = normalize_spoken_order_id(normalized)

    # 2. Normalize Spoken Numbers & Currency
    normalized = normalize_spoken_currency_and_numbers(normalized)

    # 3. Apply Indic & Colloquial Intent Map
    for pattern, replacement in INDIC_VOICE_INTENT_MAP.items():
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)

    # 4. Apply Homophone & Acoustic Confusions
    for pattern, replacement in HOMOPHONE_MAP.items():
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)

    # 5. Token-level Phonetic Correction for domain words
    words = normalized.split()
    corrected_words = []
    for w in words:
        # Strip trailing punctuation for phonetic matching
        match = re.match(r'^([a-zA-Z0-9_-]+)([\.,!\?]*)', w)
        if match:
            token, punct = match.group(1), match.group(2)
            # If not an Order ID or number, attempt phonetic correction
            if not token.upper().startswith("ORD-") and not token.isdigit():
                corrected_token = phonetic_correction_word(token)
                corrected_words.append(f"{corrected_token}{punct}")
            else:
                corrected_words.append(w)
        else:
            corrected_words.append(w)

    normalized = " ".join(corrected_words)

    # 6. Final whitespace cleanup
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    if normalized.lower() != text.strip().lower():
        logger.info(f"🎙️ [Phonetic Normalizer] '{text}' ➔ '{normalized}'")

    return normalized
