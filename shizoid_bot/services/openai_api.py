import os
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

from texts.system_message import SYSTEM_MESSAGE


load_dotenv()


def create_response(user_message: str, 
                    assistant_message: str = None):
    
    api_key = os.getenv("OPENAI_KEY")
    
    client = OpenAI(api_key=api_key)
    
    messages=[
        {"role": "developer", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": user_message},
    ]
    
    if assistant_message and len(assistant_message > 5):
        messages.append({"role": "assistant", "content": assistant_message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content

    except OpenAIError as e:
        return f"Произошла ошибка: {e}"
