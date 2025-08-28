import re
import logging

from configparser import ConfigParser
from ..config_reader import get_config
from .customer_data import CustomerData

logger = logging.getLogger(__name__)

def is_customer_data_valid(customer_data: CustomerData) -> bool:
    config = get_config()
    if not _is_age_valid(customer_data.age, config):
        logger.warning(f"Customer age was invalid: {customer_data.age}")
        return False
    if not _is_name_valid(customer_data.name):
        logger.warning(f"Customer name was invalid: {customer_data.name}")
        return False
    if not _is_banner_id_valid(customer_data.banner_id, config):
        logger.warning(f"Customer banner_id was invalid: {customer_data.banner_id}")
        return False
    return True

def _is_name_valid(name: str) -> bool:
    return re.fullmatch(r"[A-Za-z0-9 ]+", name)

def _is_age_valid(age: int, config: ConfigParser) -> bool:
    min_age = config.getint("validation", "min_age")
    max_age = config.getint("validation", "max_age")
    return min_age <= age <= max_age

def _is_banner_id_valid(banner_id: int, config: ConfigParser) -> bool:
    min_banner_id = config.getint("validation", "min_banner_id")
    max_banner_id = config.getint("validation", "max_banner_id")
    return min_banner_id <= banner_id <= max_banner_id