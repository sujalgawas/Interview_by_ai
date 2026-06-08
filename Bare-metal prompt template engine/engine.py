#engine.py
import re

#googled how to write an exception
class MissingVariableError(Exception):
    def __init__(self,variable_name):
        self.variable_name = variable_name
        super().__init__(f"Missing required variable: {variable_name}")

class PromptTemplate():
    def __init__(self,template: str):
        self.template = template
        self.subject = self.get_subject(self.template)
        
    def get_subject(self,template):
        match = re.findall(r"\{(\w+)\}",template)
        return match    
                
    def extract_variables(self):
        return self.subject
    
    def format(self,**kwargs):
        for args in self.subject:
            if args not in kwargs:
                raise MissingVariableError(
                    f"Missing required variable: {args}"
                )
        #searched format function that is build in used for string
        return self.template.format(**kwargs)