from fastapi import APIRouter
from pydantic import BaseModel

from app.services.chat_services import ask_question

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    meeting_id: int
    question: str


@router.post("/")
def chat(req: ChatRequest):

    answer = ask_question(
        meeting_id=req.meeting_id,
        question=req.question
    )

    return {
        "answer": answer
    }