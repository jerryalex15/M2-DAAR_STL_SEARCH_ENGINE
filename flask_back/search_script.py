import pickle
import re, os
import networkx as nx
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Charger la table d'index
with open("utils/indexing_table_advanced.pkl", "rb") as f:
    G_loaded = pickle.load(f)

# Charger la matrice d'adjacence
with open("utils/adjacency_df_jaccard.pkl", "rb") as f:
    adjacency_df = pickle.load(f)


def load_books_dict(file_path):
    """Charge le dictionnaire des livres depuis un fichier pickle."""
    with open(file_path, "rb") as f:
        return pickle.load(f)

def compute_centrality_scores(adjacency_matrix, filename="utils/centrality.pkl"):
    # Vérifier si le fichier existe
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            centrality_scores = pickle.load(f)
    else:
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
        
        # Sauvegarde des scores dans un fichier
        with open(filename, "wb") as f:
            pickle.dump(centrality_scores, f)
        
        print("Centrality scores computed and saved to file.")
    
    return centrality_scores

# Chargement ou calcul des centralités
centrality_scores = compute_centrality_scores(adjacency_df)
books_dict = load_books_dict("utils/books_dict.pkl")

def get_books_by_ids(book_ids, books_dict):
    
    books = []

    # Convertir book_ids en liste s'il s'agit d'un set
    book_ids = list(book_ids)

    # Traitement des IDs pour les tuples (id.txt, score) ou juste des chaînes
    if book_ids and isinstance(book_ids[0], tuple):  # Vérifier que la liste n'est pas vide
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

def search_by_keyword(keyword, G):
    keyword = keyword.lower()
    return G.get(keyword, [])

def search_by_regex(pattern, G):
    results = {}
    for term in G:
        if re.search(pattern, term, re.IGNORECASE):
            for doc, tfidf in G[term]:
                if doc not in results or results[doc] < tfidf:
                    results[doc] = tfidf
    return list(results.items())

def rank_documents_by_relevance(results, centrality_scores, centrality_type="pagerank"):
    centrality = centrality_scores.get(centrality_type, {})
    alpha = 1e-6  # Petite constante pour éviter d'annuler le tf-idf
    
    ranked_results = [(doc, tfidf * (centrality.get(doc, 0) + alpha)) for doc, tfidf in results]
    return sorted(ranked_results, key=lambda x: x[1], reverse=True)

def get_top_suggestions(top_results, adjacency_matrix, max_suggestions=10):
    suggestions = set()  # Utilisation d'un set pour éviter les doublons
    visited_results = set(doc for doc, _ in top_results)  # On garde les résultats à exclure
    
    for doc, _ in top_results:
        neighbors = adjacency_matrix.get(doc, {})  # Récupérer les voisins du document
        
        for neighbor in neighbors:
            if neighbor not in visited_results and neighbor not in suggestions:
                suggestions.add(neighbor)  # Ajouter aux suggestions
                
                if len(suggestions) >= max_suggestions:  # Stop si on atteint la limite
                    return list(suggestions)

    return list(suggestions)

@app.route('/search_by_keyword', methods=['POST'])
def search_by_keyword_route():
    data = request.get_json()
    keyword = data.get("keyword", "")

    if not keyword:
        return jsonify({"error": "No keyword provided"}), 400

    results = search_by_keyword(keyword, G_loaded)  # Assure-toi que `search_by_keyword_function` existe

    return jsonify(get_books_by_ids(results, books_dict))


@app.route('/search_by_regex', methods=['POST'])
def search_by_regex_route():
    data = request.get_json()
    pattern = data.get("pattern", "")

    if not pattern:
        return jsonify({"error": "No regex pattern provided"}), 400

    try:
        results = search_by_regex(pattern, G_loaded)  # Assure-toi que `search_by_regex_function` existe
    except re.error as e:
        return jsonify({"error": f"Invalid regex pattern: {str(e)}"}), 400

    return jsonify(get_books_by_ids(results, books_dict))


@app.route('/rank_and_suggest', methods=['POST'])
def rank_and_suggest():
    try:
        # Récupérer les données envoyées dans le corps de la requête
        data = request.get_json()
        keyword = data.get("keyword", "")
        regex_pattern = data.get("pattern", "")
        centrality_type = data.get("centrality_type", "pagerank")
        max_suggestions = data.get("max_suggestions", 10)

        if not keyword and not regex_pattern:
            return jsonify({"error": "No keyword or regex provided"}), 400

        # Étape 1: Filtrer les résultats en fonction du mot-clé ou de l'expression régulière
        top_results = []
        if keyword:
            top_results = search_by_keyword(keyword, G_loaded)
        elif regex_pattern:
            top_results = search_by_regex(regex_pattern, G_loaded)

        if not top_results:
            return jsonify({"error": "No results found"}), 404

        # Étape 2: Classer les résultats par pertinence en fonction des scores de centralité
        ranked_results = rank_documents_by_relevance(top_results, centrality_scores, centrality_type)

        # Étape 3: Récupérer les suggestions à partir des documents classés
        top_suggestions = get_top_suggestions(ranked_results, adjacency_df, max_suggestions)

        return jsonify({
            "ranked_results": get_books_by_ids(ranked_results, books_dict),
            "top_suggestions": get_books_by_ids(top_suggestions, books_dict)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)