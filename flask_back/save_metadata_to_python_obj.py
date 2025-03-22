import json
import pickle

# # Charger le JSON depuis le fichier books.json
# with open("utils/books.json", "r", encoding="utf-8") as f:
#     books_list = json.load(f)

# # Créer un dictionnaire avec les IDs comme clés
# books_dict = {book["id"]: book for book in books_list}

# # Sauvegarder le dictionnaire en format pickle
# with open("utils/books_dict.pkl", "wb") as f:
#     pickle.dump(books_dict, f)

# print(f"Dictionnaire sauvegardé avec {len(books_dict)} livres dans 'books_dict.pkl'")

####
with open("utils/books_dict.pkl", "rb") as f:
    books_dict = pickle.load(f)

print(books_dict[26184])  # Affiche les IDs des livres