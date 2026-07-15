from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime

from app.database.database import Base


class Meeting(Base):

    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    audio_file = Column(String, nullable=False)
    processed_audio_file = Column(String, default="")
    
    transcript = Column(String, default="")
    summary = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    key_points = Column(String, default="")
    action_items = Column(String, default="")
    decisions = Column(String, default="")
    questions = Column(String, default="")
    meeting_type= Column(String,default="")
    participants= Column(String,default="")
    risks= Column(String,default="")
    next_steps= Column(String,default="")
    sentiment= Column(String,default="")
    status = Column(String,default="uploaded")
    speaker_transcript = Column(String, default="")
    embeddings = Column(String,default="")
    progress =Column(Integer, default=0)
    pinned = Column(Boolean, default=False, nullable=False)
