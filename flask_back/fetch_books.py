import requests
import json
import os

def download_books(start_id=0):
    base_url = "https://gutendex.com/books"
    output_dir = "myBooks"
    metadata_file = os.path.join(output_dir, "books.json")
    max_books = 1664

    # Crée le dossier s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)

    # Charger les métadonnées existantes
    if os.path.exists(metadata_file):
        with open(metadata_file, "r", encoding="utf-8") as f:
            books_metadata = json.load(f)
    else:
        books_metadata = []

    existing_ids = {book["id"] for book in books_metadata}

    page = 1
    while len(books_metadata) < max_books:
        print(f"Fetching page {page}...")
        response = requests.get(base_url, params={"page": page})
        if response.status_code != 200:
            print("Error fetching data.")
            break

        data = response.json()
        for book in data["results"]:
            if len(books_metadata) >= max_books:
                break

            if book["id"] <= start_id:
                continue

            if "en" in book["languages"] and "text/plain; charset=us-ascii" in book["formats"] and book["id"] not in existing_ids:
                text_url = book["formats"]["text/plain; charset=us-ascii"]
                text_response = requests.get(text_url)

                # Vérifier si le contenu dépasse 10 000 mots
                text_content = text_response.text
                if len(text_content.split()) > 10000:
                    print(f"Downloading: {book['title']}")

                    # Enregistrer le texte
                    text_path = os.path.join(output_dir, f"{book['id']}.txt")
                    with open(text_path, "w", encoding="utf-8") as f:
                        f.write(text_content)

                    # Sauvegarder les métadonnées avec l'URL de l'image
                    books_metadata.append({
                        "id": book["id"],
                        "title": book["title"],
                        "authors": [author["name"] for author in book["authors"]],
                        "language": book["languages"],
                        "text_url": text_url,
                        "image_url": book["formats"].get("image/jpeg", None)
                    })

                    # Mettre à jour les métadonnées
                    with open(metadata_file, "w", encoding="utf-8") as f:
                        json.dump(books_metadata, f, ensure_ascii=False, indent=4)

        # Arrêter si aucune page suivante
        if not data["next"]:
            break

        page += 1

    print(f"Téléchargement terminé : {len(books_metadata)} livres téléchargés.")

if __name__ == "__main__":
    start_id = 1666
    download_books(start_id)


