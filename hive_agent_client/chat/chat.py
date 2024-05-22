import httpx
import logging
import os
import sys

def get_log_level():
        HIVE_AGENT_LOG_LEVEL = os.getenv('HIVE_AGENT_LOG_LEVEL', 'INFO').upper()
        return getattr(logging, HIVE_AGENT_LOG_LEVEL, logging.INFO)

logging.basicConfig(stream=sys.stdout, level=get_log_level())
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

logger = logging.getLogger()
logger.setLevel(get_log_level())



async def send_chat_message(http_client: httpx.AsyncClient, base_url: str, content: str) -> str:
    """
    Sends a chat message to the Hive Agent API and returns the response.

    :param http_client: An instance of httpx.AsyncClient to make HTTP requests.
    :param base_url: The base URL of the Hive Agent API.
    :param content: The content of the message to be sent.
    :return: The response text from the API.
    :raises ValueError: If the content is empty.
    :raises httpx.HTTPStatusError: If the request fails due to a network error or returns a 4xx/5xx response.
    :raises Exception: For other types of errors.
    """
    if not content.strip():
        raise ValueError("Content must not be empty")

    endpoint = "/api/chat"
    url = f"{base_url}{endpoint}"
    payload = {
        "messages": [{
            "role": "user",
            "content": content
        }]
    }

    try:
        logging.debug(f"Sending chat message to {url}: {content}")
        response = await http_client.post(url, json=payload)
        response.raise_for_status()
        logger.debug(f"Response from chat message {content}: {response.text}")
        return response.text
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred when sending message to {url}: {e.response.status_code} - {e.response.text}")
        raise Exception(f"HTTP error occurred when sending message to the chat API: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        logging.error(f"Request error occurred when sending message to {url}: {e}")
        raise Exception(f"Request error occurred when sending message to the chat API: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred when sending message to {url}: {e}")
        raise Exception(f"An unexpected error occurred when sending message to the chat API: {e}")
