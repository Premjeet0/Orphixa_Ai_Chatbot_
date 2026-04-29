# 🤖 Orphixa AI

> An intelligent Python chatbot featuring NLP, intent detection, sentiment analysis, conversation memory, and a web interface.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Tests](https://img.shields.io/badge/Tests-Pytest-orange)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **NLP Engine** | Custom TF-IDF cosine similarity intent classifier — no external ML library needed |
| 🎯 **Intent Detection** | Recognises 15+ intent categories (greetings, jokes, math, facts, and more) |
| 😊 **Sentiment Analysis** | Detects positive / negative / neutral tone with negation handling |
| 🧮 **Math Evaluator** | Safely evaluates arithmetic expressions from natural language |
| 💾 **Conversation Memory** | Stores recent exchanges and exports them to JSON |
| 🌐 **Web Interface** | Full dark-mode chat UI via Flask with a REST API |
| 🧪 **Test Suite** | 25+ unit tests covering all core modules |
| 🖥️ **CLI Mode** | Colour terminal chat with no browser required |

---

## 📁 Project Structure

```
orphixa_ai/
├── orphixa.py          # Core chatbot engine (NLP, intents, sentiment, memory)
├── app.py              # Flask web server + chat UI
├── tests.py            # Pytest test suite
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/orphixa-ai.git
cd orphixa-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 💬 Run as CLI Chatbot

```bash
python orphixa.py
```

```
  ╔═══════════════════════════════════════════════════╗
  ║        🤖  O R P H I X A   A I  🤖               ║
  ║            Intelligent Chatbot v1.0               ║
  ╚═══════════════════════════════════════════════════╝

  You  › hello
  Orphixa › Hey there! I'm Orphixa, your AI assistant. How can I help you today?

  You  › what is 24 * 7
  Orphixa › 🧮 24 * 7 = 168

  You  › tell me a joke
  Orphixa › Why do programmers prefer dark mode? Because light attracts bugs! 🐛
```

**Special CLI commands:**

| Command | Action |
|---|---|
| `save` | Exports conversation history to `orphixa_memory.json` |
| `history` | Shows the last 6 exchanges |
| `bye` / `exit` | Ends the session |

---

## 🌐 Run as Web App

```bash
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

### REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Chat web interface |
| `POST` | `/chat` | Send a message, get a response |
| `GET` | `/history` | Retrieve conversation history |
| `GET` | `/health` | Health check |

**Example API call:**

```bash
curl -X POST http://127.0.0.1:5000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "tell me a fun fact"}'
```

```json
{
  "response": "🌊 Fun fact: More than 80% of Earth's oceans remain unexplored.",
  "intent": "detected"
}
```

---

## 🧪 Run Tests

```bash
python -m pytest tests.py -v
```

Expected output:
```
tests.py::test_tokenize_basic         PASSED
tests.py::test_sentiment_positive     PASSED
tests.py::test_math_addition          PASSED
tests.py::test_intent_greeting        PASSED
...
25 passed in 0.45s
```

---

## 🧠 AI Concepts Used

### 1. TF-IDF Vectorisation
Each intent pattern is converted into a TF-IDF vector. User input is similarly vectorised and compared against all patterns using **cosine similarity** to find the best matching intent — all implemented from scratch without any ML library.

### 2. Intent Classification
A knowledge base of 15+ intents with multiple patterns each. The NLP engine ranks candidates by cosine similarity score, with a configurable confidence threshold and a regex-based fallback.

### 3. Sentiment Analysis
A lexicon-based approach using curated positive/negative word sets with **negation handling** (e.g. "not happy" → negative).

### 4. Conversation Memory
A sliding window deque stores the last N exchanges, enabling context-aware responses and exportable session history.

### 5. Safe Math Evaluation
A regex extractor isolates numeric expressions which are evaluated in a sandboxed `eval()` with no access to builtins.

---

## ☁️ Deploy to GitHub — Step by Step

```bash
# 1. Initialise the repo
git init
git add .
git commit -m "🤖 Initial release: Orphixa AI v1.0"

# 2. Create a new repo on GitHub (github.com → New repository → name: orphixa-ai)

# 3. Link and push
git remote add origin https://github.com/YOUR_USERNAME/orphixa-ai.git
git branch -M main
git push -u origin main
```

---

## 🛣️ Roadmap

- [ ] Integrate OpenAI / Anthropic API for advanced responses
- [ ] Add live weather via OpenWeatherMap API
- [ ] Persistent memory across sessions (SQLite)
- [ ] Voice input/output support
- [ ] Docker containerisation
- [ ] Deploy to Render / Railway / Vercel

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<p align="center">Built with ❤️ and Python · <strong>Orphixa AI v1.0</strong></p>
