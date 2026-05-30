from enum import Enum
import re

class State(Enum):
    GENERAL_STATE = "GENERAL_STATE"
    REFUND_STATE = "REFUND_STATE"

class class_state:
    def __init__(self, memory = dict, current_data=dict):
        self.memory = memory
        self.current_data = current_data
    
    def check_order_id(self,order_id):
        """function created to confirm the order id so that we don't
           pass a random 6 digit number as order_id

        Args:
            order_id (int): 6-digit order id that is unique for every order

        Returns:
            bool : checks the order id is activate or not in the backend returns True
        """
        #code to check the order id in the backend
        
        #edge case that i though while writing this verifing the order is active or not or is delivered days ago and the user is trying to cheat the system
        #if the order is active or delivered
        return True
    
    def checking_episodic(self):
        session_data = self.memory[self.current_data.session_id]

        for response in self.session_data["reponse"]:
            #googled how to add len restriction on regex
            match = re.search("^\d{6}",response)
            
            if match:
                order_id = match.group()
                self.order_id = order_id
                if self.check_order_id(order_id):
                    return order_id 
            
        return False
        
    def check_return(self):
        reponse = self.current_data.reponse
        
        if "refund" in reponse or "return" in reponse:
            state = State.REFUND_STATE
            order_id = self.checking_episodic()
            
            if order_id == False:
                return order_id,state
            else:
                return False,state
        else:
            state = State.GENERAL_STATE
        
        return False,state
        