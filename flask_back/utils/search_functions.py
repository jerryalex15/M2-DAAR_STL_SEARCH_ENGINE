import heapq
import re

def search_by_keyword(keyword, G):
    keyword = keyword.lower()
    return G.get(keyword, [])

def search_by_regex(pattern, G):
    results = {}
    
    # Parcours de chaque terme dans G
    for term in G:
        if re.search(pattern, term, re.IGNORECASE):
            for doc, tfidf in G[term]:
                # Ajouter ou mettre à jour les résultats
                if doc not in results or results[doc] < tfidf:
                    results[doc] = tfidf

    # Limiter les résultats aux 50 premiers éléments (par tfidf)
    top_results = heapq.nlargest(50, results.items(), key=lambda x: x[1])
    
    return top_results