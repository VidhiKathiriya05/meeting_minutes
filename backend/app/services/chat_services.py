from app.services.embedding.chroma_db import collection
from app.services.llm.client import OllamaClient
client = OllamaClient()
def ask_question(meeting_id: int, question: str):
    results = collection.query(
        query_texts=[question],
        n_results=5,
        where={"meeting_id": meeting_id}
    )
    context = "\n\n".join(results["documents"][0])
    print("="*50)
    print("RETRIEVED CONTEXT")
    print(context)
    print("="*50)
    print("QUESTION")
    print(question)
    prompt = f"""
You are a meeting assistant.
Answer only from the transcript below.
If the answer is not present, say:
"I couldn't find that information in this meeting."
Transcript:
{context}
Question:
{question}
Answer:
"""
    answer = client.generate(prompt)
    return answer