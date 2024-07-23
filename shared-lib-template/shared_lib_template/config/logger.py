import logging
import os


def configure_logging():
    """Base logger config"""
    root_logger = logging.getLogger()

    # If logger exists
    if root_logger.handlers:
        return

    log_level = os.getenv("APP_LOG_LEVEL", "INFO")
    root_logger.setLevel(log_level)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] - %(levelname)s - %(process)d - %(name)s:%(lineno)d: %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    containerized = os.getenv("APP_CONTAINERIZED", "false").lower() == "true"
    if not containerized and (log_path := os.getenv("APP_LOG_PATH")):
        os.makedirs(log_path, exist_ok=True)

        file_handler = logging.FileHandler(
            filename=os.path.join(log_path, "app.log"), encoding="utf-8"
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
