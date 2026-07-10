from app.services.transcription.wisper_model import model
from app.services.transcription.formatter import format_segments


def transcribe_audio(audio_path: str) -> dict:

    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        word_timestamps=True,
        vad_filter=True
    )

    segments = list(segments)

    transcript = ""

    for segment in segments:
        transcript += segment.text.strip() + " "

    result = {
        "text": transcript.strip(),
        "segments": format_segments(segments),
        "language": info.language,
        "duration": info.duration,
    }

    return result