from backend.embeddings import create_embedding
from backend.vector_store import search_similar
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_question(question):

    query_embedding = create_embedding(question)

    relevant_chunks = search_similar(query_embedding)

    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are a legal AI assistant.

Answer ONLY from the provided contract.

Contract:

{context}

Question:

{question}

If the answer is not present,
say

Information not found in contract.
"""

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]

    )

    return response.choices[0].message.content