import pickle
import os
import networkx as nx

def load_index(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f)

def load_adjacency_matrix(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f)

def load_books_dict(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f)

def compute_centrality_scores(adjacency_matrix, filename="utils/centrality.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    
    print("Computing centrality scores...")
    G_network = nx.Graph()

    for doc1, neighbors in adjacency_matrix.items():
        for doc2, weight in neighbors.items():
            if weight > 0:
                G_network.add_edge(doc1, doc2, weight=float(weight))

    centrality_scores = {
        "pagerank": nx.pagerank(G_network),
        "closeness": nx.closeness_centrality(G_network),
        "betweenness": nx.betweenness_centrality(G_network)
    }

    with open(filename, "wb") as f:
        pickle.dump(centrality_scores, f)

    print("Centrality scores computed and saved.")
    return centrality_scores

def get_books_by_ids(book_ids, books_dict):
    
    books = []

    book_ids = list(book_ids)

    if book_ids and isinstance(book_ids[0], tuple):  
        # Si ce sont des tuples (id.txt, score), on extrait l'ID et retire ".txt"
        book_ids = [book_id[0].replace('.txt', '') for book_id in book_ids]
    else:
        # Si ce sont des chaînes comme "455.txt", on retire ".txt"
        book_ids = [book_id.replace('.txt', '') for book_id in book_ids]

    # Pour chaque ID, chercher le livre dans books_dict
    for book_id in book_ids:
        try:
            # Convertir book_id en entier (si ce n'est pas déjà un entier)
            book_id_number = int(book_id)
            if book_id_number in books_dict:
                book = books_dict[book_id_number]
                books.append(book)
        except ValueError:
            print(f"Invalid book ID: {book_id}, cannot convert to number.")

    return books