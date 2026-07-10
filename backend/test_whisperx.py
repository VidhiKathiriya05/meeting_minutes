import whisperx
device = "cpu"

print("loading model...")
model = whisperx.load_model("base", device =device, compute_type="int8")
print("model loaded successfully")

audio = whisperx.load_audio(r"processed_audio\2df9bfaf-753e-4a38-9d77-737d569c23b7_processed.wav")

result = model.transcribe(audio)
print(result)