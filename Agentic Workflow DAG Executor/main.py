from engine import WorkflowEngine

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