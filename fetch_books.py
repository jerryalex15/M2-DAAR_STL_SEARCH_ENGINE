import requests
import os
import re

# Créer un dossier pour stocker les livres
os.makedirs("books", exist_ok=True)

def is_english(content):
    # Vérifier si "Language: English" apparaît dans les 5000 premières lignes
    first_5000_lines = "\n".join(content.splitlines()[:5000])
    return "Language: English" in first_5000_lines

def download_book(book_id, book_number):
    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        content = response.text
        
        # Vérifier si le livre est en anglais
        if not is_english(content):
            print(f"❌ Livre {book_id} ignoré (pas en anglais).")
            return False

        # Compter les mots
        words = re.findall(r'\b\w+\b', content)
        if len(words) >= 10000:
            # Nommer les fichiers avec un numéro basé sur l'ordre de téléchargement
            with open(f"books/book_{book_number}.txt", "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Livre {book_number} téléchargé ({len(words)} mots, Anglais).")
            return True
    return False

# Télécharger 1664 livres valides en anglais
book_count = 1119 # Compteur des livres téléchargés
for book_id in range(1119 + 1, 5000):  # Parcourir les IDs de Gutenberg
    if download_book(book_id, book_count + 1):  # Utiliser le compteur pour nommer
        book_count += 1
    if book_count >= 1664:
        print("✅ Téléchargement terminé : 1664 livres en anglais obtenus.")
        break

print(f"📚 Total de livres en anglais téléchargés : {book_count}")