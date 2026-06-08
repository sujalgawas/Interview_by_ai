# Technical Assessment: The API Retry Decorator

## Overview
AI Engineers must build resilient systems. When an LLM API returns a "429 Too Many Requests" error, the system shouldn't crash; it should wait a moment and try again, increasing the wait time with each failure (Exponential Backoff). 

Your objective is to build a Python decorator `@retry_with_backoff` that automatically handles this logic for any function it wraps.

## Core Requirements

1. **Framework:** Pure Python (3.10+).
2. **Allowed Modules:** `time`, `typing`, `functools` (Hint: you will need `functools.wraps`).
3. **Custom Exceptions:**
   * Create `RateLimitError` (Inherits from Exception).
   * Create `MaxRetriesExceededError` (Inherits from Exception).
4. **The Decorator:**
   Create a decorator named `retry_with_backoff` that accepts two arguments:
   * `retries` (int, default: 3): The maximum number of times to retry the function.
   * `initial_delay` (float, default: 1.0): The starting wait time in seconds.
   
   **The Logic:**
   * The decorator must execute the wrapped function.
   * If the function raises a `RateLimitError`, the decorator must catch it, wait for `initial_delay` seconds, and try again.
   * After every failure, the delay must **double** (e.g., 1s, then 2s, then 4s).
   * If the function raises ANY OTHER exception (e.g., `ValueError`), the decorator must NOT catch it; it should let the program crash normally.
   * If the function fails more times than the `retries` limit, the decorator must raise a `MaxRetriesExceededError`.

## Rules of Engagement

* **Time Limit:** 60 minutes.
* **Allowed Resources:** Google and official Python documentation. You may research "How to write decorators with arguments in Python."
* **Prohibited Resources:** AI Assistants (ChatGPT, Claude, Gemini, Copilot, etc.) are **STRICTLY FORBIDDEN**.
* **Goal:** Understand closures, `*args`, `**kwargs`, and function wrapping.

## The Evaluation Script

Append this exact script to the bottom of your file. Your code must pass all assertions silently. 

```python
# --- EVALUATION SCRIPT (Append this to your code) ---
import time

if __name__ == "__main__":
    
    # Trackers for testing
    execution_count = 0

    # Test 1: Successful Execution (No Retries Needed)
    @retry_with_backoff(retries=3, initial_delay=0.1)
    def fast_function():
        global execution_count
        execution_count += 1
        return "Success"

    assert fast_function() == "Success", "Failed Test 1: Function did not return correctly."
    assert execution_count == 1, "Failed Test 1: Function executed too many times."

    # Test 2: Recovers after 2 failures
    fail_count = 0
    @retry_with_backoff(retries=3, initial_delay=0.1)
    def flaky_api():
        global fail_count
        fail_count += 1
        if fail_count < 3:
            raise RateLimitError("Too many requests!")
        return "Finally Success"

    start_time = time.time()
    res2 = flaky_api()
    elapsed_time = time.time() - start_time

    assert res2 == "Finally Success", "Failed Test 2: Function did not recover."
    assert fail_count == 3, "Failed Test 2: Function did not retry the correct number of times."
    # Delay 1: 0.1s, Delay 2: 0.2s. Total wait should be roughly 0.3s.
    assert elapsed_time >= 0.3, f"Failed Test 2: Exponential backoff failed. Took {elapsed_time}s"

    # Test 3: Exhausts all retries
    @retry_with_backoff(retries=2, initial_delay=0.1)
    def doomed_api():
        raise RateLimitError("Always fails")

    try:
        doomed_api()
        assert False, "Failed Test 3: Did not raise MaxRetriesExceededError."
    except MaxRetriesExceededError:
        pass # Successfully exhausted retries

    # Test 4: Ignores other exceptions
    @retry_with_backoff(retries=3, initial_delay=0.1)
    def bad_code():
        raise ValueError("Standard error")

    try:
        bad_code()
        assert False, "Failed Test 4: Caught a ValueError instead of letting it pass."
    except ValueError:
        pass # Successfully ignored non-RateLimitErrors
    except MaxRetriesExceededError:
        assert False, "Failed Test 4: Treated ValueError like a RateLimitError."

    print("SUCCESS: All tests passed. Your system is now resilient.")