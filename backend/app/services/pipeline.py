import traceback
from app.database.database import SessionLocal
from app.database.crud import get_meeting, update_processed_audio, update_transcript, update_summary, update_status,update_progress,update_speaker_transcript
from app.services.audio.preprocessing import preprocess_audio
from app.services.transcription.transcriber import transcribe_audio
from app.services.llm.chunker import build_chunks
from app.services.llm.analyzer import analyze_chunk, merge_analysis
from sqlalchemy import Integer
from app.services.embedding.embedder import create_embedding
from app.services.embedding.chroma_db import store_chunk
from app.services.transcription.utils import builder_speaker_transcript
# from app.services.transcription.diarize import dia    rize_audio
import time 
import json

def log_time(stage, start_time):
    elapsed = time.perf_counter() - start_time
    print(f"[TIME] {stage:<30}: {elapsed:.2f} sec")

def process_meeting(meeting_id: int):

    db = SessionLocal()
    pipeline_start = time.perf_counter()

    try:
        update_status(db, meeting_id, "preprocessing")
        update_progress(db,meeting_id,5)

        meeting = get_meeting(db, meeting_id)

        if meeting is None:
            raise ValueError(f"Meeting {meeting_id} not found.")

        print("\n========== PREPROCESSING AUDIO ==========")

        t = time.perf_counter()

        processed = preprocess_audio(meeting.audio_file)
        processed_audio = processed["processed_audio"]

        log_time("Audio Preprocessing", t)

        update_processed_audio(db, meeting_id, processed_audio)
        update_status(db, meeting_id, "transcribing")
        update_progress(db, meeting_id, 20)
        print("\n========== TRANSCRIBING AUDIO ==========")

        t = time.perf_counter()

        transcript_result = transcribe_audio(processed_audio)

        log_time("Whisper Transcription", t)

        transcript = transcript_result["text"]
        segments = transcript_result["segments"]

        update_transcript(db, meeting_id, transcript)
        update_status(db, meeting_id, "chunking")
        update_progress(db,meeting_id,35)

        print("Transcript length:", len(transcript))
        print("First 100 chars:", transcript[:100])
        print(f"Transcript Length: {len(transcript)}")

        print("\n========== BUILDING CHUNKS ==========")

        t = time.perf_counter()
        chunks = build_chunks(segments)
        log_time("Chunk Building", t)

        update_status(db, meeting_id,"analyzing")
        update_progress(db, meeting_id,40)

        print(f"Total Chunks: {len(chunks)}")

        results = []

        print("\n========== PROCESSING CHUNKS ==========")

        # import time
        embedding_start = time.perf_counter()   
        for i, chunk in enumerate(chunks):
            t0 = time.time()
            embedding = create_embedding(chunk)
            t1 = time.time()
            store_chunk(meeting_id=meeting_id, chunk_id=i, text=chunk, embedding=embedding)
            t2 = time.time()
            analysis = analyze_chunk(chunk)

            
            print(f"\n===== ANALYSIS FOR CHUNK {i+1} =====")
            print(json.dumps(analysis, indent=2))
            print("===================================")
            t3 = time.time()
            print(f"Chunk {i+1}: embed={t1-t0:.1f}s store={t2-t1:.1f}s analyze={t3-t2:.1f}s")
            results.append(analysis)

        log_time("Embedding + LLM", embedding_start)
        print("\n========== MERGING RESULTS ==========")
        print("Total results:", len(results))
        for i, r in enumerate(results):
            print(f"Result {i}:")
            print(r)
        update_status(db,meeting_id,"merging")
        update_progress(db,meeting_id,85)
        
        t = time.perf_counter()
        final_analysis = merge_analysis(results)
        print("\n========== FINAL ANALYSIS ==========")
    
        print(json.dumps(final_analysis, indent=2))
        print("===================================")
        log_time("Merge Analysis", t)

        t = time.perf_counter()
        update_summary(db, meeting_id, final_analysis)
        log_time("Database Update", t)

        update_status(db,meeting_id,"generating_report")
        update_progress(db,meeting_id,95)

        update_status(db, meeting_id, "completed")
        update_progress(db,meeting_id,"100")
        print(f"\nMeeting {meeting_id} processed successfully.")
        
        

        t = time.perf_counter()

        speaker_transcript = builder_speaker_transcript(
            transcript_result["segments"]
        )

        update_speaker_transcript(
            db,
            meeting_id,
            speaker_transcript,
        )

        log_time("Speaker Transcript", t)
    except Exception:

        db.rollback()
        update_status(db, meeting_id, "failed")

        print("\n========== PIPELINE ERROR ==========")

        traceback.print_exc()

    finally:
        print("=" * 60)
        print(f"TOTAL PIPELINE TIME : "f"{time.perf_counter() - pipeline_start:.2f} sec")
        print("=" * 60)
        db.close()
