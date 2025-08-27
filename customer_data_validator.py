import re

def is_customer_data_valid(customer_data):
    return _is_age_valid(customer_data.age) and _is_name_valid(customer_data.name) and _is_banner_id_valid(customer_data.banner_id)

def _is_name_valid(name):
    return re.fullmatch(r"[A-Za-z0-9 ]+", name)

def _is_age_valid(age):
    min_age = 18
    max_age = 120
    return min_age <= age <= max_age

def _is_banner_id_valid(banner_id):
    return 0 <= banner_id <= 99