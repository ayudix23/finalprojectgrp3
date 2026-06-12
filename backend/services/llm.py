import os
import time

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def call_llm(prompt: str):

    try:

        start_time = time.time()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful e-commerce support assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        latency = round(
            time.time() - start_time,
            2
        )

        print(f"[LLM LATENCY] {latency}s")

        return response.choices[0].message.content

    except Exception as e:

        print(f"[LLM ERROR] {e}")

        return "Unable to generate response."