# Technical Assessment: Agentic Workflow DAG Executor

## Overview
In multi-agent systems, tasks often depend on the outputs of other tasks. This creates a Directed Acyclic Graph (DAG) of dependencies. 

Your objective is to build a `WorkflowEngine` that can accept a series of tasks, detect if there are any impossible infinite loops (cyclic dependencies), and output the exact order in which the tasks should be executed. 

To maximize efficiency, independent tasks should be grouped together into "batches" so they can be executed concurrently.

## Core Requirements

1. **Framework:** Pure Python (3.10+).
2. **Allowed Modules:** `collections`, `typing`. (NO `networkx`, NO external graph libraries).
3. **The `WorkflowEngine` Class:**
   You must implement a class with the following methods:
   
   * `__init__(self)`: Initialize your internal data structures.
   * `add_task(self, task_id: str, dependencies: list[str]) -> None`: Registers a task and a list of `task_id`s that MUST be completed before this task can begin. (Note: A task might have no dependencies).
   * `validate_dag(self) -> bool`: Analyzes the registered tasks. Returns `True` if the workflow can be executed. Returns `False` if there is a cyclic dependency (e.g., Task A depends on Task B, and Task B depends on Task A).
   * `get_execution_batches(self) -> list[list[str]]`: Returns a list of batches. Each batch is a list of `task_id`s that can be executed simultaneously. 
     * *Example:* If A has no dependencies, and B and C both depend only on A, the output should be `[['A'], ['B', 'C']]`.

## Rules of Engagement

* **Time Limit:** 60 minutes.
* **Allowed Resources:** Google and official Python documentation. You may research "Topological Sorting" or "DAG cycle detection" algorithms if needed.
* **Prohibited Resources:** AI Assistants (ChatGPT, Claude, Gemini, Copilot, etc.) are **STRICTLY FORBIDDEN**.
* **Execution Rule:** Code must be completely error-free and strictly type-hinted. 

## The Evaluation Script

Append this exact script to the bottom of your file. Your code must pass all assertions silently. 

```python
# --- EVALUATION SCRIPT (Append this to your code) ---
if __name__ == "__main__":
    
    # Test 1: Valid Complex Workflow
    engine = WorkflowEngine()
    engine.add_task("Summarizer", ["DataFetcher", "ConfigLoader"])
    engine.add_task("DataFetcher", ["ConfigLoader"])
    engine.add_task("ConfigLoader", [])
    engine.add_task("ReportGenerator", ["Summarizer", "ImageGenerator"])
    engine.add_task("ImageGenerator", [])

    assert engine.validate_dag() == True, "Failed: Engine incorrectly flagged a valid DAG as invalid."
    
    batches = engine.get_execution_batches()
    # Batch 0 should contain tasks with 0 dependencies
    assert set(batches[0]) == {"ConfigLoader", "ImageGenerator"}, f"Failed Batch 0: Got {batches[0]}"
    # Batch 1 should be DataFetcher (relies on ConfigLoader)
    assert set(batches[1]) == {"DataFetcher"}, f"Failed Batch 1: Got {batches[1]}"
    # Batch 2 should be Summarizer (relies on DataFetcher and ConfigLoader)
    assert set(batches[2]) == {"Summarizer"}, f"Failed Batch 2: Got {batches[2]}"
    # Batch 3 should be ReportGenerator
    assert set(batches[3]) == {"ReportGenerator"}, f"Failed Batch 3: Got {batches[3]}"

    # Test 2: Cyclic Dependency (Infinite Loop)
    bad_engine = WorkflowEngine()
    bad_engine.add_task("AgentA", ["AgentB"])
    bad_engine.add_task("AgentB", ["AgentC"])
    bad_engine.add_task("AgentC", ["AgentA"])
    
    assert bad_engine.validate_dag() == False, "Failed: Engine failed to detect a cyclic dependency."

    print("SUCCESS: All tests passed. Your graph traversal logic is solid.")