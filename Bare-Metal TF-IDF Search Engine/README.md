# Technical Assessment: Bare-Metal TF-IDF Search Engine

## Overview
This assessment evaluates your ability to implement fundamental Natural Language Processing (NLP) math using pure Python data structures. You will build an in-memory search engine that ranks documents against a user query using Term Frequency-Inverse Document Frequency (TF-IDF) and Cosine Similarity.

## Core Requirements

1. **Framework:** Pure Python 3.10+. 
2. **Allowed Modules:** `math`, `collections`, `typing`. (NO `numpy`, NO `scikit-learn`).
3. **The `MiniSearchEngine` Class:**
   You must create a class that implements the following functionality:
   
   * `__init__(self)`: Initialize any necessary data structures.
   * `fit(self, corpus: list[str]) -> None`: Takes a list of documents (strings). It must tokenize the text (lowercase, split by spaces, remove basic punctuation), calculate the Term Frequency (TF) for each document, and calculate the Inverse Document Frequency (IDF) for the entire corpus.
   * `get_vector(self, text: str) -> dict[str, float]`: Converts a single string into a TF-IDF vector (represented as a dictionary mapping words to their TF-IDF score).
   * `cosine_similarity(self, vec1: dict[str, float], vec2: dict[str, float]) -> float`: Computes the cosine similarity between two vector dictionaries.
   * `search(self, query: str, top_k: int = 1) -> list[tuple[str, float]]`: Takes a query string, vectorizes it, compares it against all documents in the fitted corpus, and returns the top `k` documents and their similarity scores, sorted highest to lowest.

## Rules of Engagement

* **Time Limit:** 60 minutes.
* **Allowed Resources:** Google and official Python documentation. You may Google the mathematical formulas for TF-IDF and Cosine Similarity if you need a refresher.
* **Prohibited Resources:** AI Assistants (ChatGPT, Claude, Gemini, Copilot, etc.) are **STRICTLY FORBIDDEN**.
* **Execution Rule:** Your code MUST run. If it throws any errors during the evaluation script, it is an automatic failure.

## The Evaluation Script

Append this exact script to the bottom of your file. Your code must pass all assertions silently and print the success message.

```python
# --- EVALUATION SCRIPT (Append this to your code) ---
if __name__ == "__main__":
    corpus = [
        "The quick brown fox jumps over the lazy dog.",
        "A fast brown fox leaps over a sleepy dog.",
        "The data scientist built a machine learning model.",
        "Machine learning and artificial intelligence are related.",
        "The quick rabbit runs away from the fox."
    ]

    engine = MiniSearchEngine()
    engine.fit(corpus)

    # Test 1: Search for a specific concept
    results = engine.search("machine learning", top_k=2)
    assert len(results) == 2, "Failed: Should return exactly top_k results."
    
    # The top result should be one of the ML sentences
    top_doc, top_score = results[0]
    assert "machine learning" in top_doc.lower(), "Failed: Did not retrieve the most relevant document."
    assert top_score > 0.0, "Failed: Score should be greater than zero for a matching query."

    # Test 2: Search for an animal
    results_animal = engine.search("quick fox", top_k=1)
    top_animal_doc, _ = results_animal[0]
    assert "fox" in top_animal_doc.lower(), "Failed: Did not retrieve the fox document."

    print("SUCCESS: All tests passed. The math and logic are sound.")