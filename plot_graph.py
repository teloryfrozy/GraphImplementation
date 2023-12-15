import networkx as nx
import matplotlib
matplotlib.use('Qt5Agg')  # or 'TkAgg', 'Agg', etc.
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edge(1, 2)
G.add_node("C")

nx.draw_spring(G, with_labels=True)
plt.show()
