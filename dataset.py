"""
Shared data for the Mood Machine lab.

This file defines:
- POSITIVE_WORDS: starter list of positive words
- NEGATIVE_WORDS: starter list of negative words
- SAMPLE_POSTS: short example posts for evaluation and training
- TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Word lists (starter words + my additions)
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    # added: emotions and slang seen in my new posts
    "proud",
    "hopeful",
    "blessed",
    "grateful",
    "fire",
    "lit",
    "win",
    "thrilled",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    # added
    "exhausted",
    "annoyed",
    "anxious",
    "ugh",
    "worst",
    "drained",
    "sucks",
    "miserable",
]

# Emoji / emoticon signals (used by mood_analyzer.py)
POSITIVE_EMOJIS = ["🔥", "😊", "😍", "🥳", "❤", ":)", ":-)"]
NEGATIVE_EMOJIS = ["😭", "😢", "😡", "😞", ":(", ":-("]

# ---------------------------------------------------------------------
# Labeled dataset
# ---------------------------------------------------------------------

SAMPLE_POSTS = [
    # --- starter posts ---
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    # --- my new posts ---
    "Lowkey stressed but kind of proud of myself",
    "I absolutely love getting stuck in traffic",
    "no cap that concert was fire 🔥",
    "Ugh this is the worst 😭",
    "I'm fine 🙂",
    "Got the job!!! so happy 😂",
    "not bad at all",
    "Just got back from the store",
    "Feeling blessed and grateful today",
    "so tired of this but the team is amazing",
]

# Human labels for each post above.
# Allowed labels: "positive", "negative", "neutral", "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "mixed",     # "Lowkey stressed but kind of proud of myself"
    "negative",  # "I absolutely love getting stuck in traffic" (sarcasm)
    "positive",  # "no cap that concert was fire 🔥"
    "negative",  # "Ugh this is the worst 😭"
    "neutral",   # "I'm fine 🙂" (ambiguous: could be masking a bad mood)
    "positive",  # "Got the job!!! so happy 😂"
    "positive",  # "not bad at all"
    "neutral",   # "Just got back from the store"
    "positive",  # "Feeling blessed and grateful today"
    "mixed",     # "so tired of this but the team is amazing"
]

assert len(SAMPLE_POSTS) == len(TRUE_LABELS), "SAMPLE_POSTS and TRUE_LABELS must be the same length"
