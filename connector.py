from logging import getLogger
from file_convertor import get_valid_customers

logger = getLogger(__name__)

def handle_csv_file(csv_file):
    logger.info(f"Handling CSV file: {csv_file}")
    valid_customers = get_valid_customers(csv_file)
    for customer in valid_customers:
        logger.info(f"Valid customer: {customer}")