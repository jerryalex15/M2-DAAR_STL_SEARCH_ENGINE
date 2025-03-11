import os
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Chemin du dossier contenant les livres
books_folder = "books"

# Récupérer la liste des fichiers texte
book_paths = [os.path.join(books_folder, f) for f in os.listdir(books_folder) if f.endswith(".txt")]

# S'assurer qu'il y a des livres à traiter
if not book_paths:
    raise ValueError("Aucun livre trouvé dans le dossier 'books'.")

# Tokenizer personnalisé : Garde uniquement les mots en alphabet latin (2 lettres minimum)
def custom_tokenizer(text):
    return [word for word in re.findall(r'\b[a-zA-Z]{2,}\b', text.lower()) if len(word) > 2 and not re.search(r'(.)\1\1', word)]

# Initialiser le vectorizer TF-IDF en utilisant un tokenizer personnalisé
tfidf_vectorizer = TfidfVectorizer(input='filename', stop_words='english', tokenizer=custom_tokenizer,) 

# Calculer la matrice TF-IDF à partir des fichiers
tfidf_matrix = tfidf_vectorizer.fit_transform(book_paths)

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

import pickle

# Enregistrer le dictionnaire G dans un fichier
with open("indexing_table.pkl", "wb") as f:
    pickle.dump(G, f)