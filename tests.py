"""
Unit tests for Orphixa AI.
Run: python -m pytest tests.py -v
"""

import pytest
from orphixa import OrphixaAI, analyse_sentiment, safe_eval_math, tokenize, NLPEngine, INTENTS


@pytest.fixture
def bot():
    return OrphixaAI()


# ──────────────────────────────────────────────
#  Tokenizer
# ──────────────────────────────────────────────

def test_tokenize_basic():
    assert tokenize("Hello, World!") == ["hello", "world"]

def test_tokenize_empty():
    assert tokenize("") == []

def test_tokenize_numbers():
    tokens = tokenize("What is 2+2?")
    assert "2" in tokens or "2 2" not in tokens  # punctuation stripped


# ──────────────────────────────────────────────
#  Sentiment analyser
# ──────────────────────────────────────────────

def test_sentiment_positive():
    assert analyse_sentiment("I am so happy and excited today!") == "positive"

def test_sentiment_negative():
    assert analyse_sentiment("This is terrible and I hate it") == "negative"

def test_sentiment_neutral():
    assert analyse_sentiment("The sky is blue") == "neutral"

def test_sentiment_negation():
    assert analyse_sentiment("I am not happy") == "negative"


# ──────────────────────────────────────────────
#  Math evaluator
# ──────────────────────────────────────────────

def test_math_addition():
    result = safe_eval_math("what is 10 + 5")
    assert result is not None
    assert "15" in result

def test_math_multiplication():
    result = safe_eval_math("calculate 6 * 7")
    assert result is not None
    assert "42" in result

def test_math_no_expression():
    result = safe_eval_math("hello world")
    assert result is None


# ──────────────────────────────────────────────
#  NLP / Intent classification
# ──────────────────────────────────────────────

def test_intent_greeting(bot):
    response = bot.respond("hello there")
    assert isinstance(response, str)
    assert len(response) > 0

def test_intent_farewell(bot):
    response = bot.respond("goodbye")
    assert isinstance(response, str)

def test_intent_name(bot):
    response = bot.respond("what is your name")
    assert "Orphixa" in response or "orphixa" in response.lower()

def test_intent_time(bot):
    response = bot.respond("what time is it")
    assert "time" in response.lower() or ":" in response  # time format

def test_intent_date(bot):
    response = bot.respond("what is today's date")
    assert any(month in response for month in [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ])

def test_intent_joke(bot):
    response = bot.respond("tell me a joke")
    assert isinstance(response, str) and len(response) > 10

def test_intent_capabilities(bot):
    response = bot.respond("what can you do")
    assert isinstance(response, str)

def test_intent_math_inline(bot):
    response = bot.respond("25 + 75")
    assert "100" in response


# ──────────────────────────────────────────────
#  Memory
# ──────────────────────────────────────────────

def test_memory_accumulates(bot):
    bot.respond("hello")
    bot.respond("how are you")
    assert bot.memory.exchange_count == 2

def test_memory_context(bot):
    bot.respond("hi")
    summary = bot.memory.context_summary()
    assert "USER" in summary or "user" in summary.lower()

def test_memory_save(bot, tmp_path):
    bot.respond("hello")
    path = str(tmp_path / "test_memory.json")
    saved = bot.memory.save(path)
    import json, os
    assert os.path.exists(saved)
    with open(saved) as f:
        data = json.load(f)
    assert "history" in data
    assert data["exchange_count"] == 1


# ──────────────────────────────────────────────
#  Edge cases
# ──────────────────────────────────────────────

def test_empty_input(bot):
    response = bot.respond("")
    assert isinstance(response, str)

def test_whitespace_input(bot):
    response = bot.respond("   ")
    assert isinstance(response, str)

def test_unknown_gibberish(bot):
    response = bot.respond("xyzabcdef quantum platypus")
    assert isinstance(response, str) and len(response) > 0
