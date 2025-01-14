import os
import logging
from asyncio import to_thread
from dotenv import load_dotenv
from openai import OpenAI

from config import (API_CONFIG, SELECTED_TEXT_TO_TEXT_API, 
                    SELECTED_IMAGE_TO_TEXT_API)


load_dotenv()
logger = logging.getLogger(__name__)

async def create_response(messages: list[dict], 
                          model_type: str = "text_to_text") -> str:
    
    if model_type == "text_to_text":
        config = API_CONFIG[SELECTED_TEXT_TO_TEXT_API]
    elif model_type == "image_to_text":
        config = API_CONFIG[SELECTED_IMAGE_TO_TEXT_API]

    api_key = os.getenv(config["api_key_env"])
    
    if not api_key:
        raise ValueError(f"Api key of {config["default_model"]} is unavailable\
            in environment variables")
    
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
        raise Exception(f"Error in create response to \
            {config["default_model"]}: {e}")
     
    logger.info(response)
    
    if not response.choices:
        raise ValueError(f"{config["default_model"]} API did not give \
            the expected response")
    
    return response.choices[0].message.content