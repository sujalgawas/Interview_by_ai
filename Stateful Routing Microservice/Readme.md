# Technical Assessment: Stateful Routing Microservice

## Overview
This repository contains a timed technical assessment for a Junior AI Engineer position. The objective is to build a high-performance, asynchronous FastAPI microservice that functions as the backend for a multi-agent customer support system. 

The service handles incoming user queries, maintains a short-term conversational episodic memory, and conditionally routes the user to specific agent states based on intent.

## Core Requirements

* **Framework:** FastAPI (Python)
* **Memory Management:** Implement an in-memory "Episodic Memory" to store conversation context. Maintain a strict sliding window of the last **5 interactions** per `session_id`.
* **Intent Routing (Mocked LLM):** Write an asynchronous mock function `evaluate_intent(user_text: str)` to simulate LLM processing.
  * Trigger `REFUND_STATE` if the text contains "refund" or "return".
  * Trigger `ESCALATION_STATE` if the text contains "human" or "escalate".
  * Default to `GENERAL_STATE` for all other inputs.
* **State Logic:**
  * `GENERAL_STATE`: Return a generic mocked response.
  * `REFUND_STATE`: Cross-reference the current message and episodic memory for a 6-digit `order_id`. If found, return a success message. If missing, prompt the user for the Order ID.
* **API Endpoints:**
  * Method: `POST /chat/{session_id}`
  * Input Payload: `{"message": "I want a refund for my last order."}`
  * Output Payload: `{"session_id": "...", "current_state": "REFUND_STATE", "response": "Please provide your 6-digit order ID.", "memory_count": 1}`

## Rules of Engagement

* **Time Limit:** 120 minutes.
* **Allowed Resources:** Google and official Python/FastAPI documentation.
* **Prohibited Resources:** AI Assistants (ChatGPT, Claude, Gemini, Copilot, etc.) are **STRICTLY FORBIDDEN**.
* **Dependencies:** Minimal requirements (FastAPI, Uvicorn, Pydantic). No external databases; use in-memory data structures for this scope.

## Evaluation Criteria

1. **Concurrency & Async:** Proper utilization of `async/await` without blocking the main event loop.
2. **Type Safety:** Strict use of Pydantic models for data validation and comprehensive Python type hinting.
3. **Modularity:** Clean separation of concerns (Routers, State Management, Memory logic).
4. **Edge Case Handling:** * Exceeding the 5-message sliding window.
   * Handling empty string inputs.
   * Managing concurrent requests hitting the same `session_id`.

## Submission Protocol

The final codebase must be submitted as a single, consolidated text block. File paths and directories must be clearly indicated using comments (e.g., `# root/backend/services/memory.py`) above the respective code blocks to demonstrate the intended modular project structure.