import httpx
import logging
from typing import Dict, List

from hive_agent_client.chat import (
    send_chat_message,
    get_chat_history,
    get_all_chats,
    send_chat_media
)
from hive_agent_client.database import (
    create_table,
    insert_data,
    read_data,
    update_data,
    delete_data,
)
from hive_agent_client.files import upload_files, list_files, delete_file, rename_file
from hive_agent_client.tools import install_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HiveAgentClient:
    """
    Client for interacting with a Hive Agent's API.
    """

    def __init__(self, base_url: str, version: str = "v1", timeout: float = 30.0):
        """
        Initializes the HiveAgentClient with the given base URL and version.

        :param base_url: The base URL of the Hive Agent API.
        :param version: The version of the Hive Agent API.
        """
        if base_url.endswith("/"):
            base_url = base_url[:-1]

        self.base_url = f"{base_url}/{version}"
        self.http_client = httpx.AsyncClient(timeout=timeout)

    async def chat(self, user_id: str, session_id: str, content: str) -> str:
        """
        Send a message to the chat endpoint.

        :param user_id: The user ID.
        :param session_id: The session ID.
        :param content: The content of the message to send.
        :return: The response from the chat API as a string.
        """
        try:
            logger.debug(f"Sending message to chat endpoint: {content}")
            return await send_chat_message(
                self.http_client, self.base_url, user_id, session_id, content
            )
        except Exception as e:
            logger.error(f"Failed to send chat message - {content}: {e}")
            raise Exception(f"Failed to send chat message: {e}")

    async def get_chat_history(self, user_id: str, session_id: str) -> List[Dict]:
        """
        Retrieve the chat history for a specified user and session.

        :param user_id: The user ID.
        :param session_id: The session ID.
        :return: The chat history as a list of dictionaries.
        """
        try:
            return await get_chat_history(
                self.http_client, self.base_url, user_id, session_id
            )
        except Exception as e:
            logger.error(
                f"Failed to get chat history for user {user_id} and session {session_id}: {e}"
            )
            raise Exception(f"Failed to get chat history: {e}")

    async def get_all_chats(self, user_id: str) -> Dict[str, List[Dict]]:
        """
        Retrieve all chat sessions for a specified user.

        :param user_id: The user ID.
        :return: All chat sessions as a dictionary with session IDs as keys and lists of messages as values.
        """

        try:
            return await get_all_chats(self.http_client, self.base_url, user_id)
        except Exception as e:
            logger.error(f"Failed to get all chats for user {user_id}: {e}")
            raise Exception(f"Failed to get all chats: {e}")

    async def chat_media(
            self,
            user_id: str,
            session_id: str,
            chat_data: str,
            files: List[str],
    ) -> str:
        """
        Send a chat message with associated media files to the chat_media endpoint.

        :param user_id: The user ID.
        :param session_id: The session ID.
        :param chat_data: The chat data in JSON format as a string.
        :param files: A list of file paths to be uploaded.
        :return: The response from the chat_media API as a string.
        """
        try:
            logger.debug(f"Sending chat media to chat_media endpoint with files: {files}")
            return await send_chat_media(
                self.http_client, self.base_url, user_id, session_id, chat_data, files
            )
        except Exception as e:
            logger.error(f"Failed to send chat media - files: {files}, error: {e}")
            raise Exception(f"Failed to send chat media: {e}")

    async def create_table(self, table_name: str, columns: dict) -> Dict:
        """
        Create a new table in the database.

        :param table_name: The name of the table to create.
        :param columns: The columns of the table to create.
        :return: A dictionary with a message about the table creation.
        """
        try:
            return await create_table(
                self.http_client, self.base_url, table_name, columns
            )
        except Exception as e:
            logger.error(
                f"Failed to create table {table_name} with columns {columns}: {e}"
            )
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

    async def read_data(self, table_name: str, filters: dict = None) -> List[Dict]:
        """
        Retrieve data from a table.

        :param table_name: The name of the table to read data from.
        :param filters: Optional filters to apply when reading data.
        :return: A list of dictionaries representing the read data.
        """
        try:
            return await read_data(self.http_client, self.base_url, table_name, filters)
        except Exception as e:
            logger.error(
                f"Failed to read data from table {table_name} with filters {filters}: {e}"
            )
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
            return await update_data(
                self.http_client, self.base_url, table_name, row_id, new_data
            )
        except Exception as e:
            logger.error(
                f"Failed to update data in table {table_name} with id {row_id} and data {new_data}: {e}"
            )
            raise Exception(f"Failed to update data: {e}")

    async def delete_data(self, table_name: str, row_id: int) -> Dict:
        """
        Delete data from a table.

        :param table_name: The name of the table to delete data from.
        :param row_id: The ID of the row to delete.
        :return: A dictionary with a message about the deletion.
        """
        try:
            return await delete_data(
                self.http_client, self.base_url, table_name, row_id
            )
        except Exception as e:
            logger.error(
                f"Failed to delete data from table {table_name} with id {row_id}: {e}"
            )
            raise Exception(f"Failed to delete data: {e}")

    async def upload_files(self, file_paths: List[str]) -> Dict:
        """
        Upload files to the server.

        :param file_paths: A list of file paths to be uploaded.
        :return: A dictionary with the names of the uploaded files.
        """
        try:
            return await upload_files(self.http_client, self.base_url, file_paths)
        except Exception as e:
            logger.error(f"Failed to upload files {file_paths}: {e}")
            raise Exception(f"Failed to upload files: {e}")

    async def list_files(self) -> Dict:
        """
        List all files stored on the server.

        :return: A dictionary with a list of file names.
        """
        try:
            return await list_files(self.http_client, self.base_url)
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            raise Exception(f"Failed to list files: {e}")

    async def delete_file(self, filename: str) -> Dict:
        """
        Delete a specified file from the server.

        :param filename: The name of the file to be deleted.
        :return: A dictionary with a message about the file deletion.
        """
        try:
            return await delete_file(self.http_client, self.base_url, filename)
        except Exception as e:
            logger.error(f"Failed to delete file {filename}: {e}")
            raise Exception(f"Failed to delete file: {e}")

    async def rename_file(self, old_filename: str, new_filename: str) -> Dict:
        """
        Rename a specified file on the server.

        :param old_filename: The current name of the file.
        :param new_filename: The new name for the file.
        :return: A dictionary with a message about the file renaming.
        """
        try:
            return await rename_file(
                self.http_client, self.base_url, old_filename, new_filename
            )
        except Exception as e:
            logger.error(
                f"Failed to rename file from {old_filename} to {new_filename}: {e}"
            )
            raise Exception(f"Failed to rename file: {e}")

    async def install_tools(self, tools: List[Dict[str, str | List[str]]]) -> Dict:
        """
        Install tools on the agent using the agent's `install_tools` API.

        :param tools: A list of dictionaries where each dictionary contains:
                      - 'url': the GitHub URL of the tool repository.
                      - 'functions': list of paths to the functions to import.
        :return: A dictionary with the response from the agent.
        """
        try:
            return await install_tools(self.http_client, self.base_url, tools)
        except Exception as e:
            logger.error(f"Failed to install tools: {e}")
            raise Exception(f"Failed to install tools: {e}")

    async def close(self):
        """
        Close the HTTP client session.
        """
        logger.debug("Closing HTTP client session...")
        await self.http_client.aclose()
