import pickle

# Charger le dictionnaire G depuis le fichier
with open("indexing_table_advanced.pkl", "rb") as f:
    G_loaded = pickle.load(f)

# Exemple d'accès à un terme après le chargement du fichier
def search_by_keyword(keyword, G):
    # Vérifier si le mot-clé est présent dans l'indexation
    if keyword in G:
        # Trier les résultats par la valeur TF-IDF décroissante
        return sorted(G[keyword], key=lambda x: x[1], reverse=True)
    return []
    

import re

def search_by_regex(pattern, G):
    results = []
    # Parcourir tous les termes de l'index
    for term in G:
        if re.search(pattern, term):
            results.extend(G[term])
    # Éliminer les doublons et trier
    return sorted(set(results), key=lambda x: x[1], reverse=True)

# Exemple d'utilisation
result = search_by_keyword("sargon", G_loaded)
print(result)

# Exemple d'utilisation
# result = search_by_regex(r"sar.*", G_loaded)
# print(result)  # Affiche les livres avec des mots commençant par "sar"