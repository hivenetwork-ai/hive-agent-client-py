import httpx
import logging

from typing import Dict

from hive_agent_client.chat import send_chat_message
from hive_agent_client.database import (
    create_table,
    insert_data,
    read_data,
    update_data,
    delete_data
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

    async def create_table(self, table_name: str, columns: dict) -> Dict:
        """
        Create a new table in the database.

        :param table_name: The name of the table to create.
        :param columns: The columns of the table to create.
        :return: A dictionary with a message about the table creation.
        """
        try:
            return await create_table(self.http_client, self.base_url, table_name, columns)
        except Exception as e:
            logger.error(f"Failed to create table {table_name} with columns {columns}: {e}")
            raise Exception(f"Failed to create table: {e}")

    async def insert_data(self, table_name: str, data: dict) -> Dict:
        """
        Insert data into a table.

        :param table_name: The name of the table to insert data into.
        :param data: The data to insert.
        :return: A dictionary with a message and the id of the inserted data.
        """
        try:
            return await insert_data(self.http_client, self.base_url, table_name, data)
        except Exception as e:
            logger.error(f"Failed to insert data {data} into table {table_name}: {e}")
            raise Exception(f"Failed to insert data: {e}")

    async def read_data(self, table_name: str, filters: dict = None) -> Dict:
        """
        Retrieve data from a table.

        :param table_name: The name of the table to read data from.
        :param filters: Optional filters to apply when reading data.
        :return: A list of dictionaries representing the read data.
        """
        try:
            return await read_data(self.http_client, self.base_url, table_name, filters)
        except Exception as e:
            logger.error(f"Failed to read data from table {table_name} with filters {filters}: {e}")
            raise Exception(f"Failed to read data: {e}")

    async def update_data(self, table_name: str, row_id: int, new_data: dict) -> Dict:
        """
        Update data in a table.

        :param table_name: The name of the table to update data in.
        :param row_id: The ID of the row to update.
        :param new_data: The new data to update in the table.
        :return: A dictionary with a message about the update.
        """
        try:
            return await update_data(self.http_client, self.base_url, table_name, row_id, new_data)
        except Exception as e:
            logger.error(f"Failed to update data in table {table_name} with id {row_id} and data {new_data}: {e}")
            raise Exception(f"Failed to update data: {e}")

    async def delete_data(self, table_name: str, row_id: int) -> Dict:
        """
        Delete data from a table.

        :param table_name: The name of the table to delete data from.
        :param row_id: The ID of the row to delete.
        :return: A dictionary with a message about the deletion.
        """
        try:
            return await delete_data(self.http_client, self.base_url, table_name, row_id)
        except Exception as e:
            logger.error(f"Failed to delete data from table {table_name} with id {row_id}: {e}")
            raise Exception(f"Failed to delete data: {e}")

    async def close(self):
        """
        Close the HTTP client session.
        """
        logger.debug("Closing HTTP client session...")
        await self.http_client.aclose()
