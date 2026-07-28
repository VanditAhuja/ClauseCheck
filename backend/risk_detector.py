import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

RISK_PROMPT = """You are an expert legal assistant that flags risky or unusual \
clauses in legal and financial documents (leases, insurance policies, contracts).

Read the document text below and identify clauses that could be risky, \
one-sided, unusual, or costly for the person signing. For each one, return:
- "clause": a short quote or paraphrase (under 20 words) identifying the clause
- "severity": "high", "medium", or "low"
- "reason": a one-sentence plain-English explanation of why it's risky

Return ONLY a JSON array, nothing else. No markdown fences, no preamble, no \
extra text before or after. If there are no risky clauses, return an empty \
array [].

Document:
{text}
"""

def detect_risk(text):
    text = text[:8000]  # keep requests within Groq's free-tier token limit
    prompt = RISK_PROMPT.format(text=text)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    raw_text = response.choices[0].message.content.strip()

    # Strip accidental markdown fences just in case
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.startswith("json"):
            raw_text = raw_text[4:].strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return []