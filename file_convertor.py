import csv
from logging_config import getLogger
from customer_data import CustomerData
from customer_data_validator import is_customer_data_valid

logger = getLogger(__name__)

def get_valid_customers(file):
    reader = csv.reader(file)
    next(reader)
    valid_customers = []
    for row in reader:
        customer_data = CustomerData(row[0], row[1], row[2], row[3])
        if(is_customer_data_valid(customer_data)):
            valid_customers.append(customer_data)
        else:
            logger.warning(f"Customer data was invalid: {customer_data}")
    return valid_customers