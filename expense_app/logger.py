import logging
from pathlib import Path


LOG_FILE = "expense_tracker.log"

logger = logging.getLogger("expense_tracker")
logger.setLevel(logging.INFO)
logger.propagate = False

log_path = Path(LOG_FILE).resolve()
if not any(
    isinstance(handler, logging.FileHandler)
    and Path(handler.baseFilename) == log_path
    for handler in logger.handlers
):
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    )
    logger.addHandler(file_handler)

logger.info("Application started")
