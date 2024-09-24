import httpx
import io
import json
import logging
import mimetypes
import os
import sys

from typing import List, Dict, Union
from fastapi import UploadFile

def get_log_level():
    HIVE_AGENT_LOG_LEVEL = os.getenv("HIVE_AGENT_LOG_LEVEL", "INFO").upper()
    return getattr(logging, HIVE_AGENT_LOG_LEVEL, logging.INFO)


logging.basicConfig(stream=sys.stdout, level=get_log_level())
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

logger = logging.getLogger()
logger.setLevel(get_log_level())


async def send_chat_message(
        http_client: httpx.AsyncClient,
        base_url: str,
        user_id: str,
        session_id: str,
        content: str,
        files: List[Union[UploadFile, str]] = None  # Can be either UploadFile or file path
) -> str:
    """
    Sends a chat message to the Hive Agent API and returns the response.

    :param http_client: An instance of httpx.AsyncClient to make HTTP requests.
    :param base_url: The base URL of the Hive Agent API.
    :param user_id: The user ID.
    :param session_id: The session ID.
    :param content: The content of the message to be sent.
    :param files: List of UploadFile objects or file paths to be uploaded.
    :return: The response text from the API.
    :raises ValueError: If the content is empty.
    :raises httpx.HTTPStatusError: If the request fails due to a network error or returns a 4xx/5xx response.
    :raises Exception: For other types of errors.
    """
    if not content.strip():
        raise ValueError("Content must not be empty")

    endpoint = "/chat"
    url = f"{base_url}{endpoint}"

    chat_data = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    })

    form_data = {
        "user_id": user_id,
        "session_id": session_id,
        "chat_data": chat_data,  # Send as a JSON string
    }

    files_to_send = []

    if files:
        for file in files:
            if isinstance(file, UploadFile):
                # Handle UploadFile (received from an HTTP request)
                files_to_send.append(
                    ("files", (file.filename, file.file, file.content_type))
                )
            elif isinstance(file, str):
                # Handle file paths
                file_name = os.path.basename(file)
                content_type, _ = mimetypes.guess_type(file)
                files_to_send.append(
                    ("files", (file_name, open(file, "rb"), content_type))
                )

    try:
        logging.debug(f"Sending chat message to {url}")
        response = await http_client.post(
            url,
            data=form_data,
            files=files_to_send  # Attach files if any
        )
        response.raise_for_status()
        logger.debug(f"Response from chat message {content}: {response.text}")
        return response.text
    except httpx.HTTPStatusError as e:
        logging.error(
            f"HTTP error occurred when sending message to {url}: {e.response.status_code} - {e.response.text}"
        )
        raise Exception(
            f"HTTP error occurred when sending message to the chat API: {e.response.status_code} - {e.response.text}"
        )
    except httpx.RequestError as e:
        logging.error(f"Request error occurred when sending message to {url}: {e}")
        raise Exception(
            f"Request error occurred when sending message to the chat API: {e}"
        )
    except Exception as e:
        logging.error(
            f"An unexpected error occurred when sending message to {url}: {e}"
        )
        raise Exception(
            f"An unexpected error occurred when sending message to the chat API: {e}"
        )
    finally:
        # Close any files opened from file paths
        for file in files_to_send:
            if isinstance(file[1][1], io.IOBase):  # Check if it's a file object
                file[1][1].close()


async def get_chat_history(
    http_client: httpx.AsyncClient, base_url: str, user_id: str, session_id: str
) -> List[Dict]:
    """
    Retrieves the chat history from the Hive Agent API.

    :param http_client: An instance of httpx.AsyncClient to make HTTP requests.
    :param base_url: The base URL of the Hive Agent API.
    :param user_id: The user ID.
    :param session_id: The session ID.
    :return: The chat history as a list of dictionaries.
    :raises httpx.HTTPStatusError: If the request fails due to a network error or returns a 4xx/5xx response.
    :raises Exception: For other types of errors.
    """
    endpoint = "/chat_history"
    url = f"{base_url}{endpoint}"
    params = {"user_id": user_id, "session_id": session_id}

    try:
        logging.debug(f"Fetching chat history from {url} with params: {params}")
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        chat_history = response.json()
        logger.debug(
            f"Chat history for user {user_id} and session {session_id}: {chat_history}"
        )
        return chat_history
    except httpx.HTTPStatusError as e:
        logging.error(
            f"HTTP error occurred when fetching chat history from {url}: {e.response.status_code} - {e.response.text}"
        )
        raise Exception(
            f"HTTP error occurred when fetching chat history from the chat API: {e.response.status_code} - {e.response.text}"
        )
    except httpx.RequestError as e:
        logging.error(
            f"Request error occurred when fetching chat history from {url}: {e}"
        )
        raise Exception(
            f"Request error occurred when fetching chat history from the chat API: {e}"
        )
    except Exception as e:
        logging.error(
            f"An unexpected error occurred when fetching chat history from {url}: {e}"
        )
        raise Exception(
            f"An unexpected error occurred when fetching chat history from the chat API: {e}"
        )


async def get_all_chats(
    http_client: httpx.AsyncClient, base_url: str, user_id: str
) -> Dict[str, List[Dict]]:
    """
    Retrieves all chat sessions for a specified user from the Hive Agent API.

    :param http_client: An instance of httpx.AsyncClient to make HTTP requests.
    :param base_url: The base URL of the Hive Agent API.
    :param user_id: The user ID.
    :return: All chat sessions as a dictionary with session IDs as keys and lists of messages as values.
    :raises httpx.HTTPStatusError: If the request fails due to a network error or returns a 4xx/5xx response.
    :raises Exception: For other types of errors.
    """

    endpoint = "/all_chats"
    url = f"{base_url}{endpoint}"
    params = {"user_id": user_id}

    try:
        logging.debug(f"Fetching all chats from {url} with params: {params}")
        response = await http_client.get(url, params=params)
        response.raise_for_status()

        all_chats = response.json()
        logger.debug(f"All chats for user {user_id}: {all_chats}")

        return all_chats
    except httpx.HTTPStatusError as e:
        logging.error(
            f"HTTP error occurred when fetching all chats from {url}: {e.response.status_code} - {e.response.text}"
        )
        raise Exception(
            f"HTTP error occurred when fetching all chats from the chat API: {e.response.status_code} - {e.response.text}"
        )
    except httpx.RequestError as e:
        logging.error(f"Request error occurred when fetching all chats from {url}: {e}")
        raise Exception(
            f"Request error occurred when fetching all chats from the chat API: {e}"
        )
    except Exception as e:
        logging.error(
            f"An unexpected error occurred when fetching all chats from {url}: {e}"
        )
        raise Exception(
            f"An unexpected error occurred when fetching all chats from the chat API: {e}"
        )
