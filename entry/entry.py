import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_entry(http_client: httpx.AsyncClient, base_url: str, namespace: str, data: dict) -> dict:
    """
    Creates an entry in the specified namespace.

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :param namespace: The namespace where the entry will be created.
    :param data: The data of the entry to be created.
    :return: The created entry as a dictionary.
    :raises Exception: If the HTTP request fails or the API returns an error response.
    """
    endpoint = f"/api/entry/{namespace}"
    url = f"{base_url}{endpoint}"

    try:
        logger.debug(f"Creating entry in {namespace} at {url}")
        response = await http_client.post(url, json=data)
        response.raise_for_status()
        logger.debug(f"Response for creating entry in {namespace} at {url}: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to create entry in {namespace}: {e}")
        raise Exception(f"Failed to create entry in {namespace}: {e.response.text}") from e


async def stream_entry(http_client: httpx.AsyncClient, base_url: str, namespace: str, data_stream):
    """
    Streams data to the specified namespace entry endpoint and yields responses.

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :param namespace: The namespace where the data will be streamed.
    :param data_stream: An asynchronous iterable providing the data to be streamed.
    :raises RuntimeError: If WebSocket communication or data processing fails.
    """
    endpoint = f"/api/entry/{namespace}/stream"
    url = f"{base_url}{endpoint}"

    try:
        logger.debug(f"Streaming data to {namespace} at {url}")
        async with http_client.ws(url) as ws:
            try:
                async for data in data_stream:
                    await ws.send_json(data)
                    response = await ws.receive_json()
                    yield response
            except httpx.WebSocketException as e:
                logger.error(f"WebSocket communication error in namespace {namespace}: {e}")
                raise RuntimeError(f"WebSocket communication error in namespace {namespace}") from e
    except httpx.RequestError as e:
        logger.error(f"Request error while establishing WebSocket connection to {url}: {e}")
        raise RuntimeError(f"Failed to establish WebSocket connection to {url}") from e


async def get_entries(http_client: httpx.AsyncClient, base_url: str, namespace: str) -> dict:
    """
    Retrieves all entries from the specified namespace.

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :param namespace: The namespace from which to retrieve entries.
    :return: A dictionary containing all entries from the namespace.
    :raises Exception: If the HTTP request fails or the API returns an error response.
    """
    endpoint = f"/api/entry/{namespace}"
    url = f"{base_url}{endpoint}"

    try:
        logger.debug(f"Getting all entries in {namespace} at {url}")
        response = await http_client.get(url)
        response.raise_for_status()
        logger.debug(f"Response for getting all entries in {namespace} at {url}: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to get entries from {namespace}: {e}")
        raise Exception(f"Failed to get entries from {namespace}: {e.response.text}") from e


async def get_entry_by_id(http_client: httpx.AsyncClient, base_url: str, namespace: str, entry_id: str) -> dict:
    """
    Retrieves a specific entry by ID from the given namespace.

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :param namespace: The namespace from which to retrieve the entry.
    :param entry_id: The ID of the entry to retrieve.
    :return: A dictionary representing the requested entry.
    :raises Exception: If the HTTP request fails or the API returns an error response.
    """
    endpoint = f"/api/entry/{namespace}/{entry_id}"
    url = f"{base_url}{endpoint}"

    try:
        logger.debug(f"Getting entry {entry_id} from {namespace} at {url}")
        response = await http_client.get(url)
        response.raise_for_status()
        logger.debug(f"Response for getting entry {entry_id} from {namespace} at {url}: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to get entry {entry_id} from {namespace}: {e}")
        raise Exception(f"Failed to get entry {entry_id} from {namespace}: {e.response.text}") from e


async def update_entry(http_client: httpx.AsyncClient, base_url: str, namespace: str, entry_id: str, data: dict) -> dict:
    """
    Updates a specific entry by ID in the given namespace.

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :param namespace: The namespace where the entry exists.
    :param entry_id: The ID of the entry to update.
    :param data: The updated data for the entry.
    :return: A dictionary representing the updated entry.
    :raises Exception: If the HTTP request fails or the API returns an error response.
    """
    endpoint = f"/api/entry/{namespace}/{entry_id}"
    url = f"{base_url}{endpoint}"

    try:
        logger.debug(f"Updating entry {entry_id} from {namespace} with {data} at {url}")
        response = await http_client.put(url, json=data)
        response.raise_for_status()
        logger.debug(f"Response for updating entry {entry_id} from {namespace} at {url}: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to update entry {entry_id} in {namespace}: {e}")
        raise Exception(f"Failed to update entry {entry_id} in {namespace}: {e.response.text}") from e


async def delete_entry(http_client: httpx.AsyncClient, base_url: str, namespace: str, entry_id: str) -> dict:
    """
    Deletes a specific entry by ID from the given namespace.

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :param namespace: The namespace where the entry exists.
    :param entry_id: The ID of the entry to delete.
    :return: A dictionary indicating the result of the deletion operation.
    :raises Exception: If the HTTP request fails or the API returns an error response.
    """
    endpoint = f"/api/entry/{namespace}/{entry_id}"
    url = f"{base_url}{endpoint}"

    try:
        logger.debug(f"Deleting {entry_id} from {namespace} at {url}")
        response = await http_client.delete(url)
        response.raise_for_status()
        logger.debug(f"Response for deleting entry {entry_id} from {namespace} at {url}: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to delete entry {entry_id} from {namespace}: {e}")
        raise Exception(f"Failed to delete entry {entry_id} from {namespace}: {e.response.text}") from e
