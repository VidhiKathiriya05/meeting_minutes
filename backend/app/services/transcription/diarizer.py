import requests
import time 
def diarize_audio(audio_path: str, min_speakers=None, max_speakers=None) -> list:
    try:
        t = time.perf_counter()
        response = requests.post(
            "http://127.0.0.1:8500/diarize",
            json={"audio_path": audio_path, "min_speakers": 1, "max_speakers": 6},
            timeout=1800,
        )
        print(f"[TIME] Diarization server:{time.perf_counter()-t:.2f} sec")
        data = response.json()
        if "error" in data:
            print("Diarization error:", data["error"])
            return []
        return data.get("segments", [])
    except requests.RequestException as e:
        print("Diarization request failed:", e)
        return []