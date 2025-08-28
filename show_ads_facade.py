import time
import requests
import logging
from customer_data import CustomerData
from exceptions.ShowAdsException import ShowAdsException
from connector_config import get_config

AUTH_BODY = {
    "ProjectKey" : "Meiro"
}

logger = logging.getLogger(__name__)


class ShowAdsFacade:
    def __init__(self):
        self.access_token = None
        
    def load_config(self):
        config = get_config()
        self.number_of_retries = config.getint("show_ads","retries")
        self.auth_url = config.get("show_ads","auth_url")
        self.show_bulk_url = config.get("show_ads","show_bulk_url")
        self.batch_size = config.getint("show_ads","batch_size")
        logger.info("Successfully loaded show ads config")

    def handle_customers_data(self, customers: list[CustomerData]) -> None:
        logger.info(f"Handeling customers of size: {len(customers)}") 

        self.load_config()
        if self.access_token is None:
            self.update_access_token()

        batch_number = 0
        failed_batches = []
        for i in range(0, len(customers), self.batch_size):
            customers_batch = customers[i:i + self.batch_size]
            batch_number += 1
            try:
                self.post_customers_data(customers_batch, batch_number)
            except ShowAdsException as e:
                logger.error(f"Failed to send batch {batch_number} with error: {e}")
                failed_batches.append(batch_number)

        if len(failed_batches) != 0:
            raise ShowAdsException(f"Failed to send batches: {failed_batches}")

    def post_customers_data(self, customers: list[CustomerData], batch_number: int, try_count: int = 1) -> None:
        logger.info(f"Sending batch {batch_number} of size: {len(customers)}, try: {try_count}")
        headers = self.create_authorization_header()
        body = self.create_show_bulk_body(customers)

        response = requests.post(self.show_bulk_url, headers=headers, json=body)

        match response.status_code:
            case 200:
                logger.info(f"Batch {batch_number} sent successfully")
            case 400:
                logger.error(f"Failed to send batch {batch_number}, bad request: {response.content}")
            case 401:
                if(try_count > self.number_of_retries):
                    raise ShowAdsException(f"Failed to send batch {batch_number} after {self.number_of_retries} retries, access token issue")
                logger.info("Access token expired, fetching a new one")
                self.update_access_token()
                self.post_customers_data(customers, batch_number, 1 + try_count)
            case 429:
                if(try_count >= self.number_of_retries):
                    raise ShowAdsException(f"Failed to send batch {batch_number} after {self.number_of_retries} retries, rate limit issue")
                logger.info("Rate limit exceeded, waiting 1 second and retrying")
                time.sleep(1)
                self.post_customers_data(customers, batch_number, 1 + try_count)
            case 500:
                if(try_count >= self.number_of_retries):
                    raise ShowAdsException(f"Failed to send batch {batch_number} after {self.number_of_retries} retries, server issue")
                logger.warning(f"Failed to send batch {batch_number}, server error: {response.content}, waiting 1 second and retrying")
                time.sleep(1)
                self.post_customers_data(customers, batch_number, 1 + try_count)
            case _:
                logger.error(f"Failed to send batch {batch_number}, unexpected status code: {response.status_code} and error: {response.content}")


    def update_access_token(self, try_count: int=1) -> None:
        response = requests.post(self.auth_url, json=AUTH_BODY)

        match response.status_code:
            case 200:
                self.access_token = response.json().get("AccessToken")
                logger.info(f"Fetched new access token {self.access_token}")
                return
            case 400:
                logger.error(f"Failed to retreive access token, bad request: {response.content}")
            case 429:
                if(try_count >= self.number_of_retries):
                    raise ShowAdsException(f"Failed to retreive access token after {self.number_of_retries} retries, rate limit issue")
                logger.info("Rate limit exceeded, waiting 1 second and retrying")
                self.update_access_token(1 + try_count)
            case 500:
                logger.error(f"Failed to retreive access token, server error: {response.content}")
                if(try_count >= self.number_of_retries):
                    raise ShowAdsException(f"Failed to retreive access token after {self.number_of_retries} retries, server issue")
                logger.warning(f"Failed to retreive, server error: {response.content}, waiting 1 second and retrying")
                time.sleep(1)
                self.update_access_token(1 + try_count)
            case _:
                logger.error(f"Failed to retreive access token, unexpected status code: {response.status_code} and error: {response.content}")
        raise ShowAdsException("Failed to retreive access token")

        
    def create_show_bulk_body(self, customers: list[CustomerData]) -> dict:
        body = {
            "Data": [
                {
                    "VisitorCookie": c.cookie,
                    "BannerId": c.banner_id
                }
                for c in customers
            ]
        }
        return body
    
    def create_authorization_header(self) -> dict:
        return {
            "Authorization" : f"Bearer {self.access_token}"
        }