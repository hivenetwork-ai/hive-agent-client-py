import os
import httpx
import pytest
import respx

from hive_agent_client.files import (
    upload_files,
    list_files,
    delete_file,
    rename_file
)

base_url = "http://example.com"


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
async def test_upload_files_success(temp_files):
    expected_response = {"filenames": ["test1.txt", "test2.txt"]}

    with respx.mock() as mock:
        mock.post(f"{base_url}/uploadfiles/").mock(
            return_value=httpx.Response(200, json=expected_response))

        async with httpx.AsyncClient() as client:
            response = await upload_files(client, base_url, temp_files)
            assert response == expected_response


@pytest.mark.asyncio
async def test_upload_files_http_error(temp_files):
    with respx.mock() as mock:
        mock.post(f"{base_url}/uploadfiles/").mock(
            return_value=httpx.Response(400))

        async with httpx.AsyncClient() as client:
            with pytest.raises(Exception) as excinfo:
                await upload_files(client, base_url, temp_files)
            assert "Failed to upload files" in str(excinfo.value)


@pytest.mark.asyncio
async def test_list_files_success():
    expected_response = {"files": ["test1.txt", "test2.txt"]}

    with respx.mock() as mock:
        mock.get(f"{base_url}/files/").mock(
            return_value=httpx.Response(200, json=expected_response))

        async with httpx.AsyncClient() as client:
            response = await list_files(client, base_url)
            assert response == expected_response


@pytest.mark.asyncio
async def test_list_files_http_error():
    with respx.mock() as mock:
        mock.get(f"{base_url}/files/").mock(
            return_value=httpx.Response(400))

        async with httpx.AsyncClient() as client:
            with pytest.raises(Exception) as excinfo:
                await list_files(client, base_url)
            assert "Failed to list files" in str(excinfo.value)


@pytest.mark.asyncio
async def test_delete_file_success():
    filename = "test_delete.txt"
    expected_response = {"message": f"File {filename} deleted successfully."}

    with respx.mock() as mock:
        mock.delete(f"{base_url}/files/{filename}").mock(
            return_value=httpx.Response(200, json=expected_response))

        async with httpx.AsyncClient() as client:
            response = await delete_file(client, base_url, filename)
            assert response == expected_response


@pytest.mark.asyncio
async def test_delete_file_http_error():
    filename = "test_delete.txt"

    with respx.mock() as mock:
        mock.delete(f"{base_url}/files/{filename}").mock(
            return_value=httpx.Response(400))

        async with httpx.AsyncClient() as client:
            with pytest.raises(Exception) as excinfo:
                await delete_file(client, base_url, filename)
            assert "Failed to delete file" in str(excinfo.value)


@pytest.mark.asyncio
async def test_rename_file_success():
    old_filename = "old_name.txt"
    new_filename = "new_name.txt"
    expected_response = {"message": f"File {old_filename} renamed to {new_filename} successfully."}

    with respx.mock() as mock:
        mock.put(f"{base_url}/files/{old_filename}/{new_filename}").mock(
            return_value=httpx.Response(200, json=expected_response))

        async with httpx.AsyncClient() as client:
            response = await rename_file(client, base_url, old_filename, new_filename)
            assert response == expected_response


@pytest.mark.asyncio
async def test_rename_file_http_error():
    old_filename = "old_name.txt"
    new_filename = "new_name.txt"

    with respx.mock() as mock:
        mock.put(f"{base_url}/files/{old_filename}/{new_filename}").mock(
            return_value=httpx.Response(400))

        async with httpx.AsyncClient() as client:
            with pytest.raises(Exception) as excinfo:
                await rename_file(client, base_url, old_filename, new_filename)
            assert "Failed to rename file" in str(excinfo.value)
