from pydantic_settings import BaseSettings
from pydantic import field_validator


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

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug_mode(cls, value):
        """Accept common deployment labels in addition to boolean values."""
        if isinstance(value, str) and value.lower() in {"release", "production", "prod"}:
            return False
        if isinstance(value, str) and value.lower() in {"development", "dev"}:
            return True
        return value

    DIARIZATION_PYTHON: str = r"\backend\whisperx_venv\Scripts\python.exe"
    DIARIZATION_SCRIPT: str = r"diarization_env/diarize_worker.py"
    DIARIZATION_TIMEOUT: int = 800

    class Config:
        env_file = ".env"


settings = Settings()
