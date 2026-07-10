from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.database import get_db 
from app.database.crud import get_meeting 
from app.services.export.pdf_generator import generate_pdf
from app.services.export.docx_generator import generate_docx
router = APIRouter(prefix="/meetings",tags=['Export'])

@router.get("/{meeting_id}/pdf")
def download_pdf(meeting_id:int, db:Session=Depends(get_db)):
    meeting = get_meeting(db,meeting_id)
    if meeting is None: raise HTTPException(status_code=404,detail="meeting not found")
    pdf_path = generate_pdf(meeting)
    return FileResponse(path = pdf_path, filename=f"meeting_{meeting.id}.pdf", media_type= "application/pdf")


@router.get("/{meeting_id}/docx")
def download_docz(meeting_id:int, db:Session=Depends(get_db)):
    meeting =get_meeting(db,meeting_id)
    if meeting is None: raise HTTPException(status_code=404,detail="Meeting not found")
    docx_path = generate_docx(meeting)
    return FileResponse(path = docx_path,filename=f"meeting {meeting.id}.docx", media_type="application/vnd.openxmlformats-officedocument.wordpressingml.document",)