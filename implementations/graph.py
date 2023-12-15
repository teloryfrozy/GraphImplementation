'''
 ============================================================================
 Name        : graph.py
 Author      : Augustin ROLET
 Version     : 1.0
 Copyright   : Copyright Free
 Description : Basic Graph implementation
 ============================================================================
'''
class Graph:
    """Class to implement a graph"""

    def __init__(self, adj={}):
        """Creates a graph defined by its adjacency list.
        If the graph is directed, the adjacency list should be that of successors.

        Parameters:
            - (dict) adj: adjacency list

        By default:
            - The adjacency list is empty
        """
        self.adj = adj

    def get_neighbors(self, node):
        """Returns the neighbors of node or empty list if node not found"""
        return self.adj.get(node, [])

    def get_adjacency_list(self):
        """Returns the adjacency list of the graph"""
        return self.adj

    def is_oriented(self):
        """Returns True if the graph is directed, False otherwise.

        Algorithm:
            Traverse rows and columns
                Compare rows and columns
                If there is a difference
                    Return False
            Return True
        """
        matrix = self.get_matrix()
        for i in range(self.get_order()):
            row = matrix[i]
            column = [matrix[j][i] for j in range(self.get_order())]
            if row != column:
                return True
        return False

    def is_complete(self):
        """Returns True if the graph is complete, False otherwise"""
        for node in self.adj.keys():
            if self.get_degree(node) != self.get_order()-1:
                return False
        return True
    
    def is_labeled(self) -> bool:
        """Checks if the edges in the graph have assigned values (labels)"""
        for node, neighbors in self.adj.items():
            for neighbor in neighbors:
                if isinstance(neighbor, str) and neighbor != "":
                    return True
        return False
    
    def get_order(self):
        """Returns the order of the graph"""
        return len(self.adj.keys())

    def get_degree(self, node):
        """Returns the degree of node"""
        return len(self.adj[node]) if node in self.adj.keys() else None

    def get_vertices(self) -> list:
        """Returns the list of vertices in the graph"""
        return list(self.adj.keys())

    def get_matrix(self):
        """Returns the adjacency matrix from an adjacency list.

        Algorithm:
            Create a null matrix of column order and row order
            Traverse the keys of the graph
                i: index of the key in the dictionary
                Traverse the neighbors of the keys
                    j: index of the value in the list
                    m[j][i]: 1
        """
        order = self.get_order()
        m = [[0 for i in range(order)] for i in range(order)]
        i = -1
        vl = self.get_vertices()
        vl.sort()
        
        for node in vl:
            i += 1
            for j in range(len(self.adj[node])):
                m[i][j] = 1
        return m

    def show_matrix(self):
        """Displays the adjacency matrix of an undirected graph or the
        successor and predecessor matrices of a directed graph.
        """
        if self.is_oriented():
            print("\nAdjacency matrix of predecessors")
            for line in Graph(self.get_pred()).get_matrix():
                print(line)
            print("\nAdjacency matrix of successors")
        else:
            print("\nAdjacency matrix of the graph")
        for line in self.get_matrix():
            print(line)

    def get_pred(self) -> dict:
        """Returns the adjacency list of predecessors in a directed graph.

        Algorithm:
            Initialize an empty dictionary 'pred'.
            For each node in the graph:
                If the node is not in 'pred', add it with an empty list.
                For each neighbor of the node:
                    If the neighbor is not in 'pred', add it with the current node.
                    Otherwise, append the current node to the list of neighbors.
            Return the 'pred' dictionary.
        """
        pred = {}
        vl = self.get_vertices()
        vl.sort()

        for node in vl:
            if node not in pred.keys():
                pred[node] = []
            for voisin in self.adj[node]:
                if voisin not in pred.keys():
                    pred[voisin] = [node]
                else:
                    pred[voisin].append(node)
        return pred
    
    def set_neighbors(self, node: str, neighbor: list):
        """Associates the tuple of neighbors 'neighbor' with the specified 'node'.

        Parameters:
            - (str) node: The node to which neighbors are associated
            - (list) neighbor: The adjacency list representing neighbors of the node
        """
        self.adj[node] = neighbor
    
    ###################################################
    #     Graph Traversal Algorithms: DFS and BFS     #
    ###################################################
    def BFS(self, node) -> list:
        """Returns the breadth-first traversal of a graph.

        Arguments:
            - (str) node: any node in the graph

        Algorithm:
            tmp: queue containing node
            traversal: empty list
            While tmp is not empty
                x: dequeue(tmp)
                Add x to traversal
                For each neighbor of x
                    If neighbor is not marked
                        Add neighbor to tmp
            Return traversal
        """
        parcours, temp = [], [node]
        while temp != []:
            x = temp.pop(0)
            if type(self.adj[x]) is list:
                l = list(self.adj[x])
            else:
                l = [self.adj[x]]
            parcours.append(x)
            for voisin in l:
                if voisin not in temp and voisin not in parcours:
                    temp.append(voisin)
        return parcours

    def DFS(self, start, visited=None) -> list:
        """Returns the list of visited nodes using DFS algorithm"""
        if visited is None:
            visited = []
        visited.append(start)

        for neighbor in self.adj[start]:
            if neighbor not in visited:
                self.DFS(neighbor, visited)
        return visited

    def paths(self, departure, arrival) -> list:
        """Returns the paths from 'departure' to 'arrival'.

        Arguments:
            - (str) departure: starting node
            - (str) arrival: destination node
        """
        paths, visited, tmp_stack = [], [departure], [[departure]]
        while tmp_stack != []:
            x = tmp_stack.pop(0)
            neighbors = self.adj[x[-1]] if type(self.adj[x[-1]]) is list else [self.adj[x[-1]]]

            for neighbor in neighbors:
                if neighbor == arrival:
                    paths.append(x + [neighbor])
                elif neighbor not in x:
                    if neighbor not in visited:
                        visited.append(neighbor)
                    tmp_stack.append(x + [neighbor])
        return paths

    def get_shortest_path(self, paths: list):
        """Returns the shortest path among the paths from one node to another.

        Argument:
            - (list) paths: list of all paths from a node to another in a graph
        """
        shortest_path = paths[0]

        for path in paths[1:]:
            if len(path) < len(shortest_path):
                shortest_path = path
        return shortest_path
    
    def add_node(self, node: str, values: list):
        """Adds a node to the graph and its associated values"""
        if node not in self.get_vertices():
            self.set_neighbors(node, values)


###################################################
#               TESTING AND EXAMPLES              #
###################################################
def example():
    """Testing the class with graph examples"""
    # Undirected Graphs
    social_links = Graph(
        {
            "Jean": ["Jade"],
            "Jade": ["Paul"],
            "Paul": ["Thomas", "René", "Pierre"],
            "Pierre": [],
            "Thomas": ["Jean"],
            "René": ["Marie"],
            "Marie": ["René"]
        }
    )
    # Undirected Graphs - defined with letters
    lower_example = Graph(
        {
            "a": ["b", "c"],
            "b": ["a", "d", "e"],
            "c": ["a", "d"],
            "d": ["b", "c", "e"],
            "e": ["b", "d", "f", "g"],
            "f": ["e", "g"],
            "g": ["e", "f", "h"],
            "h": ["g"]
        }
    )

    # Directed Graph, Successor List
    upper_example = Graph(
        {
            "A": ["C"],
            "B": ["A"],
            "C": ["B", "D"],
            "D": ["A", "B"],
            "E": ["D"]
        }
    )


    ###################################################
    #                  ASSERTION TESTS                #
    ###################################################
    assert upper_example.get_degree('C') == 2
    assert social_links.get_degree('Jean') == 1
    assert social_links.is_labeled() == True
    assert lower_example.get_shortest_path(lower_example.paths("g", "c")) == ['g', 'e', 'd', 'c']
    assert social_links.get_degree('Paul') == 3


    ###################################################
    #                     SHOW CASES                  #
    ###################################################    
    print("----------- social_links Graph --------------"
          "\nNodes:", \
          social_links.get_vertices(), \
          "BFS search with node 'Jean'", \
          social_links.BFS("Jean")
    )
    social_links.show_matrix()
    
    print()

    print("----------- upper_example Graph --------------")
    upper_example.show_matrix()

    print()
    
    print("----------- lower_example Graph --------------" \
          f"\nThe list of paths to go from node: 'a' to node: 'g' is:\n{lower_example.paths(departure='a', arrival='g')}" \
          f"\nA breadth-first traversal of graph Gl from node 'g' is:\n{lower_example.DFS('g')}" \
          f"\nDFS applied started from node: 'a' is:\n{lower_example.DFS('a')}"
    )
    lower_example.show_matrix()


if __name__ == "__main__":
    example()