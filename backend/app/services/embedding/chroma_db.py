import chromadb
from pathlib import Path

# ChromaDB Initialization
DB_PATH = Path("chroma_db").resolve()

print("=" * 60)
print("Initializing ChromaDB...")
print("Database Path:", DB_PATH)

client = chromadb.PersistentClient(path=str(DB_PATH))
collection = client.get_or_create_collection(
    name="meeting_chunks"
)

print("Collection Name:", collection.name)
print("Current Documents:", collection.count())
print("=" * 60)


# Store Chunk
def store_chunk(meeting_id: int, chunk_id: int, text: str, embedding):
    # Store one transcript chunk inside ChromaDB.
    doc_id = f"{meeting_id}_{chunk_id}"
    print(f"\nStoring Chunk {chunk_id}")
    print("Document ID:", doc_id)
    print("Text Length:", len(text))
    print("Embedding Length:", len(embedding))

    try:
        # Remove existing chunk if it already exists
        try:
            collection.delete(ids=[doc_id])
        except Exception:
            pass

        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[
                {
                    "meeting_id": meeting_id,
                    "chunk_id": chunk_id,
                }
            ],
        )

        print(f"Chunk {chunk_id} stored successfully.")
        print("Collection Count:", collection.count())
    except Exception as e:
        print("ERROR storing chunk:")
        print(e)
        raise


# Debug Utility
def print_collection():
    # Prints everything currently stored in ChromaDB.
    print("\nCHROMADB CONTENT ")

    print("Total Documents:", collection.count())

    data = collection.get()

    ids = data.get("ids", [])
    docs = data.get("documents", [])
    metas = data.get("metadatas", [])

    for i in range(len(ids)):
        print("-" * 50)
        print("ID:", ids[i])
        print("Metadata:", metas[i])
        print("Text Preview:", docs[i][:200])

    print("=" * 50)