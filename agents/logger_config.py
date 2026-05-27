import logging
import os


# BASE DIRECTORY


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# LOG DIRECTORY


LOG_DIR = os.path.join(
    BASE_DIR,
    "..",
    "logs"
)

os.makedirs(
    LOG_DIR,
    exist_ok=True
)

# LOG FILE PATH


LOG_FILE = os.path.join(
    LOG_DIR,
    "system.log"
)

# CREATE LOGGER


logger = logging.getLogger("walmart_ai_logger")

logger.setLevel(logging.INFO)

# PREVENT DUPLICATE HANDLERS

if not logger.handlers:

    # FILE HANDLER

    file_handler = logging.FileHandler(

        LOG_FILE,

        encoding="utf-8"
    )

    file_handler.setLevel(logging.INFO)

    # FORMATTER

    formatter = logging.Formatter(

        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(formatter)

    # ADD HANDLER


    logger.addHandler(file_handler)

print(f"\n Logging Active: {LOG_FILE}")