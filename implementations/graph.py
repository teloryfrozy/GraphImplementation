'''
 ============================================================================
 Name        : graph.py
 Author      : Augustin ROLET
 Version     : 1.0
 Copyright   : Copyright Free
 Description : Graph implementation
 ============================================================================
'''

"""
Problème et Contrainte:
    - Méthode paths à vérifier

Liste des méthodes à implémenter restantes:
    - étiqueté: permet de savoir si les arrêtes ont des valeurs attribuées
    - valué (= pondéré): permet de savoir si le graphe est valué
    - extrémités: permet de connaitre les 2 nodes adajcants à une arrête, permet de calculer le cout (ou le temps) d'un transfert par exemple
    - poids d'une chaine: permet de connaitre le poids d'une chaine si le graphe est valué
    - connexe ("fortement connexe": graphe orienté): permet de savoir si un graphe est connexe ou non
"""
from random import choice


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

    def get_pred(self):
        """Returns the adjacency list of predecessors in a directed graph.

        Algorithm:
            pred: {}
            For each node in the graph
                pred[node]: ()
                For each neighbor of the node
                    pred[neighbor] += node
        """
        pred = {}
        vl = self.get_vertices()
        vl.sort()

        for node in vl:
            if node not in pred.keys():
                pred[node] = ()
            for voisin in self.adj[node]:
                if voisin not in pred.keys():
                    pred[voisin] = tuple(node)
                else:
                    pred[voisin] += tuple(node)
        return pred
    
    def set_neighbors(self, node, neighbor):
        """Associates the tuple of neighbors 'neighbor' with the specified 'node'.

        Parameters:
            - (str) node: The node to which neighbors are associated
            - (tuple) neighbor: The adjacency list representing neighbors of the node
        """
        self.adj[node] = neighbor
    
    ###################################################
    #     Graph Traversal Algorithms: DFS and BFS     #
    ###################################################
    def BFS(self, node):
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
            if type(self.adj[x]) is tuple:
                l = list(self.adj[x])
            else:
                l = [self.adj[x]]
            parcours.append(x)
            for voisin in l:
                if voisin not in temp and voisin not in parcours:
                    temp.append(voisin)
        return parcours

    def DFS(self, node):
        """Returns a breadth-first traversal of a graph.

        Arguments:
            - (str) node: any node in the graph

        Algorithm:
            visited_nodes: []
            closed_nodes: []
            stack: []
            While stack is not empty
                tmp: first node in the stack
                neighbors: [list of unvisited neighbors of tmp]
                If neighbors is not empty
                    pop(stack)
                    closed_nodes + tmp
                Else
                    rd_n: random neighbor from neighbors
                    visited_nodes + rd_n
                    push(v) into stack
            Return closed_nodes
        """
        visited_nodes, closed_nodes, stack = [node], [], [node]
        while stack != []:
            tmp = stack[-1]
            if type(self.adj[tmp]) is tuple:
                l = list(self.adj[tmp])
            else:
                l = [self.adj[tmp]]
            
            # --- Unvisited neighbors --- #
            neighbors = [voisin for voisin in l if voisin not in visited_nodes]
            if neighbors != []:
                rd_n = choice(neighbors)
                visited_nodes.append(rd_n)
                stack.append(rd_n)
            else:
                stack.pop(-1)
                closed_nodes.append(tmp)
        return closed_nodes


    def paths(self, departure, arrival):
        """Returns the paths from 'departure' to 'arrival'.

        Arguments:
            - (str) departure: starting node
            - (str) arrival: destination node
        """
        paths, visited, tmp_stack = [], [departure], [[departure]]
        while tmp_stack != []:
            x = tmp_stack.pop(0)
            neighbors = self.adj[x[-1]] if type(self.adj[x[-1]]) is tuple else [self.adj[x[-1]]]

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

    



###################################################
#               TESTING AND EXAMPLES              #
###################################################
def assertion_test():
    Gl = Graph(
        {
            "a": ("b", "c"),
            "b": ("a", "d", "e"),
            "c": ("a", "d"),
            "d": ("b", "c", "e"),
            "e": ("b", "d", "f", "g"),
            "f": ("e", "g"),
            "g": ("e", "f", "h"),
            "h": ("g")
        }
    )

    assert Gl.get_shortest_path(Gl.paths("g", "c")) == ['g', 'e', 'd', 'c']

def example():
    """Test de la classe avec des exemples de graphe."""
    # Undirected Graphs
    social_links = Graph(
        {
            "Jean": ("Jade"),
            "Jade": ("Paul"),
            "Paul": ("Thomas", "René"),
            "Thomas": ("Jean"),
            "René": ("Marie"),
            "Marie": ("René")
        }
    )
    # Undirected Graphs - defined with letters
    lower_example = Graph(
        {
            "a": ("b", "c"),
            "b": ("a", "d", "e"),
            "c": ("a", "d"),
            "d": ("b", "c", "e"),
            "e": ("b", "d", "f", "g"),
            "f": ("e", "g"),
            "g": ("e", "f", "h"),
            "h": ("g")
        }
    )
    # Directed Graph, Successor List
    upper_example = Graph(
        {
            "A": ("C"),
            "B": ("A"),
            "C": ("B", "D"),
            "D": ("A", "B"),
            "E": ("D")
        }
    )

    print("----------- social_links Graph --------------"
          "\nNodes:", \
          social_links.get_vertices(), \
          "BFS search with node 'Jean'", \
          social_links.BFS("Jean")
    )
    social_links.show_matrix()
    
    print()

    print("----------- upper_example Graph --------------", \
          f"\nC is of degree {upper_example.get_degree('C')}"
    )
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
