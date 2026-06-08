#main.py
from engine import PromptTemplate, MissingVariableError

# --- EVALUATION SCRIPT (Append this to your code) ---
if __name__ == "__main__":
    
    # Test 1: Basic Extraction
    t1 = PromptTemplate("Tell me a {adjective} joke about {subject}.")
    vars1 = t1.extract_variables()
    assert set(vars1) == {"adjective", "subject"}, f"Failed Test 1: Got {vars1}"

    # Test 2: Standard Formatting using **kwargs
    res1 = t1.format(adjective="funny", subject="robots", extra_arg="ignored")
    assert res1 == "Tell me a funny joke about robots.", f"Failed Test 2: Got {res1}"

    # Test 3: Missing Kwarg Exception
    try:
        t1.format(adjective="sad") # Missing 'subject'
        assert False, "Failed Test 3: Did not raise MissingVariableError."
    except MissingVariableError:
        pass # Successfully caught the custom exception

    # Test 4: Escaped Braces (The JSON Edge Case)
    t2 = PromptTemplate("System: Output JSON {{'name': '{user_name}'}}")
    res2 = t2.format(user_name="Alice")
    assert res2 == "System: Output JSON {'name': 'Alice'}", f"Failed Test 4: Got {res2}"

    print("SUCCESS: All tests passed. Your Python fundamentals are solidifying.")