# Converts uploaded audio into a Whisper-compatible format only if needed.
from pathlib import Path
from pydub import AudioSegment
from app.services.audio.loader import get_audio_info

def needs_conversion(file_path: str) -> bool:

    # Returns True if the audio needs conversion.
    info = get_audio_info(file_path)
    extension = Path(file_path).suffix.lower()
    # Already Whisper compatible?
    if (
        extension == ".wav"
        and info["sample_rate"] == 16000
        and info["channels"] == 1
    ):
        return False
    return True

def convert_to_wav(input_path: str, output_path: str) -> str:

    # Convert audio to: ( WAV - Mono - 16kHz)
    # If conversion is not required, returns the original file path.

    if not needs_conversion(input_path):
        print("Audio already compatible with Whisper.")
        return input_path
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    audio.export(
        output,
        format="wav"
    )
    print("Audio converted successfully.")
    return str(output)