from app.services.llm.client import OllamaClient
from app.services.llm.prompts import summary_prompt

client = OllamaClient()


def summarize(transcript: str):

    prompt = summary_prompt(transcript)

    summary = client.generate(prompt)

    return summary