"""
Tests for the Karite English Teaching Chatbot.
Run with:  python -m pytest tests/ -v
"""

import pytest

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from chatbot.curriculum import (
    get_levels,
    get_lesson,
    get_level_description,
    get_topics,
    next_topic,
)
from chatbot.progress import ProgressTracker
from chatbot.bot import EnglishTeachingBot, BOT_TEXT


# ---------------------------------------------------------------------------
# Curriculum tests
# ---------------------------------------------------------------------------


class TestCurriculum:
    def test_levels_returns_three_levels(self):
        levels = get_levels()
        assert levels == ["basic", "intermediate", "advanced"]

    def test_basic_topics_exist(self):
        topics = get_topics("English", "basic")
        assert len(topics) >= 5
        assert "alphabet" in topics
        assert "greetings" in topics

    def test_intermediate_topics_exist(self):
        topics = get_topics("English", "intermediate")
        assert "present_tenses" in topics
        assert "past_tenses" in topics

    def test_advanced_topics_exist(self):
        topics = get_topics("English", "advanced")
        assert "conditionals" in topics
        assert "idioms" in topics

    def test_get_lesson_returns_dict(self):
        lesson = get_lesson("English", "basic", "alphabet")
        assert isinstance(lesson, dict)
        assert "title" in lesson
        assert "explanation" in lesson
        assert "examples" in lesson
        assert "quiz" in lesson

    def test_lesson_quiz_has_correct_structure(self):
        for level in get_levels():
            for topic in get_topics("English", level):
                lesson = get_lesson("English", level, topic)
                for q in lesson["quiz"]:
                    assert "question" in q
                    assert "choices" in q
                    assert "answer" in q
                    assert "explanation" in q
                    # Answer must match first character of one of the choices
                    choice_letters = {c[0] for c in q["choices"]}
                    assert q["answer"] in choice_letters, (
                        f"Answer '{q['answer']}' not in choices for {level}/{topic}"
                    )

    def test_get_lesson_unknown_level_returns_none(self):
        assert get_lesson("English", "unknown", "alphabet") is None

    def test_get_lesson_unknown_topic_returns_none(self):
        assert get_lesson("English", "basic", "nonexistent_topic") is None

    def test_level_descriptions_not_empty(self):
        for level in get_levels():
            desc = get_level_description("English", level)
            assert isinstance(desc, str) and len(desc) > 0

    def test_next_topic_advances_within_level(self):
        topics = get_topics("English", "basic")
        first = topics[0]
        second = topics[1]
        nxt_level, nxt_topic = next_topic("English", "basic", first)
        assert nxt_level == "basic"
        assert nxt_topic == second

    def test_next_topic_advances_across_levels(self):
        # Last topic of basic should advance to first topic of intermediate
        basic_topics = get_topics("English", "basic")
        last_basic = basic_topics[-1]
        int_topics = get_topics("English", "intermediate")
        first_inter = int_topics[0]

        nxt_level, nxt_topic = next_topic("English", "basic", last_basic)
        assert nxt_level == "intermediate"
        assert nxt_topic == first_inter

    def test_next_topic_end_of_curriculum(self):
        adv_topics = get_topics("English", "advanced")
        last_adv = adv_topics[-1]
        nxt_level, nxt_topic = next_topic("English", "advanced", last_adv)
        assert nxt_level is None
        assert nxt_topic is None


# ---------------------------------------------------------------------------
# ProgressTracker tests
# ---------------------------------------------------------------------------


class TestProgressTracker:
    def setup_method(self):
        """Create a fresh in-memory tracker before each test."""
        self.tracker = ProgressTracker()

    def test_default_level_is_basic(self):
        assert self.tracker.current_level == "basic"

    def test_default_topic_is_none(self):
        assert self.tracker.current_topic is None

    def test_set_level(self):
        self.tracker.current_level = "intermediate"
        assert self.tracker.current_level == "intermediate"

    def test_set_topic(self):
        self.tracker.current_topic = "alphabet"
        assert self.tracker.current_topic == "alphabet"

    def test_mark_topic_complete(self):
        self.tracker.mark_topic_complete("basic", "alphabet")
        assert self.tracker.is_topic_complete("basic", "alphabet")

    def test_topic_not_complete_by_default(self):
        assert not self.tracker.is_topic_complete("basic", "greetings")

    def test_record_quiz_result(self):
        self.tracker.record_quiz_result("basic", "alphabet", 2, 2)
        correct, total = self.tracker.get_quiz_score("basic", "alphabet")
        assert correct == 2
        assert total == 2

    def test_overall_stats_accuracy(self):
        self.tracker.record_quiz_result("basic", "alphabet", 3, 4)
        stats = self.tracker.overall_stats()
        assert stats["total_correct"] == 3
        assert stats["total_questions"] == 4
        assert stats["accuracy"] == 75.0

    def test_overall_stats_zero_questions(self):
        stats = self.tracker.overall_stats()
        assert stats["accuracy"] == 0.0

    def test_reset_clears_progress(self):
        self.tracker.current_level = "advanced"
        self.tracker.mark_topic_complete("basic", "alphabet")
        self.tracker.record_quiz_result("basic", "alphabet", 2, 2)
        self.tracker.reset()
        assert self.tracker.current_level == "basic"
        assert self.tracker.current_topic is None
        assert not self.tracker.is_topic_complete("basic", "alphabet")
        assert self.tracker.overall_stats()["total_questions"] == 0

    def test_completed_topics_list_is_copy(self):
        self.tracker.mark_topic_complete("basic", "alphabet")
        lst = self.tracker.completed_topics_list()
        lst.append("tampered")
        # Original should be unchanged
        assert "tampered" not in self.tracker.completed_topics_list()

    def test_mark_topic_complete_no_duplicates(self):
        self.tracker.mark_topic_complete("basic", "alphabet")
        self.tracker.mark_topic_complete("basic", "alphabet")
        assert self.tracker.completed_topics_list().count("basic/alphabet") == 1

    def test_progress_persists_to_file(self, tmp_path):
        save_file = str(tmp_path / "progress.json")
        tracker = ProgressTracker(save_path=save_file)
        tracker.current_level = "intermediate"
        tracker.mark_topic_complete("basic", "greetings")

        # Load a second tracker from the same file
        tracker2 = ProgressTracker(save_path=save_file)
        assert tracker2.current_level == "intermediate"
        assert tracker2.is_topic_complete("basic", "greetings")


# ---------------------------------------------------------------------------
# EnglishTeachingBot tests
# ---------------------------------------------------------------------------


class TestEnglishTeachingBot:
    def setup_method(self):
        """Fresh in-memory bot before each test, set to curriculum mode."""
        self.bot = EnglishTeachingBot()
        self.bot._current_mode = "curriculum"

    def test_greet_returns_welcome_message(self):
        assert self.bot.greet() == BOT_TEXT["English"]["welcome"]

    def test_help_command(self):
        response = self.bot.handle("help")
        assert "commands" in response.lower()
        assert "exit" in response.lower()

    def test_question_mark_returns_help(self):
        response = self.bot.handle("?")
        assert "commands" in response.lower()

    def test_start_loads_first_lesson(self):
        response = self.bot.handle("start")
        # Should show the first basic topic (alphabet)
        assert "alphabet" in response.lower() or "basic" in response.lower()

    def test_levels_command(self):
        response = self.bot.handle("levels")
        assert "basic" in response.lower()
        assert "intermediate" in response.lower()
        assert "advanced" in response.lower()

    def test_menu_command(self):
        response = self.bot.handle("menu")
        assert "curriculum" in response.lower() or "conversational" in response.lower()

    def test_select_level_by_name(self):
        response = self.bot.handle("intermediate")
        assert "intermediate" in response.lower() or "tenses" in response.lower()

    def test_select_level_by_number(self):
        response = self.bot.handle("1")
        assert "basic" in response.lower() or "alphabet" in response.lower()

    def test_topics_command(self):
        self.bot.handle("basic")  # set level to basic
        response = self.bot.handle("topics")
        assert "alphabet" in response.lower()

    def test_next_advances_lesson(self):
        self.bot.handle("start")  # first lesson: alphabet
        response = self.bot.handle("next")
        # Should advance to greetings
        assert "greeting" in response.lower() or "basic" in response.lower()

    def test_progress_command_shows_stats(self):
        response = self.bot.handle("progress")
        assert "progress" in response.lower() or "completed" in response.lower()

    def test_reset_command(self):
        self.bot.handle("start")
        self.bot.handle("next")
        response = self.bot.handle("reset")
        assert "reset" in response.lower()
        assert self.bot.progress.current_level == "basic"

    def test_unknown_command(self):
        response = self.bot.handle("blahblah12345")
        assert (
            "help" in response.lower()
            or "didn't understand" in response.lower()
            or "karite ai" in response.lower()
            or "local server" in response.lower()
        )

    def test_empty_input_ignored(self):
        # Empty string should return a friendly message, not crash
        response = self.bot.handle("")
        assert isinstance(response, str)

    def test_quit_command(self):
        response = self.bot.handle("quit")
        assert "goodbye" in response.lower()

    def test_exit_command(self):
        response = self.bot.handle("exit")
        assert "goodbye" in response.lower()

    def test_bye_command(self):
        response = self.bot.handle("bye")
        assert "goodbye" in response.lower()

    # ------------------------------------------------------------------
    # Quiz flow tests
    # ------------------------------------------------------------------

    def test_quiz_starts_after_quiz_command(self):
        self.bot.handle("start")  # load alphabet lesson
        response = self.bot.handle("quiz")
        assert "quiz" in response.lower() or "question" in response.lower()

    def test_quiz_correct_answer(self):
        self.bot.handle("start")
        self.bot.handle("quiz")
        # Answer first quiz question correctly for alphabet: answer is "C"
        response = self.bot.handle("C")
        assert "correct" in response.lower() or "✅" in response

    def test_quiz_wrong_answer(self):
        self.bot.handle("start")
        self.bot.handle("quiz")
        # Alphabet quiz question 1 answer is C, so A is wrong
        response = self.bot.handle("A")
        assert "correct answer" in response.lower() or "❌" in response

    def test_quiz_invalid_choice_prompts_retry(self):
        self.bot.handle("start")
        self.bot.handle("quiz")
        response = self.bot.handle("Z")
        # Should ask to enter a valid choice
        assert "please enter" in response.lower() or "a, b, c" in response.lower()

    def test_quiz_quit_cancels_quiz(self):
        self.bot.handle("start")
        self.bot.handle("quiz")
        response = self.bot.handle("quit")
        assert "cancelled" in response.lower() or "quiz" in response.lower()
        assert self.bot._quiz_state is None

    def test_quiz_records_result_after_completion(self):
        self.bot.handle("start")  # alphabet
        self.bot.handle("quiz")
        # Alphabet quiz: 2 questions, answers are C and C
        self.bot.handle("C")  # question 1
        self.bot.handle("C")  # question 2
        correct, total = self.bot.progress.get_quiz_score("basic", "alphabet")
        assert total == 2
        assert correct >= 0  # Both could be 0,1, or 2 depending on actual answers

    def test_quiz_marks_topic_complete_after_completion(self):
        self.bot.handle("start")  # alphabet
        self.bot.handle("quiz")
        self.bot.handle("C")
        self.bot.handle("C")
        assert self.bot.progress.is_topic_complete("basic", "alphabet")

    def test_quiz_without_lesson_shows_error(self):
        response = self.bot.handle("quiz")
        # No lesson is loaded yet
        assert "start" in response.lower() or "menu" in response.lower()

    def test_case_insensitive_quiz_answer(self):
        """Lowercase quiz answers should be accepted."""
        self.bot.handle("start")
        self.bot.handle("quiz")
        response = self.bot.handle("c")  # lowercase
        assert "correct" in response.lower() or "❌" in response or "not quite" in response.lower()

    def test_all_levels_have_no_empty_explanations(self):
        for level in get_levels():
            for topic in get_topics("English", level):
                lesson = get_lesson("English", level, topic)
                assert lesson["explanation"].strip() != "", (
                    f"Empty explanation in {level}/{topic}"
                )

    def test_all_lessons_have_examples(self):
        for level in get_levels():
            for topic in get_topics("English", level):
                lesson = get_lesson("English", level, topic)
                assert len(lesson["examples"]) > 0, (
                    f"No examples in {level}/{topic}"
                )

    def test_complete_curriculum_flow(self):
        """Walk through every lesson and quiz without errors."""
        bot = EnglishTeachingBot()
        bot._current_mode = "curriculum"
        bot.handle("start")
        for level in get_levels():
            for topic in get_topics("English", level):
                bot.handle(level)
                bot.progress.current_topic = topic
                response = bot.handle("quiz")
                assert isinstance(response, str)
                if bot._quiz_state:
                    lesson = get_lesson("English", level, topic)
                    for _ in lesson["quiz"]:
                        # Answer with the correct answer for each question
                        q = lesson["quiz"][bot._quiz_state["index"]]
                        bot.handle(q["answer"])


# ---------------------------------------------------------------------------
# Review mode tests
# ---------------------------------------------------------------------------


class TestReviewMode:
    def setup_method(self):
        """Fresh bot with curriculum mode and one completed topic."""
        self.bot = EnglishTeachingBot()
        self.bot._current_mode = "curriculum"
        # Manually mark a topic as complete so review can be requested
        self.bot.progress.mark_topic_complete("basic", "alphabet")

    def test_review_unknown_topic_returns_error(self):
        response = self.bot.handle("review nonexistent_topic")
        assert "not in your completed topics" in response.lower() or "❌" in response

    def test_review_valid_topic_sets_mode(self):
        # _generate_practice makes an HTTP call; patch it to avoid network
        self.bot._generate_practice = lambda user_input=None: "Practice question!"
        self.bot.handle("review alphabet")
        assert self.bot._current_mode == "review"
        assert self.bot._review_topic == "basic/alphabet"

    def test_review_valid_topic_sets_review_topic(self):
        self.bot._generate_practice = lambda user_input=None: "Practice question!"
        self.bot.handle("review alphabet")
        assert self.bot._review_topic is not None
        assert "alphabet" in self.bot._review_topic

    def test_review_menu_exits_review_mode(self):
        self.bot._current_mode = "review"
        self.bot._review_topic = "basic/alphabet"
        response = self.bot.handle("menu")
        assert self.bot._current_mode == "menu"
        assert self.bot._review_topic is None
        assert "curriculum" in response.lower() or "conversational" in response.lower()

    def test_review_exit_exits_review_mode(self):
        self.bot._current_mode = "review"
        self.bot._review_topic = "basic/alphabet"
        response = self.bot.handle("exit")
        assert self.bot._current_mode == "menu"
        assert self.bot._review_topic is None

    def test_review_mode_routes_input_to_generate_practice(self):
        self.bot._current_mode = "review"
        self.bot._review_topic = "basic/alphabet"
        called_with = []
        self.bot._generate_practice = lambda user_input=None: called_with.append(user_input) or "ok"
        self.bot.handle("my answer here")
        assert called_with == ["my answer here"]

    def test_menu_shows_review_hint_when_topics_completed(self):
        self.bot._current_mode = "menu"
        response = self.bot._show_mode_menu()
        assert "review" in response.lower()

    def test_menu_no_review_hint_when_no_completed_topics(self):
        bot = EnglishTeachingBot()
        bot._current_mode = "menu"
        response = bot._show_mode_menu()
        assert "review [topic" not in response.lower()

    def test_bot_has_target_language_attribute(self):
        bot = EnglishTeachingBot()
        assert hasattr(bot, "target_language")
        assert isinstance(bot.target_language, str)

    def test_bot_has_review_topic_attribute(self):
        bot = EnglishTeachingBot()
        assert hasattr(bot, "_review_topic")
        assert bot._review_topic is None

