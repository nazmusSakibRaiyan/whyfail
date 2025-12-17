"""
Utility functions for whyfail.
"""
from typing import Any, Dict, List


def get_dict_suggestions(available_keys: List[str], attempted_key: str) -> List[str]:
    """
    Generate suggestions for missing dictionary keys.
    
    Args:
        available_keys: List of available keys in the dictionary
        attempted_key: The key that was attempted
    
    Returns:
        List of suggestion strings
    """
    suggestions = [
        f"Check the spelling of '{attempted_key}'",
        f"Print available keys: dict.keys()",
        "Initialize the key before accessing it",
    ]
    
    # Find close matches (simple edit distance)
    close_matches = find_close_matches(attempted_key, available_keys)
    if close_matches:
        suggestions.insert(0, f"Did you mean: {', '.join(close_matches)}?")
    
    return suggestions


def find_close_matches(word: str, candidates: List[str], n: int = 3, cutoff: float = 0.6) -> List[str]:
    """
    Find close matches to a word from a list of candidates (simple implementation).
    
    Args:
        word: The word to match
        candidates: List of candidate words
        n: Maximum number of matches to return
        cutoff: Similarity threshold (0-1)
    
    Returns:
        List of close matches
    """
    matches = []
    word_lower = word.lower()
    
    for candidate in candidates:
        candidate_lower = str(candidate).lower()
        similarity = calculate_similarity(word_lower, candidate_lower)
        if similarity >= cutoff:
            matches.append((candidate, similarity))
    
    # Sort by similarity and return top n
    matches.sort(key=lambda x: x[1], reverse=True)
    return [match[0] for match in matches[:n]]


def calculate_similarity(s1: str, s2: str) -> float:
    """
    Calculate simple string similarity (Levenshtein-based).
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Similarity score between 0 and 1
    """
    if not s1 or not s2:
        return 0.0
    
    # Simple overlap-based similarity
    matches = sum(1 for a, b in zip(s1, s2) if a == b)
    return matches / max(len(s1), len(s2))


def truncate_string(s: str, max_length: int = 100) -> str:
    """
    Truncate a string to a maximum length.
    
    Args:
        s: String to truncate
        max_length: Maximum length
    
    Returns:
        Truncated string
    """
    if len(s) > max_length:
        return s[:max_length - 3] + "..."
    return s


def format_value(value: Any, max_length: int = 50) -> str:
    """
    Format a value for display in error messages.
    
    Args:
        value: The value to format
        max_length: Maximum length of the formatted string
    
    Returns:
        Formatted string representation
    """
    try:
        s = str(value)
        return truncate_string(s, max_length)
    except Exception:
        return "<unprintable>"
