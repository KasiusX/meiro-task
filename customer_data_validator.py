import logging
import re
from customer_data import CustomerData
from connector_config import get_config

def is_customer_data_valid(customer_data: CustomerData) -> bool:
    return _is_age_valid(customer_data.age) and _is_name_valid(customer_data.name) and _is_banner_id_valid(customer_data.banner_id)

def _is_name_valid(name: str) -> bool:
    return re.fullmatch(r"[A-Za-z0-9 ]+", name)

def _is_age_valid(age: int) -> bool:
    config = get_config()
    min_age = config.getint("validation", "min_age", fallback=18)
    max_age = config.getint("validation", "max_age", fallback=120)
    return min_age <= age <= max_age

def _is_banner_id_valid(banner_id: int) -> bool:
    return 0 <= banner_id <= 99