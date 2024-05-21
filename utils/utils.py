def get_log_level():
    HIVE_AGENT_LOG_LEVEL = os.getenv('HIVE_AGENT_LOG_LEVEL', 'INFO').upper() # Check for env variable on the server and default to INFO if none is provided
    return getattr(logging, HIVE_AGENT_LOG_LEVEL, logging.INFO)