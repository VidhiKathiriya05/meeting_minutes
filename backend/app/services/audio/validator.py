from pathlib import Path
import os
# Allowed audio formats
ALLOWED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a"
}
# Maximum upload size
# 500 MB
MAX_FILE_SIZE = 500 * 1024 * 1024

def file_exists(file_path: str) -> bool:
    # Check whether a file exists.
    return Path(file_path).exists()

def get_extension(file_path: str) -> str:    
    # Returns file extension in lowercase.
    return Path(file_path).suffix.lower()

def is_supported_audio(file_path: str) -> bool:
    # Checks whether the uploaded file is a supported audio format.
    extension = get_extension(file_path)
    return extension in ALLOWED_EXTENSIONS

def get_file_size(file_path: str) -> int:
    # Returns file size in bytes.
    return os.path.getsize(file_path)


def validate_file_size(file_path: str) -> bool:
    # Returns True if file size is within the allowed limit.
    size = get_file_size(file_path)
    return size <= MAX_FILE_SIZE

def get_file_name(file_path: str) -> str:
    
    # Returns filename only.
    return Path(file_path).name

def validate_audio(file_path: str):

    # Complete validation.
    if not file_exists(file_path):
        return {
            "valid": False,
            "message": "File does not exist."
        }
    
    if not is_supported_audio(file_path):
        return {
            "valid": False,
            "message": "Unsupported audio format."
        }

    if not validate_file_size(file_path):
        return {
            "valid": False,
            "message": "File exceeds maximum allowed size."
        }
    return {
        "valid": True,
        "message": "Audio file validated successfully.",
        "filename": get_file_name(file_path),
        "extension": get_extension(file_path),
        "size": get_file_size(file_path)
    }