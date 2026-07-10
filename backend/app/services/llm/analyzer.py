import json
import re
from app.core.settings import settings

from app.services.llm.client import OllamaClient

from app.services.llm.prompts import meeting_analysis_prompt, final_merge_prompt

client = OllamaClient()



def clean_json_response(response: str):
    response = response.strip()

    # Remove markdown
    response = re.sub(r"```json", "", response)
    response = re.sub(r"```", "", response)

    # Extract only JSON object
    match = re.search(r"\{.*\}", response, re.DOTALL)

    if not match:
        raise ValueError("No JSON found.")

    return json.loads(match.group())

def analyze_chunk(chunk: str):
    
    # Analyze a single transcript chunk.
    
    prompt = meeting_analysis_prompt(chunk)

    response = client.generate(prompt, model=settings.CHUNK_MODEL)

    print("\n CHUNK RESPONSE ")
    print(response)
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
    except Exception:
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