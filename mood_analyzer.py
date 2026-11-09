# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

Pipeline:
- preprocess: lowercase, normalize repeated letters, keep emojis as tokens
- score_text: +1 for positive signals, -1 for negative signals,
              with simple negation handling ("not happy" counts as negative)
- predict_label: positive / negative / neutral / mixed
"""

import re
from typing import List, Optional, Tuple

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS, POSITIVE_EMOJIS, NEGATIVE_EMOJIS

NEGATORS = {
    "not", "no", "never", "dont", "don't", "isn't", "isnt", "aint", "ain't",
    "wasn't", "wasnt", "cant", "can't", "didn't", "didnt", "won't", "wont",
}

# words, emoticons like :) or :-(, and any single non-ASCII character (emoji)
TOKEN_PATTERN = re.compile(r":-?\)|:-?\(|[a-z0-9']+|[^\x00-\x7f]")


class MoodAnalyzer:
    """A simple, rule based mood classifier."""

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)
        self.positive_emojis = set(POSITIVE_EMOJIS)
        self.negative_emojis = set(NEGATIVE_EMOJIS)

    # ---------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------
    def preprocess(self, text: str) -> List[str]:
        """
        Lowercase, collapse 3+ repeated characters to 2 ("soooo" -> "soo"),
        drop ASCII punctuation, and keep emojis/emoticons as their own tokens.
        """
        cleaned = text.strip().lower()
        cleaned = re.sub(r"(.)\1{2,}", r"\1\1", cleaned)
        tokens = TOKEN_PATTERN.findall(cleaned)
        # drop invisible emoji modifiers (variation selectors / joiners)
        return [t for t in tokens if t not in ("️", "‍")]

    # ---------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------
    def _analyze(self, text: str) -> Tuple[int, List[str], List[str]]:
        """Return (score, positive_hits, negative_hits) for the text."""
        tokens = self.preprocess(text)
        positive_hits: List[str] = []
        negative_hits: List[str] = []

        for i, token in enumerate(tokens):
            polarity = 0
            if token in self.positive_words or token in self.positive_emojis:
                polarity = 1
            elif token in self.negative_words or token in self.negative_emojis:
                polarity = -1
            if polarity == 0:
                continue

            # Negation: a negator in the previous two tokens flips the signal
            # ("not happy" -> negative, "not bad" -> positive).
            if any(t in NEGATORS for t in tokens[max(0, i - 2):i]):
                polarity = -polarity
                token = f"not {token}"

            if polarity > 0:
                positive_hits.append(token)
            else:
                negative_hits.append(token)

        score = len(positive_hits) - len(negative_hits)
        return score, positive_hits, negative_hits

    def score_text(self, text: str) -> int:
        """Net mood score: positive signals minus negative signals."""
        score, _, _ = self._analyze(text)
        return score

    # ---------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------
    def predict_label(self, text: str) -> str:
        """
        - both positive and negative signals present -> "mixed"
        - otherwise score > 0 -> "positive", score < 0 -> "negative"
        - no signals (or they cancel with none of either) -> "neutral"
        """
        score, pos, neg = self._analyze(text)
        if pos and neg:
            return "mixed"
        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------
    # Explanations
    # ---------------------------------------------------------------
    def explain(self, text: str) -> str:
        """Short human readable reason for the prediction."""
        score, pos, neg = self._analyze(text)
        return (
            f"Score = {score} "
            f"(positive: {pos or '[]'}, negative: {neg or '[]'})"
        )
