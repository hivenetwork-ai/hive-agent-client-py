import json

import httpx
import pytest
import respx

from hive_agent_client.database import (
    create_table,
    insert_data,
    read_data,
    update_data,
    delete_data,
)

base_url = "http://example.com"


@pytest.mark.asyncio
async def test_create_table_success():
    table_name = "test_table"
    columns = {"id": "Integer", "name": "String"}
    expected_response = {"message": f"Table {table_name} created successfully."}

    with respx.mock() as mock:
        mock.post(
            f"{base_url}/database/create-table",
            json={"table_name": table_name, "columns": columns},
        ).mock(return_value=httpx.Response(200, json=expected_response))

        async with httpx.AsyncClient() as client:
            response = await create_table(client, base_url, table_name, columns)
            assert response == expected_response


@pytest.mark.asyncio
async def test_create_table_http_error():
    table_name = "test_table"
    columns = {"id": "Integer", "name": "String"}

    with respx.mock() as mock:
        mock.post(
            f"{base_url}/database/create-table",
            json={"table_name": table_name, "columns": columns},
        ).mock(return_value=httpx.Response(400))

        async with httpx.AsyncClient() as client:
            with pytest.raises(Exception) as excinfo:
                await create_table(client, base_url, table_name, columns)
            assert "Failed to create table" in str(excinfo.value)


@pytest.mark.asyncio
async def test_insert_data_success():
    table_name = "test_table"
    data = {"name": "Test"}
    expected_response = {"message": "Data inserted successfully.", "id": 1}

    with respx.mock() as mock:
        mock.post(
            f"{base_url}/database/insert-data",
            json={"table_name": table_name, "data": data},
        ).mock(return_value=httpx.Response(200, json=expected_response))

        async with httpx.AsyncClient() as client:
            response = await insert_data(client, base_url, table_name, data)
            assert response == expected_response


@pytest.mark.asyncio
async def test_insert_data_http_error():
    table_name = "test_table"
    data = {"name": "Test"}

    with respx.mock() as mock:
        mock.post(
            f"{base_url}/database/insert-data",
            json={"table_name": table_name, "data": data},
        ).mock(return_value=httpx.Response(400))

        async with httpx.AsyncClient() as client:
            with pytest.raises(Exception) as excinfo:
                await insert_data(client, base_url, table_name, data)
            assert "Failed to insert data" in str(excinfo.value)


@pytest.mark.asyncio
async def test_read_data_success():
    table_name = "test_table"
    filters = {"id": [1]}
    expected_response = [{"id": 1, "name": "Test"}]

    with respx.mock() as mock:
        mock.post(
            f"{base_url}/database/read-data",
            json={"table_name": table_name, "filters": filters},
        ).mock(return_value=httpx.Response(200, json=expected_response))

        async with httpx.AsyncClient() as client:
            response = await read_data(client, base_url, table_name, filters)
            assert response == expected_response


@pytest.mark.asyncio
async def test_read_data_http_error():
    table_name = "test_table"
    filters = {"id": [1]}

    with respx.mock() as mock:
        mock.post(
            f"{base_url}/database/read-data",
            json={"table_name": table_name, "filters": filters},
        ).mock(return_value=httpx.Response(400))

        async with httpx.AsyncClient() as client:
            with pytest.raises(Exception) as excinfo:
                await read_data(client, base_url, table_name, filters)
            assert "Failed to read data" in str(excinfo.value)


@pytest.mark.asyncio
async def test_update_data_success():
    table_name = "test_table"
    row_id = 1
    new_data = {"name": "Updated Test"}
    expected_response = {"message": "Data updated successfully."}

    with respx.mock() as mock:
        mock.put(
            f"{base_url}/database/update-data",
            json={"table_name": table_name, "id": row_id, "data": new_data},
        ).mock(return_value=httpx.Response(200, json=expected_response))

        async with httpx.AsyncClient() as client:
            response = await update_data(client, base_url, table_name, row_id, new_data)
            assert response == expected_response


@pytest.mark.asyncio
async def test_update_data_http_error():
    table_name = "test_table"
    row_id = 1
    new_data = {"name": "Updated Test"}

    with respx.mock() as mock:
        mock.put(
            f"{base_url}/database/update-data",
            json={"table_name": table_name, "id": row_id, "data": new_data},
        ).mock(return_value=httpx.Response(400))

        async with httpx.AsyncClient() as client:
            with pytest.raises(Exception) as excinfo:
                await update_data(client, base_url, table_name, row_id, new_data)
            assert "Failed to update data" in str(excinfo.value)


@pytest.mark.asyncio
async def test_delete_data_success():
    table_name = "test_table"
    row_id = 1
    expected_response = {"message": "Data deleted successfully."}

    with respx.mock() as mock:
        mock.request(
            "DELETE",
            f"{base_url}/database/delete-data",
            content=json.dumps({"table_name": table_name, "id": row_id}),
        ).mock(return_value=httpx.Response(200, json=expected_response))

        async with httpx.AsyncClient() as client:
            response = await delete_data(client, base_url, table_name, row_id)
            assert response == expected_response


@pytest.mark.asyncio
async def test_delete_data_http_error():
    table_name = "test_table"
    row_id = 1

    with respx.mock() as mock:
        mock.request(
            "DELETE",
            f"{base_url}/database/delete-data",
            content=json.dumps({"table_name": table_name, "id": row_id}),
        ).mock(return_value=httpx.Response(400))

        async with httpx.AsyncClient() as client:
            with pytest.raises(Exception) as excinfo:
                await delete_data(client, base_url, table_name, row_id)
            assert "Failed to delete data" in str(excinfo.value)
