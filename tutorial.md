# Using the Hive Agent Client: A Tutorial

This tutorial will guide you through using the `HiveAgentClient`, a Python class designed to interact with a Hive Agent's API. The client facilitates various operations such as sending chat messages and sending data to a Hive Agent.

## Setup

Ensure you have `httpx` installed in your environment:

```bash
pip install httpx
```

Import the `HiveAgentClient` in your Python script:

```python
from hive_agent_client import HiveAgentClient
```

Instantiate the client with the base URL of your Hive Agent API:

```python
base_url = "https://api.example.com"  # Replace with your actual API URL
client = HiveAgentClient(base_url)
```

## Sending Chat Messages

To send a chat message using the `chat` method:

```python
async def send_message(content):
    try:
        response = await client.chat(content)
        print("Chat response:", response)
    except Exception as e:
        print("Error:", e)
```

## Creating a Table

Create a new table in the database:

```python
async def create_new_table(table_name, columns):
    try:
        response = await client.create_table(table_name, columns)
        print("Table creation response:", response)
    except Exception as e:
        print("Error:", e)
```

## Inserting Data

Insert data into a specified table:

```python
async def insert_new_data(table_name, data):
    try:
        response = await client.insert_data(table_name, data)
        print("Data insertion response:", response)
    except Exception as e:
        print("Error:", e)
```

## Read Data

To get data from a table with optional filters:

```python
async def retrieve_data(table_name, filters=None):
    try:
        data = await client.read_data(table_name, filters)
        print("Retrieved data:", data)
    except Exception as e:
        print("Error:", e)
```

## Read Specific Data with Filters

To read specific data, use filters:

```python
async def retrieve_filtered_data(table_name):
    filters = {"id": [1], "name": ["Test"]}
    try:
        data = await client.read_data(table_name, filters)
        print("Filtered data:", data)
    except Exception as e:
        print("Error:", e)
```

## Updating Data

To update existing data in a table:


```python
async def update_existing_data(table_name, row_id, new_data):
    try:
        updated_data = await client.update_data(table_name, row_id, new_data)
        print("Updated data:", updated_data)
    except Exception as e:
        print("Error:", e)
```

## Deleting Data

To delete data from a table:


```python
async def delete_existing_data(table_name, row_id):
    try:
        result = await client.delete_data(table_name, row_id)
        print("Delete result:", result)
    except Exception as e:
        print("Error:", e)
```

## Closing the Client

Finally, ensure you close the client to free up resources:

```python
async def close_client():
    await client.close()
```

## Example Usage

Here is how you might use the client in an asynchronous context:

```python
import asyncio

async def main():
    await send_message("Hello, world!")
    await create_new_table("my_table", {"id": "Integer", "name": "String"})
    await insert_new_data("my_table", {"name": "Test"})
    await retrieve_data("my_table", {"id": [1]})
    await update_existing_data("my_table", 1, {"name": "Updated Test"})
    await delete_existing_data("my_table", 1)
    await close_client()

asyncio.run(main())
```

Replace "my_table", {"id": "Integer", "name": "String"}, and other placeholders with your actual data.

This tutorial provides a basic overview of how to interact with the Hive Agent API using the HiveAgentClient.
