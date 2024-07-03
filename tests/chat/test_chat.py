import httpx
import pytest

from unittest.mock import AsyncMock
from hive_agent_client.chat import send_chat_message, get_chat_history, get_all_chats


@pytest.mark.asyncio
async def test_send_chat_message_success():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.text = "Hello, world!"
    mock_client.post.return_value = mock_response

    base_url = "http://example.com/api/v1"
    user_id = "user123"
    session_id = "session123"
    content = "Hello, how are you?"

    result = await send_chat_message(
        mock_client, base_url, user_id, session_id, content
    )

    assert result == "Hello, world!"
    mock_client.post.assert_called_once_with(
        "http://example.com/api/v1/chat",
        json={
            "user_id": user_id,
            "session_id": session_id,
            "chat_data": {"messages": [{"role": "user", "content": content}]},
        },
    )


@pytest.mark.asyncio
async def test_send_chat_message_empty_content():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    base_url = "http://example.com"
    user_id = "user123"
    session_id = "session123"
    content = ""

    with pytest.raises(ValueError, match="Content must not be empty"):
        await send_chat_message(mock_client, base_url, user_id, session_id, content)


@pytest.mark.asyncio
async def test_send_chat_message_http_error():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.status_code = 400
    mock_response.text = "Bad request"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        message="Bad request", request=mock_response.request, response=mock_response
    )
    mock_client.post.return_value = mock_response

    base_url = "http://example.com"
    user_id = "user123"
    session_id = "session123"
    content = "Hello, how are you?"

    with pytest.raises(
        Exception,
        match="HTTP error occurred when sending message to the chat API: 400 - Bad request",
    ):
        await send_chat_message(mock_client, base_url, user_id, session_id, content)


@pytest.mark.asyncio
async def test_get_chat_history_success():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.status_code = 200
    expected_history = [
        {
            "user_id": "user123",
            "session_id": "session123",
            "message": "Hello",
            "role": "user",
            "timestamp": "2023-01-01T00:00:00Z",
        },
        {
            "user_id": "user123",
            "session_id": "session123",
            "message": "Hi there",
            "role": "assistant",
            "timestamp": "2023-01-01T00:00:01Z",
        },
    ]
    mock_response.json.return_value = expected_history
    mock_client.get.return_value = mock_response

    base_url = "http://example.com/api/v1"
    user_id = "user123"
    session_id = "session123"

    result = await get_chat_history(mock_client, base_url, user_id, session_id)

    assert result == expected_history
    mock_client.get.assert_called_once_with(
        f"http://example.com/api/v1/chat_history",
        params={"user_id": user_id, "session_id": session_id},
    )


@pytest.mark.asyncio
async def test_get_chat_history_failure():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.status_code = 400
    mock_response.text = "Bad request"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        message="Bad request", request=mock_response.request, response=mock_response
    )
    mock_client.get.return_value = mock_response

    base_url = "http://example.com/api/v1"
    user_id = "user123"
    session_id = "session123"

    with pytest.raises(
        Exception,
        match="HTTP error occurred when fetching chat history from the chat API: 400 - Bad request",
    ):
        await get_chat_history(mock_client, base_url, user_id, session_id)


@pytest.mark.asyncio
async def test_get_all_chats_success():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.status_code = 200

    expected_all_chats = {
        "session1": [
            {
                "message": "Hello in session1",
                "role": "USER",
                "timestamp": "2023-01-01T00:00:00Z",
            },
            {
                "message": "Response in session1",
                "role": "ASSISTANT",
                "timestamp": "2023-01-01T00:00:01Z",
            },
        ],
        "session2": [
            {
                "message": "Hello in session2",
                "role": "USER",
                "timestamp": "2023-01-01T00:00:02Z",
            },
            {
                "message": "Response in session2",
                "role": "ASSISTANT",
                "timestamp": "2023-01-01T00:00:03Z",
            },
        ],
    }

    mock_response.json.return_value = expected_all_chats
    mock_client.get.return_value = mock_response

    base_url = "http://example.com/api/v1"
    user_id = "user123"

    result = await get_all_chats(mock_client, base_url, user_id)
    assert result == expected_all_chats

    mock_client.get.assert_called_once_with(
        f"http://example.com/api/v1/all_chats",
        params={"user_id": user_id},
    )


@pytest.mark.asyncio
async def test_get_all_chats_failure():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.status_code = 400
    mock_response.text = "Bad request"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        message="Bad request", request=mock_response.request, response=mock_response
    )
    mock_client.get.return_value = mock_response

    base_url = "http://example.com/api/v1"
    user_id = "user123"

    with pytest.raises(
        Exception,
        match="HTTP error occurred when fetching all chats from the chat API: 400 - Bad request",
    ):
        await get_all_chats(mock_client, base_url, user_id)
