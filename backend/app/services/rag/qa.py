from app.services.llm.client import OllamaClient
from app.services.rag.retriever import retrieve_context
from app.services.rag.prompts import rag_prompt

client = OllamaClient()


def ask_meeting(question: str, meeting_id: int):

    context = retrieve_context(question, meeting_id)

    if not context:
        return {
            "answer": "I couldn't find that information in this meeting."
        }

    prompt = rag_prompt(context, question)

    answer = client.generate(prompt)

    return {
        "answer": answer.strip()
    }