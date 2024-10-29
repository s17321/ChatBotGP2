from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Load the language model pipeline for text generation
model = pipeline("text-generation", model="distilgpt2")

# Define the request and response data structure
class Prompt(BaseModel):
    prompt: str

@app.post("/generate/")
async def generate_response(prompt: Prompt):
    # Generate response using the model with specific parameters
    response = model(
        prompt.prompt,
        max_length=50,            # Limit the max length of response
        num_return_sequences=1,
        temperature=0.7,          # Control creativity (lower is more deterministic)
        top_k=50,                 # Limit possible words at each step
        truncation=True           # Ensure responses are truncated at max_length
    )
    return {"response": response[0]["generated_text"]}