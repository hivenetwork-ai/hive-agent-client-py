from setuptools import setup, find_packages

setup(
    name="hive-agent-client",
    version="0.0.1",
    packages=find_packages(include=["hive_agent_client", "hive_agent_client.*"]),
    install_requires=["httpx==0.27.0"],
    description="A client library for sending messages to a Hive Agent",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
