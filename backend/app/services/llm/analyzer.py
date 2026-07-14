import json
import re
from app.core.settings import settings

from app.services.llm.client import OllamaClient

from app.services.llm.prompts import meeting_analysis_prompt, final_merge_prompt

client = OllamaClient()

def clean_json_response(response: str):
    response = response.strip()
    response = response.replace("```json", "")
    response = response.replace("```", "")

    print("\n===== CLEAN RESPONSE =====")
    print(repr(response))

    start = response.find("{")
    end = response.rfind("}")

    print("Start:", start)
    print("End:", end)

    if start == -1:
        raise ValueError("No opening brace found.")

    if end == -1:
        # Repair attempt: model likely got cut off before closing the object.
        print("No closing brace found — attempting repair by appending '}'")
        repaired = response.rstrip().rstrip(",") + "\n}"
        try:
            parsed = json.loads(repaired[start:])
            print("Repair succeeded.")
            return parsed
        except json.JSONDecodeError as e:
            raise ValueError(f"Missing closing brace. Repair attempt also failed: {e}")

    json_text = response[start:end + 1]

    print("\n===== JSON TO PARSE =====")
    print(json_text)
    print("=========================")

    return json.loads(json_text)

def analyze_chunk(chunk: str):
    
    # Analyze a single transcript chunk.
    
    prompt = meeting_analysis_prompt(chunk)

    response = client.generate(prompt, model=settings.CHUNK_MODEL)

    print("\n===== RAW RESPONSE =====")
    print(repr(response))
    print("========================")
    print("====================================\n")

    try:
        result = clean_json_response(response)
        # Normalize sentiment key
        if "sentiments" in result and "sentiment" not in result:
            result["sentiment"] = result.pop("sentiments")

        # Ensure sentiment always exists
        if "sentiment" not in result:
            result["sentiment"] = {
                "overall": "Neutral",
                "confidence": "Medium"
            }
    except Exception as e:
        print("Chunk JSON Error:", e)
        print(response)
        result = {}
    defaults = {
        "participants": [],
        
        "key_points": [],
        "action_items": [],
        "decisions": [],
        "questions": [],
        "risks": [],
        "next_steps": []
    }

    for key, value in defaults.items():
        if key not in result or result[key] is None:
            result[key] = value

    return result


def merge_analysis(results):
    """
    Merge all chunk analyses using the LLM.
    """

    print("\n========== MERGING CHUNKS ==========\n")

    prompt = final_merge_prompt(results)

    response = client.generate(prompt, model= settings.MERGE_MODEL)

    print("\n========== FINAL MERGED RESPONSE ==========")
    print(response)
    print("==========================================\n")

    try:
        final_result = clean_json_response(response)
        # Some models return 'sentiments'
        if "sentiments" in final_result and "sentiment" not in final_result:
            final_result["sentiment"] = final_result.pop("sentiments")
    except Exception as e:
        print("JSON Parsing Error:", e)
        final_result = {}

    defaults = {
        "summary": "",
        "meeting_type": "Unknown",
        "participants": [],
        "key_points": [],
        "action_items": [],
        "decisions": [],
        "questions": [],
        "risks": [],
        "next_steps": [],
        "sentiment": {
            "overall": "Neutral",
            "confidence": "Medium"
        }
    }

    for key, value in defaults.items():
        if key not in final_result or final_result[key] is None:
            final_result[key] = value

    return final_result