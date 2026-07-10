from pathlib import Path
import uuid
from app.services.audio.converter import convert_to_wav
from app.services.audio.noise import reduce_noise
from app.services.audio.validator import validate_audio

PROCESSED_DIR = Path("processed_audio")
PROCESSED_DIR.mkdir(exist_ok=True)

def preprocess_audio(audio_path:str)->dict:
    """steps:
    1 validate audio 
    2 convert to whisper-compatible WAV
    3 apply niose reduction 
    4 return processed files
    """
    
    # step 1
    validation = validate_audio(audio_path)
    if not validation['valid']:
        return {"error": validation['message']}
    
    # step 2 
    input_file= Path(audio_path)
    base_name = input_file.stem
    output_filename = f"{base_name}_processed.wav"
    output_path = PROCESSED_DIR / output_filename
    processed_file = convert_to_wav(audio_path, str(output_path))

    # step 3 
    processed_file= reduce_noise(processed_file)
    return {
        "status":"success",
        "original_audio":audio_path,
        "processed_audio": processed_file
        }