import os

from dotenv import load_dotenv


env_variables = {
    "APP_MODE": "LOCAL",
    "APP_CONTAINERIZED": "false",
    "APP_LOG_LEVEL": "DEBUG",
    "APP_HTTPX_LOG_LEVEL": "WARNING",
    "APP_HTTPCORE_LOG_LEVEL": "WARNING",
    "APP_OPENAI_LOG_LEVEL": "WARNING",
    "APP_LOG_PATH": "logs",
    "WHATSAPP_WEBHOOK_TOKEN": "test",
    "WHATSAPP_API_TOKEN": "test",
    "APP_TOKEN": "test",
    "WHATSAPP_VALIDATE_SIGNATURE": "False",
}


def apply_local_env():
    load_dotenv()

    for var_key, var_val in env_variables.items():
        if os.getenv(var_key) is None:
            os.environ[var_key] = str(var_val)
