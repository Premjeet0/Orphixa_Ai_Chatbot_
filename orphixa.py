"""
Orphixa AI - A Python chatbot with NLP, intent detection, sentiment analysis,
memory, and a conversational AI personality.
"""

import os
import json
import datetime
import random
import re
import math
from collections import defaultdict, deque


# ─────────────────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────────────────

CONFIG = {
    "name": "Orphixa",
    "version": "1.0.0",
    "max_memory": 20,          # last N exchanges remembered
    "confidence_threshold": 0.35,
}

COLORS = {
    "cyan":   "\033[96m",
    "green":  "\033[92m",
    "yellow": "\033[93m",
    "red":    "\033[91m",
    "blue":   "\033[94m",
    "purple": "\033[95m",
    "reset":  "\033[0m",
    "bold":   "\033[1m",
    "dim":    "\033[2m",
}


# ─────────────────────────────────────────────────────────
#  INTENT KNOWLEDGE BASE
# ─────────────────────────────────────────────────────────

INTENTS = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "good morning", "good evening",
                     "good afternoon", "howdy", "what's up", "sup", "greetings"],
        "responses": [
            "Hey there! I'm Orphixa, your AI assistant. How can I help you today?",
            "Hello! Great to see you. What's on your mind?",
            "Hi! Orphixa here — ready to assist. What can I do for you?",
            "Hey! Happy to chat. What would you like to explore?",
        ],
    },
    "farewell": {
        "patterns": ["bye", "goodbye", "see you", "take care", "later",
                     "farewell", "quit", "exit", "cya", "ttyl"],
        "responses": [
            "Goodbye! It was a pleasure chatting. Come back anytime!",
            "See you later! Stay curious.",
            "Take care! Orphixa will be here whenever you need me.",
            "Bye! Don't hesitate to return if you have more questions.",
        ],
    },
    "thanks": {
        "patterns": ["thanks", "thank you", "thx", "ty", "appreciate it",
                     "cheers", "much appreciated", "helpful"],
        "responses": [
            "You're very welcome! Glad I could help.",
            "Anytime! That's what I'm here for.",
            "Happy to help! Let me know if you need anything else.",
            "No problem at all!",
        ],
    },
    "name": {
        "patterns": ["what is your name", "who are you", "what are you called",
                     "your name", "tell me your name", "what should i call you"],
        "responses": [
            "I'm Orphixa AI — an intelligent chatbot built to assist, converse, and learn with you!",
            "My name is Orphixa. I'm an AI assistant created to help you with questions, conversations, and tasks.",
        ],
    },
    "capabilities": {
        "patterns": ["what can you do", "your capabilities", "help me", "features",
                     "what do you know", "abilities", "skills", "how can you help"],
        "responses": [
            (
                "Here's what I can do:\n"
                "  🧠  Answer general knowledge questions\n"
                "  💬  Hold natural conversations\n"
                "  😊  Detect your sentiment and adapt\n"
                "  🧮  Do basic math calculations\n"
                "  🕐  Tell you the current time & date\n"
                "  🌤  Share a fun fact or joke\n"
                "  📚  Remember our conversation context\n"
                "  🔍  Understand intent from your words\n"
                "\nJust type anything to get started!"
            ),
        ],
    },
    "time": {
        "patterns": ["what time is it", "current time", "tell me the time", "time now"],
        "responses": ["__TIME__"],
    },
    "date": {
        "patterns": ["what is the date", "today's date", "what day is it",
                     "current date", "date today"],
        "responses": ["__DATE__"],
    },
    "joke": {
        "patterns": ["tell me a joke", "joke", "make me laugh", "something funny",
                     "funny", "humor me"],
        "responses": [
            "Why don't scientists trust atoms?\nBecause they make up everything! 😄",
            "I told my computer I needed a break.\nNow it won't stop sending me Kit-Kat ads. 😂",
            "Why do programmers prefer dark mode?\nBecause light attracts bugs! 🐛",
            "A SQL query walks into a bar, walks up to two tables and asks...\n'Can I join you?' 😆",
            "Why did the robot go on a diet?\nBecause it had too many bytes! 🤖",
        ],
    },
    "fact": {
        "patterns": ["fun fact", "random fact", "tell me something interesting",
                     "interesting fact", "did you know", "trivia"],
        "responses": [
            "🌍 Fun fact: Honey never spoils. Archaeologists found 3,000-year-old honey in Egyptian tombs that was still edible!",
            "🧠 Fun fact: Your brain generates about 12–25 watts of electricity — enough to power a low-watt LED bulb.",
            "🐙 Fun fact: Octopuses have three hearts and blue blood!",
            "🌊 Fun fact: More than 80% of Earth's oceans remain unexplored.",
            "🚀 Fun fact: A day on Venus is longer than a year on Venus — it rotates slower than it orbits the Sun.",
            "🐦 Fun fact: Crows can recognize human faces and hold grudges against people who wrong them.",
        ],
    },
    "math": {
        "patterns": ["calculate", "what is \\d", "compute", "solve",
                     "math", "\\d+\\s*[+\\-*/]\\s*\\d+"],
        "responses": ["__MATH__"],
    },
    "weather": {
        "patterns": ["weather", "temperature", "forecast", "rain", "sunny", "cold", "hot"],
        "responses": [
            "I don't have live weather data, but you can check:\n"
            "  • https://weather.com\n"
            "  • https://openweathermap.org\n\n"
            "If you integrate an API key, I can fetch live weather for you!",
        ],
    },
    "age": {
        "patterns": ["how old are you", "your age", "when were you created", "when were you born"],
        "responses": [
            "I was born the moment someone wrote my first line of code — so I'm perpetually version 1.0! 😄",
            "Age is just a number — but I'm Orphixa v1.0.0, fresh and ready to learn!",
        ],
    },
    "feeling": {
        "patterns": ["how are you", "how do you feel", "are you okay", "you good",
                     "how's it going", "how are you doing"],
        "responses": [
            "I'm doing great, thanks for asking! I'm always energized when I get to have a good conversation.",
            "Running at full capacity and feeling fantastic! How about you?",
            "I'm wonderful! Every conversation is a new adventure for me.",
        ],
    },
    "creator": {
        "patterns": ["who made you", "who created you", "who built you",
                     "who is your creator", "who programmed you"],
        "responses": [
            "I was created with Python and a passion for AI! My creator built me to be a helpful and intelligent assistant.",
            "I'm a Python-powered AI chatbot — crafted with love, logic, and a touch of machine intelligence!",
        ],
    },
    "positive_emotion": {
        "patterns": ["i am happy", "i feel great", "wonderful", "awesome",
                     "i love this", "this is amazing", "excellent"],
        "responses": [
            "That's wonderful to hear! Your positive energy is contagious 😊",
            "Love that! Keep that great energy going!",
            "Amazing! It's always great to hear you're doing well.",
        ],
    },
    "negative_emotion": {
        "patterns": ["i am sad", "i feel down", "depressed", "frustrated",
                     "i hate this", "terrible", "awful", "i'm not okay"],
        "responses": [
            "I'm sorry to hear that. Remember, it's okay to have tough days. Is there anything I can help with?",
            "That sounds rough. I'm here to listen if you want to talk about it.",
            "I hear you. Sometimes just having a conversation helps. What's going on?",
        ],
    },
}


# ─────────────────────────────────────────────────────────
#  NLP ENGINE — TF-IDF-like cosine similarity matcher
# ─────────────────────────────────────────────────────────

def tokenize(text: str) -> list[str]:
    """Lowercase, remove punctuation, split into tokens."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return text.split()


def build_vocab(corpus: list[list[str]]) -> dict[str, int]:
    vocab = {}
    idx = 0
    for tokens in corpus:
        for t in tokens:
            if t not in vocab:
                vocab[t] = idx
                idx += 1
    return vocab


def tf(tokens: list[str]) -> dict[str, float]:
    counts: dict[str, int] = defaultdict(int)
    for t in tokens:
        counts[t] += 1
    total = len(tokens) or 1
    return {t: c / total for t, c in counts.items()}


def idf(vocab: dict[str, int], corpus: list[list[str]]) -> dict[str, float]:
    N = len(corpus)
    df: dict[str, int] = defaultdict(int)
    for doc in corpus:
        seen = set(doc)
        for t in seen:
            df[t] += 1
    return {t: math.log((N + 1) / (df.get(t, 0) + 1)) + 1 for t in vocab}


def vectorize(tokens: list[str], vocab: dict[str, int], idf_scores: dict[str, float]) -> list[float]:
    tf_scores = tf(tokens)
    vec = [0.0] * len(vocab)
    for t, i in vocab.items():
        vec[i] = tf_scores.get(t, 0.0) * idf_scores.get(t, 0.0)
    return vec


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x ** 2 for x in a))
    mag_b = math.sqrt(sum(x ** 2 for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


class NLPEngine:
    """
    Builds a TF-IDF vector space from intent patterns and classifies
    user input using cosine similarity.
    """

    def __init__(self, intents: dict):
        self.intents = intents
        self._build_index()

    def _build_index(self):
        self.label_patterns: list[tuple[str, list[str]]] = []
        corpus: list[list[str]] = []

        for intent, data in self.intents.items():
            for pattern in data["patterns"]:
                tokens = tokenize(pattern)
                self.label_patterns.append((intent, tokens))
                corpus.append(tokens)

        self.vocab = build_vocab(corpus)
        self.idf_scores = idf(self.vocab, corpus)
        self.pattern_vectors = [
            vectorize(tokens, self.vocab, self.idf_scores)
            for _, tokens in self.label_patterns
        ]

    def classify(self, text: str) -> tuple[str, float]:
        """Return (intent_name, confidence_score)."""
        tokens = tokenize(text)
        query_vec = vectorize(tokens, self.vocab, self.idf_scores)

        best_intent = "unknown"
        best_score = 0.0

        for i, pattern_vec in enumerate(self.pattern_vectors):
            score = cosine_similarity(query_vec, pattern_vec)
            if score > best_score:
                best_score = score
                best_intent = self.label_patterns[i][0]

        # Fallback: direct keyword scan for low-confidence matches
        if best_score < CONFIG["confidence_threshold"]:
            lower = text.lower()
            for intent, data in self.intents.items():
                for pattern in data["patterns"]:
                    if re.search(pattern, lower):
                        return intent, 0.6

        return best_intent, best_score


# ─────────────────────────────────────────────────────────
#  SENTIMENT ANALYSER
# ─────────────────────────────────────────────────────────

POSITIVE_WORDS = {
    "happy", "great", "wonderful", "amazing", "love", "excellent",
    "fantastic", "awesome", "good", "nice", "brilliant", "beautiful",
    "joy", "glad", "excited", "perfect", "best", "fun", "helpful",
}

NEGATIVE_WORDS = {
    "sad", "bad", "hate", "terrible", "awful", "horrible", "worst",
    "angry", "frustrated", "upset", "disappointed", "useless", "broken",
    "ugly", "stupid", "trash", "fail", "error", "problem", "wrong",
}

NEGATIONS = {"not", "no", "never", "don't", "doesn't", "isn't", "wasn't", "can't"}


def analyse_sentiment(text: str) -> str:
    tokens = tokenize(text)
    score = 0
    negate = False

    for token in tokens:
        if token in NEGATIONS:
            negate = True
            continue
        if token in POSITIVE_WORDS:
            score += -1 if negate else 1
        elif token in NEGATIVE_WORDS:
            score += 1 if negate else -1
        negate = False

    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    return "neutral"


# ─────────────────────────────────────────────────────────
#  MATH EVALUATOR
# ─────────────────────────────────────────────────────────

def safe_eval_math(text: str) -> str | None:
    """Extract and safely evaluate a math expression from text."""
    expression = re.search(r"[\d\s\+\-\*/\(\)\.]+", text)
    if not expression:
        return None
    expr = expression.group().strip()
    if not expr or len(expr) < 3:
        return None
    try:
        # Only allow safe characters
        if re.fullmatch(r"[\d\s\+\-\*/\(\)\.]+", expr):
            result = eval(expr, {"__builtins__": {}})  # noqa: S307
            return f"🧮 {expr.strip()} = **{result}**"
    except Exception:
        pass
    return None


# ─────────────────────────────────────────────────────────
#  CONVERSATION MEMORY
# ─────────────────────────────────────────────────────────

class Memory:
    def __init__(self, maxlen: int = 20):
        self.history: deque = deque(maxlen=maxlen)
        self.session_start = datetime.datetime.now()
        self.exchange_count = 0

    def add(self, role: str, text: str):
        self.history.append({"role": role, "text": text,
                              "ts": datetime.datetime.now().isoformat()})
        if role == "user":
            self.exchange_count += 1

    def context_summary(self) -> str:
        if not self.history:
            return ""
        recent = list(self.history)[-6:]
        lines = [f"  {m['role'].upper()}: {m['text'][:80]}" for m in recent]
        return "\n".join(lines)

    def save(self, filepath: str = "orphixa_memory.json"):
        data = {
            "session_start": self.session_start.isoformat(),
            "exchange_count": self.exchange_count,
            "history": list(self.history),
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        return filepath


# ─────────────────────────────────────────────────────────
#  ORPHIXA CHATBOT CORE
# ─────────────────────────────────────────────────────────

class OrphixaAI:
    def __init__(self):
        self.nlp = NLPEngine(INTENTS)
        self.memory = Memory(CONFIG["max_memory"])
        self.name = CONFIG["name"]

    def _resolve_response(self, intent: str, user_input: str) -> str:
        responses = INTENTS[intent]["responses"]
        response = random.choice(responses)

        if response == "__TIME__":
            now = datetime.datetime.now()
            return f"🕐 The current time is **{now.strftime('%I:%M %p')}**."

        if response == "__DATE__":
            now = datetime.datetime.now()
            return f"📅 Today is **{now.strftime('%A, %B %d, %Y')}**."

        if response == "__MATH__":
            result = safe_eval_math(user_input)
            return result if result else "I couldn't find a valid math expression. Try: 'calculate 25 * 4'"

        return response

    def _unknown_response(self, user_input: str, sentiment: str) -> str:
        if sentiment == "negative":
            return (
                "I noticed some frustration there — I'm sorry I couldn't quite understand. "
                "Could you rephrase your question? I'm here to help!"
            )
        options = [
            f"Hmm, I'm not quite sure how to respond to that. Could you elaborate?",
            f"That's an interesting one! I don't have a good answer yet — try asking differently.",
            f"I'm still learning! I didn't catch that. Want to try a different question?",
            f"Oops, that went over my circuits! Could you rephrase that for me?",
        ]
        return random.choice(options)

    def respond(self, user_input: str) -> str:
        user_input = user_input.strip()
        if not user_input:
            return "I didn't catch that — feel free to type something!"

        self.memory.add("user", user_input)
        sentiment = analyse_sentiment(user_input)
        intent, confidence = self.nlp.classify(user_input)

        # Math shortcut — detect expressions directly
        if re.search(r"\d+\s*[+\-*/]\s*\d+", user_input):
            result = safe_eval_math(user_input)
            if result:
                response = result
                self.memory.add("orphixa", response)
                return response

        if intent == "unknown" or confidence < CONFIG["confidence_threshold"]:
            response = self._unknown_response(user_input, sentiment)
        else:
            response = self._resolve_response(intent, user_input)

        # Add sentiment-aware prefix for positive input
        if sentiment == "positive" and intent not in ("positive_emotion", "greeting"):
            prefix = random.choice(["😊 ", "✨ ", ""])
            response = prefix + response

        self.memory.add("orphixa", response)
        return response


# ─────────────────────────────────────────────────────────
#  CLI INTERFACE
# ─────────────────────────────────────────────────────────

def print_banner():
    c = COLORS
    banner = f"""
{c['cyan']}{c['bold']}
  ╔═══════════════════════════════════════════════════╗
  ║                                                   ║
  ║        🤖  O R P H I X A   A I  🤖               ║
  ║            Intelligent Chatbot v1.0               ║
  ║                                                   ║
  ╚═══════════════════════════════════════════════════╝
{c['reset']}
{c['dim']}  Built with Python · NLP · Intent Detection · Sentiment Analysis{c['reset']}
{c['dim']}  Type 'help' for capabilities · 'bye' to quit · 'save' to export memory{c['reset']}
"""
    print(banner)


def main():
    print_banner()
    bot = OrphixaAI()
    c = COLORS

    while True:
        try:
            user_input = input(f"{c['green']}{c['bold']}  You  ›{c['reset']} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{c['cyan']}  Orphixa ›{c['reset']} Goodbye! Session ended.\n")
            break

        if not user_input:
            continue

        # Special CLI commands
        if user_input.lower() == "save":
            path = bot.memory.save()
            print(f"{c['yellow']}  [System] Memory saved to {path}{c['reset']}\n")
            continue

        if user_input.lower() == "history":
            summary = bot.memory.context_summary()
            print(f"{c['yellow']}  [Recent context]\n{summary}{c['reset']}\n")
            continue

        if user_input.lower() in ("exit", "quit"):
            user_input = "bye"

        response = bot.respond(user_input)
        print(f"\n{c['cyan']}{c['bold']}  Orphixa ›{c['reset']} {response}\n")

        if any(kw in user_input.lower() for kw in ("bye", "goodbye", "farewell")):
            print(f"{c['dim']}  [Session: {bot.memory.exchange_count} exchanges]{c['reset']}\n")
            break


if __name__ == "__main__":
    main()
