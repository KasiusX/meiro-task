import io
import logging

from .file_convertor import get_valid_customers
from ..show_ads.show_ads_facade import ShowAdsFacade
from ..exceptions.ShowAdsException import ShowAdsException
from ..exceptions.ConnectorErrorException import ConnectorErrorException
from ..exceptions.ConnectorInvalidInputException import ConnectorInvalidInputException

show_ads_facade = ShowAdsFacade()
logger = logging.getLogger(__name__) 

def handle_csv_file(csv_file: io.StringIO) -> None:
    logger.info(f"Connector handling CSV file: Testing file")
    valid_customers = get_valid_customers(csv_file)
    if len(valid_customers) == 0:
        logger.error("No valid customers data found")
        raise ConnectorInvalidInputException("No valid customers data found")

    try:
        show_ads_facade.handle_customers_data(valid_customers)
    except ShowAdsException as e:
        raise ConnectorErrorException(str(e))
