import os
import logging
from asyncio import to_thread
from openai import OpenAI
from dotenv import load_dotenv

from config import API_CONFIG, SELECTED_API


load_dotenv()
logger = logging.getLogger(__name__)

async def create_response(messages: list[dict]) -> str:
    config = API_CONFIG[SELECTED_API]
    api_key = os.getenv(config["api_key_env"])
    
    if not api_key:
        raise ValueError(f"{config['api_key_env']} is unavailable in environment variables")
    
    client = OpenAI(
        base_url=config["base_url"],
        api_key=api_key,
    )
    
    try:
        response = await to_thread(
            client.chat.completions.create,
            model=config["default_model"],
            messages=messages,
            max_tokens=config["max_tokens"],
            temperature=config["temperature"],
        )
    except Exception as e:
        logger.error(f"Error in create_response: {e}")
        raise
    
    logger.info(response)
    
    if not response.choices:
        logger.error("API response does not contain 'choices'")
        raise ValueError("Unexpected API response: no 'choices' found")
    
    return response.choices[0].message.content
