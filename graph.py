class Vertex:
    taskLoad = 0

    def __init__(self, taskLoad):
        self.taskLoad = taskLoad

class Graph:
    vertices = [] # Map
    edges = []

    def __init__(self):
        self.vertices = []

    def addVertex(self, v):
        if self.containsVertex(v):
            return False
        self.vertices[v] = [] # Map Edge:Pair<Vertex>
    
    def containsVertex(self, v):
        if v in self.vertices:
            return True
        return False
    
    def addEdge(self, e, v1, v2, utilisation):
        if not self.containsVertex(v1) or not self.containsVertex(v2):
            return False
        
        if self.findEdge(v1, v2) == False:
            return False

        pair = Pair(v1, v2, utilisation)
        self.edges[e] = pair


class Pair:
    v1 = Vertex
    v2 = Vertex
    utilisation = 0.0

    def __init__(self, v1, v2, utilisation):
        self.v1 = v1
        self.v2 = v2
        self.utilisation = utilisation