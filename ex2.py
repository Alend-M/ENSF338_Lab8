import timeit
import matplotlib.pyplot as plt

'''
 In the lecture, we have discussed Dijkstras algorithm for computing
shortest paths in a graph.
• One of the core step of the algorithms, at each iteration, is the
identification of the node with the shortest path from the source:
• But... how quickly can we find the node with the smallest distance?
• In other words, how is our queue implemented? The question is
important because it affects efficiency


1: List two possible ways to implement this queue, with different
efficiency (a slow one which uses linear search, and something
faster)
    - One way to implement the queue is slower with linear search, where you
    you maintain a list of vertices yet to be explored, and you linearly search through 
    this list to find the vertex with the smallest tentative distance. 
    The overall time complexity is O(|V|)^2, V=Vertices
    - Thhe other way is faster using a priority queue (min heap). The pirority queue
    can more efficiently select the vertex with the smallest current distance.
    The time complexity is O((|E| + |V|)log|V|), E=Edges, V=Vertices'''


'''2: Implementation with class Graph from ex1:'''

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
    
    def fastSP(self, start_node):
        distances = {vertex: float('inf') for vertex in self.adjacency_list}
        distances[start_node] = 0
       
        # Custom priority queue using a dictionary
        priority_queue = {start_node: 0}
       
        while priority_queue:
            current_vertex = min(priority_queue, key=priority_queue.get) #This is to find the vertex with the smallest tentative distance. This operation finds the minimum key in the dictionary based on its corresponding value.
            del priority_queue[current_vertex] #delete the selected vertex from the priority_queue after processing it to ensure it is not considered again.
           
            for neighbor, weight in self.adjacency_list[current_vertex]:
                distance = distances[current_vertex] + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    priority_queue[neighbor] = distance  
       
        return distances

    def slowSP(self, start_node):
        distances = {vertex: float('inf') for vertex in self.adjacency_list}
        distances[start_node] = 0
       
        unvisited = list(self.adjacency_list.keys())
       
        while unvisited:
            min_distance = float('inf')
            min_vertex = None
            for vertex in unvisited:
                if distances[vertex] < min_distance:
                    min_distance = distances[vertex]
                    min_vertex = vertex
            current_vertex = min_vertex
            unvisited.remove(current_vertex)
           
            for neighbor, weight in self.adjacency_list[current_vertex]:
                if (distances[current_vertex] + weight < distances[neighbor]):
                    distances[neighbor] = distances[current_vertex] + weight
       
        return distances
    



''' 3: Measure the performance of each algorithm on the sample graph
provided on the lab's D2L (random.dot).
    • Time the execution of the algorithm, for all nodes
    • Report average, max and min time'''

graph = Graph()
file_path = "random.dot"
graph.importFromFile(file_path)
#####graph.printGraph() #to verify that its been imported correctly, and yes, it has :)

slowSP_times = []
fastSP_times = []

for node in graph.adjacency_list:
    slowSP_time = timeit.timeit(lambda: graph.slowSP(node), number=10)
    fastSP_time = timeit.timeit(lambda: graph.fastSP(node), number=10)
    slowSP_times.append(slowSP_time)
    fastSP_times.append(fastSP_time)

# Calculate the minimum, maximum, and average times for slowSP
slowSP_minTime = min(slowSP_times)
slowSP_maxTime = max(slowSP_times)
slowSP_avgTime = sum(slowSP_times) / len(slowSP_times)

# Calculate the minimum, maximum, and average times for fastSP
fastSP_minTime = min(fastSP_times)
fastSP_maxTime = max(fastSP_times)
fastSP_avgTime = sum(fastSP_times) / len(fastSP_times)

# Print the results
print("slowSP performance:")
print("Min time:", slowSP_minTime)
print("Max time:", slowSP_maxTime)
print("Avg time:", slowSP_avgTime)

print("\nfastSP performance:")
print("Min time:", fastSP_minTime)
print("Max time:", fastSP_maxTime)
print("Avg time:", fastSP_avgTime)


''' 4: Plot a histogram of the distribution of execution times across all
nodes, and discuss the results'''

plt.figure(figsize=(10, 5))

plt.hist(slowSP_times, bins=20, color='blue', alpha=0.5, label='slowSP')

plt.hist(fastSP_times, bins=20, color='red', alpha=0.5, label='fastSP')

plt.title('Distribution of Execution Times for slowSP and fastSP')
plt.xlabel('Execution Time')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()

'''
Results: 
slowSP performance:
Min time: 0.4861818529999997
Max time: 1.4863040210000236
Avg time: 0.5910209192091381

fastSP performance:
Min time: 0.15888888899999998
Max time: 0.5342903769999907
Avg time: 0.20847883316751298

Fast is faster than slow. This is to be expected because FastSP uses a priority queue,
which is more efficient than linear search in finding the smalling distance between nodes.
'''