#!/usr/bin/env python3
"""
Karite English Teaching Chatbot – CLI entry point.

Run with:
    python main.py
"""

import sys


def main():
    # Import here so that the package is importable from the project root
    from chatbot import EnglishTeachingBot

    bot = EnglishTeachingBot(save_path=".progress.json")

    print(bot.greet())
    print()

    while True:
        try:
            mode = bot._current_mode
            if mode == "curriculum":
                prompt = "[📚 Curriculum] You: "
            elif mode == "conversational":
                prompt = "[💬 Sandbox] You: "
            else:
                prompt = "You: "
            user_input = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Keep practicing your English. 👋")
            sys.exit(0)

        if not user_input:
            continue

        response = bot.handle(user_input)
        print(f"\nBot: {response}\n")

        cmd = user_input.lower()
        if cmd in ("quit", "bye") or (
            cmd == "exit" and bot._current_mode != "conversational"
        ):
            sys.exit(0)


if __name__ == "__main__":
    main()
