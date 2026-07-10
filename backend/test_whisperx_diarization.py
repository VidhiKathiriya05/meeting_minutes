import whisperx
device ="cpu"
AUDIO_FILE = r"processed_audio\2df9bfaf-753e-4a38-9d77-737d569c23b7_processed.wav"
audio = whisperx.load_audio(AUDIO_FILE)
print("loading diarization model....")
diarize_model = whisperx.DiarizationPipeline(use_auth_token="tox",device =device)
print("running...")
diarize_segments= diarize_model(audio)
print(diarize_segments)