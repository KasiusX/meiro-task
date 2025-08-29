import re
import logging

from ..config_reader import get_config
from .customer_data import CustomerData

logger = logging.getLogger(__name__)

class CustomerDataValidator:
    def __init__(self):
        self.config = get_config()

    def is_customer_data_valid(self, customer_data: CustomerData) -> bool:
        if not self._is_age_valid(customer_data.age):
            logger.warning(f"Customer age was invalid: {customer_data.age}")
            return False
        if not self._is_name_valid(customer_data.name):
            logger.warning(f"Customer name was invalid: {customer_data.name}")
            return False
        if not self._is_banner_id_valid(customer_data.banner_id):
            logger.warning(f"Customer banner_id was invalid: {customer_data.banner_id}")
            return False
        return True

    def _is_name_valid(self, name: str) -> bool:
        return re.fullmatch(r"[A-Za-z0-9 ]+", name)

    def _is_age_valid(self, age: int) -> bool:
        min_age = self.config.getint("validation", "min_age")
        max_age = self.config.getint("validation", "max_age")
        return min_age <= age <= max_age

    def _is_banner_id_valid(self, banner_id: int) -> bool:
        min_banner_id = self.config.getint("validation", "min_banner_id")
        max_banner_id = self.config.getint("validation", "max_banner_id")
        return min_banner_id <= banner_id <= max_banner_id