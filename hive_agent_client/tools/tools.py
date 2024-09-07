import httpx
import logging
import os
import sys

from typing import List, Dict, Any


def get_log_level():
    HIVE_AGENT_LOG_LEVEL = os.getenv("HIVE_AGENT_LOG_LEVEL", "INFO").upper()
    return getattr(logging, HIVE_AGENT_LOG_LEVEL, logging.INFO)


logging.basicConfig(stream=sys.stdout, level=get_log_level())
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

logger = logging.getLogger()
logger.setLevel(get_log_level())


async def install_tools(
    http_client: httpx.AsyncClient,
    base_url: str,
    tools: List[Dict[str, Any]]
) -> Dict:
    """
    Installs tools to the Hive Agent API and returns the response.

    :param http_client: An instance of httpx.AsyncClient to make HTTP requests.
    :param base_url: The base URL of the Hive Agent API.
    :param tools: A list of tool configurations where each dictionary contains:
                  - 'url': The GitHub URL of the tool repository.
                  - 'functions': The list of paths to the functions in the tool.
    :return: The response as JSON (a dictionary).
    :raises httpx.HTTPStatusError: If the request fails due to a network error or returns a 4xx/5xx response.
    :raises Exception: For other types of errors.
    """
    endpoint = "/install_tools"
    url = f"{base_url}{endpoint}"
    payload = tools

    try:
        logging.debug(f"Installing tools to {url} with data: {payload}")
        response = await http_client.post(url, json=payload)
        response.raise_for_status()
        logger.debug(f"Response from installing tools: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(
            f"HTTP error occurred when installing tools to {url}: {e.response.status_code} - {e.response.text}"
        )
        raise Exception(
            f"HTTP error occurred when installing tools to the API: {e.response.status_code} - {e.response.text}"
        )
    except httpx.RequestError as e:
        logging.error(f"Request error occurred when installing tools to {url}: {e}")
        raise Exception(
            f"Request error occurred when installing tools to the API: {e}"
        )
    except Exception as e:
        logging.error(f"An unexpected error occurred when installing tools: {e}")
        raise Exception(
            f"An unexpected error occurred when installing tools to the API: {e}"
        )
