import io
import csv
import logging

from ..model.customer_data import CustomerData
from ..model.customer_data_validator import CustomerDataValidator

logger = logging.getLogger(__name__)

def get_valid_customers(file: io.StringIO) -> list[CustomerData]:
    logger.info("Retrieving valid customers from CSV file")
    reader = csv.DictReader(file)
    valid_customers = []
    customer_data_validator = CustomerDataValidator()
    for row in reader:
        customer_data = None
        try:
            customer_data = CustomerData(row["Name"], row["Age"], row["Cookie"], row["Banner_id"]) 
        except KeyError as e:
            logger.error(f"CSV file is missing required columns: {e}")
            return []
        except (TypeError, ValueError) as e:
            logger.error(f"Failed to convert customer row {row}, has invalid data types: {e}")
            continue
            
        if(customer_data_validator.is_customer_data_valid(customer_data)):
            valid_customers.append(customer_data)
        else:
            logger.warning(f"Customer data was invalid: {customer_data}")
    return valid_customers