import openai
from dotenv import load_dotenv
import os

API_KEY_GPT = os.getenv("OPENAI_API_KEY")

def call_gpt(prompt, max_tokens=150):
    openai.api_key = API_KEY_GPT
    response = openai.Completion.create(
        model = "gpt-3.5-turbo",
        messages=[{"role": "user", "content": wText}],
        request_timeout = 60, 
        temperature = 0.5,
    )
    return response.choices[0].text.strip()
