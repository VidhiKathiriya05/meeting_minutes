from sqlalchemy.orm import Session
from app.database.models import Meeting
import json
from sqlalchemy import or_
from app.services.embedding import embedder
# CREATE
def create_meeting(
    db,
    title,
    original_filename,
    audio_file
):

    meeting = Meeting(title=title, original_filename=original_filename, audio_file=audio_file)

    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    return meeting
# READ

def get_meeting(db: Session, meeting_id: int):
    print("Searching meeting:", meeting_id)

    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    print("Result:", meeting)

    return meeting
# UPDATE
def update_processed_audio( db: Session, meeting_id: int, processed_audio: str
):
    meeting = get_meeting(db, meeting_id)
    meeting.processed_audio_file = processed_audio
    db.commit()
    db.refresh(meeting)
    return meeting

def update_transcript( db: Session, meeting_id: int, transcript: str):

    meeting = get_meeting(db, meeting_id)
    meeting.transcript = transcript
    db.commit()
    db.refresh(meeting)
    return meeting


def update_status(db,meeting_id, status):

    meeting = get_meeting(db, meeting_id)
    if meeting is None:
        return None
    meeting =db.query(Meeting).filter(Meeting.id==meeting_id).first()    
    meeting.status = status
    db.commit()
    db.refresh(meeting)
    return meeting

def update_progress(db, meeting_id: int, progress: int):
    meeting = get_meeting(db, meeting_id)

    if meeting is None:
        return None

    meeting.progress = progress
    db.commit()
    db.refresh(meeting)
    return meeting

def update_summary(db: Session, meeting_id: int, analysis: dict):

    meeting = get_meeting(db, meeting_id)

    if meeting is None:
        return None

    summary = analysis.get("summary", "")

    if isinstance(summary, dict):
        meeting.summary = json.dumps(summary, indent=2)
    else:
        meeting.summary = summary
        
    meeting.meeting_type = analysis.get("meeting_type", "")

    meeting.participants = json.dumps(analysis.get("participants", []))
    meeting.key_points = json.dumps(analysis.get("key_points", []))
    meeting.action_items = json.dumps(analysis.get("action_items", []))
    meeting.decisions = json.dumps(analysis.get("decisions", []))
    meeting.questions = json.dumps(analysis.get("questions", []))
    meeting.risks = json.dumps(analysis.get("risks", []))
    meeting.next_steps = json.dumps(analysis.get("next_steps", []))

    sentiment = analysis.get("sentiment", {})

    if isinstance(sentiment, dict):
        meeting.sentiment = sentiment.get("overall", "")
    else:
        meeting.sentiment = str(sentiment)

    db.commit()
    db.refresh(meeting)

    return meeting

def get_all_meetings(db:Session):
    return (db.query(Meeting).order_by(Meeting.created_at.desc()).all())


def search_meetings(db:Session, query:str):
    return(db.query(Meeting).filter(
        or_(
            Meeting.title.ilike(f"%{query}%"),
            Meeting.summary.ilike(f"%{query}%"),
            Meeting.transcript.ilike(f"%{query}%")
        )
    ).order_by(Meeting.created_at.desc()).all())

def update_speaker_transcript(db:Session, meeting_id:int,speaker_transcript:str):
    meeting = get_meeting(db, meeting_id)
    if meeting is None: return None

    meeting.speaker_transcript= speaker_transcript
    db.commit()
    db.refresh(meeting)
    return meeting

def update_embedding(db,meeting_id,embedding):
    meeting =get_meeting(db, meeting_id)

    if meeting is None: return None

    meeting.embeddings = embedding
    db.commit()
    db.refresh(meeting)
    return meeting