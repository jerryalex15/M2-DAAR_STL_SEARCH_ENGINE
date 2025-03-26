import heapq
import re

def search_by_keyword(keyword, G):
    keyword = keyword.lower()
    return G.get(keyword, [])

# def search_by_regex(pattern, G):
#     results = {}
    
#     # Parcours de chaque terme dans G
#     for term in G:
#         if re.search(pattern, term, re.IGNORECASE):
#             for doc, tfidf in G[term]:
#                 # Ajouter ou mettre à jour les résultats
#                 if doc not in results or results[doc] < tfidf:
#                     results[doc] = tfidf

#     return results
    # # Limiter les résultats aux 50 premiers éléments (par tfidf)
    # top_results = heapq.nlargest(50, results.items(), key=lambda x: x[1])
    
    # return top_results

def search_by_regex(pattern, G):
    results = {}

    for term in G:  # On parcourt tous les termes indexés
        if re.search(pattern, term, re.IGNORECASE):  # Si le terme correspond à la regex
            for doc, tfidf in G[term]:  # G[term] est une liste de (doc, tfidf)
                # On garde le score TF-IDF le plus élevé pour chaque document
                if doc not in results or results[doc] < tfidf:
                    results[doc] = tfidf

    # Convertir en liste de tuples [(doc, tfidf)] pour avoir le même format de retour que search_by_keyword
    return list(results.items())