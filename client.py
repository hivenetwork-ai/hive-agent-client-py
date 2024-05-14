import httpx
import logging

from typing import AsyncGenerator, Dict

from hive_agent_client.chat import send_chat_message
from hive_agent_client.entry import (
    create_entry,
    stream_entry,
    get_entries,
    get_entry_by_id,
    update_entry,
    delete_entry
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HiveAgentClient:
    """
    Client for interacting with a Hive Agent's API.
    """

    def __init__(self, base_url: str):
        """
        Initializes the HiveAgentClient with the given base URL.

        :param base_url: The base URL of the Hive Agent API.
        """
        self.base_url = base_url
        self.http_client = httpx.AsyncClient()

    async def chat(self, content: str) -> str:
        """
        Send a message to the chat endpoint.

        :param content: The content of the message to send.
        :return: The response from the chat API as a string.
        """
        try:
            logger.debug(f"Sending message to chat endpoint: {content}")
            return await send_chat_message(self.http_client, self.base_url, content)
        except Exception as e:
            logger.error(f"Failed to send chat message - {content}: {e}")
            raise Exception(f"Failed to send chat message: {e}")

    async def create_entry(self, namespace: str, data: dict) -> Dict:
        """
        Create a new entry in the specified namespace.

        :param namespace: The namespace in which to create the entry.
        :param data: The data to be stored in the entry.
        :return: A dictionary representing the created entry.
        """
        try:
            return await create_entry(self.http_client, self.base_url, namespace, data)
        except Exception as e:
            logger.error(f"Failed to create entry {data} in {namespace}: {e}")
            raise Exception(f"Failed to create entry: {e}")

    async def stream_entry_data(self, namespace: str, data_stream: AsyncGenerator) -> AsyncGenerator:
        """
        Stream data to the entry endpoint.

        :param namespace: The namespace in which to stream the data.
        :param data_stream: The async generator providing the data to stream.
        :yield: Messages received in response to the streamed data.
        """
        try:
            async for message in stream_entry(self.http_client, self.base_url, namespace, data_stream):
                yield message
        except Exception as e:
            logger.error(f"Failed to stream entry data from {namespace}: {e}")
            raise Exception(f"Failed to stream entry data: {e}")

    async def get_entries(self, namespace: str) -> Dict:
        """
        Retrieve all entries from the specified namespace.

        :param namespace: The namespace from which to retrieve entries.
        :return: A dictionary containing the retrieved entries.
        """
        try:
            return await get_entries(self.http_client, self.base_url, namespace)
        except Exception as e:
            logger.error(f"Failed to get entries in {namespace}: {e}")
            raise Exception(f"Failed to get entries: {e}")

    async def get_entry_by_id(self, namespace: str, entry_id: str) -> Dict:
        """
        Retrieve a specific entry by its ID.

        :param namespace: The namespace of the entry.
        :param entry_id: The ID of the entry to retrieve.
        :return: A dictionary representing the retrieved entry.
        """
        try:
            return await get_entry_by_id(self.http_client, self.base_url, namespace, entry_id)
        except Exception as e:
            logger.error(f"Failed to get entry {entry_id} from {namespace}: {e}")
            raise Exception(f"Failed to get entry by ID: {e}")

    async def update_entry(self, namespace: str, entry_id: str, data: dict) -> Dict:
        """
        Update a specific entry by its ID.

        :param namespace: The namespace of the entry.
        :param entry_id: The ID of the entry to update.
        :param data: The data to update the entry with.
        :return: A dictionary representing the updated entry.
        """
        try:
            return await update_entry(self.http_client, self.base_url, namespace, entry_id, data)
        except Exception as e:
            logger.error(f"Failed to update entry {entry_id} from {namespace} with {data}: {e}")
            raise Exception(f"Failed to update entry: {e}")

    async def delete_entry(self, namespace: str, entry_id: str) -> Dict:
        """
        Delete a specific entry by its ID.

        :param namespace: The namespace of the entry.
        :param entry_id: The ID of the entry to delete.
        :return: A dictionary containing the status of the deletion.
        """
        try:
            return await delete_entry(self.http_client, self.base_url, namespace, entry_id)
        except Exception as e:
            logger.error(f"Failed to delete entry {entry_id} from {namespace}: {e}")
            raise Exception(f"Failed to delete entry: {e}")

    async def close(self):
        """
        Close the HTTP client session.
        """
        logger.debug("Closing HTTP client session...")
        await self.http_client.aclose()
      