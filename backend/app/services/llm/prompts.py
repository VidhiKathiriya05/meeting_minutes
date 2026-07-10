import json 

def  meeting_analysis_prompt(transcript:str)->str:
    return f"""
    you are an AI assistant strcutured facts from ONE CHUNK of meeting transcript.
    INPORTANT:
    - This transcript os ONLY ONE PART of the meeting.
    - do not summarize the entire meeting.
    - Extract ONLY information explicitly mentioned in this chunk.
    - DO NOT guess or hallucinate. 
    - If something is not present, return []
    -Never return placeholder values such as:
    {{
        "task":"",
        "owner":"",
        "deadline":""
    }}
    - Ignore greetings, introductions filler conversation and jokes.

    return only valid JSON.
    
    JSON Schema:
    {{
        "participants":[""],
        "key_points":[""],
        "action_items":[
            {{
                "task": "Task description",
                "owner": "Person responsible",
                "deadline": "Deadline if mentioned"
            }}
        ],
        "decisions":[""],
        "questions": [""],
        "risks": [ ""],
        "next_steps": [ ""]

    }}
    
    RULES: 
    1. return ONLY JSON.
    2. never use markdown
    3. never explain anything 
    4. never invent information.
    5. remove empty objects.
    6. if there are no action items, return [].
    7. if there are no dicisions, return [].
    8. if there are no risks, return [].
    9. if there are no questions, return [].
    10. do not classify the meeting type.
    11. do not generate a meeting summary.
    12. do not generate a sentiment.
    
    Transcript:

    \"\"\"{transcript}\"\"\"
    """


def final_merge_prompt(results:list)-> str:
    return f"""
    You are a JSON generator.

    Your ONLY job is to produce valid JSON.

    Never explain.
    Never apologize.
    Never use markdown.
    Never write ```json.
    Never write text before the JSON.
    Never write text after the JSON.
    below are structured JSON outputs extracted from different chunks of the SAME meeting.
    your job is to merge them into ONE final meeting report.
    IMPORTANT RULES:
    1. the meeting is continuous.
    2. Merge duplicated information.
    3. Remove repeated key points. 
    4. remove repeated action items.
    5. remove repeated decisions.
    6. remove repeated decisions. 
    7. remove repeated risks. 
    8. remove repeated next steps.
    9. merge participants into one unique list.
    10. remove empty action items. 
    11. ignore meaningless questions.
    12. ignore filler conversations. 
    13. remove placeholders like: 
        - ""
        - None
        - "unknown"
        - "not mentioned"
    14. infer missing information whenever it is clearly implied.
    15. generate ONE overall meeting summary 
    16. determine ONE meeting type for the entire meeting  
    17. determine ONE overall sentiments.

    return ONLY valid JSON.

    Schema:

{{
    "summary":"",

    "meeting_type":"",

    "participants":[
        ""
    ],

    "key_points":[
        ""
    ],

    "action_items":[
        {{
            "task":"",
            "owner":"",
            "deadline":""
        }}
    ],

    "decisions":[
        ""
    ],

    "questions":[
        ""
    ],

    "risks":[
        ""
    ],

    "next_steps":[
        ""
    ],

    "sentiment":{{
        "overall":"",
        "confidence":""
    }}
}}

SUMMARY REQUIREMENTS

The summary should NOT be a concatenation.

Instead create:

• Meeting objective

• Main discussion

• Important conclusions

• Final outcome

KEY POINTS

Return only the most important points.
Maximum 10.

ACTION ITEMS

only include real action items. 
remove entries where task ==""  owner==""  deadline ==""

QUESTIONS 
only keep unresolved questions. 
do not include casual interview questions. 

PARTICIPANTS
return only unique participants.
if one person appears multiple times with slightly different names, merge them into one.
example "aditi" "aditi goel" "aditi G"-> "aditi Goel"
Include only people who explicitly identify themselves or are explicitly introduced as attendees.
Do not include names merely mentioned during discussion.
Do not infer participants from context.
Do not guess names from unclear transcription.
If confidence is low, return [].

Extract only people who are actively participating in the conversation.
Do NOT include:
- People mentioned as examples.
- Family members.
- Celebrities discussed.
- Historical figures.
- Companies.
- Customers.
- Third parties.
- People referred to as "he", "she", "her husband", "his manager", etc.
A participant must satisfy at least one of these:
- Speaks in the transcript.
- Is explicitly introduced as attending the meeting.
- Is directly addressed as part of the meeting.
If uncertain, exclude the name.
Return [] rather than guessing.
PARTICIPANTS RULES

A participant is someone who actively speaks in this transcript.

Do NOT include:
- Family members
- Friends
- Celebrities being discussed
- People mentioned in stories
- People referred to by relationship (husband, wife, mother, father, etc.)

If a person is only talked about and never speaks, they are NOT a participant.

Never replace descriptions with real names.
Example:
Transcript: "my husband"
❌ Ritesh
❌ Husband
✅ Return nothing

RISKS
return only actual project/business risks.
ignore personal opinions.

NEXT STEPS
return only actionable next steps 

INPUT:{json.dumps(results, indent=2)}
"""