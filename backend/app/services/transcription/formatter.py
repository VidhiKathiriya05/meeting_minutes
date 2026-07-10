def format_segments(segments):
    
    formatted = []
    for segment in segments:
        formatted.append({
            "speaker": None,
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip()
        })
    return formatted