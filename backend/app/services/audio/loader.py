
from pathlib import Path
from pydub import AudioSegment


def load_audio(file_path: str) -> AudioSegment:
    """
    Loads an audio file.
    Returns: AudioSegment object
    """
    return AudioSegment.from_file(file_path)

def get_duration(audio: AudioSegment) -> float:
        # Returns duration in seconds.
    return len(audio) / 1000

def get_sample_rate(audio: AudioSegment) -> int:
    # Returns sample rate.
    return audio.frame_rate

def get_channels(audio: AudioSegment) -> int:
    # Returns number of channels.
    return audio.channels

def get_sample_width(audio: AudioSegment) -> int:
    # Returns sample width in bytes.
    return audio.sample_width

def get_audio_info(file_path: str) -> dict:
    # Returns all important metadata.
    audio = load_audio(file_path)
    return {
        "filename": Path(file_path).name,
        "duration": round(get_duration(audio), 2),
        "sample_rate": get_sample_rate(audio),
        "channels": get_channels(audio),
        "sample_width": get_sample_width(audio)
    }