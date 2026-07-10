from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.crud import (get_meeting, update_transcript)
from app.services.transcription.transcriber import transcribe_audio

router = APIRouter()

@router.post("/transcribe/{meeting_id}")
def transcribe(meeting_id:int, db:Session = Depends(get_db)):

    meeting = get_meeting(db, meeting_id)

    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    result = transcribe_audio(meeting.processed_audio_file)
    update_transcript(db, meeting_id, result["text"])
    return result

