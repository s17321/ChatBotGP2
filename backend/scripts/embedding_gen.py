from sentence_transformers import SentenceTransformer
import chromadb
from PyPDFLoader import PyPDFLoader
import os

# Inicjalizacja modelu do generowania embeddingów i klienta ChromaDB
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.create_collection("knowledge_base")

# Funkcja do wczytania PDF i zapisania w bazie wektorowej
def load_pdf_to_database(file_path):
    print("Rozpoczynanie ładowania pliku PDF...")
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()  # Wczytywanie i dzielenie na strony
    print(f"Liczba stron w dokumencie: {len(pages)}")

    for i, page in enumerate(pages):
        text = page.page_content.strip()  # Pobranie tekstu ze strony (używając PyPDFLoader)
        if text:  # Sprawdzenie, czy strona nie jest pusta
            embedding = model.encode(text).tolist()  # Generowanie embeddingu
            collection.add({
                "id": f"page_{i}",
                "text": text,
                "embedding": embedding
            })
            print(f"Przetworzono stronę {i+1}")
    print("Baza danych została załadowana!")

    # Tworzenie pliku informacyjnego po zakończeniu przetwarzania
    with open("backend/data/knowledge_base_initialized.txt", "w") as f:
        f.write("Baza wiedzy została wygenerowana.")
    print("Plik knowledge_base_initialized.txt został utworzony.")

# Wywołanie funkcji z plikiem PDF
if __name__ == "__main__":
    load_pdf_to_database("backend/data/BSI_ALL.pdf")
