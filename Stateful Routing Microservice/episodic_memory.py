class episodic:
    def __init__(self, memory = dict , current_data = dict):
        self.memory = memory
        self.current_data = current_data
        self.session_id = self.current_data.session
    def check_session(self):
        
        if not self.current_data.session_id in self.memory:
            self.memory[self.current_data.session_id] = []
            return False
            
        return True
    
    def get_memory_count(self):
        if len(self.memory[self.session_id]) < 5 and len(self.memory[self.session_id]) > 0:
            current_count = self.memory[self.current_data.session_id][-1]["memory_count"]
            return current_count
        
        return 1

    def updating_memory(self):
        
        if not len(self.memory[self.session_id]) < 5:
           self.memory[self.current_data[self.session_id]].pop(0)
        
        
        current_count = self.get_memory_count()
        
        if current_count:            
            self.memory[self.current.session_id].append({"session_id":self.current_data.session_id,
                                                        "memory_count":current_count + 1,
                                                        "current_state":self.current_data.state,
                                                        "reponse":self.current_data.state})
        else:
            current_count = 1
            
            self.memory[self.current.session_id].append({"session_id":self.current_data.session_id,
                                                        "memory_count":current_count,
                                                        "current_state":self.current_data.state,
                                                        "reponse":self.current_data.current_state})
        
        return "updated memory"