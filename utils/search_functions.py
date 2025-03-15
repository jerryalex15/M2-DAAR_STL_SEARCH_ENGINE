import re

def search_by_keyword(keyword, G):
    keyword = keyword.lower()
    return G.get(keyword, [])

def search_by_regex(pattern, G):
    results = {}
    for term in G:
        if re.search(pattern, term, re.IGNORECASE):
            for doc, tfidf in G[term]:
                if doc not in results or results[doc] < tfidf:
                    results[doc] = tfidf
    return list(results.items())