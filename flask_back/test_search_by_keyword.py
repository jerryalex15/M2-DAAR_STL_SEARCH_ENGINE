import time
import csv
import os
import sys



from utils.data_loader import load_index, load_adjacency_matrix, load_books_dict, compute_centrality_scores, get_books_by_ids
from utils.search_functions import search_by_keyword, search_by_regex
from utils.ranking import rank_documents_by_relevance
from utils.suggestions import get_top_suggestions
import re

G_loaded = load_index("utils/indexing_table_advanced.pkl")
adjacency_df = load_adjacency_matrix("utils/adjacency_df_jaccard.pkl")
books_dict = load_books_dict("utils/books_dict.pkl")
centrality_scores = compute_centrality_scores(adjacency_df)

# Liste des 5 mots-clés à tester
keywords = ["Sargon", "Lewis", "babylon", "network", "king"]

# Fichier CSV où nous allons enregistrer les résultats
output_csv = "search_times.csv"

def test_search_by_keywords():
    # Créer ou ouvrir le fichier CSV pour sauvegarder les résultats
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Écrire l'en-tête du fichier CSV
        writer.writerow(["Keyword", "Execution Time (s)", "Number of Books Returned"])
        
        # Pour chaque mot-clé dans la liste
        for keyword in keywords:
            start_time = time.time()  # Démarrer le chronomètre
            
            # Effectuer la recherche par mot-clé
            results = search_by_keyword(keyword, G_loaded)
            books = get_books_by_ids(results, books_dict)
            
            # Calculer le temps d'exécution
            execution_time = time.time() - start_time
            num_books = len(books)  # Nombre de livres retournés
            
            # Écrire les résultats dans le fichier CSV
            writer.writerow([keyword, execution_time, num_books])
            
            # Afficher les résultats dans le terminal
            print(f"Keyword: {keyword}, Execution Time: {execution_time:.4f} s, Number of Books: {num_books}")

if __name__ == "__main__":
    test_search_by_keywords()