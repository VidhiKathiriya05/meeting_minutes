from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    HOST: str
    PORT: int
    DEBUG: bool
    DATABASE_URL: str
    UPLOAD_FOLDER: str
    OUTPUT_FOLDER: str
    LOG_FOLDER: str
    MAX_FILE_SIZE: int
    WHISPER_MODEL: str
    CHUNK_MODEL: str = "llama3.2:3b"
    MERGE_MODEL: str = "qwen2.5:7b"
    HF_TOKEN: str

    DIARIZATION_PYTHON: str = r"\backend\whisperx_venv\Scripts\python.exe"
    DIARIZATION_SCRIPT: str = r"diarization_env/diarize_worker.py"
    DIARIZATION_TIMEOUT: int = 800

    class Config:
        env_file = ".env"


settings = Settings()