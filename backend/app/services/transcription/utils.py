def builder_speaker_transcript(segments):
    transcript=''
    for segment in segments: 
        speaker = segment.get("speaker")
        if speaker is None: speaker= 'speaker'
        transcript+= f"{speaker}: {segment['text']}\n\n"
    return transcript.strip()