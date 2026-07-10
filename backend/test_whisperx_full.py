import whisperx

device = "cpu"

AUDIO_FILE = r"processed_audio\2df9bfaf-753e-4a38-9d77-737d569c23b7_processed.wav"

# 1. Load model
model = whisperx.load_model( "base", device, compute_type="int8")

# 2. Load audio
audio = whisperx.load_audio(AUDIO_FILE)

# 3. Transcribe
result = model.transcribe(audio)

#  Alignment
model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device )
result = whisperx.align(result["segments"], model_a, metadata, audio, device)

# Diarizatio
diarize_model = whisperx.DiarizationPipeline(use_auth_token="token", device=device)
diarize_segments = diarize_model(audio)

# Assign speakers
result = whisperx.assign_word_speakers(diarize_segments, result)

# Print final transcript
for segment in result["segments"]:
    speaker = segment.get("speaker", "Unknown")
    print(f"[{speaker}] {segment['text']}")