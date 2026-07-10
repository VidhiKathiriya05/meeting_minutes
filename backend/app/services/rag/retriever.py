from app.services.embedding.embedder import create_embedding
from app.services.embedding.chroma_db import collection

def retrieve_context(question, meeting_id, top_k=3):

    print("Creating embedding...")
    query_embedding = create_embedding(question)

    print("Querying Chroma...")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"meeting_id": meeting_id}
    )

    print("Results received")
    print(results)

    return results["documents"][0]