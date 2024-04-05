# ex3.py

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
        
# 'find' method for union-find
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])  

# 'union' method for union-find  
    def union(self, parent, rank, nodex, nodey):
        xroot = self.find(parent, nodex)
        yroot = self.find(parent, nodey)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

# full kruskal algorithm implementation w/ union-find
    def mst(self):
        parent = {}
        rank = {}
        for node in self.adjacency_list:
            parent[node] = node
            rank[node] = 0
        sorted_edges = []
        for node in self.adjacency_list:
            for neighbor, weight in self.adjacency_list[node]:
                sorted_edges.append((node, neighbor, weight))
        sorted_edges.sort(key = lambda item: item[2])
        mst_edges = []
        for edge in sorted_edges:
            nodex, nodey, weight = edge
            xroot = self.find(parent, nodex)
            yroot = self.find(parent, nodey)
            
            if (xroot != yroot):
                mst_edges.append(edge)
                self.union(parent, rank, xroot, yroot)
        return mst_edges

# Example usage w/ example graph from ex3.pdf:
graph = Graph()
graph.addNode('A')
graph.addNode('B')
graph.addNode('C')
graph.addNode('D')
graph.addNode('E')
graph.addNode('F')

graph.addEdge(GraphNode('A'), GraphNode('B'), 3)
graph.addEdge(GraphNode('A'), GraphNode('D'), 1)
graph.addEdge(GraphNode('A'), GraphNode('E'), 9)
graph.addEdge(GraphNode('C'), GraphNode('B'), 12)
graph.addEdge(GraphNode('C'), GraphNode('D'), 3)
graph.addEdge(GraphNode('D'), GraphNode('B'), 10)
graph.addEdge(GraphNode('D'), GraphNode('F'), 2)
graph.addEdge(GraphNode('F'), GraphNode('E'), 15)

mst = graph.mst()
print("Minimum spanning tree:")
for edge in mst:
    print(edge)