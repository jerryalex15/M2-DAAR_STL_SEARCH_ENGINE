import os
import re
import pickle
import nltk
from concurrent.futures import ProcessPoolExecutor, as_completed
from nltk.corpus import stopwords

# Télécharger les stop words si nécessaire
# nltk.download('stopwords')

# Charger les stop words en anglais
stop_words = set(stopwords.words('english'))

# Tokenizer personnalisé : Garde uniquement les mots en alphabet latin (2 lettres minimum)
def custom_tokenizer(text):
    return [word for word in re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
            if len(word) > 2 and not re.search(r'(.)\1\1', word) and word not in stop_words]

# Extraire les mots-clés de chaque livre dans le dossier 'books'
def extract_keywords_from_books(books_directory):
    books_keywords = {}
    for book in os.listdir(books_directory):
        book_path = os.path.join(books_directory, book)
        if os.path.isfile(book_path):
            with open(book_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            words = custom_tokenizer(text)
            books_keywords[book] = set(words)
    return books_keywords

# Calcul de la distance Jaccard entre deux ensembles
def jaccard_distance(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return 1 - (intersection / union) if union != 0 else 1

# Fonction pour calculer la distance Jaccard entre une paire de livres
def compute_jaccard_pair(pair):
    book1, book2, keywords1, keywords2, threshold = pair
    jaccard_distance_val = jaccard_distance(keywords1, keywords2)
    if jaccard_distance_val < threshold:
        return (book1, book2, jaccard_distance_val)
    return None

if __name__ == '__main__':
    # Charger les livres et leurs mots-clés
    books_directory = 'myBooks'
    books_keywords = extract_keywords_from_books(books_directory)

    # Initialiser la matrice de distance Jaccard
    book_list = list(books_keywords.keys())
    adjacency_df = {book1: {book2: 0 for book2 in book_list} for book1 in book_list}

    # Préparer les paires de livres pour le calcul
    threshold = 0.5
    pairs = [(book1, book2, books_keywords[book1], books_keywords[book2], threshold)
            for i, book1 in enumerate(book_list) for j, book2 in enumerate(book_list) if i < j]

    # Paralléliser le calcul des distances Jaccard
    print(f"🔄 Lancement du calcul sur {len(pairs)} paires avec {os.cpu_count()} cœurs...")

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(compute_jaccard_pair, pair) for pair in pairs]
        for future in as_completed(futures):
            result = future.result()
            if result:
                book1, book2, distance = result
                adjacency_df[book1][book2] = distance
                adjacency_df[book2][book1] = distance  # Symétrie

    # Sauvegarder la matrice d'adjacence (distance Jaccard)
    with open("utils/adjacency_df_jaccard.pkl", "wb") as f:
        pickle.dump(adjacency_df, f)

    print("✅ Matrice d'adjacence (Jaccard) sauvegardée avec succès.")
