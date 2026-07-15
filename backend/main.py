from fastapi import FastAPI
from app import api
from app.core.settings import settings
from app.api.export import router as export_router
from app.database.database import engine, ensure_meetings_schema
from app.database.models import Base
from app.api.meeting import router as meeting_router
from app.api.upload import router as upload_router
from app.api.transcription import router as transcription_router
from app.api.chat import router as chat_router
from app.api.frontend import router as frontend_router 
from app.api.chat import chat
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

Base.metadata.create_all(bind=engine)
ensure_meetings_schema()



app.include_router(upload_router)


@app.get("/")
def home():
    return RedirectResponse(url="/index")

app.include_router(transcription_router)

app.include_router(meeting_router)

app.include_router(chat_router)
app.include_router(export_router)
app.include_router(frontend_router)
# app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
