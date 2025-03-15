import os

def count_books_in_mybooks(directory="myBooks"):
    try:
        book_count = len([filename for filename in os.listdir(directory) if filename.endswith(".txt")])
        print("Nombre total de livres:", book_count)
    except Exception as e:
        print("Erreur lors du comptage des livres:", e)

if __name__ == "__main__":
    count_books_in_mybooks()