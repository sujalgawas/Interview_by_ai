from engine import AgentExecutor
from tool import ToolRegistry

# --- EVALUATION SCRIPT (Append this to your code) ---
if __name__ == "__main__":
    # 1. Setup Mock Tools
    def fetch_stock_price(ticker: str) -> str:
        if ticker == "AAPL": return "150.25"
        if ticker == "GOOGL": return "2800.50"
        raise ValueError(f"Unknown ticker: {ticker}")

    def calculate_math(expression: str) -> str:
        # Mocking a calculator tool
        if expression == "2 + 2": return "4"
        return "Unknown"

    # 2. Register Tools
    registry = ToolRegistry()
    registry.register("stock_ticker", "Fetches stock price", fetch_stock_price)
    registry.register("calculator", "Performs basic math", calculate_math)

    executor = AgentExecutor(registry)

    # Test 1: Successful Execution
    valid_output = '''
    Thought: The user wants to know Apple's stock price.
    Action: stock_ticker
    Action Input: {"ticker": "AAPL"}
    '''
    result1 = executor.execute_llm_output(valid_output)
    assert result1 == "Observation: 150.25", f"Failed Test 1: Got {result1}"

    # Test 2: Tool Not Found
    missing_tool_output = '''
    Thought: I should check the weather.
    Action: weather_api
    Action Input: {"city": "London"}
    '''
    result2 = executor.execute_llm_output(missing_tool_output)
    assert result2 == "Error: Tool 'weather_api' not found.", f"Failed Test 2: Got {result2}"

    # Test 3: Malformed JSON Input
    bad_json_output = '''
    Thought: Let's do some math.
    Action: calculator
    Action Input: {"expression": "2 + 2" # Missing closing brace
    '''
    result3 = executor.execute_llm_output(bad_json_output)
    assert result3 == "Error: Invalid JSON input for tool.", f"Failed Test 3: Got {result3}"

    # Test 4: Tool Execution Exception
    exception_output = '''
    Thought: Let's check a fake stock.
    Action: stock_ticker
    Action Input: {"ticker": "FAKE"}
    '''
    result4 = executor.execute_llm_output(exception_output)
    assert result4 == "Error: Tool execution failed - Unknown ticker: FAKE", f"Failed Test 4: Got {result4}"

    print("SUCCESS: All tests passed. Your ReAct engine is production-ready.")