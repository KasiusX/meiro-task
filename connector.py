from logging import getLogger
from show_ads_facade import ShowAdsFacade
from file_convertor import get_valid_customers
from exceptions.ShowAdsException import ShowAdsException
from exceptions.ConnectorException import ConnectorException


logger = getLogger(__name__)
show_ads_facade = ShowAdsFacade()

def handle_csv_file(csv_file):
    logger.info(f"Handling CSV file: {csv_file}")
    valid_customers = get_valid_customers(csv_file)
    try:
        show_ads_facade.handle_customers_data(valid_customers)
    except ShowAdsException as e:
        raise ConnectorException(str(e))
