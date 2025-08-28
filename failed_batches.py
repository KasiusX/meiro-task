import json
import logging

from datetime import datetime
import os
from connector_config import get_config


logger = logging.getLogger(__name__)

def save_failed_batch(batch: dict, batch_number: int) -> None:
    config = get_config()
    directory = config.get("failed_batches", "save_directory")
    os.makedirs(directory, exist_ok=True)

    filename = get_filename(batch_number)
    file_path = os.path.join(directory, filename)
    
    
    with open(file_path, "a") as f:
        f.write(json.dumps(batch) + "\n")

    logger.info(f"Saved failed batch into {file_path}")
    
def get_filename(batch_number: int) -> str:
    datetime_string = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{datetime_string}-batch-{batch_number}.json"