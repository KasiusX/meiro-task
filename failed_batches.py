import json
import logging

logger = logging.getLogger(__name__)

def save_failed_batch(batch: dict) -> None:
    with open("failed_batches.txt", "a") as f:
        f.write(json.dumps(batch) + "\n")
    logger.info("Saved failed batch into failed_batches.txt")