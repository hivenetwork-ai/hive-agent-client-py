import httpx
import logging
import os
import sys


def get_log_level():
    HIVE_AGENT_LOG_LEVEL = os.getenv("HIVE_AGENT_LOG_LEVEL", "INFO").upper()
    return getattr(logging, HIVE_AGENT_LOG_LEVEL, logging.INFO)


logging.basicConfig(stream=sys.stdout, level=get_log_level())
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

logger = logging.getLogger()
logger.setLevel(get_log_level())


async def sample_prompts(http_client: httpx.AsyncClient, base_url: str) -> dict:
    """
    Lists all sample prompts for the agent

    :param http_client: An HTTP client for sending requests.
    :param base_url: The base URL of the Hive Agent API.
    :return: A dictionary containing the list of all the suggested prompts for starting an interaction with the agent.
    :raises Exception: If the HTTP request fails or the API returns an error response.
    """
    endpoint = "/sample_prompts/"
    url = f"{base_url}{endpoint}"

    try:
        logger.debug(f"Listing sample prompts at {url}")
        response = await http_client.get(url)
        response.raise_for_status()
        logger.debug(f"Response for sample prompts at {url}: {response.json()}")
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to get sample prompts: {e}")
        raise Exception(f"Failed to get sample prompts: {e.response.text}") from e