
class WorkflowEngine():
    def __init__(self):
        self.task_dict = {} 
        self.batch = []
        
    def delete_node(self, graph,node):
        if node in graph:
            del graph[node]
        
        for neighbors in graph.values():
            if node in neighbors:
                neighbors.remove(node)
    
    def validate_dag(self) -> bool:
        graph = self.task_dict

        visited = set()
        path = set()

        def dfs(node):
            if node in path:
                return True  

            if node in visited:
                return False

            path.add(node)

            for neighbor in graph[node]:
                if dfs(neighbor):
                    return True

            path.remove(node)
            visited.add(node)

            return False

        for node in graph:
            if dfs(node):
                return False

        return True 
                
    def get_execution_batches(self):
        graph = self.task_dict.copy()

        while graph:
            batch = []

            for node, deps in graph.items():
                if not deps:
                    batch.append(node)

            for node in batch:
                self.delete_node(graph, node)

            self.batch.append(batch)

        return self.batch
                
    def add_task(self,task_id : str,dependenies : list[str]) -> None:
        
        if task_id not in self.task_dict:
            self.task_dict[task_id] = dependenies

if __name__ == "__main__":
    
    # Test 1: Valid Complex Workflow
    engine = WorkflowEngine()
    engine.add_task("Summarizer", ["DataFetcher", "ConfigLoader"])
    engine.add_task("DataFetcher", ["ConfigLoader"])
    engine.add_task("ConfigLoader", [])
    engine.add_task("ReportGenerator", ["Summarizer", "ImageGenerator"])
    engine.add_task("ImageGenerator", [])

    print(engine.validate_dag())