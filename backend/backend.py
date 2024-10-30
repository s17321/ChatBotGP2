from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import chromadb

app = FastAPI()

# Model do generowania odpowiedzi
model = pipeline("text-generation", model="distilgpt2")

# Model i baza do wyszukiwania kontekstowego
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.get_collection("knowledge_base")

# Struktury zapytań do FastAPI
class Prompt(BaseModel):
    prompt: str

class QueryRequest(BaseModel):
    query: str

# Endpoint do generowania odpowiedzi chatbota
@app.post("/generate/")
async def generate_response(prompt: Prompt):
    response = model(
        prompt.prompt,
        max_length=50,
        num_return_sequences=1,
        temperature=0.7,
        top_k=50,
        truncation=True
    )
    return {"response": response[0]["generated_text"]}

# Endpoint do wyszukiwania w bazie wiedzy
@app.post("/knowledge_query/")
async def knowledge_query(request: QueryRequest):
    query_embedding = embedding_model.encode(request.query).tolist()
    results = collection.find_similar(embedding=query_embedding, limit=3)
    answers = [result["text"] for result in results]
    return {"answers": answers}
