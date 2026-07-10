import json
from sentence_transformers import SentenceTransformer
model = SentenceTransformer ("all-MiniLM-L6-v2")

def create_embedding(text: str):
    embedding =model.encode(text).tolist()
    if isinstance(embedding,list): return embedding
    return embedding.tolist()
