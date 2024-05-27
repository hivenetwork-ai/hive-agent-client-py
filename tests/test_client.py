import os
import httpx
import json
import pytest
import respx

from hive_agent_client.client import HiveAgentClient

base_url = "http://example.com"


def check_response(response: int) -> int:
    if response != 200:
        raise Exception(f"Unexpected status code: {response}")
    else:
        return response


@pytest.fixture
def temp_files():
    file_paths = ["test1.txt", "test2.txt"]
    for file_path in file_paths:
        with open(file_path, "w") as f:
            f.write("test content")
    yield file_paths
    for file_path in file_paths:
        os.remove(file_path)


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
async def test_create_table_success():
    table_name = "test_table"
    columns = {"id": "Integer", "name": "String"}
    expected_response = {"message": f"Table {table_name} created successfully."}

    with respx.mock() as mock:
        mock.post(f"{base_url}/database/create-table", json={"table_name": table_name, "columns": columns}).mock(
            return_value=httpx.Response(200, json=expected_response))

        client = HiveAgentClient(base_url)
        response = await client.create_table(table_name, columns)
        assert response == expected_response


@pytest.mark.asyncio
async def test_create_table_failure():
    table_name = "test_table"
    columns = {"id": "Integer", "name": "String"}

    with respx.mock() as mock:
        mock.post(f"{base_url}/database/create-table", json={"table_name": table_name, "columns": columns}).mock(
            return_value=httpx.Response(400))

        client = HiveAgentClient(base_url)
        with pytest.raises(Exception) as excinfo:
            await client.create_table(table_name, columns)
        assert "Failed to create table" in str(excinfo.value)


@pytest.mark.asyncio
async def test_insert_data_success():
    table_name = "test_table"
    data = {"name": "Test"}
    expected_response = {"message": "Data inserted successfully.", "id": 1}

    with respx.mock() as mock:
        mock.post(f"{base_url}/database/insert-data", json={"table_name": table_name, "data": data}).mock(
            return_value=httpx.Response(200, json=expected_response))

        client = HiveAgentClient(base_url)
        response = await client.insert_data(table_name, data)
        assert response == expected_response


@pytest.mark.asyncio
async def test_insert_data_failure():
    table_name = "test_table"
    data = {"name": "Test"}

    with respx.mock() as mock:
        mock.post(f"{base_url}/database/insert-data", json={"table_name": table_name, "data": data}).mock(
            return_value=httpx.Response(400))

        client = HiveAgentClient(base_url)
        with pytest.raises(Exception) as excinfo:
            await client.insert_data(table_name, data)
        assert "Failed to insert data" in str(excinfo.value)


@pytest.mark.asyncio
async def test_read_data_success():
    table_name = "test_table"
    filters = {"id": [1]}
    expected_response = [{"id": 1, "name": "Test"}]

    with respx.mock() as mock:
        mock.post(f"{base_url}/database/read-data", json={"table_name": table_name, "filters": filters}).mock(
            return_value=httpx.Response(200, json=expected_response))

        client = HiveAgentClient(base_url)
        response = await client.read_data(table_name, filters)
        assert response == expected_response


@pytest.mark.asyncio
async def test_read_data_failure():
    table_name = "test_table"
    filters = {"id": [1]}

    with respx.mock() as mock:
        mock.post(f"{base_url}/database/read-data", json={"table_name": table_name, "filters": filters}).mock(
            return_value=httpx.Response(400))

        client = HiveAgentClient(base_url)
        with pytest.raises(Exception) as excinfo:
            await client.read_data(table_name, filters)
        assert "Failed to read data" in str(excinfo.value)


@pytest.mark.asyncio
async def test_update_data_success():
    table_name = "test_table"
    row_id = 1
    data = {"name": "Updated Test"}
    expected_response = {"message": "Data updated successfully."}

    with respx.mock() as mock:
        mock.put(f"{base_url}/database/update-data", json={"table_name": table_name, "id": row_id, "data": data}).mock(
            return_value=httpx.Response(200, json=expected_response))

        client = HiveAgentClient(base_url)
        response = await client.update_data(table_name, row_id, data)
        assert response == expected_response


@pytest.mark.asyncio
async def test_update_data_failure():
    table_name = "test_table"
    row_id = 1
    data = {"name": "Updated Test"}

    with respx.mock() as mock:
        mock.put(f"{base_url}/database/update-data", json={"table_name": table_name, "id": row_id, "data": data}).mock(
            return_value=httpx.Response(400))

        client = HiveAgentClient(base_url)
        with pytest.raises(Exception) as excinfo:
            await client.update_data(table_name, row_id, data)
        assert "Failed to update data" in str(excinfo.value)


@pytest.mark.asyncio
async def test_delete_data_success():
    table_name = "test_table"
    row_id = 1
    expected_response = {"message": "Data deleted successfully."}

    with respx.mock() as mock:
        mock.request("DELETE", f"{base_url}/database/delete-data",
                     content=json.dumps({"table_name": table_name, "id": row_id})).mock(
            return_value=httpx.Response(200, json=expected_response))

        client = HiveAgentClient(base_url)
        response = await client.delete_data(table_name, row_id)
        assert response == expected_response


@pytest.mark.asyncio
async def test_delete_data_failure():
    table_name = "test_table"
    row_id = 1

    with respx.mock() as mock:
        mock.request("DELETE", f"{base_url}/database/delete-data",
                     content=json.dumps({"table_name": table_name, "id": row_id})).mock(
            return_value=httpx.Response(400))

        client = HiveAgentClient(base_url)
        with pytest.raises(Exception) as excinfo:
            await client.delete_data(table_name, row_id)
        assert "Failed to delete data" in str(excinfo.value)


@pytest.mark.asyncio
async def test_upload_files_success(temp_files):
    expected_response = {"filenames": ["test1.txt", "test2.txt"]}

    with respx.mock() as mock:
        mock.post(f"{base_url}/uploadfiles/").mock(
            return_value=httpx.Response(200, json=expected_response))

        client = HiveAgentClient(base_url)
        response = await client.upload_files(temp_files)
        assert response == expected_response


@pytest.mark.asyncio
async def test_upload_files_failure(temp_files):
    with respx.mock() as mock:
        mock.post(f"{base_url}/uploadfiles/").mock(
            return_value=httpx.Response(400))

        client = HiveAgentClient(base_url)
        with pytest.raises(Exception) as excinfo:
            await client.upload_files(temp_files)
        assert "Failed to upload files" in str(excinfo.value)


@pytest.mark.asyncio
async def test_list_files_success():
    expected_response = {"files": ["test1.txt", "test2.txt"]}

    with respx.mock() as mock:
        mock.get(f"{base_url}/files/").mock(
            return_value=httpx.Response(200, json=expected_response))

        client = HiveAgentClient(base_url)
        response = await client.list_files()
        assert response == expected_response


@pytest.mark.asyncio
async def test_list_files_failure():
    with respx.mock() as mock:
        mock.get(f"{base_url}/files/").mock(
            return_value=httpx.Response(400))

        client = HiveAgentClient(base_url)
        with pytest.raises(Exception) as excinfo:
            await client.list_files()
        assert "Failed to list files" in str(excinfo.value)


@pytest.mark.asyncio
async def test_delete_file_success():
    filename = "test_delete.txt"
    expected_response = {"message": f"File {filename} deleted successfully."}

    with respx.mock() as mock:
        mock.delete(f"{base_url}/files/{filename}").mock(
            return_value=httpx.Response(200, json=expected_response))

        client = HiveAgentClient(base_url)
        response = await client.delete_file(filename)
        assert response == expected_response


@pytest.mark.asyncio
async def test_delete_file_failure():
    filename = "test_delete.txt"

    with respx.mock() as mock:
        mock.delete(f"{base_url}/files/{filename}").mock(
            return_value=httpx.Response(400))

        client = HiveAgentClient(base_url)
        with pytest.raises(Exception) as excinfo:
            await client.delete_file(filename)
        assert "Failed to delete file" in str(excinfo.value)


@pytest.mark.asyncio
async def test_rename_file_success():
    old_filename = "old_name.txt"
    new_filename = "new_name.txt"
    expected_response = {"message": f"File {old_filename} renamed to {new_filename} successfully."}

    with respx.mock() as mock:
        mock.put(f"{base_url}/files/{old_filename}/{new_filename}").mock(
            return_value=httpx.Response(200, json=expected_response))

        client = HiveAgentClient(base_url)
        response = await client.rename_file(old_filename, new_filename)
        assert response == expected_response


@pytest.mark.asyncio
async def test_rename_file_failure():
    old_filename = "old_name.txt"
    new_filename = "new_name.txt"

    with respx.mock() as mock:
        mock.put(f"{base_url}/files/{old_filename}/{new_filename}").mock(
            return_value=httpx.Response(400))

        client = HiveAgentClient(base_url)
        with pytest.raises(Exception) as excinfo:
            await client.rename_file(old_filename, new_filename)
        assert "Failed to rename file" in str(excinfo.value)


@pytest.mark.asyncio
async def test_close_http_client():
    client = HiveAgentClient(base_url)
    await client.close()  # test passes if this completes without error


# Negative Tests

@pytest.mark.asyncio
async def test_network_failure_handling():
    with respx.mock() as mock:
        mock.get(f"{base_url}/database/read-data").mock(return_value=httpx.Response(504))

        response = await httpx.AsyncClient().get(f"{base_url}/database/read-data")

        with pytest.raises(Exception) as excinfo:
            check_response(response.status_code)
        assert "Unexpected status code" in str(excinfo.value)


@pytest.mark.asyncio
async def test_out_of_scope():
    with respx.mock() as mock:
        mock.get(f"{base_url}/database/read-data").mock(return_value=httpx.Response(404))

        response = await httpx.AsyncClient().get(f"{base_url}/database/read-data")

        with pytest.raises(Exception) as excinfo:
            check_response(response.status_code)
        assert "Unexpected status code" in str(excinfo.value)


@pytest.mark.asyncio
async def test_heavy_load():
    with respx.mock() as mock:
        mock.get(f"{base_url}/database/read-data").mock(return_value=httpx.Response(429))

        response = await httpx.AsyncClient().get(f"{base_url}/database/read-data")

        with pytest.raises(Exception) as excinfo:
            check_response(response.status_code)
        assert "Unexpected status code" in str(excinfo.value)


@pytest.mark.asyncio
async def test_internal_server():
    with respx.mock() as mock:
        mock.get(f"{base_url}/database/read-data").mock(return_value=httpx.Response(500))

        response = await httpx.AsyncClient().get(f"{base_url}/database/read-data")

        with pytest.raises(Exception) as excinfo:
            check_response(response.status_code)
        assert "Unexpected status code" in str(excinfo.value)


@pytest.mark.asyncio
async def test_large_data_entry():
    with respx.mock() as mock:
        mock.get(f"{base_url}/database/read-data").mock(return_value=httpx.Response(413))

        response = await httpx.AsyncClient().get(f"{base_url}/database/read-data")

        with pytest.raises(Exception) as excinfo:
            check_response(response.status_code)
        assert "Unexpected status code" in str(excinfo.value)


@pytest.mark.asyncio
async def test_unprocessable_data_entry():
    with respx.mock() as mock:
        mock.get(f"{base_url}/database/read-data").mock(return_value=httpx.Response(422))

        response = await httpx.AsyncClient().get(f"{base_url}/database/read-data")

        with pytest.raises(Exception) as excinfo:
            check_response(response.status_code)
        assert "Unexpected status code" in str(excinfo.value)


@pytest.mark.asyncio
async def test_response_success():
    with respx.mock() as mock:
        mock.get(f"{base_url}/database/read-data").mock(return_value=httpx.Response(200))

        response = await httpx.AsyncClient().get(f"{base_url}/database/read-data")

        check_response(response.status_code)
        assert response.status_code == 200
