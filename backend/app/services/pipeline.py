import traceback
from app.database.database import SessionLocal
from app.database.crud import get_meeting, update_processed_audio, update_transcript, update_summary, update_status,update_progress
from app.services.audio.preprocessing import preprocess_audio
from app.services.transcription.transcriber import transcribe_audio

from app.services.llm.chunker import build_chunks
from app.services.llm.analyzer import analyze_chunk, merge_analysis
from sqlalchemy import Integer
from app.services.embedding.embedder import create_embedding
from app.services.embedding.chroma_db import store_chunk


def process_meeting(meeting_id: int):

    db = SessionLocal()

    try:
        update_status(db, meeting_id, "preprocessing")
        update_progress(db,meeting_id,5)

        meeting = get_meeting(db, meeting_id)

        if meeting is None:
            raise ValueError(f"Meeting {meeting_id} not found.")

        print("\n========== PREPROCESSING AUDIO ==========")

        processed = preprocess_audio(meeting.audio_file)
        processed_audio = processed["processed_audio"]

        update_processed_audio(db, meeting_id, processed_audio)
        update_status(db, meeting_id, "transcribing")
        update_progress(db, meeting_id, 20)
        print("\n========== TRANSCRIBING AUDIO ==========")

        transcript_result = transcribe_audio(processed_audio)

        transcript = transcript_result["text"]
        segments = transcript_result["segments"]

        update_transcript(db, meeting_id, transcript)
        update_status(db, meeting_id, "chunking")
        update_progress(db,meeting_id,35)

        print("Transcript length:", len(transcript))
        print("First 100 chars:", transcript[:100])
        print(f"Transcript Length: {len(transcript)}")

        print("\n========== BUILDING CHUNKS ==========")

        chunks = build_chunks(segments)
        update_status(db, meeting_id,"analyzing")
        update_progress(db, meeting_id,40)

        print(f"Total Chunks: {len(chunks)}")

        results = []

        print("\n========== PROCESSING CHUNKS ==========")

        for i, chunk in enumerate(chunks):
            progress =40+ int(((i+1)/len(chunks))*40)
            update_progress(db,meeting_id,progress)
            print(f"\nChunk {i+1}/{len(chunks)}")

            # Create embedding
            embedding = create_embedding(chunk)

            # Store in Chroma
            store_chunk(
                meeting_id=meeting_id,
                chunk_id=i,
                text=chunk,
                embedding=embedding,
            )
            print("ollama loading ")
            # Analyze chunk
            analysis = analyze_chunk(chunk)
            print("ollama finished")

            results.append(analysis)

        print("\n========== MERGING RESULTS ==========")
        print("Total results:", len(results))
        for i, r in enumerate(results):
            print(f"Result {i}:")
            print(r)
        update_status(db,meeting_id,"merging")
        update_progress(db,meeting_id,85)
        final_analysis = merge_analysis(results)

        update_summary(db, meeting_id, final_analysis)
        update_status(db,meeting_id,"generating_report")
        update_progress(db,meeting_id,95)

        update_status(db, meeting_id, "completed")
        update_progress(db,meeting_id,"100")
        print(f"\nMeeting {meeting_id} processed successfully.")

    except Exception:

        db.rollback()
        update_status(db, meeting_id, "failed")

        print("\n========== PIPELINE ERROR ==========")

        traceback.print_exc()

    finally:
        db.close()