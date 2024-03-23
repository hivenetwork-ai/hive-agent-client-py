import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HiveAgentClient:
    """
    A client for sending messages to the chat API of a Hive Agent.
    """

    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initializes the HiveAgentClient with the given base URL and timeout.

        :param base_url: The base URL of the chat API.
        :param timeout: The timeout for HTTP requests in seconds.
        """
        self.base_url = base_url
        self.timeout = timeout

    def chat(self, content: str) -> str:
        """
        Sends a message to the chat API.

        :param content: The content of the message to send.
        :return: The chat response as a string from the API.
        :raises ValueError: If the content is empty.
        :raises Exception: If the request fails or the API returns an error.
        """
        if not content.strip():
            raise ValueError("Content must not be empty")

        endpoint = "/api/chat"
        url = f"{self.base_url}{endpoint}"
        payload = {
            "messages": [{
                "role": "user",
                "content": content
            }]
        }

        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()  # raises exception for 4xx/5xx errors

            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"failed to send message to {url}: {e}")
            raise Exception(f"an error occurred when sending message to the chat API: {e}")
