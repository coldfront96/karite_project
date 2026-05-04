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
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Keep practicing your English. 👋")
            sys.exit(0)

        if not user_input:
            continue

        response = bot.handle(user_input)
        print(f"\nBot: {response}\n")

        if user_input.lower() in ("quit", "exit", "bye"):
            sys.exit(0)


if __name__ == "__main__":
    main()
