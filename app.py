# app.py
import subprocess
import sys

def run_backend():
    # Run the FastAPI backend using Uvicorn
    subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.backend:app", "--reload"])

def run_frontend():
    # Run the Streamlit frontend
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "frontend/frontend.py"])

if __name__ == "__main__":
    # Start the backend and frontend
    run_backend()
    run_frontend()
