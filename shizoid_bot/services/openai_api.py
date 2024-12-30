import os
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv


load_dotenv()

def create_response(messages: list[dict]) -> str:
    api_key = os.getenv("OPENAI_KEY")
    if not api_key:
        raise ValueError("OPENAI_KEY не установлено в переменных окружения.")
    
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].message.content
