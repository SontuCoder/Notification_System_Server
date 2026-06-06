# import logging


# from app.core.config import settings

# logging.basicConfig(
#     level=settings.LOG_LEVEL,
#     format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
# )

# logger = logging.getLogger("notification-service")

import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("notification-service")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=10_000_000,
    backupCount=5
)

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)