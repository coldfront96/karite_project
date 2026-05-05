"""
Core chatbot logic for the English Teaching Chatbot.
Handles conversation state, user input routing, and response generation.
"""

import os
import requests

from .memory import load_dictionary, save_translation
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

BOT_TEXT = {
    "English": {
        "welcome": (
            "╔══════════════════════════════════════════════════════════════╗\n"
            "║       Welcome to Karite English Teaching Chatbot!            ║\n"
            "╚══════════════════════════════════════════════════════════════╝\n"
            "\n"
            "I can help you learn English from absolute basics to advanced level.\n"
            "\n"
            "Please choose your learning mode:\n"
            "\n"
            "[1] 📚 Guided Curriculum (Structured Lessons & Quizzes)\n"
            "[2] 💬 Conversational Sandbox (AI Translation & Slang Breakdown)\n"
            "\n"
            "Type 1 or 2 to select a mode. Type 'help' for more commands."
        ),
        "help": (
            "Available commands:\n"
            "  menu             – Return to the main menu\n"
            "  help             – Show this help message\n"
            "  start            – Start your learning journey\n"
            "  levels           – List difficulty levels\n"
            "  topics           – List topics\n"
            "  next             – Next lesson\n"
            "  quiz             – Take quiz\n"
            "  progress         – View progress\n"
            "  exit             – Return to main menu"
        ),
        "goodbye": "Goodbye! Keep practicing. 👋",
        "mode_menu": (
            "\n"
            "╔══════════════════════════════════════════════════════════════╗\n"
            "║              Choose Your Learning Mode                       ║\n"
            "╚══════════════════════════════════════════════════════════════╝\n"
            "\n"
            "[1] 📚 Guided Curriculum (Structured Lessons & Quizzes)\n"
            "[2] 💬 Conversational Sandbox (AI Translation & Slang Breakdown)\n"
            "\n"
            "Type 1 or 2 to select a mode."
        ),
    },
    "Samoan": {
        "welcome": (
            "╔══════════════════════════════════════════════════════════════╗\n"
            "║       Afio mai i le Karite Faiaoga Igilisi!                  ║\n"
            "╚══════════════════════════════════════════════════════════════╝\n"
            "\n"
            "E mafai ona ou fesoasoani ia te oe e a'o le Igilisi.\n"
            "\n"
            "Fa'amolemole filifili lau auala e a'o ai:\n"
            "\n"
            "[1] 📚 Lesona Fa'atulagaina (Lesona & Su'ega)\n"
            "[2] 💬 Talanoaga Saoloto (Fa'aliliuga AI)\n"
            "\n"
            "Ta'i le 1 po'o le 2 e filifili ai. Ta'i le 'help' mo nisi tulafono."
        ),
        "help": (
            "Tulafono e mafai ona fa'aaoga:\n"
            "  menu             – Toe fo'i i le lisi autu\n"
            "  help             – Faaali mai lenei fesoasoani\n"
            "  start            – Amata lau a'oa'oga\n"
            "  levels           – Lisi vaega faigata\n"
            "  topics           – Lisi autu\n"
            "  next             – Lesona e soso'o ai\n"
            "  quiz             – Fai le su'ega\n"
            "  progress         – Va'ai i le alualu i luma\n"
            "  exit             – Toe fo'i i le lisi autu"
        ),
        "goodbye": "Tofa! Ia faaauau pea le fa'ata'ita'i. 👋",
        "mode_menu": (
            "\n"
            "╔══════════════════════════════════════════════════════════════╗\n"
            "║              Filifili Lau Auala e A'o Ai                     ║\n"
            "╚══════════════════════════════════════════════════════════════╝\n"
            "\n"
            "[1] 📚 Lesona Fa'atulagaina\n"
            "[2] 💬 Talanoaga Saoloto\n"
            "\n"
            "Ta'i le 1 po'o le 2 e filifili ai."
        ),
    },
}


class EnglishTeachingBot:
    """
    The main English Teaching Chatbot.

    Attributes:
        progress: ProgressTracker instance for managing user progress.
    """

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def __init__(self, save_path=None, initial_progress=None, save_callback=None):
        """
        Args:
            save_path: Optional path to persist progress (JSON file).
            initial_progress: Optional dict with pre-loaded progress data
                              (e.g. fetched from the database).
            save_callback: Optional callable(progress_dict) invoked whenever
                           progress changes (used by the database backend).
        """
        self.progress = ProgressTracker(
            save_path=save_path,
            initial_data=initial_progress,
            save_callback=save_callback,
        )
        self._quiz_state = None          # Active quiz session or None
        self._current_mode = None        # "menu", "curriculum", "conversational", "review", or "admin"
        self._admin_pending_phrase = None  # Phrase awaiting admin correction
        self._admin_awaiting_password = False  # True while waiting for admin password
        self.target_language = "English"
        self.ui_language = "English"
        self._review_topic = None        # Topic currently being reviewed in endless practice loop

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def greet(self):
        """Return the welcome message."""
        lang = self.ui_language if self.ui_language in BOT_TEXT else "English"
        return BOT_TEXT[lang]["welcome"]

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

        # Always-available commands
        if cmd in ("quit", "bye"):
            lang = self.ui_language if self.ui_language in BOT_TEXT else "English"
            return BOT_TEXT[lang]["goodbye"]

        if cmd in ("help", "?"):
            lang = self.ui_language if self.ui_language in BOT_TEXT else "English"
            return BOT_TEXT[lang]["help"]

        # ── Admin password prompt ──────────────────────────────────────
        if self._admin_awaiting_password:
            return self._handle_admin_password(text)

        # Handle review command: "review [topic]" – available from any mode
        if cmd.startswith("review "):
            topic_key = cmd[len("review "):].strip()
            return self._start_review(topic_key)

        # ── No mode set / mode menu ────────────────────────────────────
        if self._current_mode is None or self._current_mode == "menu":
            return self._handle_mode_selection(cmd)

        # "menu" returns to mode selection from any active mode
        if cmd == "menu":
            self._current_mode = "menu"
            self._admin_pending_phrase = None
            self._review_topic = None
            return self._show_mode_menu()

        # ── Admin teaching mode ────────────────────────────────────────
        if self._current_mode == "admin":
            if cmd == "exit":
                self._current_mode = "menu"
                self._admin_pending_phrase = None
                return self._show_mode_menu()
            return self._handle_admin_mode(text)

        # ── Conversational sandbox ─────────────────────────────────────
        if self._current_mode == "conversational":
            if cmd == "exit":
                self._current_mode = "menu"
                return self._show_mode_menu()
            return self._ask_local_ai(text)

        # ── Endless Practice (review) mode ─────────────────────────────
        if self._current_mode == "review":
            if cmd in ("menu", "exit"):
                self._current_mode = "menu"
                self._review_topic = None
                return self._show_mode_menu()
            return self._generate_practice(user_input=text)

        # ── Curriculum mode ────────────────────────────────────────────
        if cmd == "exit":
            lang = self.ui_language if self.ui_language in BOT_TEXT else "English"
            return BOT_TEXT[lang]["goodbye"]

        if cmd in ("start", "begin", "go"):
            return self._start_learning()

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
        if cmd in get_levels(self.target_language):
            return self._select_level(cmd)

        # Fallback: try to find a topic by name
        topic_response = self._maybe_select_topic(cmd)
        if topic_response:
            return topic_response

        # Fallback: Route to the local AI
        return self._ask_local_ai(text)

    # ------------------------------------------------------------------
    # Mode menu helpers
    # ------------------------------------------------------------------

    def _show_mode_menu(self):
        lang = self.ui_language if self.ui_language in BOT_TEXT else "English"
        menu = BOT_TEXT[lang]["mode_menu"]
        completed = self.progress.completed_topics_list()
        if completed:
            menu += (
                "\n\n🔁 You have past topics you can revisit!\n"
                "Type 'review [topic name]' to enter the Endless Practice Loop for a past subject!"
            )
        return menu

    def _handle_mode_selection(self, cmd):
        if cmd == "1":
            self._current_mode = "curriculum"
            return (
                "📚 Curriculum Mode activated!\n\n"
                "Type 'start' to begin your first lesson, 'levels' to browse topics,\n"
                "or 'help' for all available commands."
            )
        if cmd == "2":
            self._current_mode = "conversational"
            return (
                "💬 Conversational Sandbox activated!\n\n"
                "Type any phrase in English or Samoan and I'll translate it for you.\n"
                "Type 'exit' or 'menu' to return to the main menu."
            )
        if cmd == "admin":
            # Hidden command – intentionally omitted from help/menu text so that
            # regular users are not aware of the admin interface.
            self._admin_awaiting_password = True
            return "🔒 Admin mode requested. Please enter the admin password:"
        return self._show_mode_menu()

    # ------------------------------------------------------------------
    # Admin mode helpers
    # ------------------------------------------------------------------

    # Admin password is read from the KARITE_ADMIN_PASSWORD environment variable.
    # Falls back to the default value only when the variable is not set.
    _ADMIN_PASSWORD = os.environ.get("KARITE_ADMIN_PASSWORD", "samoa2026")

    def _handle_admin_password(self, text):
        """Validate the admin password and transition into admin mode."""
        self._admin_awaiting_password = False
        if text == self._ADMIN_PASSWORD:
            self._current_mode = "admin"
            self._admin_pending_phrase = None
            return (
                "✅ Admin Teaching Mode activated!\n\n"
                "Type a Samoan phrase and I'll show you my current translation.\n"
                "You can then confirm or correct it.\n"
                "Type 'exit' or 'menu' to leave admin mode."
            )
        return (
            "❌ Incorrect password. Returning to the main menu.\n\n"
            + self._show_mode_menu()
        )

    def _handle_admin_mode(self, text):
        """
        Admin teaching loop.

        - If no phrase is pending: treat input as the Samoan phrase to test.
          Ask the AI for its translation, show it, and ask the admin to confirm
          or correct it.
        - If a phrase is pending: treat input as the admin's verdict.
          'yes' → nothing to save; otherwise save the correction.
        """
        if self._admin_pending_phrase is None:
            # First turn: test the AI's translation
            self._admin_pending_phrase = text
            ai_response = self._ask_local_ai(text)
            return (
                f"{ai_response}\n\n"
                "❓ Did I get this right?\n"
                "   • Type 'yes' if the translation is perfect.\n"
                "   • Type the correct English meaning if I was wrong."
            )
        else:
            # Second turn: receive the admin's verdict
            phrase = self._admin_pending_phrase
            self._admin_pending_phrase = None

            if text.strip().lower() == "yes":
                return (
                    "👍 Great! No correction needed. The translation has been kept as-is.\n\n"
                    "Type another Samoan phrase to test, or 'menu' to exit admin mode."
                )
            else:
                save_translation(phrase, text)
                return (
                    f"✅ Saved! I'll now remember:\n"
                    f"   '{phrase}'  →  '{text}'\n\n"
                    "Type another Samoan phrase to test, or 'menu' to exit admin mode."
                )

    # ------------------------------------------------------------------
    # Learning flow
    # ------------------------------------------------------------------

    def _start_learning(self):
        level = self.progress.current_level
        topic = self.progress.current_topic

        if topic is None:
            # Start at the first topic of the current level
            topics = get_topics(self.target_language, level)
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

        nxt_level, nxt_topic = next_topic(self.target_language, level, topic)
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
        lesson = get_lesson(self.target_language, level, topic)
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
            "  Type 'quiz'   to test your knowledge",
            "  Type 'next'   to move to the next topic",
            "  Type 'levels' to choose a different level",
            "  Type 'menu'   to return to the main mode menu",
        ]
        return "\n".join(line for line in lines if line is not None)

    # ------------------------------------------------------------------
    # Menu helpers
    # ------------------------------------------------------------------

    def _show_menu(self):
        lines = ["", "=== LEARNING MENU ===", ""]
        for i, level in enumerate(get_levels(self.target_language), 1):
            desc = get_level_description(self.target_language, level)
            lines.append(f"  {i}. {level.upper()}")
            lines.append(f"     {desc}")
            lines.append("")
        lines.append("Type a level name (e.g. 'basic') or number to begin.")
        lines.append("Type 'menu' to return to the main mode selection menu.")
        return "\n".join(lines)

    def _list_levels(self):
        levels = get_levels(self.target_language)
        lines = ["Available levels:"]
        for lv in levels:
            lines.append(f"  • {lv}")
        lines.append("\nType a level name to choose it.")
        return "\n".join(lines)

    def _list_topics(self):
        level = self.progress.current_level
        topics = get_topics(self.target_language, level)
        lines = [f"Topics for level '{level.upper()}':"]
        for topic in topics:
            lesson = get_lesson(self.target_language, level, topic)
            title = lesson["title"] if lesson else topic
            done = " ✓" if self.progress.is_topic_complete(level, topic) else ""
            lines.append(f"  • {topic}  –  {title}{done}")
        lines.append("\nType a topic name to jump to it.")
        return "\n".join(lines)

    def _select_level(self, level):
        self.progress.current_level = level
        topics = get_topics(self.target_language, level)
        if not topics:
            return f"No topics available for level '{level}'."
        first_topic = topics[0]
        self.progress.current_topic = first_topic
        return self._present_lesson(level, first_topic)

    def _handle_number_choice(self, number):
        levels = get_levels(self.target_language)
        if 1 <= number <= len(levels):
            return self._select_level(levels[number - 1])
        # Maybe it's a topic number
        level = self.progress.current_level
        topics = get_topics(self.target_language, level)
        if 1 <= number <= len(topics):
            topic = topics[number - 1]
            self.progress.current_topic = topic
            return self._present_lesson(level, topic)
        return f"Invalid choice '{number}'. Type 'menu' to see options."

    def _maybe_select_topic(self, text):
        level = self.progress.current_level
        topics = get_topics(self.target_language, level)
        for topic in topics:
            if text == topic or text.replace(" ", "_") == topic:
                self.progress.current_topic = topic
                return self._present_lesson(level, topic)
        # Also search all levels
        for lv in get_levels(self.target_language):
            for topic in get_topics(self.target_language, lv):
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

        lesson = get_lesson(self.target_language, level, topic)
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
            "  Type 'next'   to continue to the next lesson",
            "  Type 'quiz'   to retry this quiz",
            "  Type 'levels' to choose a different level",
            "  Type 'menu'   to return to the main mode menu",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Endless Practice (review) mode
    # ------------------------------------------------------------------

    def _start_review(self, topic_key):
        """Validate topic_key against completed topics and enter review mode."""
        completed = self.progress.completed_topics_list()
        # topic_key can be bare topic name or "level/topic" – normalise
        matched_key = None
        normalised = topic_key.replace(" ", "_")
        for key in completed:
            _, tp = key.split("/", 1)
            if normalised == tp.replace(" ", "_") or topic_key == key:
                matched_key = key
                break
        if matched_key is None:
            return (
                f"❌ '{topic_key}' is not in your completed topics.\n"
                "Complete a topic quiz first, then type 'review [topic name]' to revisit it.\n"
                "Type 'progress' to see your completed topics."
            )
        self._current_mode = "review"
        self._review_topic = matched_key
        return self._generate_practice()

    def _generate_practice(self, user_input=None):
        """Generate an AI-driven practice question or evaluate a user answer."""
        system_prompt = (
            f"You are Karite, an expert {self.target_language} teacher. "
            f"The user is in an endless practice loop reviewing the topic: '{self._review_topic}'. "
        )
        if user_input is None:
            user_message = (
                "Generate ONE brief, brand new example teaching this concept, "
                "and then ask the user ONE question to test their understanding. "
                "Do NOT provide the answer yet."
            )
        else:
            user_message = (
                f"The user answered: '{user_input}'. "
                f"Evaluate their answer. If wrong, explain why using {self.target_language} rules. "
                "Then, immediately generate ONE new example and question to keep the practice loop going."
            )

        payload = {
            "model": "llama3",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.7,
        }

        try:
            response = requests.post(
                "http://localhost:11434/v1/chat/completions",
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            ai_reply = data["choices"][0]["message"]["content"]
            return f"🤖 Karite AI: {ai_reply}\n\n(Type 'menu' or 'exit' to leave the practice loop.)"
        except (requests.exceptions.RequestException, KeyError, IndexError):
            return "Oops! I couldn't reach my AI brain. Please make sure the local server is running! 🌸"

    # ------------------------------------------------------------------
    # Local AI bridge
    # ------------------------------------------------------------------

    def _ask_local_ai(self, text):
        """Routes unknown questions to the local LLM server."""
        # Load the dictionary universally
        custom_dict = load_dictionary()
        memory_context = ""
        if custom_dict:
            entries = "\n".join(
                f"  - '{k}' means '{v}'" for k, v in custom_dict.items()
            )
            memory_context = (
                "\n\nIMPORTANT – Custom translation memory (admin-verified):\n"
                + entries
                + "\nAlways use these verified translations when the phrase appears."
            )
        if self._current_mode in ("conversational", "admin"):
            if self._current_mode == "admin":
                context_description = (
                    "An admin teacher is testing your translations in Admin Teaching Mode. "
                    "Provide your best Samoan-to-English (or English-to-Samoan) translation "
                    "so the admin can verify or correct it."
                )
            else:
                context_description = (
                    "The user is in the Conversational Sandbox. "
                    "They will give you a phrase in English or Samoan."
                )
            system_prompt = (
                "You are Karite, an expert Samoan-English bilingual teacher. "
                + context_description
                + " You MUST output your response in this exact strict format: "
                "\n\n1. 🤖 **Direct Translation:** (The literal, word-for-word meaning) "
                "\n2. 🗣️ **Conversational Translation:** (How a native speaker would actually say it in casual conversation) "
                "\n3. 🧠 **The Breakdown:** (Explain WHY the conversational version is different. Point out any idioms, dropped words, or cultural context)."
                + f"CRITICAL INSTRUCTION: The user is studying the '{self.target_language}' course. You MUST explain all grammar, vocabulary, and concepts using the rules of {self.target_language}. Furthermore, you MUST speak, converse, and provide all of your explanations entirely in {self.ui_language}. Use {self.ui_language} as your primary medium of communication."
                + memory_context
            )
        else:
            current_level = self.progress.current_level
            current_topic = self.progress.current_topic or "general English basics"
            lesson_context = ""
            if self._current_mode == "curriculum" and self.progress.current_topic:
                # Safely attempt to fetch the current lesson text from the curriculum dictionary
                try:
                    topic_data = CURRICULUM["English"][self.progress.current_level][self.progress.current_topic]
                    lesson_text = topic_data.get("explanation", "")
                    lesson_context = f"\n\nCRITICAL CONTEXT: The user is currently reading this exact lesson: '{lesson_text}'. Answer their question based strictly on this lesson."
                except KeyError:
                    pass
            system_prompt = (
                "You are Karite, an enthusiastic and expert Samoan-English bilingual teacher. "
                f"The user is currently studying the '{current_level}' level, specifically '{current_topic}'. "
                "If the user asks a general question, answer it clearly and concisely. "
                "CRITICAL INSTRUCTION: If the user inputs a sentence for translation (either Samoan to English, or English to Samoan), you MUST strictly follow this format: "
                "\n1. 🎯 **Translation:** Provide the direct translation. "
                "\n2. 🧠 **How it Works (Grammar):** Explain the sentence structure. Explicitly point out grammatical differences, such as English Subject-Verb-Object (SVO) versus Samoan Verb-Subject-Object (VSO) patterns. "
                "\n3. 📖 **Vocabulary Breakdown:** Briefly define the key words used."
                + lesson_context
                + f" CRITICAL INSTRUCTION: You MUST speak, converse, and provide all explanations entirely in {self.ui_language}. Use {self.ui_language} as your primary medium of communication."
                + memory_context
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
                lesson = get_lesson(self.target_language, lv, tp)
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
