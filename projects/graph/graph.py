"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            # If v1 and v2 vertices exist, then branch out v2 from v1
            self.vertices[v1].add(v2)
        else:
            raise IndexError("nonexistent vertex")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        visited = set()
        q = Queue()
        q.enqueue(starting_vertex) # Initializing queue

        while q.size() > 0:
            current = q.dequeue()
            if current not in visited:
                print(current)
                visited.add(current)

                for n in self.get_neighbors(current):
                    q.enqueue(n) # Add to end of queue

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        visited = set()
        s = Stack()
        s.push(starting_vertex) # Initializing stack

        while s.size() > 0:
            current = s.pop()
            if current not in visited:
                print(current)
                visited.add(current)

                for n in self.get_neighbors(current):
                    s.push(n) # Add to end of stack

    def dft_recursive(self, starting_vertex, visited=set()):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        # visited = set() # Had to pass this as parameter in for-loop, so I initialized it above instead.

        if starting_vertex not in visited:
            print(starting_vertex)
            visited.add(starting_vertex)

            for n in self.get_neighbors(starting_vertex):
                # Realized that self.dft_recursive(n) would keep re-creating an empty set for visited unless I include it in recursion
                self.dft_recursive(n, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        visited = set()
        q = Queue()
        q.enqueue([starting_vertex]) # Initializing queue

        while q.size() > 0:
            path = q.dequeue()
            last = path[-1] # Copy tail into "last"
            if last not in visited:
                if last == destination_vertex:
                    # Found it!
                    return path
                visited.add(last)

                for n in self.vertices[last]:
                    copied = path.copy()
                    copied.append(n)
                    q.enqueue(copied)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        visited = set()
        s = Stack()
        s.push([starting_vertex]) # Initialize stack

        while s.size() > 0:
            path = s.pop()
            last = path[-1] # Copy tail into "last"

            if last not in visited:
                if last == destination_vertex:
                    # Found it!
                    return path
                visited.add(last)

                for n in self.vertices[last]:
                    copied = path.copy()
                    copied.append(n)
                    s.push(copied)

    def dfs_recursive(self, starting_vertex, destination_vertex, visited=set(), path=[]):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        # Similar to dft_recursive() above, I added some additional parameters to this function

        visited.add(starting_vertex)
        path = path + [starting_vertex] # Keep track of entire path throughout recursion

        if starting_vertex == destination_vertex:
            # Found it!
            return path
        for n in self.get_neighbors(starting_vertex):
            if n not in visited:
                newpath = self.dfs_recursive(n, destination_vertex, visited, path)
                if newpath != None:
                    return newpath

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
