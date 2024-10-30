import subprocess
import sys
import os

def run_embeddings():
    # Sprawdza, czy baza wiedzy istnieje, np. czy baza jest załadowana do ChromaDB
    # Jeśli nie, uruchamia skrypt generowania embeddingów
    if not os.path.exists("/backend/data/knowledge_base_initialized.txt"):
        print("Generowanie bazy wiedzy...")
        subprocess.run([sys.executable, "/backend/scripts/embedding_gen.py"])
        
        # Po wygenerowaniu tworzymy plik informacyjny
        with open("/backend/data/knowledge_base_initialized.txt", "w") as f:
            f.write("Baza wiedzy została wygenerowana.")
    else:
        print("Baza wiedzy jest już załadowana.")

def run_backend():
    # Uruchamia backend FastAPI za pomocą Uvicorn
    subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.backend:app", "--reload"])

def run_frontend():
    # Uruchamia frontend Streamlit
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "frontend/frontend.py"])

if __name__ == "__main__":
    # Najpierw sprawdzamy i ewentualnie generujemy embeddingi
    run_embeddings()
    
    # Uruchamiamy backend i frontend
    run_backend()
    run_frontend()
