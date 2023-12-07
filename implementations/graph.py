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
    - Méthode chemins à vérifier

Liste des méthodes à implémenter restantes:
    - étiqueté: permet de savoir si les arrêtes ont des valeurs attribuées
    - valué (= pondéré): permet de savoir si le graphe est valué
    - extrémités: permet de connaitre les 2 sommets adajcants à une arrête, permet de calculer le cout (ou le temps) d'un transfert par exemple
    - poids d'une chaine: permet de connaitre le poids d'une chaine si le graphe est valué
    - connexe ("fortement connexe": graphe orienté): permet de savoir si un graphe est connexe ou non
"""

from random import choice

class Graph:
    """Class to create a graph."""

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

    def getListeAdj(self):
        """Renvoie la liste d'adjacence du graphe."""
        return self.adj

    def oriente(self):
        """Renvoie Vrai si le graphe est orienté, Faux sinon.

        Algorithme:
            Parcours des lignes et des colonnes
                Comparaison des lignes et des colonnes
                Si il existe une différence
                    Renvoyer Faux
            Renvoyer Vrai
        """
        m = self.getMatrice()
        for i in range(self.getOrdre()):
            ligne = m[i]
            colonne = [m[j][i] for j in range(self.getOrdre())]
            if ligne != colonne:
                return True
        return False

    def complet(self):
        """Renvoie Vrai si le graphe est complet, Faux sinon."""
        for node in self.adj.keys():
            if self.getDegre(node) != self.getOrdre()-1:
                return False
        return True

    def getOrdre(self):
        """Renvoie l'ordre du graphe."""
        return len(self.adj.keys())

    def getDegre(self, s):
        """Renvoie le degré du sommet s."""
        if s in self.adj.keys():
            return len(self.adj[s])
        return "le sommet " + s + " n'existe pas."

    def getSommets(self):
        """Retourne la liste des sommets du graphe."""
        return list(self.adj.keys())

    def getMatrice(self):
        """Renvoie la matrice d'adjacence d'une liste d'adjacence.

        Algorithme:
            Création d'une matrice nulle de ordre colonnes et de ordre lignes
            Parcours des clés du graphe
                i: indice de la clé dans le dictionnaire
                Parcours des voisins des clés
                    j: indice de la valeur dans la liste
                    m[j][i]: 1
        """
        ordre = self.getOrdre()
        m = [[0 for i in range(ordre)] for i in range(ordre)]
        i = -1
        ls = self.getSommets()
        ls.sort()
        for sommet in ls:
            i += 1
            for j in range(len(self.adj[sommet])):
                m[i][j] = 1
        return m

    def printMatrice(self):
        """Affiche la matrice d'adjacence d'un graphe non orienté ou les
        matrices des successeurs et des prédecesseurs d'un graphe orienté.
        """
        if self.oriente():
            print("\nMatrice d'adjacence des prédecesseurs")
            for ligne in Graphe(self.getPred()).getMatrice():
                print(ligne)
            print("\nMatrice d'adjacence des successeurs")
        else:
            print("\nMatrice d'adjacence du graphe")
        for ligne in self.getMatrice():
            print(ligne)

    def getPred(self):
        """Renvoie la liste d'adjacence des prédecesseurs d'un graphe orienté.

        Algorithme:
            pred: {}
            Pour chaque sommet du graphe
                pred[sommet]: ()
                Pour chaque voisin du sommet
                    pred[voisin]+: sommet
        """
        pred = {}
        ls = self.getSommets()
        ls.sort()
        for sommet in ls:
            if sommet not in pred.keys():
                pred[sommet] = ()
            for voisin in self.adj[sommet]:
                if voisin not in pred.keys():
                    pred[voisin] = tuple(sommet)
                else:
                    pred[voisin] += tuple(sommet)
        return pred

    # Parcours
    def BFS(self, sommet):
        """Renvoie le parcours en largeur d'un graphe.

        Arguments:
            - (str) sommet: sommet quelconque du graphe

        Algorithme:
            tmp: file contenant sommet
            parcours: liste vide
            Tant que temp n'est pas vide
                x: defiler(temp)
                Ajouter x dans parcours
                Pour chaque voisin de x
                    Si voisin n'est pas marqué
                        Ajouter voisin dans temp
            Renvoyer parcours
        """
        parcours, temp = [], [sommet]
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

    def DFS(self, sommet):
        """Renvoie un parcours en largeur d'un graphe.

        Arguments:
            - (str) sommet: sommet quelconque du graphe

        Algorithme:
            sommets_visites: []
            sommets_fermes: []
            pile: []
            Tant que pile n'est pas vide
                tmp: premier sommet de la pile
                voisins: [liste des voisins de tmp non visités]
                Si voisins n'est pas vide
                    depiler(pile)
                    sommets_fermes + tmp
                Sinon
                    v: voisin aléatoire de voisins
                    sommets_visites + v
                    empiler(v) dans pile
            Renvoyer sommets_fermes
        """
        sommets_visites, sommets_fermes, pile = [sommet], [], [sommet]
        while pile != []:
            tmp = pile[-1]
            if type(self.adj[tmp]) is tuple:
                l = list(self.adj[tmp])
            else:
                l = [self.adj[tmp]]
            voisins = [voisin for voisin in l if voisin not in sommets_visites]
            if voisins != []:
                v = choice(voisins)
                sommets_visites.append(v)
                pile.append(v)
            else:
                pile.pop(-1)
                sommets_fermes.append(tmp)
        return sommets_fermes

    def chemins(self, depart, arrivee):
        """Renvoie les chemins de depart à arrivee.

        Arguments:
            - (str) depart: sommet de départ
            - (str) arrivee: sommet d'arriée
        """
        chemins, visites, file_temp = [], [depart], [[depart]]
        while file_temp != []:
            x = file_temp.pop(0)
            if type(self.adj[x[-1]]) is tuple:
                l = list(self.adj[x[-1]])
            else:
                l = [self.adj[x[-1]]]
            for voisin in l:
                if voisin == arrivee:
                    chemins.append(x + [voisin])
                elif voisin not in x:
                    if voisin not in visites:
                        visites.append(voisin)
                    file_temp.append(x + [voisin])
        return chemins

    def courtChemin(self, chemins):
        """Renvoie le plus court chemin parmis les chemins d'un sommet à un autre.

        Argument:
            - (list) chemins: liste de tout les chemins d'un graphe d'un point à un autre
        """
        court_chemin = chemins[0]
        for chemin in chemins[1:]:
            if len(chemin) < len(court_chemin):
                court_chemin = chemin
        return court_chemin

    # Modifieurs
    def setVoisins(self, s, v):
        """Ajoute le tuple des voisins v associés au sommet s.

        Paramètres:
            - (str) s: sommet
            - (tuple) v: liste d'adjacence de s
        """
        self.adj[s] = v

def _test():
    """Test de la classe avec des exemples de graphe."""
    # Graphes non-orientés
    G = Graphe(
        {
            "Jean": ("Jade"),
            "Jade": ("Paul"),
            "Paul": ("Thomas", "René"),
            "Thomas": ("Jean"),
            "René": ("Marie"),
            "Marie": ("René")
        }
    )
    Gl = Graphe(
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
    # Graphe orienté, liste des successeurs
    GOs = Graphe(
        {
            "A": ("C"),
            "B": ("A"),
            "C": ("B", "D"),
            "D": ("A", "B"),
            "E": ("D")
        }
    )
    print(G.getSommets())
    G.printMatrice()
    GOs.printMatrice()
    print("C est de degré " + str(GOs.getDegre("C")))
    Gl.printMatrice()
    print(G.BFS("Jean"))
    print(G.chemins(depart="Jade", arrivee="Paul"))
    print("Un parcours en largeur du graphe Gl par le sommet 'g' est", Gl.DFS("g"))
    assert Gl.courtChemin(Gl.chemins("g", "c")) == ['g', 'e', 'd', 'c']
    print(G.DFS(sommet="Jean"))

if __name__ == "__main__":
    _test()
