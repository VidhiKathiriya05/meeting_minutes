from app.services.transcription.wisper_model import model
from app.services.transcription.formatter import format_segments    
from app.services.transcription.diarizer import diarize_audio
import time 

def transcribe_audio(audio_path: str) -> dict:
    t = time.perf_counter()
    segments, info = model.transcribe(
        audio_path,
        beam_size=2,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
        condition_on_previous_text=False,
        temperature=0.0,
        language=None,
        initial_prompt=None,
    )
    print(f"Detected language: {info.language}")
    print(f"[TIME] Language detection: {time.perf_counter()-t:.2f} sec")

    if info.language == "ur":
        print("Detected Urdu. Retrying transcription with Hindi forced...")
        t = time.perf_counter()
        segments, info = model.transcribe(
            audio_path,
            beam_size=2,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
            condition_on_previous_text=False,
            repetition_penalty=1.3,
            no_repeat_ngram_size=3,
            temperature=0.0,
            language="hi",
            initial_prompt=None)
        print(f"Starting Hindi-forced transcription at {time.strftime('%H:%M:%S')}")

        segments = list(segments)   # only ONE full pass now

        print(f"[TIME] Hindi transcription: {time.perf_counter()-t:.2f} sec")
    else:
        segments = list(segments)   # normal case: only one pass, already correct

    if info.language not in ["hi", "en", "gu"]:
        raise ValueError(f"Unsupported language detected: {info.language}. Only Hindi, English, and Gujarati are supported.")
    transcript= ""
    for segment in segments:
        transcript += segment.text.strip() + " "
    
    t = time.perf_counter()
    diarization_segments = diarize_audio(audio_path)
    print(f"[TIME] Diarization: {time.perf_counter()-t:.2f} sec")
    t = time.perf_counter()
    formatted_segments = format_segments(segments, diarization_segments)
    print(f"[TIME] Whisper:{time.perf_counter()-t:.2f} sec")

    result = {
        "text": transcript.strip(),
        "segments": formatted_segments,
        "language": info.language,
        "duration": info.duration,
    }

    return result