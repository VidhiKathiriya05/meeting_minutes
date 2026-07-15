from pathlib import Path
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.crud import get_meeting,get_all_meetings,search_meetings
from app.utils.serializer import parse_json_field
from fastapi.responses import FileResponse
from app.services.export.pdf_generator import generate_pdf
from app.services.export.docx_generator import generate_docx

router=APIRouter(prefix="/meetings",tags=["meetings"])


class MeetingUpdate(BaseModel):
    filename: str | None = None
    pinned: bool | None = None


def remove_stored_file(path_value: str | None, allowed_directory: Path) -> None:
    """Only remove files that belong to this application's managed folders."""
    if not path_value:
        return
    try:
        file_path = Path(path_value).resolve()
        allowed_path = allowed_directory.resolve()
        if allowed_path in file_path.parents and file_path.is_file():
            file_path.unlink()
    except OSError:
        # A missing/locked generated file must not prevent database cleanup.
        pass

# router = APIRouter(prefix="/meeting", tags=["Export"])


@router.get("/{meeting_id}/pdf")
def download_pdf(meeting_id: int, db: Session = Depends(get_db)):
    meeting = get_meeting(db, meeting_id)

    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")

    pdf = generate_pdf(meeting)

    return FileResponse(
        pdf,
        filename=f"meeting_{meeting.id}.pdf",
        media_type="application/pdf",
    )


@router.get("/{meeting_id}/docx")
def download_docx(meeting_id: int, db: Session = Depends(get_db)):
    meeting = get_meeting(db, meeting_id)

    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")

    docx = generate_docx(meeting)

    return FileResponse(
        docx,
        filename=f"meeting_{meeting.id}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

@router.get("/search")
def search(q:str,db:Session=Depends(get_db)):
    meetings=search_meetings(db,q)
    return[{ 
            "id": meeting.id,
            "title": meeting.title,
            "original_filename": meeting.original_filename,
            "pinned": meeting.pinned,
            "summary": meeting.summary,
            "status": meeting.status,
            "created_at": meeting.created_at,
            "meeting_type":meeting.meeting_type,
          }for meeting in meetings
    ]


@router.get("/{meeting_id}")
def read_meeting(meeting_id:int,db:Session=Depends(get_db)):
    meeting=get_meeting(db,meeting_id)
    if not meeting:
        raise HTTPException(status_code=404,detail="Meeting not found")
    return {
    "id": meeting.id,
    "title": meeting.title,
    "original_filename": meeting.original_filename,
    "pinned": meeting.pinned,
    "summary": meeting.summary or "",
    "status": meeting.status,
    "progress":meeting.progress,
    "transcript": meeting.transcript,
    "speaker_transcript":meeting.speaker_transcript,
    "meeting_type": meeting.meeting_type,
    "participants": parse_json_field(meeting.participants),
    "key_points": parse_json_field(meeting.key_points),
    "action_items": parse_json_field(meeting.action_items),
    "decisions": parse_json_field(meeting.decisions),
    "questions": parse_json_field(meeting.questions),
    "risks": parse_json_field(meeting.risks),
    "next_steps": parse_json_field(meeting.next_steps),
    "sentiment": meeting.sentiment,
    "created_at": meeting.created_at
}


@router.patch("/{meeting_id}")
def update_meeting(meeting_id: int, payload: MeetingUpdate, db: Session = Depends(get_db)):
    meeting = get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    if payload.filename is not None:
        filename = Path(payload.filename.strip()).name
        if not filename:
            raise HTTPException(status_code=422, detail="A file name is required")
        meeting.original_filename = filename
        meeting.title = Path(filename).stem or filename
    if payload.pinned is not None:
        meeting.pinned = payload.pinned

    db.commit()
    db.refresh(meeting)
    return {"id": meeting.id, "title": meeting.title, "original_filename": meeting.original_filename, "pinned": meeting.pinned}


@router.delete("/{meeting_id}", status_code=204)
def delete_meeting(meeting_id: int, db: Session = Depends(get_db)):
    meeting = get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    remove_stored_file(meeting.audio_file, Path("uploads"))
    remove_stored_file(meeting.processed_audio_file, Path("processed_audio"))
    for extension in ("pdf", "docx"):
        remove_stored_file(str(Path("output") / f"meeting_{meeting.id}.{extension}"), Path("output"))

    db.delete(meeting)
    db.commit()



@router.get("/")
def list_meeting(db:Session = Depends(get_db)):
    meetings= get_all_meetings(db)
    return [
        { 
            "id": meeting.id,
            "title": meeting.title,
            "original_filename": meeting.original_filename,
            "pinned": meeting.pinned,
            "summary": meeting.summary,
            "status": meeting.status,
            "progress":meeting.progress,
            "created_at": meeting.created_at,
            "meeting_type":meeting.meeting_type,
                    }for meeting in meetings
    ]

