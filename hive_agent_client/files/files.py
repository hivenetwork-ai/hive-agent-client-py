import httpx
import logging
import os
import sys

from typing import List


def get_log_level():
    HIVE_AGENT_LOG_LEVEL = os.getenv('HIVE_AGENT_LOG_LEVEL', 'INFO').upper()
    return getattr(logging, HIVE_AGENT_LOG_LEVEL, logging.INFO)


logging.basicConfig(stream=sys.stdout, level=get_log_level())
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

logger = logging.getLogger()
logger.setLevel(get_log_level())


async def upload_files(http_client: httpx.AsyncClient, base_url: str, file_paths: List[str]) -> dict:
    """
    Uploads files to the server.

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :param file_paths: A list of file paths to be uploaded.
    :return: A dictionary with the names of the uploaded files.
    :raises Exception: If the HTTP request fails or the API returns an error response.
    """
    endpoint = "/uploadfiles/"
    url = f"{base_url}{endpoint}"
    files = [("files", (os.path.basename(file_path), open(file_path, "rb"), "multipart/form-data")) for file_path in file_paths]

    try:
        logger.debug(f"Uploading files to {url}")
        response = await http_client.post(url, files=files)
        response.raise_for_status()
        logger.debug(f"Response for uploading files to {url}: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to upload files: {e}")
        raise Exception(f"Failed to upload files: {e.response.text}") from e
    finally:
        for _, (name, file, _) in files:
            file.close()


async def list_files(http_client: httpx.AsyncClient, base_url: str) -> dict:
    """
    Lists all files stored on the server.

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :return: A dictionary with a list of file names.
    :raises Exception: If the HTTP request fails or the API returns an error response.
    """
    endpoint = "/files/"
    url = f"{base_url}{endpoint}"

    try:
        logger.debug(f"Listing files at {url}")
        response = await http_client.get(url)
        response.raise_for_status()
        logger.debug(f"Response for listing files at {url}: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to list files: {e}")
        raise Exception(f"Failed to list files: {e.response.text}") from e


async def delete_file(http_client: httpx.AsyncClient, base_url: str, filename: str) -> dict:
    """
    Deletes a specified file from the server.

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :param filename: The name of the file to be deleted.
    :return: A dictionary with a message about the file deletion.
    :raises Exception: If the HTTP request fails or the API returns an error response.
    """
    endpoint = f"/files/{filename}"
    url = f"{base_url}{endpoint}"

    try:
        logger.debug(f"Deleting file {filename} at {url}")
        response = await http_client.delete(url)
        response.raise_for_status()
        logger.debug(f"Response for deleting file {filename} at {url}: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to delete file {filename}: {e}")
        raise Exception(f"Failed to delete file {filename}: {e.response.text}") from e


async def rename_file(http_client: httpx.AsyncClient, base_url: str, old_filename: str, new_filename: str) -> dict:
    """
    Renames a specified file on the server.

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :param old_filename: The current name of the file.
    :param new_filename: The new name for the file.
    :return: A dictionary with a message about the file renaming.
    :raises Exception: If the HTTP request fails or the API returns an error response.
    """
    endpoint = f"/files/{old_filename}/{new_filename}"
    url = f"{base_url}{endpoint}"

    try:
        logger.debug(f"Renaming file from {old_filename} to {new_filename} at {url}")
        response = await http_client.put(url)
        response.raise_for_status()
        logger.debug(f"Response for renaming file from {old_filename} to {new_filename} at {url}: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to rename file from {old_filename} to {new_filename}: {e}")
        raise Exception(f"Failed to rename file from {old_filename} to {new_filename}: {e.response.text}") from e
