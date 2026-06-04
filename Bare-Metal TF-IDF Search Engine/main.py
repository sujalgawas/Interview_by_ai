#main.py
from engine import MiniSearchEngine

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