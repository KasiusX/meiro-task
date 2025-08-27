from logging import getLogger
from file_convertor import get_valid_customers
from show_ads_facade import ShowAdsFacade

logger = getLogger(__name__)
show_ads_facade = ShowAdsFacade()

def handle_csv_file(csv_file):
    logger.info(f"Handling CSV file: {csv_file}")
    valid_customers = get_valid_customers(csv_file)
    show_ads_facade.handle_custommers_data(valid_customers)
