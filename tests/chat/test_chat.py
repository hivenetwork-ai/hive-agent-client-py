import httpx
import pytest


from unittest.mock import AsyncMock
from hive_agent_client.chat import send_chat_message


@pytest.mark.asyncio
async def test_send_chat_message_success():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.text = "Hello, world!"
    mock_client.post.return_value = mock_response

    base_url = "http://example.com/api/v1"
    content = "Hello, how are you?"

    result = await send_chat_message(mock_client, base_url, content)

    assert result == "Hello, world!"
    mock_client.post.assert_called_once_with(
        "http://example.com/api/v1/chat",
        json={"messages": [{"role": "user", "content": content}]}
    )


@pytest.mark.asyncio
async def test_send_chat_message_empty_content():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    base_url = "http://example.com/api/v1"
    content = ""

    with pytest.raises(ValueError, match="Content must not be empty"):
        await send_chat_message(mock_client, base_url, content)


@pytest.mark.asyncio
async def test_send_chat_message_http_error():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.status_code = 400
    mock_response.text = "Bad request"
    mock_client.post.return_value = mock_response

    base_url = "http://example.com/api/v1"
    content = "Hello, how are you?"

    with pytest.raises(Exception, match="HTTP error occurred when sending message to the chat API: 400 - Bad request"):
        await send_chat_message(mock_client, base_url, content)


@pytest.mark.asyncio
async def test_send_chat_message_http_error():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.status_code = 400
    mock_response.text = "Bad request"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(message="Bad request", request=mock_response.request, response=mock_response)
    mock_client.post.return_value = mock_response

    base_url = "http://example.com/api/v1"
    content = "Hello, how are you?"

    with pytest.raises(Exception, match="HTTP error occurred when sending message to the chat API: 400 - Bad request"):
        await send_chat_message(mock_client, base_url, content)
