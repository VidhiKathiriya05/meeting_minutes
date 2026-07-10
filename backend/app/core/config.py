from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

UPLOAD_PATH = BASE_DIR / "uploads"

OUTPUT_PATH = BASE_DIR / "outputs"

LOG_PATH = BASE_DIR / "logs"

UPLOAD_PATH.mkdir(exist_ok=True)

OUTPUT_PATH.mkdir(exist_ok=True)

LOG_PATH.mkdir(exist_ok=True)