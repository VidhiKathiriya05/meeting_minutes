from app.services.rag.qa import ask_meeting


def ask_question(meeting_id: int, question: str):
    """
    Wrapper around the RAG QA service.
    """

    return ask_meeting(
        question=question,
        meeting_id=meeting_id
    )   