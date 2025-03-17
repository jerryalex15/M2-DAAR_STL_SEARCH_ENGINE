from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.data_loader import load_index, load_adjacency_matrix, load_books_dict, compute_centrality_scores, get_books_by_ids
from utils.search_functions import search_by_keyword, search_by_regex
from utils.ranking import rank_documents_by_relevance
from utils.suggestions import get_top_suggestions
import re

app = Flask(__name__)

# Autoriser toutes les origines (développement)
CORS(app)

# Ou pour autoriser uniquement Angular (localhost:4200)
# CORS(app, origins=["http://localhost:4200"])


# Chargement des données
G_loaded = load_index("utils/indexing_table_advanced.pkl")
adjacency_df = load_adjacency_matrix("utils/adjacency_df_jaccard.pkl")
books_dict = load_books_dict("utils/books_dict.pkl")
centrality_scores = compute_centrality_scores(adjacency_df)

@app.route('/search_by_keyword', methods=['POST'])
def search_by_keyword_route():
    data = request.get_json()
    keyword = data.get("keyword", "")

    if not keyword:
        return jsonify({"error": "No keyword provided"}), 400

    results = search_by_keyword(keyword, G_loaded)
    return jsonify(get_books_by_ids(results, books_dict))

@app.route('/search_by_regex', methods=['POST'])
def search_by_regex_route():
    data = request.get_json()
    pattern = data.get("pattern", "")

    if not pattern:
        return jsonify({"error": "No regex pattern provided"}), 400

    try:
        results = search_by_regex(pattern, G_loaded)
    except re.error as e:
        return jsonify({"error": f"Invalid regex pattern: {str(e)}"}), 400

    return jsonify(get_books_by_ids(results, books_dict))

@app.route('/rank_and_suggest', methods=['POST'])
def rank_and_suggest():
    try:
        data = request.get_json()
        keyword = data.get("keyword", "")
        regex_pattern = data.get("pattern", "")
        centrality_type = data.get("centrality_type", "pagerank")
        max_suggestions = data.get("max_suggestions", 10)

        if not keyword and not regex_pattern:
            return jsonify({"error": "No keyword or regex provided"}), 400

        top_results = search_by_keyword(keyword, G_loaded) if keyword else search_by_regex(regex_pattern, G_loaded)
        if not top_results:
            return jsonify({"error": "No results found"}), 404

        ranked_results = rank_documents_by_relevance(top_results, centrality_scores, centrality_type)
        top_suggestions = get_top_suggestions(ranked_results, adjacency_df, max_suggestions)

        return jsonify({
            "ranked_results": get_books_by_ids(ranked_results, books_dict),
            "top_suggestions": get_books_by_ids(top_suggestions, books_dict)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)