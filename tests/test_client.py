import httpx
import pytest
import respx

from hive_agent_client import HiveAgentClient

base_url = "http://example.com"

def check_response(response: int) -> int:        
    if response != 200:
        raise Exception(f"Unexpected status code: {response}")
    else:
        return response
        
@pytest.mark.asyncio
async def test_chat_success():
    content = "Hello"
    expected_response = "Response from chat"

    with respx.mock() as mock:
        mock.post(f"{base_url}/api/chat").mock(return_value=httpx.Response(200, text=expected_response))

        client = HiveAgentClient(base_url)
        response = await client.chat(content)
        assert response == expected_response


@pytest.mark.asyncio
async def test_chat_failure():
    content = "Hello"

    with respx.mock() as mock:
        mock.post(f"{base_url}/api/chat").mock(return_value=httpx.Response(400))

        client = HiveAgentClient(base_url)
        with pytest.raises(Exception) as excinfo:
            await client.chat(content)
        assert "Failed to send chat message" in str(excinfo.value)


@pytest.mark.asyncio
async def test_create_entry_success():
    namespace = "test"
    data = {"key": "value"}
    expected_response = {"id": "123", "key": "value"}

    with respx.mock() as mock:
        mock.post(f"{base_url}/api/entry/{namespace}", json=data).mock(
            return_value=httpx.Response(200, json=expected_response))

        client = HiveAgentClient(base_url)
        response = await client.create_entry(namespace, data)
        assert response == expected_response


@pytest.mark.asyncio
async def test_create_entry_failure():
    namespace = "test"
    data = {"key": "value"}

    with respx.mock() as mock:
        mock.post(f"{base_url}/api/entry/{namespace}", json=data).mock(return_value=httpx.Response(400))

        client = HiveAgentClient(base_url)
        with pytest.raises(Exception) as excinfo:
            await client.create_entry(namespace, data)
        assert "Failed to create entry" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_entries_success():
    namespace = "test"
    expected_response = [{"id": "1", "key": "value"}]

    with respx.mock() as mock:
        mock.get(f"{base_url}/api/entry/{namespace}").mock(return_value=httpx.Response(200, json=expected_response))

        client = HiveAgentClient(base_url)
        response = await client.get_entries(namespace)
        assert response == expected_response


@pytest.mark.asyncio
async def test_get_entries_failure():
    namespace = "test"

    with respx.mock() as mock:
        mock.get(f"{base_url}/api/entry/{namespace}").mock(return_value=httpx.Response(400))

        client = HiveAgentClient(base_url)
        with pytest.raises(Exception) as excinfo:
            await client.get_entries(namespace)
        assert "Failed to get entries" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_entry_by_id_success():
    namespace = "test"
    entry_id = "1"
    expected_response = {"id": "1", "key": "value"}

    with respx.mock() as mock:
        mock.get(f"{base_url}/api/entry/{namespace}/{entry_id}").mock(
            return_value=httpx.Response(200, json=expected_response))

        client = HiveAgentClient(base_url)
        response = await client.get_entry_by_id(namespace, entry_id)
        assert response == expected_response


@pytest.mark.asyncio
async def test_get_entry_by_id_failure():
    namespace = "test"
    entry_id = "1"

    with respx.mock() as mock:
        mock.get(f"{base_url}/api/entry/{namespace}/{entry_id}").mock(return_value=httpx.Response(400))

        client = HiveAgentClient(base_url)
        with pytest.raises(Exception) as excinfo:
            await client.get_entry_by_id(namespace, entry_id)
        assert "Failed to get entry by ID" in str(excinfo.value)


@pytest.mark.asyncio
async def test_update_entry_success():
    namespace = "test"
    entry_id = "1"
    data = {"key": "updated value"}
    expected_response = {"id": "1", "key": "updated value"}

    with respx.mock() as mock:
        mock.put(f"{base_url}/api/entry/{namespace}/{entry_id}", json=data).mock(
            return_value=httpx.Response(200, json=expected_response))

        client = HiveAgentClient(base_url)
        response = await client.update_entry(namespace, entry_id, data)
        assert response == expected_response


@pytest.mark.asyncio
async def test_update_entry_failure():
    namespace = "test"
    entry_id = "1"
    data = {"key": "updated value"}

    with respx.mock() as mock:
        mock.put(f"{base_url}/api/entry/{namespace}/{entry_id}", json=data).mock(return_value=httpx.Response(400))

        client = HiveAgentClient(base_url)
        with pytest.raises(Exception) as excinfo:
            await client.update_entry(namespace, entry_id, data)
        assert "Failed to update entry" in str(excinfo.value)


@pytest.mark.asyncio
async def test_delete_entry_success():
    namespace = "test"
    entry_id = "1"
    expected_response = {"message": "Entry deleted successfully"}

    with respx.mock() as mock:
        mock.delete(f"{base_url}/api/entry/{namespace}/{entry_id}").mock(
            return_value=httpx.Response(200, json=expected_response))

        client = HiveAgentClient(base_url)
        response = await client.delete_entry(namespace, entry_id)
        assert response == expected_response


@pytest.mark.asyncio
async def test_delete_entry_failure():
    namespace = "test"
    entry_id = "1"

    with respx.mock() as mock:
        mock.delete(f"{base_url}/api/entry/{namespace}/{entry_id}").mock(return_value=httpx.Response(400))

        client = HiveAgentClient(base_url)
        with pytest.raises(Exception) as excinfo:
            await client.delete_entry(namespace, entry_id)
        assert "Failed to delete entry" in str(excinfo.value)


@pytest.mark.asyncio
async def test_close_http_client():
    client = HiveAgentClient(base_url)
    await client.close()  # test passes if this completes without error

# Negative Tests

@pytest.mark.asyncio
async def test_network_failure_handling():
    namespace = "test"
    entry_id = "1"

    with respx.mock() as mock:
        mock.get(f"{base_url}/api/entry/{namespace}/{entry_id}").mock(return_value=httpx.Response(504))

        response = await httpx.AsyncClient().get(f"{base_url}/api/entry/{namespace}/{entry_id}")

        with pytest.raises(Exception) as excinfo:
            check_response(response.status_code)
        assert "Unexpected status code" in str(excinfo.value)

@pytest.mark.asyncio
async def test_out_of_scope():
    namespace = "test"
    entry_id = "1"

    with respx.mock() as mock:
        mock.get(f"{base_url}/api/entry/{namespace}/{entry_id}").mock(return_value=httpx.Response(404))

        response = await httpx.AsyncClient().get(f"{base_url}/api/entry/{namespace}/{entry_id}")

        with pytest.raises(Exception) as excinfo:
            check_response(response.status_code)
        assert "Unexpected status code" in str(excinfo.value)

@pytest.mark.asyncio
async def test_heavy_load():
    namespace = "test"
    entry_id = "1"

    with respx.mock() as mock:
        mock.get(f"{base_url}/api/entry/{namespace}/{entry_id}").mock(return_value=httpx.Response(429))

        response = await httpx.AsyncClient().get(f"{base_url}/api/entry/{namespace}/{entry_id}")

        with pytest.raises(Exception) as excinfo:
            check_response(response.status_code)
        assert "Unexpected status code" in str(excinfo.value)

@pytest.mark.asyncio
async def test_internal_server():
    namespace = "test"
    entry_id = "1"

    with respx.mock() as mock:
        mock.get(f"{base_url}/api/entry/{namespace}/{entry_id}").mock(return_value=httpx.Response(500))

        response = await httpx.AsyncClient().get(f"{base_url}/api/entry/{namespace}/{entry_id}")

        with pytest.raises(Exception) as excinfo:
            check_response(response.status_code)
        assert "Unexpected status code" in str(excinfo.value)

@pytest.mark.asyncio
async def test_large_data_entry():
    namespace = "test"
    entry_id = "1"

    with respx.mock() as mock:
        mock.get(f"{base_url}/api/entry/{namespace}/{entry_id}").mock(return_value=httpx.Response(413))

        response = await httpx.AsyncClient().get(f"{base_url}/api/entry/{namespace}/{entry_id}")

        with pytest.raises(Exception) as excinfo:
            check_response(response.status_code)
        assert "Unexpected status code" in str(excinfo.value)

@pytest.mark.asyncio
async def test_unprocessable_data_entry():
    namespace = "test"
    entry_id = "1"

    with respx.mock() as mock:
        mock.get(f"{base_url}/api/entry/{namespace}/{entry_id}").mock(return_value=httpx.Response(422))

        response = await httpx.AsyncClient().get(f"{base_url}/api/entry/{namespace}/{entry_id}")

        with pytest.raises(Exception) as excinfo:
            check_response(response.status_code)
        assert "Unexpected status code" in str(excinfo.value)

@pytest.mark.asyncio
async def test_response_success():
    namespace = "test"
    entry_id = "1"

    with respx.mock() as mock:
        mock.get(f"{base_url}/api/entry/{namespace}/{entry_id}").mock(return_value=httpx.Response(200))

        response = await httpx.AsyncClient().get(f"{base_url}/api/entry/{namespace}/{entry_id}")

        check_response(response.status_code)
        assert response.status_code == 200
