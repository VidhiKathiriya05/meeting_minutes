import whisperx
device = "cpu"
audio = whisperx.load_audio(r"processed_audio\2df9bfaf-753e-4a38-9d77-737d569c23b7_processed.wav")
model = whisperx.load_model("base", device=device, compute_type ="int8")


result = model.transcribe(audio)
model_a,metadata = whisperx.load_align_model(language_code=result["language"], device= device)

result = whisperx.align(result["segments"], model_a,metadata,audio,device)


print(result["segments"][0])