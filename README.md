# 🇬🇧 Karite English Teaching Chatbot

An interactive command-line chatbot that teaches English from **basic to advanced** level. No internet connection or API keys required — everything runs locally.

---

## Features

| Level | Topics |
|---|---|
| **Basic** | Alphabet, Greetings, Numbers, Everyday Vocabulary, Basic Sentences |
| **Intermediate** | Present/Past/Future Tenses, Prepositions, Intermediate Vocabulary |
| **Advanced** | Conditionals, Passive Voice, Reported Speech, Idioms & Phrasal Verbs, Academic Writing |

- **Interactive lessons** with clear explanations and real-world examples
- **Multiple-choice quizzes** after every lesson with instant feedback
- **Progress tracking** — your progress is saved to `.progress.json` automatically
- **Curriculum navigation** — jump between levels and topics freely

---

## Requirements

- Python 3.8 or higher (no external dependencies for the chatbot itself)
- `pytest` for running tests (optional)

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/coldfront96/karite_project.git
cd karite_project

# Run the chatbot
python main.py
```

---

## Usage

Once running, type commands at the `You:` prompt:

| Command | Description |
|---|---|
| `start` | Start or resume your learning journey |
| `menu` | Show all levels and topics |
| `levels` | List difficulty levels |
| `topics` | List topics in the current level |
| `basic` / `intermediate` / `advanced` | Jump to a level |
| `next` | Advance to the next lesson |
| `quiz` | Take the quiz for the current lesson |
| `progress` | View completed topics and quiz scores |
| `reset` | Reset all progress |
| `help` | Show the help message |
| `quit` / `exit` / `bye` | Exit the chatbot |

---

## Example Session

```
You: start

Bot:
──────────────────────────────────────────────────────────────
  Level: BASIC  |  Topic: The English Alphabet
──────────────────────────────────────────────────────────────

The English alphabet has 26 letters:
  Vowels (5):   A  E  I  O  U
  ...

You: quiz

Bot:
  Quiz  (1/2)
  How many letters are in the English alphabet?

    A) 24
    B) 25
    C) 26
    D) 28

  Type the letter of your answer (A, B, C, or D):

You: C

Bot: ✅  Correct!
  💡 There are 26 letters in the English alphabet.
  ...
```

---

## Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

---

## Project Structure

```
karite_project/
├── chatbot/
│   ├── __init__.py       # Package entry point
│   ├── bot.py            # Core chatbot logic & conversation handler
│   ├── curriculum.py     # All lesson content (basic → advanced)
│   └── progress.py       # Progress tracking (in-memory + JSON persistence)
├── tests/
│   ├── __init__.py
│   └── test_bot.py       # Comprehensive test suite
├── main.py               # CLI entry point
├── requirements.txt      # Dependencies
└── README.md
```
