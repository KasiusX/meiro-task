import requests
from exceptions.ShowAdsException import ShowAdsException

from logging_config import getLogger

BASE_URL = "https://golang-assignment-968918017632.europe-west3.run.app"
AUTH_URL = f"{BASE_URL}/auth"
SHOW_BULK_URL = f"{BASE_URL}/banners/show/bulk"

AUTH_BODY = {
    "ProjectKey" : "Meiro"
}

BATCH_SIZE = 10
logger = getLogger(__name__)


class ShowAdsFacade:
    def __init__(self):
        self.access_token = None

    def handle_customers_data(self, customers):
        logger.info(f"Handeling customers of size: {len(customers)}") 
        if self.access_token is None:
            self.update_access_token()
            
        batch_number = 0
        for i in range(0, len(customers), BATCH_SIZE):
            customers_batch = customers[i:i + BATCH_SIZE]
            batch_number += 1
            self.post_customers_data(customers_batch, batch_number)
        
    def post_customers_data(self, customers, batch_number, try_count=0):
        logger.info(f"Sending batch {batch_number} of size: {len(customers)}")
        headers = self.create_authorization_header()
        body = self.create_show_bulk_body(customers)

        response = requests.post(SHOW_BULK_URL, headers=headers, json=body)
        
        match response.status_code:
            case 200:
                logger.info(f"Batch {batch_number} sent successfully")
                return
            case 400:
                logger.error(f"Failed to send batch {batch_number}, bad request: {response.content}")
            case 401:
                if(try_count >= 3):
                    raise ShowAdsException(f"Failed to send batch {batch_number} after 3 retries, access token issue")
                logger.info("Access token expired, fetching a new one")
                self.update_access_token()
                self.post_customers_data(customers, 1+ try_count)
            case 500:
                logger.error(f"Failed to send batch {batch_number}, server error: {response.content}")
            case _:
                logger.error(f"Failed to send batch {batch_number}, unexpected status code: {response.status_code} and error: {response.content}")
        
            
    def update_access_token(self):
        response = requests.post(AUTH_URL, json=AUTH_BODY)

        match response.status_code:
            case 200:
                self.access_token = response.json().get("AccessToken")
                logger.info(f"Fetched new access token {self.access_token}")
                return
            case 400:
                logger.error(f"Failed to retreive access token, bad request: {response.content}")
            case 500:
                logger.error(f"Failed to retreive access token, server error: {response.content}")
            case _:
                logger.error(f"Failed to retreive access token, unexpected status code: {response.status_code} and error: {response.content}")
        raise ShowAdsException("Failed to retreive access token")

        
    def create_show_bulk_body(self, customers):
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
    
    def create_authorization_header(self):
        return {
            "Authorization" : f"Bearer {self.access_token}"
        }