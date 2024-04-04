# ex4.py

import timeit

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

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        traversal_order = [start]
        for neighbor, i in self.adjacency_list[start]:
            if neighbor not in visited:
                traversal_order.extend(self.dfs(neighbor, visited))
        return traversal_order


class Graph2:
    def __init__(self):
        self.adjacency_matrix = {}

    def addNode(self, data):
        if data not in self.adjacency_matrix:
            self.adjacency_matrix[data] = {}
            return GraphNode(data)
        return None

    def removeNode(self, node):
        if node.data in self.adjacency_matrix:
            del self.adjacency_matrix[node.data]
            for key in self.adjacency_matrix:
                if node.data in self.adjacency_matrix[key]:
                    del self.adjacency_matrix[key][node.data]

    def addEdge(self, n1, n2, weight=1):
        if n1.data in self.adjacency_matrix and n2.data in self.adjacency_matrix:
            self.adjacency_matrix[n1.data][n2.data] = weight
            self.adjacency_matrix[n2.data][n1.data] = weight

    def removeEdge(self, n1, n2):
        if n1.data in self.adjacency_matrix and n2.data in self.adjacency_matrix:
            del self.adjacency_matrix[n1.data][n2.data]
            del self.adjacency_matrix[n2.data][n1.data]

    def printGraph(self):
        for node in self.adjacency_matrix:
            connections = self.adjacency_matrix[node]
            print(f"Node {node} connects to:")
            for neighbor, weight in connections.items():
                print(f"  {neighbor} with weight {weight}\n")

    def importFromFile(self, file):
        try:
            with open(file, 'r') as f:
                graph_content = f.read()

            if "strict graph" not in graph_content:
                return None

            self.adjacency_matrix = {}
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

    def dfs(self, start, visited = None):
        if visited is None:
            visited = set()
        visited.add(start)
        traversal_order = [start]
        for neighbor in self.adjacency_matrix[start]:
            if neighbor not in visited:
                traversal_order.extend(self.dfs(neighbor, visited))
        return traversal_order

def measure_dfs_graph1():
    time_taken = timeit.timeit(lambda: graph1.dfs(list(graph1.adjacency_list.keys())[0]), number = 10)
    return time_taken

def measure_dfs_graph2():
    time_taken = timeit.timeit(lambda: graph2.dfs(list(graph2.adjacency_matrix.keys())[0]), number = 10)
    return time_taken

graph_file = "random.dot"

graph1 = Graph()
graph2 = Graph2()

graph1.importFromFile(graph_file)
graph2.importFromFile(graph_file)

execution_times_graph = [measure_dfs_graph1() for i in range(10)]
execution_times_graph2 = [measure_dfs_graph2() for i in range(10)]

max_time_graph = max(execution_times_graph)
min_time_graph = min(execution_times_graph)
avg_time_graph = sum(execution_times_graph) / len(execution_times_graph)

max_time_graph2 = max(execution_times_graph2)
min_time_graph2 = min(execution_times_graph2)
avg_time_graph2 = sum(execution_times_graph2) / len(execution_times_graph2)

print("Performance of dfs() for adjacency list graph (Graph class):")
print(f'Max time: {max_time_graph} seconds')
print(f'Min time: {min_time_graph} seconds')
print(f'Average time: {avg_time_graph} seconds')

print("Performance of dfs() for adjacency matrix graph (Graph2 class):")
print(f'Max time: {max_time_graph2} seconds')
print(f'Min time: {min_time_graph2} seconds')
print(f'Average time: {avg_time_graph2} seconds')