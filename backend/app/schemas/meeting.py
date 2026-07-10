from pydantic import BaseModel


class MeetingResponse(BaseModel):
    id: int
    title: str
    audio_file: str
    
    class Config:
        from_attributes = True