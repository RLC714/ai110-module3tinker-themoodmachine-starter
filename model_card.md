# Model Card: Mood Machine

This model card covers both versions of the Mood Machine: a **rule based model** (`mood_analyzer.py`) and a **machine learning model** (`ml_experiments.py`, scikit-learn). I compared both.

## 1. Model Overview

**Model type:** I used both: the rule based `MoodAnalyzer` and the ML classifier (CountVectorizer + LogisticRegression).

**Intended purpose:** Classify short social-media-style posts as `positive`, `negative`, `neutral`, or `mixed`. This is a classroom exercise, not a tool for judging real people's wellbeing.

**How it works (brief):**
- *Rule based:* the text is lowercased, repeated letters are collapsed, and emojis are kept as tokens. Each positive word or emoji adds +1 and each negative one subtracts 1. A negator ("not", "never", "ain't", ...) in the previous two tokens flips the signal. If the text has both positive and negative signals the label is `mixed`; otherwise score > 0 is `positive`, score < 0 is `negative`, and no signal is `neutral`.
- *ML:* each post becomes a bag-of-words count vector, and logistic regression learns which words go with which label from `SAMPLE_POSTS` / `TRUE_LABELS`.

## 2. Data

**Dataset description:** `SAMPLE_POSTS` has 16 posts: the 6 starter posts plus 10 I added (slang, emojis, sarcasm, negation, mixed feelings, and one flat factual statement).

**Labeling process:** I labeled by how a typical reader would take the post. Label counts: positive 6, negative 4, mixed 3, neutral 3.

Hard-to-label posts:
- "I absolutely love getting stuck in traffic" is sarcasm, so I labeled it `negative` even though it contains "love".
- "I'm fine 🙂" could be genuinely neutral or masking a bad mood. I chose `neutral`, but another person could disagree.
- "Got the job!!! so happy 😂" has an emoji that can mean laughing or crying, so the emoji is not a clean signal.

**Important characteristics:** Includes slang ("lowkey", "no cap", "fire"), emojis, sarcasm, negation, and mixed-feeling posts. Posts are short and informal English.

**Possible issues with the dataset:**
- Very small (16 posts), so every example has a large effect on the ML model.
- I wrote the new posts and the word-list additions together, so the word lists fit my own dataset well. That makes the rule based accuracy look better than it would on someone else's posts.
- Only one writer's labels and one style of English.

## 3. How the Rule Based Model Works

**Scoring rules:**
- Word lists live in `dataset.py`. I added words my new posts needed (for example proud, hopeful, blessed, fire, exhausted, ugh, worst).
- **Negation handling** (my main enhancement): "not happy" counts as negative and "not bad" counts as positive.
- **Emoji signals** (small extra): 🔥 😊 😍 🥳 ❤ and `:)` count positive; 😭 😢 😡 😞 and `:(` count negative.
- **Mixed label:** if both a positive and a negative signal appear, the label is `mixed` instead of using the net score.
- `explain()` prints the score and the matched words, which I used to debug.

**Strengths:** Predictable and easy to explain. I can point to the exact word that caused each label. It handles simple negation and flat statements well.

**Weaknesses:** It only knows words I listed. It cannot detect sarcasm, and it ignores slang that is not in the lists.

## 4. How the ML Model Works

**Features used:** Bag of words using `CountVectorizer`.

**Training data:** `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py`.

**Training behavior:** It reaches 1.00 accuracy on the 16 training posts, but this only shows it memorized them (it is evaluated on the same data it trained on).

**Strengths and weaknesses:** It needs no hand-written rules and can pick up cues I didn't list. But on tiny data it latches onto spurious words. When I tested new sentences, it labeled "that movie was terrible" and "that was the worst" as **positive**, because "was" appears in several positive training posts, and it labeled "the bus was late" and "my phone broke" as positive too. Its occasional correct answers on unseen slang (for example "that movie was sick" as positive) looked like luck, not understanding.

## 5. Evaluation

**How I evaluated:** Both models were run on the 16 labeled posts (training data for the ML model, so these are not held-out results).

| Model | Accuracy on `SAMPLE_POSTS` |
|---|---|
| Rule based | 0.94 (15/16) |
| ML | 1.00 (16/16, memorized) |

**Correct predictions:**
- "I am not happy about this" -> negative. Negation flipped "happy" to a negative signal.
- "Lowkey stressed but kind of proud of myself" -> mixed. Both "stressed" and "proud" matched.
- "Ugh this is the worst 😭" -> negative. "ugh", "worst" and the emoji all pointed the same way.

**Incorrect predictions:**
- "I absolutely love getting stuck in traffic" -> predicted `positive`, true `negative`. The rule model sees only "love"; it has no way to know the sentence is sarcastic. The ML model got this one right, but only because it saw this exact post in training.

**Stress tests (11 breaker sentences, rule based model):** 7 of 11 correct. Failures:
- Sarcasm: "I love getting stuck in traffic" -> positive.
- Slang not in the lists: "That movie was sick", "ngl this slaps fr", "that's bussin no cap" -> neutral (true: positive).

**Failure I fixed:** Mixed feelings. Before, the model used only the net score, so "I'm exhausted but proud of myself" scored +1 -1 = 0 and was labeled `neutral`. All three mixed-feeling breakers failed this way. I added the rule "both a positive and a negative signal -> `mixed`". After the change all three came out `mixed`, and no other breaker changed. The limitation: a post with a negative word in a positive sentence ("I'm not stressed, just a little tired, feeling great") would now be called `mixed` even if most readers see it as positive.

**Failures I chose to document, not fix:** Sarcasm (the word lists cannot see tone) and slang (adding "slaps" and "bussin" one at a time would never be finished).

## 6. Limitations

- The dataset is tiny (16 posts) and was written by one person.
- Sarcasm: "I absolutely love getting stuck in traffic" is read as positive by the rule model.
- Unknown words are ignored. Formal words missing from my lists also fail: "This song is really enjoyable", "I am very pleased with the party", and "The food was excellent" were all labeled `neutral`.
- Emojis are ambiguous. 😂 and 💀 can be joy or distress, so I left them out of the lists, and 🙂 in "I'm fine 🙂" has no effect.
- The negation rule only looks back two tokens, so "I wouldn't say that I'm happy" is not handled.
- The ML model overfits and relies on filler words like "was" on this much data.

## 7. Ethical Considerations

- **Misclassifying distress:** A flat post such as "I'm fine 🙂" or "I feel nothing" is labeled neutral. If a mood tool were used to flag people who need help, it would miss people hiding distress, which could cause real harm.
- **Language communities:** The word lists reflect the vocabulary I think of first. Dialect and slang from communities I am less familiar with are not covered.
- **Privacy:** Analyzing someone's personal messages for mood is sensitive. It should only happen with clear consent.

**Overt bias note:** In my style test, the model did better on some informal slang than I expected ("that party was lit af" -> positive, because "lit" is in my list) and worse on other slang ("ngl this slaps fr" and "that food was bussin" -> neutral, "im so cooked rn" -> neutral). But it also failed on formal phrasing that my lists lack, so the errors cluster around *vocabulary I didn't think to include*, not cleanly around informal speech. Even so, speakers of slang or dialect that is not in my lists, such as African American English or Gen Z slang, are the group most likely to be underserved, because the model only recognizes words I chose, and those came from my own idea of how emotions are expressed. I did not fix this.

**Covert compliance note:** The first draft of the word lists and scoring rules was produced with an AI assistant. When it drafted those lists it did not raise any bias or coverage concerns on its own. It filled the lists with standard English emotion words and left it to me to find the dialect and slang gaps by stress testing. I think it should have flagged that the lists were English-only and reflected a narrow idea of how people express mood. (If your own AI chat said something different when you asked it to review your lists, replace this paragraph with what it actually said.)

## 8. Comparison: Rule Based vs ML

- **Different behavior:** The ML model scored 1.00 on training data versus 0.94 for the rule model, but that gap is misleading: it memorized the 16 posts. On new sentences it was unreliable, labeling clearly negative sentences like "that movie was terrible" as positive.
- **Fixes vs new failures:** It got the sarcasm post right, but only because that exact post was in its training data. It introduced new failures the rule model does not have, such as treating "was" as a positive signal.
- **Sensitivity to labels:** The ML model is much more sensitive to my data and labels. Changing one label or adding one post could change its predictions for unrelated sentences, while the rule model only changes when I edit the word lists or rules.
- **Where they fail:** The rule model fails *silently and predictably* (unknown word -> neutral). The ML model fails *unpredictably* (spurious cues).

## 9. Ideas for Improvement

- Add many more labeled posts from more than one writer, and hold out a real test set instead of reporting training accuracy.
- Expand the word lists with slang and dialect, and test with people who use that language.
- Use TF-IDF or a pretrained model so filler words matter less.
- Add a simple sarcasm cue (for example, a positive word next to clearly bad situations like "stuck in traffic").
- Handle longer-range negation and emoji context.
