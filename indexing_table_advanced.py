import os
import re
import shutil
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Chemin du dossier contenant les livres
books_folder = "books"

# Récupérer la liste des fichiers texte
book_paths = [os.path.join(books_folder, f) for f in os.listdir(books_folder) if f.endswith(".txt")]

# S'assurer qu'il y a des livres à traiter
if not book_paths:
    raise ValueError("Aucun livre trouvé dans le dossier 'books'.")

# Fonction pour extraire le titre et l'auteur à partir des métadonnées
def extract_metadata(text):
    title_match = re.search(r"^Title:\s*(.*?)(?=\n|$)", text, re.IGNORECASE)
    author_match = re.search(r"^Author:\s*(.*?)(?=\n|$)", text, re.IGNORECASE)

    title = title_match.group(1) if title_match else "Unknown Title"
    author = author_match.group(1) if author_match else "Unknown Author"
    
    return title, author

# Tokenizer personnalisé : Garde uniquement les mots en alphabet latin (2 lettres minimum)
def custom_tokenizer(text):
    return [word for word in re.findall(r'\b[a-zA-Z]{2,}\b', text.lower()) if len(word) > 2 and not re.search(r'(.)\1\1', word)]

# Initialiser le vectorizer TF-IDF en utilisant un tokenizer personnalisé
tfidf_vectorizer = TfidfVectorizer(input='filename', stop_words='english', tokenizer=custom_tokenizer)

# Créer un dossier temporaire pour les livres enrichis
temp_folder = "books_temp"
os.makedirs(temp_folder, exist_ok=True)

# Lire et préparer le texte des livres avec les métadonnées
for book_path in book_paths:
    with open(book_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
        # Extraire le titre et l'auteur
        title, author = extract_metadata(content)

        num_repetitions_title = 10
        num_repetitions_author = 15
        
        # Ajouter le titre et l'auteur plusieurs fois
        augmented_text = f"{' '.join([title] * num_repetitions_title)} {' '.join([author] * num_repetitions_author)} " + content
        
        # Créer un chemin temporaire pour le livre enrichi
        temp_book_path = os.path.join(temp_folder, os.path.basename(book_path))
        
        # Sauvegarder le texte augmenté dans le fichier temporaire
        with open(temp_book_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(augmented_text)

# Calculer la matrice TF-IDF à partir des fichiers augmentés dans le dossier temporaire
book_paths_temp = [os.path.join(temp_folder, f) for f in os.listdir(temp_folder) if f.endswith(".txt")]

# Calculer la matrice TF-IDF à partir des livres enrichis
tfidf_matrix = tfidf_vectorizer.fit_transform(book_paths_temp)

# Nettoyer : Supprimer le dossier temporaire après utilisation
shutil.rmtree(temp_folder)

# Créer un DataFrame où chaque ligne est un livre et chaque colonne est un mot
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), index=[os.path.basename(p) for p in book_paths], columns=tfidf_vectorizer.get_feature_names_out())

# Afficher un aperçu du DataFrame
print(tfidf_df.head())

# Initialisation du dictionnaire vide
G = {}

# Parcourir les colonnes (termes) et les lignes (livres) du DataFrame
for term in tfidf_df.columns:  # Parcours de chaque terme (colonne)
    for book in tfidf_df.index:  # Parcours de chaque livre (ligne)
        tfidf_value = tfidf_df.loc[book, term]
        
        if tfidf_value > 0.0:  # Ignorer les termes avec un TF-IDF de 0.0
            if term not in G:  # Si le terme n'est pas encore dans le dictionnaire, on le crée
                G[term] = set()  # Créer un ensemble pour ce terme
            
            # Ajouter le couple (nom_du_livre, tfidf_value) au terme
            G[term].add((book, tfidf_value))

# Sauvegarder le dictionnaire G dans un fichier
import pickle

with open("indexing_table_advanced.pkl", "wb") as f:
    pickle.dump(G, f)

print("Dictionnaire G sauvegardé avec succès.")
