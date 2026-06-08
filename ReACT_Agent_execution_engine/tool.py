# tool.py
from typing import Callable

class ToolRegistry():
    def __init__(self):
        self.name_to_function = {}
    
    def register(self,action_name: str,description: str,function: Callable) -> None:
        self.name_to_function[action_name] = function