def get_top_suggestions(top_results, adjacency_matrix, max_suggestions=10):
    suggestions = set()
    visited_results = set(doc for doc, _ in top_results)

    for doc, _ in top_results:
        neighbors = adjacency_matrix.get(doc, {})

        for neighbor in neighbors:
            if neighbor not in visited_results and neighbor not in suggestions:
                suggestions.add(neighbor)

                if len(suggestions) >= max_suggestions:
                    return list(suggestions)

    return list(suggestions)