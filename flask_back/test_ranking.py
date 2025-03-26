import time
import csv
import random

from utils.data_loader import load_index, load_adjacency_matrix, load_books_dict, compute_centrality_scores, get_books_by_ids
from utils.search_functions import search_by_keyword, search_by_regex
from utils.ranking import rank_documents_by_relevance
from utils.suggestions import get_top_suggestions

# Chargement des données
G_loaded = load_index("utils/indexing_table_advanced.pkl")
adjacency_df = load_adjacency_matrix("utils/adjacency_df_jaccard.pkl")
books_dict = load_books_dict("utils/books_dict.pkl")
centrality_scores = compute_centrality_scores(adjacency_df)

# Liste des mots-clés et expressions régulières à tester
keywords = ["Sargon", "Lewis", "babylon", "network", "king"]
# Liste des 5 expressions régulières à tester
regex_patterns = [
    r"Sar.*(on)$",  # Mot exact
    r"^Clin.*on$",   # Mot commençant par L et finissant par is
    r"baby.*n$",  # Soit "babylon" soit "network"
    r"ki.*s$",  # "king" ou "kings"
    r"\b[a-zA-Z]{20}\b"  # Mots de 6 lettres exactement
]

# Fichiers CSV de sortie
output_keyword_csv = "ranking_keyword_search.csv"
output_regex_csv = "ranking_regex_search.csv"
output_suggestions_csv = "suggestions_results.csv"

def test_ranking_with_search(search_function, queries, output_csv, search_type):
    """Test du ranking avec une recherche spécifique (mot-clé ou regex)."""
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Query", "Execution Time (s)", "Number of Books Returned, Number of suggestions"])
        
        for query in queries:
            start_time = time.time()

            # Exécuter la recherche (par mot-clé ou regex)
            results = search_function(query, G_loaded)
            ranked_results = rank_documents_by_relevance(results, centrality_scores)

            top_suggestions = get_top_suggestions(ranked_results, adjacency_df, 100)

            execution_time = time.time() - start_time
            num_books = len(ranked_results)
            num_suggestions = len(top_suggestions)

            writer.writerow([query, execution_time, num_books, num_suggestions])
            print(f"[{search_type}] Query: {query}, Execution Time: {execution_time:.4f} s, Number of Books: {num_books}")

def test_suggestions():
    """Test de la génération de suggestions en utilisant un des résultats obtenus."""
    with open(output_suggestions_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Selected Document", "Number of Suggestions", "Suggested Books"])

        # Effectuer une recherche pour récupérer un échantillon de documents
        results = search_by_keyword(random.choice(keywords), G_loaded)
        ranked_results = rank_documents_by_relevance(results, centrality_scores)

        if ranked_results:
            selected_doc = ranked_results[0][0]  # Prendre le document le plus pertinent
            top_suggestions = get_top_suggestions(ranked_results, adjacency_df)

            suggested_books = get_books_by_ids(top_suggestions, books_dict)
            writer.writerow([selected_doc, len(suggested_books), suggested_books])
            print(f"[Suggestions] Selected Document: {selected_doc}, Number of Suggestions: {len(suggested_books)}")

if __name__ == "__main__":
    # Tester le ranking avec recherche par mot-clé
    test_ranking_with_search(search_by_keyword, keywords, output_keyword_csv, "Keyword Search")

    # Tester le ranking avec recherche par regex
    test_ranking_with_search(search_by_regex, regex_patterns, output_regex_csv, "Regex Search")

    # # Tester la génération de suggestions
    # test_suggestions()