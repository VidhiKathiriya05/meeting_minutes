def build_chunks(segments, max_words=1000, overlap_words=150):
    """
    Build overlapping transcript chunks.

    max_words = maximum words per chunk
    overlap_words = words shared with previous chunk
    """

    chunks = []

    current_chunk = []
    current_words = 0

    for segment in segments:

        text = segment["text"].strip()
        words = len(text.split())

        # If adding this segment exceeds chunk size
        if current_words + words > max_words:

            chunks.append(" ".join(current_chunk))

            # -------- Create overlap --------
            overlap = []
            overlap_count = 0

            for previous in reversed(current_chunk):
                overlap.insert(0, previous)
                overlap_count += len(previous.split())

                if overlap_count >= overlap_words:
                    break

            current_chunk = overlap
            current_words = overlap_count

        current_chunk.append(text)
        current_words += words

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks