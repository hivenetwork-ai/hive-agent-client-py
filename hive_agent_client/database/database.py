import json

import httpx
import logging
import os
import sys

from typing import Optional


def get_log_level():
    HIVE_AGENT_LOG_LEVEL = os.getenv('HIVE_AGENT_LOG_LEVEL', 'INFO').upper()
    return getattr(logging, HIVE_AGENT_LOG_LEVEL, logging.INFO)


logging.basicConfig(stream=sys.stdout, level=get_log_level())
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

logger = logging.getLogger()
logger.setLevel(get_log_level())


async def create_table(http_client: httpx.AsyncClient, base_url: str, table_name: str, columns: dict) -> dict:
    """
    Creates a table in the database.

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :param table_name: The name of the table to be created.
    :param columns: The columns of the table to be created.
    :return: A dictionary with a message about the table creation.
    :raises Exception: If the HTTP request fails or the API returns an error response.
    """
    endpoint = "/database/create-table"
    url = f"{base_url}{endpoint}"
    data = {"table_name": table_name, "columns": columns}

    try:
        logger.debug(f"Creating table {table_name} at {url}")
        response = await http_client.post(url, json=data)
        response.raise_for_status()
        logger.debug(f"Response for creating table {table_name} at {url}: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to create table {table_name}: {e}")
        raise Exception(f"Failed to create table {table_name}: {e.response.text}") from e


async def insert_data(http_client: httpx.AsyncClient, base_url: str, table_name: str, data: dict) -> dict:
    """
    Inserts data into a table in the database.

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :param table_name: The name of the table where the data will be inserted.
    :param data: The data to be inserted.
    :return: A dictionary with a message and the id of the inserted data.
    :raises Exception: If the HTTP request fails or the API returns an error response.
    """
    endpoint = "/database/insert-data"
    url = f"{base_url}{endpoint}"
    payload = {"table_name": table_name, "data": data}

    try:
        logger.debug(f"Inserting data into {table_name} at {url}")
        response = await http_client.post(url, json=payload)
        response.raise_for_status()
        logger.debug(f"Response for inserting data into {table_name} at {url}: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to insert data into {table_name}: {e}")
        raise Exception(f"Failed to insert data into {table_name}: {e.response.text}") from e


async def read_data(http_client: httpx.AsyncClient, base_url: str, table_name: str,
                    filters: Optional[dict] = None) -> list:
    """
    Reads data from a table in the database.

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :param table_name: The name of the table from which to read data.
    :param filters: Optional filters to apply when reading data.
    :return: A list of dictionaries representing the read data.
    :raises Exception: If the HTTP request fails or the API returns an error response.
    """
    endpoint = "/database/read-data"
    url = f"{base_url}{endpoint}"
    payload = {"table_name": table_name, "filters": filters}

    try:
        logger.debug(f"Reading data from {table_name} at {url} with filters: {filters}")
        response = await http_client.post(url, json=payload)
        response.raise_for_status()
        logger.debug(f"Response for reading data from {table_name} at {url}: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to read data from {table_name}: {e}")
        raise Exception(f"Failed to read data from {table_name}: {e.response.text}") from e


async def update_data(http_client: httpx.AsyncClient, base_url: str, table_name: str, row_id: int,
                      new_data: dict) -> dict:
    """
    Updates data in a table in the database.

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :param table_name: The name of the table where the data will be updated.
    :param row_id: The ID of the row to be updated.
    :param new_data: The new data to update in the table.
    :return: A dictionary with a message about the update.
    :raises Exception: If the HTTP request fails or the API returns an error response.
    """
    endpoint = "/database/update-data"
    url = f"{base_url}{endpoint}"
    payload = {"table_name": table_name, "id": row_id, "data": new_data}

    try:
        logger.debug(f"Updating data in {table_name} with id {row_id} at {url} with new data: {new_data}")
        response = await http_client.put(url, json=payload)
        response.raise_for_status()
        logger.debug(f"Response for updating data in {table_name} with id {row_id} at {url}: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to update data in {table_name} with id {row_id}: {e}")
        raise Exception(f"Failed to update data in {table_name} with id {row_id}: {e.response.text}") from e


async def delete_data(http_client: httpx.AsyncClient, base_url: str, table_name: str, row_id: int) -> dict:
    """
    Deletes data from a table in the database.

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :param table_name: The name of the table where the data will be deleted.
    :param row_id: The ID of the row to be deleted.
    :return: A dictionary with a message about the deletion.
    :raises Exception: If the HTTP request fails or the API returns an error response.
    """
    endpoint = "/database/delete-data"
    url = f"{base_url}{endpoint}"
    payload = {"table_name": table_name, "id": row_id}

    try:
        logger.debug(f"Deleting data from {table_name} with id {row_id} at {url}")
        response = await http_client.request("DELETE", url, content=json.dumps(payload))
        response.raise_for_status()
        logger.debug(f"Response for deleting data from {table_name} with id {row_id} at {url}: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to delete data from {table_name} with id {row_id}: {e}")
        raise Exception(f"Failed to delete data from {table_name} with id {row_id}: {e.response.text}") from e

