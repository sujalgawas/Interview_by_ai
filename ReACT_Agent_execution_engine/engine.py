# engine.py
import re 
import json 

class AgentExecutor():
    def __init__(self, registry):
        self.registry = registry
    
    def get_action(self,response) -> str:
        match = re.search(r'Action:\s*(.+)', response)
        
        if match:
            output = match.group(1)
        else:
            return "no match"
                
        return output
    
    def get_input(self,response) -> str:
        match = re.search(r'Action Input:\s*(\{.*\})', response)
        
        if match:
            output = match.group(1)
        else:
            return "no match"
                
        return output
           
    def execute_llm_output(self,response) -> str:
        action_name = self.get_action(response)
        
        if action_name not in self.registry.name_to_function:
            return f"Error: Tool '{action_name}' not found."

        action_input = self.get_input(response)
        
        
        try:
            json_input = json.loads(action_input.strip())
            variable, input1 = json_input.items().__iter__().__next__()
        except:
            return "Error: Invalid JSON input for tool."
        
        try:
            output = self.registry.name_to_function[action_name](input1)
        except Exception as e:
            return f"Error: Tool execution failed - {e}"
        
        if "Unknown" in output:
            return f"Error: Tool execution failed - {output}"
        
        return f"Observation: {output}"