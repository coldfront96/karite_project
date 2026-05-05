"""
Memory handler for the Admin Teaching Mode.
Reads and writes custom Samoan-to-English translations to a local JSON file.
"""

import json
import os

DICTIONARY_PATH = os.path.join(os.path.dirname(__file__), "..", "custom_dictionary.json")


def load_dictionary():
    """
    Read custom translations from custom_dictionary.json.

    Returns:
        dict: Mapping of Samoan phrases to English translations.
              Returns an empty dict if the file doesn't exist.
    """
    path = os.path.abspath(DICTIONARY_PATH)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_translation(samoan_phrase, english_translation):
    """
    Add or update a translation in custom_dictionary.json.

    Args:
        samoan_phrase: The Samoan phrase (used as the key).
        english_translation: The correct English meaning (used as the value).
    """
    path = os.path.abspath(DICTIONARY_PATH)
    dictionary = load_dictionary()
    dictionary[samoan_phrase] = english_translation
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)
