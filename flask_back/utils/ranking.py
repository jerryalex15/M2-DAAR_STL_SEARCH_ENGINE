def rank_documents_by_relevance(results, centrality_scores, centrality_type="pagerank"):
    centrality = centrality_scores.get(centrality_type, {})
    alpha = 1e-6

    # Calculer la pertinence des résultats en fonction du TF-IDF et de la centralité
    ranked_results = [(doc, tfidf * (centrality.get(doc, 0) + alpha)) for doc, tfidf in results]
    
    # Trier les résultats par pertinence (du plus pertinent au moins pertinent)
    sorted_results = sorted(ranked_results, key=lambda x: x[1], reverse=True)
    
    # Limiter le nombre de résultats à 50
    return sorted_results[:50]