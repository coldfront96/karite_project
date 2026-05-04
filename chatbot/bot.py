"""
Core chatbot logic for the English Teaching Chatbot.
Handles conversation state, user input routing, and response generation.
"""

import requests

from .curriculum import (
    CURRICULUM,
    get_levels,
    get_lesson,
    get_level_description,
    get_topics,
    next_topic,
)
from .progress import ProgressTracker

# -----------------------------------------------------------------------
# Public constants
# -----------------------------------------------------------------------

WELCOME_MESSAGE = """
╔══════════════════════════════════════════════════════════════╗
║       Welcome to Karite English Teaching Chatbot! 🇬🇧        ║
╚══════════════════════════════════════════════════════════════╝

I can help you learn English from absolute basics to advanced level.

I offer three levels:
  1. Basic       – Alphabet, greetings, numbers, vocabulary, sentences
  2. Intermediate – Tenses, prepositions, richer vocabulary
  3. Advanced    – Conditionals, passive voice, idioms, academic writing

Type 'help' at any time to see available commands.
Type 'start' to begin learning!
""".strip()

HELP_TEXT = """
Available commands:
  start            – Start or resume your learning journey
  menu             – Show the main level/topic menu
  levels           – List available difficulty levels
  topics           – List topics in the current level
  next             – Move to the next lesson
  quiz             – Take the quiz for the current lesson
  progress         – View your progress and quiz scores
  reset            – Reset all progress and start over
  help             – Show this help message
  quit / exit / bye – Exit the chatbot
""".strip()


class EnglishTeachingBot:
    """
    The main English Teaching Chatbot.

    Attributes:
        progress: ProgressTracker instance for managing user progress.
    """

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def __init__(self, save_path=None):
        """
        Args:
            save_path: Optional path to persist progress (JSON).
        """
        self.progress = ProgressTracker(save_path=save_path)
        self._quiz_state = None   # Active quiz session or None

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def greet(self):
        """Return the welcome message."""
        return WELCOME_MESSAGE

    def handle(self, user_input):
        """
        Process a line of user input and return the bot's response string.

        Args:
            user_input: Raw string from the user.

        Returns:
            str: The bot's response.
        """
        text = user_input.strip()

        # If a quiz is in progress, delegate to the quiz handler
        if self._quiz_state is not None:
            return self._handle_quiz_answer(text)

        cmd = text.lower()

        if cmd in ("quit", "exit", "bye", "q"):
            return "Goodbye! Keep practicing your English. 👋"

        if cmd in ("help", "?"):
            return HELP_TEXT

        if cmd in ("start", "begin", "go"):
            return self._start_learning()

        if cmd == "menu":
            return self._show_menu()

        if cmd == "levels":
            return self._list_levels()

        if cmd == "topics":
            return self._list_topics()

        if cmd in ("next", "continue"):
            return self._next_lesson()

        if cmd in ("quiz", "test", "q"):
            return self._start_quiz()

        if cmd == "progress":
            return self._show_progress()

        if cmd == "reset":
            return self._reset_progress()

        # Handle numeric menu choices
        if cmd.isdigit():
            return self._handle_number_choice(int(cmd))

        # Handle level selection by name
        if cmd in get_levels():
            return self._select_level(cmd)

        # Fallback: try to find a topic by name
        topic_response = self._maybe_select_topic(cmd)
        if topic_response:
            return topic_response

        # Fallback: Route to the local AI
        return self._ask_local_ai(text)

    # ------------------------------------------------------------------
    # Learning flow
    # ------------------------------------------------------------------

    def _start_learning(self):
        level = self.progress.current_level
        topic = self.progress.current_topic

        if topic is None:
            # Start at the first topic of the current level
            topics = get_topics(level)
            topic = topics[0] if topics else None

        if topic is None:
            return "No topics found. Type 'menu' to choose a level."

        self.progress.current_topic = topic
        return self._present_lesson(level, topic)

    def _next_lesson(self):
        level = self.progress.current_level
        topic = self.progress.current_topic

        if topic is None:
            return self._start_learning()

        # Mark current topic complete (if not already)
        self.progress.mark_topic_complete(level, topic)

        nxt_level, nxt_topic = next_topic(level, topic)
        if nxt_level is None:
            return (
                "🎉 Congratulations! You have completed ALL lessons!\n\n"
                "Type 'progress' to see your final score, or 'reset' to start over."
            )

        # Advance
        if nxt_level != level:
            self.progress.current_level = nxt_level
        self.progress.current_topic = nxt_topic
        return self._present_lesson(nxt_level, nxt_topic)

    def _present_lesson(self, level, topic):
        lesson = get_lesson(level, topic)
        if lesson is None:
            return f"Lesson not found for {level}/{topic}."

        correct, total = self.progress.get_quiz_score(level, topic)
        done_marker = f"  ✓ Quiz completed: {correct}/{total}" if total > 0 else ""

        lines = [
            f"{'─'*62}",
            f"  Level: {level.upper()}  |  Topic: {lesson['title']}",
            f"{'─'*62}",
            "",
            lesson["explanation"],
            "",
            "─── Examples ──────────────────────────────────────────────",
        ]
        for ex in lesson.get("examples", []):
            lines.append(f"  {ex}")

        lines += [
            "",
            done_marker if done_marker else "",
            "─── What next? ────────────────────────────────────────────",
            "  Type 'quiz'  to test your knowledge",
            "  Type 'next'  to move to the next topic",
            "  Type 'menu'  to choose a different topic",
        ]
        return "\n".join(line for line in lines if line is not None)

    # ------------------------------------------------------------------
    # Menu helpers
    # ------------------------------------------------------------------

    def _show_menu(self):
        lines = ["", "=== LEARNING MENU ===", ""]
        for i, level in enumerate(get_levels(), 1):
            desc = get_level_description(level)
            lines.append(f"  {i}. {level.upper()}")
            lines.append(f"     {desc}")
            lines.append("")
        lines.append("Type a level name (e.g. 'basic') or number to begin.")
        return "\n".join(lines)

    def _list_levels(self):
        levels = get_levels()
        lines = ["Available levels:"]
        for lv in levels:
            lines.append(f"  • {lv}")
        lines.append("\nType a level name to choose it.")
        return "\n".join(lines)

    def _list_topics(self):
        level = self.progress.current_level
        topics = get_topics(level)
        lines = [f"Topics for level '{level.upper()}':"]
        for topic in topics:
            lesson = get_lesson(level, topic)
            title = lesson["title"] if lesson else topic
            done = " ✓" if self.progress.is_topic_complete(level, topic) else ""
            lines.append(f"  • {topic}  –  {title}{done}")
        lines.append("\nType a topic name to jump to it.")
        return "\n".join(lines)

    def _select_level(self, level):
        self.progress.current_level = level
        topics = get_topics(level)
        if not topics:
            return f"No topics available for level '{level}'."
        first_topic = topics[0]
        self.progress.current_topic = first_topic
        return self._present_lesson(level, first_topic)

    def _handle_number_choice(self, number):
        levels = get_levels()
        if 1 <= number <= len(levels):
            return self._select_level(levels[number - 1])
        # Maybe it's a topic number
        level = self.progress.current_level
        topics = get_topics(level)
        if 1 <= number <= len(topics):
            topic = topics[number - 1]
            self.progress.current_topic = topic
            return self._present_lesson(level, topic)
        return f"Invalid choice '{number}'. Type 'menu' to see options."

    def _maybe_select_topic(self, text):
        level = self.progress.current_level
        topics = get_topics(level)
        for topic in topics:
            if text == topic or text.replace(" ", "_") == topic:
                self.progress.current_topic = topic
                return self._present_lesson(level, topic)
        # Also search all levels
        for lv in get_levels():
            for topic in get_topics(lv):
                if text == topic or text.replace(" ", "_") == topic:
                    self.progress.current_level = lv
                    self.progress.current_topic = topic
                    return self._present_lesson(lv, topic)
        return None

    # ------------------------------------------------------------------
    # Quiz logic
    # ------------------------------------------------------------------

    def _start_quiz(self):
        level = self.progress.current_level
        topic = self.progress.current_topic

        if topic is None:
            return "Please start a lesson first. Type 'start' or 'menu'."

        lesson = get_lesson(level, topic)
        if lesson is None:
            return "No lesson loaded. Type 'menu' to choose a topic."

        quiz_questions = lesson.get("quiz", [])
        if not quiz_questions:
            return "No quiz available for this topic yet."

        self._quiz_state = {
            "level": level,
            "topic": topic,
            "questions": quiz_questions,
            "index": 0,
            "correct": 0,
        }
        return self._present_quiz_question()

    def _present_quiz_question(self):
        state = self._quiz_state
        q_list = state["questions"]
        idx = state["index"]
        total = len(q_list)

        if idx >= total:
            return self._finish_quiz()

        q = q_list[idx]
        lines = [
            "",
            f"  Quiz  ({idx + 1}/{total})",
            f"  {q['question']}",
            "",
        ]
        for choice in q["choices"]:
            lines.append(f"    {choice}")
        lines.append("")
        lines.append("  Type the letter of your answer (A, B, C, or D):")
        return "\n".join(lines)

    def _handle_quiz_answer(self, text):
        state = self._quiz_state
        answer = text.strip().upper()

        if answer in ("QUIT", "EXIT", "STOP", "Q"):
            self._quiz_state = None
            return "Quiz cancelled. Type 'quiz' to try again."

        q_list = state["questions"]
        idx = state["index"]

        if idx >= len(q_list):
            return self._finish_quiz()

        q = q_list[idx]
        valid_choices = {c[0] for c in q["choices"]}  # first character of each choice

        if answer not in valid_choices:
            return (
                f"  Please enter one of: {', '.join(sorted(valid_choices))}\n"
                f"  (or type 'quit' to exit the quiz)"
            )

        correct_answer = q["answer"].upper()
        is_correct = answer == correct_answer

        if is_correct:
            state["correct"] += 1
            feedback = "✅  Correct!"
        else:
            feedback = f"❌  Not quite. The correct answer is {correct_answer}."

        explanation = f"  💡 {q['explanation']}"
        state["index"] += 1

        # Check if quiz is over
        if state["index"] >= len(q_list):
            result_lines = [feedback, explanation, ""]
            result_lines.append(self._finish_quiz())
            self._quiz_state = None
            return "\n".join(result_lines)

        return f"{feedback}\n{explanation}\n" + self._present_quiz_question()

    def _finish_quiz(self):
        state = self._quiz_state
        level = state["level"]
        topic = state["topic"]
        correct = state["correct"]
        total = len(state["questions"])

        self.progress.record_quiz_result(level, topic, correct, total)
        self.progress.mark_topic_complete(level, topic)
        self._quiz_state = None

        percentage = int(correct / total * 100) if total else 0
        if percentage == 100:
            grade = "🏆 Perfect score!"
        elif percentage >= 80:
            grade = "⭐ Excellent!"
        elif percentage >= 60:
            grade = "👍 Good job!"
        else:
            grade = "📚 Keep practicing – you'll get there!"

        lines = [
            "",
            f"  ── Quiz Results ──────────────────────────",
            f"  Score: {correct}/{total} ({percentage}%)",
            f"  {grade}",
            "",
            "  Type 'next'  to continue to the next lesson",
            "  Type 'quiz'  to retry this quiz",
            "  Type 'menu'  to choose a different topic",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Local AI bridge
    # ------------------------------------------------------------------

    def _ask_local_ai(self, text):
        """Routes unknown questions to the local LLM server."""
        current_level = self.progress.current_level
        current_topic = self.progress.current_topic or "general English basics"

        system_prompt = (
            "You are Karite, an enthusiastic and expert Samoan-English bilingual teacher. "
            f"The user is currently studying the '{current_level}' level, specifically '{current_topic}'. "
            "Answer their question accurately. If they ask for a translation from Samoan to English, or English to Samoan, provide it clearly with a brief explanation. Keep your answer under 4 sentences."
        )

        payload = {
            "model": "llama3", # Note: We can change this to the exact local model name later
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            "temperature": 0.3
        }

        try:
            response = requests.post(
                "http://localhost:11434/v1/chat/completions",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            ai_reply = data["choices"][0]["message"]["content"]
            return f"🤖 Karite AI: {ai_reply}"
        except (requests.exceptions.RequestException, KeyError, IndexError):
            return "Oops! I couldn't reach my AI brain. Please make sure the local server is running! 🌸"

    # ------------------------------------------------------------------
    # Progress & reset
    # ------------------------------------------------------------------

    def _show_progress(self):
        stats = self.progress.overall_stats()
        completed = self.progress.completed_topics_list()
        level = self.progress.current_level
        topic = self.progress.current_topic

        lines = [
            "",
            "═══ Your Progress ══════════════════════════════════",
            f"  Current level:  {level.upper()}",
            f"  Current topic:  {topic or 'None selected'}",
            f"  Topics completed: {stats['completed']}",
            f"  Quiz accuracy:  {stats['total_correct']}/{stats['total_questions']} "
            f"({stats['accuracy']}%)",
            "",
            "  Completed topics:",
        ]

        if completed:
            for key in completed:
                lv, tp = key.split("/", 1)
                lesson = get_lesson(lv, tp)
                title = lesson["title"] if lesson else tp
                c, t = self.progress.get_quiz_score(lv, tp)
                score_str = f"  (quiz: {c}/{t})" if t > 0 else ""
                lines.append(f"    ✓ [{lv.upper()}] {title}{score_str}")
        else:
            lines.append("    None yet. Type 'start' to begin!")

        lines.append("═══════════════════════════════════════════════════")
        return "\n".join(lines)

    def _reset_progress(self):
        self.progress.reset()
        return (
            "Progress has been reset. You're starting fresh!\n"
            "Type 'start' to begin your learning journey."
        )
