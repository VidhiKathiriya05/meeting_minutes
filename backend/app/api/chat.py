from fastapi import APIRouter
from pydantic import BaseModel 

from app.services.rag.qa import ask_meeting 
router =APIRouter(prefix="/meeting",tags=['chat'])

class ChatRequest(BaseModel): question:str

@router.post("/{meeting_id}/ask")
def chat(meeting_id:int, request:ChatRequest):
    return ask_meeting(request.question,meeting_id)