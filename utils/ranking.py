def rank_documents_by_relevance(results, centrality_scores, centrality_type="pagerank"):
    centrality = centrality_scores.get(centrality_type, {})
    alpha = 1e-6

    ranked_results = [(doc, tfidf * (centrality.get(doc, 0) + alpha)) for doc, tfidf in results]
    return sorted(ranked_results, key=lambda x: x[1], reverse=True)