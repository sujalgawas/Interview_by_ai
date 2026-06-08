# Technical Assessment: Bare-Metal Prompt Template Engine

## Overview
AI Engineers constantly need to format complex text strings to feed into LLMs. Your task is to build a `PromptTemplate` class that parses a string, identifies the required variables, and dynamically injects values securely.

## Core Requirements

1. **Framework:** Pure Python (3.10+).
2. **Allowed Modules:** `re`, `typing`. 
3. **The `MissingVariableError` Exception:**
   * Create a custom Python Exception class named `MissingVariableError`.
4. **The `PromptTemplate` Class:**
   You must implement a class with the following methods:
   
   * `__init__(self, template_string: str)`: Initializes the template and stores the string.
   * `extract_variables(self) -> list[str]`: Scans the template string and returns a list of all unique variable names enclosed in single curly braces (e.g., `{topic}`). 
   * `format(self, **kwargs) -> str`: Accepts dynamic keyword arguments. It must replace all valid variables in the template with their corresponding values from `kwargs`.

## The Edge Cases (Crucial for Passing)
1. **Missing Variables:** If the user calls `.format()` but forgets to provide a required keyword argument, the method MUST raise your custom `MissingVariableError`.
2. **Escaped Braces (The "JSON" Problem):** AI prompts often contain JSON formatting. If the template contains double braces like `{{` or `}}`, your engine must **ignore** them (they are not variables) and format them down to single braces `{` and `}` in the final output string. 
   * *Example:* `template = "{{ 'key': '{value}' }}"`
   * *Formatted Output:* `{ 'key': 'my_value' }`

## Rules of Engagement

* **Time Limit:** 60 minutes.
* **Allowed Resources:** Google and official Python documentation. 
* **Prohibited Resources:** AI Assistants (ChatGPT, Claude, Gemini, Copilot, etc.) are **STRICTLY FORBIDDEN**.
* **Goal:** Zero runtime errors, perfect edge-case handling, and strict use of `**kwargs`.

## The Evaluation Script

Append this exact script to the bottom of your file. Your code must pass all assertions silently. 

```python
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