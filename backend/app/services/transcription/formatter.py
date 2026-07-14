def assign_speaker(segment_start, segment_end, diarization_segments):
    best_speaker = None
    best_overlap = 0.0

    for d in diarization_segments:
        overlap = min(segment_end, d["end"]) - max(segment_start, d["start"])
        if overlap > best_overlap:
            best_overlap = overlap
            best_speaker = d["speaker"]

    return best_speaker


def format_segments(segments, diarization_segments=None):
    diarization_segments = diarization_segments or []

    formatted = []
    for segment in segments:
        start = round(segment.start, 2)
        end = round(segment.end, 2)
        speaker = assign_speaker(start, end, diarization_segments)
        print(f"Whisper [{start:.2f}-{end:.2f}] " f"-> Speaker: {speaker}")
        formatted.append({
            "speaker": speaker,
            "start": start,
            "end": end,
            "text": segment.text.strip(),
        })
    return formatted