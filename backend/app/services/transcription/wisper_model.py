from faster_whisper import WhisperModel
# Load model only once
# tiny, base, small, medium, large-v3
MODEL_SIZE = "medium"

print("Loading Whisper model...")
model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)
print("Whisper model loaded.")