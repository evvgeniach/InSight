import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def ask_question(schema, sample, data_json, question, history):
    system = f"""You are InSight, an expert data analyst assistant.
The user has loaded a dataset. Answer their questions using the data provided.

SCHEMA:
{schema}

SAMPLE (first 5 rows):
{sample}

FULL DATA:
{data_json}

Respond ONLY with a JSON object in this exact format:
{{
  "insight": "2-3 sentence answer with specific numbers from the data",
  "stats": [
    {{"label": "metric name", "value": "computed value", "sub": "optional context"}}
  ],
  "chart": {{
    "type": "bar or line or doughnut or null",
    "labels": ["label1", "label2"],
    "values": [10, 20],
    "title": "chart title"
  }},
  "followups": ["question 1", "question 2", "question 3"]
}}

Rules:
- stats: 2-4 key metrics. Empty array if not applicable.
- chart: only include when a chart genuinely adds value. Set type to null if not.
- followups: 3 smart follow-up questions based on what you found.
- Return ONLY the JSON. No markdown, no explanation outside the JSON.
"""

    history.append({"role": "user", "content": question})

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        system=system,
        messages=history
    )

    raw = response.content[0].text
    history.append({"role": "assistant", "content": raw})

    try:
        clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(clean), history
    except json.JSONDecodeError:
        return {"insight": raw, "stats": [], "chart": {"type": None}, "followups": []}, history