
# WhisperX Transcription Service

from __future__ import annotations

import whisperx
from typing import Optional
class WhisperXService:
    def __init__( self,model_name: str = "medium",device: str = "cpu", compute_type: str = "int8",
    ):
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type

        print(f"Loading WhisperX model: {model_name}")

        self.model = whisperx.load_model(
            whisper_arch=model_name,
            device=device,
            compute_type=compute_type,
        )

    def transcribe(self, audio_path: str,) -> dict:
        """
        Transcribe audio.

        Parameters
        ----------
        audio_path : str
            Path to audio file.

        language : str | None
            en   -> English
            hi   -> Hindi
            gu   -> Gujarati
        """

        audio = whisperx.load_audio(audio_path)

        result = self.model.transcribe(audio,lan)

        detected_language = result["language"]
        if detected_language == "ur":
            detected_language = result["language"]

            print(f"Detected language: {detected_language}")

            if detected_language not in ["hi", "en"]:
                raise ValueError(
                    f"Unsupported language '{detected_language}'. Only Hindi and English are supported."
                )
        if detected_language not in ["hi", "en"]:
            raise ValueError(
                f"Unsupported language '{detected_language}'. Only Hindi and English are supported."
            )
        
        alignment_model, metadata = whisperx.load_align_model(
            language_code=detected_language,
            device=self.device,
        )

        aligned_result = whisperx.align(
            result["segments"],
            alignment_model,
            metadata,
            audio,
            self.device,
        )

        transcript = "\n".join(
            segment["text"].strip()
            for segment in aligned_result["segments"]
        )

        return {
            "language": detected_language,
            "language_confidence": result.get(
                "language_probability",
                None,
            ),
            "transcript": transcript,
            "segments": aligned_result["segments"],
            "word_segments": aligned_result.get("word_segments", []),
        }
whisper_service = WhisperXService()