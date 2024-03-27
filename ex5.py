''' 1: Topological sorting can be implemented using an algorithm seen in
class. Which algorithm? Why?'''

'''Topilogical sorting can be implemented with a variant of the recursive 
depth first traversal. Depth first traversal goes as far as possible through the nodes 
until it finds a sink, and then goes back. So, it's suitable for ordering which nodes 
can be visited. DFS can detect if the graph has cycles, which is important 
because topological sorting is for acyclic graphs. It is also efficient because it has
linear time complexity
'''
#+ using a stack 


''' 2: Extend your Graph class (exercise 1) with an isdag() method that
returns true only if a graph does not contain cycles'''

''' 3: Extend the same class with a toposort() method
        1. Checks if the graph is a DAG
        2. If yes, returns a list of nodes in topological order. Return None otherwise.'''

#Used AI to make the comments on code explanation more concise


class GraphNode:
    def __init__(self, data):
        self.data = data

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def addNode(self, data):
        if data not in self.adjacency_list:
            self.adjacency_list[data] = []
            return GraphNode(data)
        return None

    def removeNode(self, node):
        if node.data in self.adjacency_list:
            del self.adjacency_list[node.data]

    def addEdge(self, n1, n2, weight=1):
        if n1.data in self.adjacency_list and n2.data in self.adjacency_list:
            self.adjacency_list[n1.data].append((n2.data, weight))
            self.adjacency_list[n2.data].append((n1.data, weight))

    def removeEdge(self, n1, n2):
        if n1.data in self.adjacency_list and n2.data in self.adjacency_list:
            self.adjacency_list[n1.data] = [(neighbor, weight) for neighbor, weight in self.adjacency_list[n1.data] if neighbor != n2.data]
            self.adjacency_list[n2.data] = [(neighbor, weight) for neighbor, weight in self.adjacency_list[n2.data] if neighbor != n1.data]

    def printGraph(self):
        for node in self.adjacency_list:
            connections = self.adjacency_list[node]
            print(f"Node {node} connects to:")
            for neighbor, weight in connections:
                print(f"  {neighbor} with weight {weight}\n")

    def importFromFile(self, file):
        try:
            with open(file, 'r') as f:
                graph_content = f.read()

            if "strict graph" not in graph_content:
                return None

            self.adjacency_list = {}
            lines = graph_content.split('\n')

            for line in lines:
                if '--' in line:
                    nodes, attributes = line.split('[')
                    node1, node2 = nodes.strip().split('--')
                    node1 = node1.strip()
                    node2 = node2.strip()
                    weight = 1
                    if 'weight' in attributes:
                        weight = int(attributes.split('=')[1].strip('];'))
                    self.addNode(node1)
                    self.addNode(node2)
                    self.addEdge(GraphNode(node1), GraphNode(node2), weight)

        except FileNotFoundError:
            print("File not found.")
            return None
        except Exception as e:
            print("Error occurred while parsing the file:", e)
            return None

    
    #Method that checks if the graph is a Directed Acyclic Graph (DAG):
    #uses depth first search
    def isdag(self):

        '''
        Checks if the graph is a Directed Acyclic Graph (DAG).

        Returns:
            bool: True if the graph is a DAG (does not contain cycles), False otherwise.'''

        visited = set()
        stack = set()
        
        def dfs(node):

            '''
            Depth-First Search (DFS) helper function to traverse the graph and detect cycles.

            Args:
                node: The current node being visited.

            Returns:
                bool: True if a cycle is detected, False otherwise.'''

            visited.add(node)
            stack.add(node)
            for neighbor, _ in self.adjacency_list.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in stack:
                    return True
            stack.remove(node)
            return False
        
        for node in self.adjacency_list:
            if node not in visited:
                if dfs(node):
                    return False
        return True

    def toposort(self):
        '''
        Performs topological sort on the graph if it is a DAG.
        Returns:
            list or None: A list of nodes in topological order if the graph is a DAG, None otherwise.'''
        if not self.isdag():
            return None
        
        visited = set()
        result = []
        
        def dfs_topo(node):
            '''
            Depth-First Search (DFS) helper function to perform topological sort.
            Args:
                node: The current node being visited.'''

            visited.add(node)
            for neighbor, _ in self.adjacency_list.get(node, []):
                if neighbor not in visited:
                    dfs_topo(neighbor)
            result.append(node)
        
        for node in self.adjacency_list:
            if node not in visited:
                dfs_topo(node)
        
        return result[::-1]  # Reversing because we want topological ordering