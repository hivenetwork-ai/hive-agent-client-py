# Using the Hive Agent Client: A Tutorial

This tutorial will guide you through using the `HiveAgentClient`, a Python class designed to interact with a Hive Agent's API. The client facilitates various operations such as sending chat messages, managing entries, and streaming data.

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

## Creating an Entry

Create a new entry in a specified namespace:

```python
async def create_new_entry(namespace, data):
    try:
        entry = await client.create_entry(namespace, data)
        print("Created entry:", entry)
    except Exception as e:
        print("Error:", e)
```

## Streaming Entry Data

To stream data to an entry, use the `stream_entry_data` method. Ensure your data source is an asynchronous generator:

```python
async def stream_data(namespace, data_stream):
    try:
        async for message in client.stream_entry_data(namespace, data_stream):
            print("Stream response:", message)
    except Exception as e:
        print("Error:", e)
```

## Retrieving Entries

To get all entries from a namespace:

```python
async def retrieve_entries(namespace):
    try:
        entries = await client.get_entries(namespace)
        print("Entries:", entries)
    except Exception as e:
        print("Error:", e)
```

## Retrieving a Specific Entry

To retrieve a specific entry by ID:

```python
async def retrieve_entry_by_id(namespace, entry_id):
    try:
        entry = await client.get_entry_by_id(namespace, entry_id)
        print("Entry:", entry)
    except Exception as e:
        print("Error:", e)
```

## Updating an Entry

To update an existing entry:

```python
async def update_existing_entry(namespace, entry_id, data):
    try:
        updated_entry = await client.update_entry(namespace, entry_id, data)
        print("Updated entry:", updated_entry)
    except Exception as e:
        print("Error:", e)
```

## Deleting an Entry

To delete an entry:

```python
async def delete_existing_entry(namespace, entry_id):
    try:
        result = await client.delete_entry(namespace, entry_id)
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
    await create_new_entry("my_namespace", {"key": "value"})
    await retrieve_entries("my_namespace")
    await retrieve_entry_by_id("my_namespace", "entry_id")
    await update_existing_entry("my_namespace", "entry_id", {"key": "new value"})
    await delete_existing_entry("my_namespace", "entry_id")
    await close_client()

asyncio.run(main())
```

Replace `"my_namespace"`, `"entry_id"`, and other placeholders with your actual data.

This tutorial provides a basic overview of how to interact with the Hive Agent API using the `HiveAgentClient`. Adapt the examples to fit your application's requirements.
