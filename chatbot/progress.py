"""
Progress tracking for the English Teaching Chatbot.
Stores user progress in memory (and optionally on disk as JSON).
"""

import json
import os
import sys


class ProgressTracker:
    """Tracks which lessons and quizzes the user has completed."""

    def __init__(self, save_path=None, initial_data=None, save_callback=None):
        """
        Args:
            save_path: Optional filesystem path to persist progress as JSON.
                       If None, progress is stored in memory only.
            initial_data: Optional dict to pre-populate progress (e.g. from a
                          database). Takes precedence over save_path loading.
            save_callback: Optional callable(progress_dict) invoked whenever
                           progress changes. Used by the database backend.
        """
        self._save_path = save_path
        self._save_callback = save_callback
        self._data = {
            "current_level": "basic",
            "current_topic": None,
            "completed_topics": [],   # list of "level/topic" strings
            "quiz_scores": {},        # {"level/topic": {"correct": n, "total": n}}
            "total_correct": 0,
            "total_questions": 0,
        }
        if initial_data:
            for key in self._data:
                if key in initial_data:
                    self._data[key] = initial_data[key]
        elif save_path and os.path.exists(save_path):
            self._load()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def current_level(self):
        return self._data["current_level"]

    @current_level.setter
    def current_level(self, value):
        self._data["current_level"] = value
        self._save()

    @property
    def current_topic(self):
        return self._data["current_topic"]

    @current_topic.setter
    def current_topic(self, value):
        self._data["current_topic"] = value
        self._save()

    def mark_topic_complete(self, level, topic):
        """Record that the user has completed a topic."""
        key = f"{level}/{topic}"
        if key not in self._data["completed_topics"]:
            self._data["completed_topics"].append(key)
            self._save()

    def is_topic_complete(self, level, topic):
        """Return True if the user has already completed this topic."""
        return f"{level}/{topic}" in self._data["completed_topics"]

    def record_quiz_result(self, level, topic, correct, total):
        """Store quiz results for a topic."""
        key = f"{level}/{topic}"
        self._data["quiz_scores"][key] = {"correct": correct, "total": total}
        self._data["total_correct"] += correct
        self._data["total_questions"] += total
        self._save()

    def get_quiz_score(self, level, topic):
        """Return (correct, total) for a topic's quiz, or (0, 0) if not taken."""
        key = f"{level}/{topic}"
        result = self._data["quiz_scores"].get(key, {})
        return result.get("correct", 0), result.get("total", 0)

    def completed_topics_list(self):
        """Return a copy of the completed topics list."""
        return self._data["completed_topics"][:]

    def overall_stats(self):
        """Return a dict with overall progress statistics."""
        return {
            "completed": len(self._data["completed_topics"]),
            "total_correct": self._data["total_correct"],
            "total_questions": self._data["total_questions"],
            "accuracy": self._accuracy(),
        }

    def reset(self):
        """Reset all progress."""
        self._data = {
            "current_level": "basic",
            "current_topic": None,
            "completed_topics": [],
            "quiz_scores": {},
            "total_correct": 0,
            "total_questions": 0,
        }
        self._save()

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def _accuracy(self):
        total = self._data["total_questions"]
        if total == 0:
            return 0.0
        return round(self._data["total_correct"] / total * 100, 1)

    def _save(self):
        if self._save_path:
            try:
                with open(self._save_path, "w", encoding="utf-8") as fh:
                    json.dump(self._data, fh, indent=2)
            except OSError:
                pass  # Don't crash if we can't write progress
        if self._save_callback:
            try:
                self._save_callback(self._data)
            except Exception as exc:
                print(
                    f"Warning: progress save callback failed ({exc}).",
                    file=sys.stderr,
                )

    def _load(self):
        try:
            with open(self._save_path, "r", encoding="utf-8") as fh:
                loaded = json.load(fh)
            # Only load keys we recognise to avoid corruption issues
            for key in self._data:
                if key in loaded:
                    self._data[key] = loaded[key]
        except (OSError, json.JSONDecodeError, KeyError) as exc:
            print(
                f"Warning: could not load progress from '{self._save_path}' "
                f"({exc}). Starting with default progress.",
                file=sys.stderr,
            )
