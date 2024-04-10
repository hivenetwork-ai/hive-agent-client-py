import httpx
import pytest
import respx

from hive_agent_client.entry import (
    create_entry,
    stream_entry,
    get_entries,
    get_entry_by_id,
    update_entry,
    delete_entry
)

base_url = "http://example.com"
namespace = "test-namespace"


@pytest.mark.asyncio
async def test_create_entry_success():
    data = {"key": "value"}
    expected_response = {"id": "123", "key": "value"}

    with respx.mock() as mock:
        mock.post(f"{base_url}/api/entry/{namespace}", json=data).mock(
            return_value=httpx.Response(200, json=expected_response))

        async with httpx.AsyncClient() as client:
            response = await create_entry(client, base_url, namespace, data)
            assert response == expected_response


@pytest.mark.asyncio
async def test_create_entry_http_error():
    data = {"key": "value"}

    with respx.mock() as mock:
        mock.post(f"{base_url}/api/entry/{namespace}", json=data).mock(return_value=httpx.Response(400))

        async with httpx.AsyncClient() as client:
            with pytest.raises(Exception) as excinfo:
                await create_entry(client, base_url, namespace, data)
            assert "Failed to create entry" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_entries_success():
    expected_response = [{"id": "123", "key": "value"}]

    with respx.mock() as mock:
        mock.get(f"{base_url}/api/entry/{namespace}").mock(return_value=httpx.Response(200, json=expected_response))

        async with httpx.AsyncClient() as client:
            response = await get_entries(client, base_url, namespace)
            assert response == expected_response


@pytest.mark.asyncio
async def test_get_entries_http_error():
    with respx.mock() as mock:
        mock.get(f"{base_url}/api/entry/{namespace}").mock(return_value=httpx.Response(400))

        async with httpx.AsyncClient() as client:
            with pytest.raises(Exception) as excinfo:
                await get_entries(client, base_url, namespace)
            assert "Failed to get entries" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_entry_by_id_success():
    entry_id = "123"
    expected_response = {"id": "123", "key": "value"}

    with respx.mock() as mock:
        mock.get(f"{base_url}/api/entry/{namespace}/{entry_id}").mock(
            return_value=httpx.Response(200, json=expected_response))

        async with httpx.AsyncClient() as client:
            response = await get_entry_by_id(client, base_url, namespace, entry_id)
            assert response == expected_response


@pytest.mark.asyncio
async def test_get_entry_by_id_http_error():
    entry_id = "123"

    with respx.mock() as mock:
        mock.get(f"{base_url}/api/entry/{namespace}/{entry_id}").mock(return_value=httpx.Response(400))

        async with httpx.AsyncClient() as client:
            with pytest.raises(Exception) as excinfo:
                await get_entry_by_id(client, base_url, namespace, entry_id)
            assert "Failed to get entry" in str(excinfo.value)


@pytest.mark.asyncio
async def test_update_entry_success():
    entry_id = "123"
    data = {"key": "updated value"}
    expected_response = {"id": "123", "key": "updated value"}

    with respx.mock() as mock:
        mock.put(f"{base_url}/api/entry/{namespace}/{entry_id}", json=data).mock(
            return_value=httpx.Response(200, json=expected_response))

        async with httpx.AsyncClient() as client:
            response = await update_entry(client, base_url, namespace, entry_id, data)
            assert response == expected_response


@pytest.mark.asyncio
async def test_update_entry_http_error():
    entry_id = "123"
    data = {"key": "updated value"}

    with respx.mock() as mock:
        mock.put(f"{base_url}/api/entry/{namespace}/{entry_id}", json=data).mock(return_value=httpx.Response(400))

        async with httpx.AsyncClient() as client:
            with pytest.raises(Exception) as excinfo:
                await update_entry(client, base_url, namespace, entry_id, data)
            assert "Failed to update entry" in str(excinfo.value)


@pytest.mark.asyncio
async def test_delete_entry_success():
    entry_id = "123"
    expected_response = {"message": "Entry deleted"}

    with respx.mock() as mock:
        mock.delete(f"{base_url}/api/entry/{namespace}/{entry_id}").mock(
            return_value=httpx.Response(200, json=expected_response))

        async with httpx.AsyncClient() as client:
            response = await delete_entry(client, base_url, namespace, entry_id)
            assert response == expected_response


@pytest.mark.asyncio
async def test_delete_entry_http_error():
    entry_id = "123"

    with respx.mock() as mock:
        mock.delete(f"{base_url}/api/entry/{namespace}/{entry_id}").mock(return_value=httpx.Response(400))

        async with httpx.AsyncClient() as client:
            with pytest.raises(Exception) as excinfo:
                await delete_entry(client, base_url, namespace, entry_id)
            assert "Failed to delete entry" in str(excinfo.value)
