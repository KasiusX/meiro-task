import configparser

def get_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read('connector_config.ini')
    return config