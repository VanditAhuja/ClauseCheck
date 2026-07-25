import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def summarize_document(text):

    prompt = f"""
You are an expert legal assistant.

Summarize the following legal document in simple English.

Give:

1. TLDR
2. Important obligations
3. Important dates
4. Important costs
5. Important conditions

Document:

{text}
"""

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

    return response.choices[0].message.content