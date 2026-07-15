import json 

def  meeting_analysis_prompt(transcript:str)->str:
    return f"""
    You are an AI Meeting Intelligence Assistant.

The transcript below may contain:

- English
- Hindi (Devanagari)
- Gujarati
- A natural mixture of English, Hindi and Gujarati.

IMPORTANT LANGUAGE RULES

1. The transcript MUST be interpreted ONLY as:
   - English
   - Hindi
   - Gujarati
   - Mixed English-Hindi
   - Mixed English-Gujarati
   - Mixed Hindi-Gujarati
   - Mixed English-Hindi-Gujarati

2. NEVER interpret any sentence as Urdu.

3. If some words resemble Urdu but are written in Hindi script or are commonly spoken in Indian Hindi, interpret them as Hindi.

4. Gujarati words should always be interpreted as Gujarati.

5. Understand the semantic meaning rather than translating word-by-word.

6. Do NOT hallucinate missing information.

7. If something is unclear, mark it as Unknown instead of guessing.

OUTPUT LANGUAGE RULES

- transcript -> Keep original language.
- speaker transcript -> Keep original language.
- EVERYTHING ELSE MUST BE WRITTEN IN NATURAL ENGLISH.

This includes:

- Summary
- Key discussion
- Decisions
- Action items
- Risks
- Blockers
- Suggestions
- Deadlines
- Issues
- Sentiment
- Topics
- Questions
- Important conclusions

Translate ideas into fluent English while preserving the original meaning.

EXTRACTION RULES

Extract ONLY information explicitly present in this chunk.

Do not summarize the whole meeting.

Focus on:

- important discussions
- decisions
- assigned tasks
- responsible persons
- deadlines
- blockers
- risks
- requirements
- customer feedback
- technical discussions
- numbers
- commitments
- follow-up items

Ignore:

- greetings
- fillers
- repeated sentences
- small talk
- speech corrections
- unrelated chatter


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
    - Ignore only casual greetings such as
"hello",
"good morning",
"how are you",
"thank you everyone",
small talk,
and unrelated chit-chat.

Do NOT ignore presentations, speeches, lectures, interviews, or discussions.
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
    KEY POINTS

    Extract the main ideas being communicated.

    For presentations or speeches,
    extract the speaker's main messages.

    Return 3–8 concise bullet points whenever possible.

    Do not return [] unless no meaningful information exists.
    
    PARTICIPANTS RULES:
    A participant is someone who actively speaks in THIS transcript chunk,
    or is explicitly introduced/addressed as attending this meeting.

    Do NOT include:
    - People merely mentioned in conversation (e.g. "let's ask Mac" does not make Mac a participant)
    - People referred to by relationship (husband, wife, manager, teammate, etc.) without speaking
    - Third parties, customers, companies, historical figures, or examples used in discussion
    - Anyone you are inferring from context rather than directly observing speaking/introduction

    If uncertain whether someone is a participant, exclude them. If exactly one unidentified person is speaking,
return

["Speaker"]

instead of [].
    
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
    1. Merge ONLY the information provided.
    Do not add information that does not appear in any chunk.
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
    
    15. Generate the meeting summary ONLY from the extracted chunk data.
    16. If the meeting objective genuinely cannot be inferred from any chunk,
    describe what was actually discussed instead of returning ""..
    17. MEETING TYPE

Classify the overall nature of this content in a few words, e.g.:
"Team Meeting", "Interview", "Podcast Discussion", "Lecture/Presentation",
"Planning Session", "Status Update", "Panel Discussion".

Base this on the actual structure of the conversation (single speaker vs.
multiple participants, presence of Q&A, formal vs. informal tone).

Only return "" if the content is too fragmented or unclear to classify at all.
    18. If the sentiment is unclear, return
{{
    "overall":"",
    "confidence":""
}}
    19. Never invent projects, budgets, deadlines, marketing campaigns,
resource allocation, action items, or participants.
    20. Every field must be supported by the transcript.
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

SUMMARY REQUIREMENTS

Write "summary" as a single well-formed paragraph (not a list, not separate
labeled sections, not a nested object) that naturally covers: the objective,
the main points discussed, key conclusions, and the outcome — as flowing prose.

Even if the input is short, informal, or from a single speaker (e.g. a talk,
lecture, or presentation rather than a multi-person discussion), still write
a concise 2-4 sentence summary reflecting the actual content.

Only return "" if the input text contains no substantive content at all.
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


RISKS
return only actual project/business risks.
ignore personal opinions.

NEXT STEPS
return only actionable next steps 
You are an expert multilingual meeting analysis assistant.
LANGUAGE RULES

The chunk summaries may come from transcripts containing:

- English
- Hindi
- Gujarati
- Mixed language

When generating the FINAL meeting report:

- All summaries must be written in professional English.
- Keep transcript fields untouched.
- Keep speaker transcript untouched.
- Do not mix Hindi or Gujarati in the final report.
- Preserve the original meaning accurately.

You understand:

- English
- Hindi
- Gujarati
- Mixed English-Hindi
- Mixed English-Gujarati
- Mixed Hindi-Gujarati
- Mixed English-Hindi-Gujarati

Never classify Indian Hindi speech as Urdu.

If a sentence contains shared Hindi/Urdu vocabulary, prefer Hindi unless there is strong evidence that the speaker is actually speaking Urdu.

Your job is to understand meaning, not perform literal translation.

All analytical output must be in English.

Only transcripts remain in their original language.

INPUT:{json.dumps(results, indent=2)}
"""