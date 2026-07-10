import shutil
import uuid
from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException,
    BackgroundTasks
)

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.crud import create_meeting
from app.services.pipeline import process_meeting

router = APIRouter()

# ---------------------------------------
# Upload Folder
# ---------------------------------------

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ---------------------------------------
# Allowed Audio Formats
# ---------------------------------------

ALLOWED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a"
}


@router.post("/upload")
def upload_audio(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    audio: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    extension = Path(audio.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format."
        )

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{extension}"

    filepath = UPLOAD_DIR / unique_filename

    # Save uploaded audio
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    # Save meeting in database
    meeting = create_meeting(
        db=db,
        title=title,
        original_filename=audio.filename,
        audio_file=str(filepath)
    )
    print("created meeting: ",meeting.id)
    # Start AI processing in background
    background_tasks.add_task(
        process_meeting,
        meeting.id
    )

    return {
        "message": "Meeting uploaded successfully.",
        "meeting_id": meeting.id,
        "status": "processing"
    }   