from app.services.transcription.whisperx import whisper_service

audio_path = r"C:\Users\Excel\Downloads\test1.mp3"

result = whisper_service.transcribe(audio_path)

print("\nDetected Language:")
print(result["language"])

print("\nTranscript:")
print(result["transcript"])

print("\nSegments:")
print(len(result["segments"]))

print("\nWord Segments:")
print(len(result["word_segments"]))