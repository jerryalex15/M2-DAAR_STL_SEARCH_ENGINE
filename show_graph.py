import pickle
import networkx as nx
import matplotlib.pyplot as plt

# Charger la matrice d'adjacence
with open("adjacency_df_jaccard.pkl", "rb") as f:
    adjacency_df = pickle.load(f)

# Créer un graphe non orienté
G = nx.Graph()

# Ajouter les nœuds (livres)
for book in adjacency_df:
    G.add_node(book)

# Ajouter les arêtes avec les poids (distances Jaccard)
for book1 in adjacency_df:
    for book2 in adjacency_df[book1]:
        distance = adjacency_df[book1][book2]
        if distance > 0:  # Ajouter uniquement les arêtes avec une distance non nulle
            G.add_edge(book1, book2, weight=distance)

# Nombre total d'arêtes créées
total_edges = G.number_of_edges()
print(f"Le nombre total d'arêtes créées est : {total_edges}")

# Visualisation du graphe
plt.figure(figsize=(10, 10))

# Dessiner le graphe
pos = nx.spring_layout(G, k=0.15, iterations=20)  # Positionnement des nœuds
nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue')
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.7)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

# Afficher les étiquettes des arêtes (distances Jaccard)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Afficher le graphe
plt.title("Graph des livres avec leurs distances Jaccard")
plt.axis('off')  # Enlever l'axe pour une meilleure visualisation
plt.show()