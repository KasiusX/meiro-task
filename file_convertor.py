import io
import csv
import logging
from customer_data import CustomerData
from customer_data_validator import is_customer_data_valid

logger = logging.getLogger(__name__)

def get_valid_customers(file: io.StringIO) -> list[CustomerData]:
    reader = csv.DictReader(file)
    valid_customers = []
    for row in reader:
        customer_data = CustomerData(row["Name"], row["Age"], row["Cookie"], row["Banner_id"]) 
        if(is_customer_data_valid(customer_data)):
            valid_customers.append(customer_data)
        else:
            logger.warning(f"Customer data was invalid: {customer_data}")
    return valid_customers