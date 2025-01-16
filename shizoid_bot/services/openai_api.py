import os
import logging
from asyncio import to_thread
from dotenv import load_dotenv
from openai import OpenAI

from config import (API_CONFIG, SELECTED_TEXT_TO_TEXT_API, 
                    SELECTED_IMAGE_TO_TEXT_API)
from exceptions.exceptions import (APIRequestError, APIResponseError, 
                                   APIKeyError)


load_dotenv()
logger = logging.getLogger(__name__)

async def create_response(messages: list[dict], 
                          model_type: str = "text_to_text") -> str:
    try:
        if model_type == "text_to_text":
            config = API_CONFIG[SELECTED_TEXT_TO_TEXT_API]
        elif model_type == "image_to_text":
            config = API_CONFIG[SELECTED_IMAGE_TO_TEXT_API]

        api_key = os.getenv(config["api_key_env"])
        if not api_key:
            raise APIKeyError(f"API key for {config['default_model']} is missing")

        client = OpenAI(
            base_url=config["base_url"],
            api_key=api_key,
        )
        response = await to_thread(
            client.chat.completions.create,
            model=config["default_model"],
            messages=messages,
            max_tokens=config["max_tokens"],
            temperature=config["temperature"],
        )

        if not response.choices:
            raise APIResponseError(f"No valid response from {config['default_model']} API")

        return response.choices[0].message.content

    except APIKeyError as e:
        logger.error(f"API Key Error: {e}")
        raise
    except APIResponseError as e:
        logger.error(f"API Response Error: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unhandled error during API call: {e}")
        raise APIRequestError(f"Unhandled error: {e}")