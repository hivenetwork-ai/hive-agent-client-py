# hive-agent-client-py
Client library to interact with Hive Agents.

## Project Requirements

- Python 3.6 or higher

## Setup

To use the `HiveAgentClient` library, you first need to ensure that you have Python installed on your system and then install the required dependencies.

1. **Install Poetry**

    If you don't have Poetry installed, you can install it using the following commands:
    `$ curl -sSL https://install.python-poetry.org | python3 -`
    `$ export PATH="$HOME/.local/bin:$PATH"`

2. **Activate the Virtual Environment**
    Activate the virtual environment created by Poetry with the following command:
    `$ poetry shell`

3. **Install Dependencies**

    `$ poetry install --no-root`


## Usage

To use the `HiveAgentClient` library in your project, you need to import the `HiveAgentClient` class from the library and then create an instance of the class with the appropriate configuration.

```python
from hive_agent_client import HiveAgentClient

# initialize the client with the base URL of your Hive Agent's chat API
client = HiveAgentClient(base_url="http://localhost:8000", timeout=30)

# send a message and receive the response
try:
    response = client.chat("Hello, Hive Agent!")
    print(response)
except Exception as e:
    print(f"an error occurred: {e}")
```

### Tutorial
The complete tutorial can be found at [./tutorial.md](./tutorial.md).


## Learn More

https://hivenetwork.ai
