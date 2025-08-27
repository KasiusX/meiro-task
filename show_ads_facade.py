import json
import requests

from logging_config import getLogger

BASE_URL = "https://golang-assignment-968918017632.europe-west3.run.app"
AUTH_URL = f"{BASE_URL}/auth"
SHOW_BULK_URL = f"{BASE_URL}/banners/show/bulk"

AUTH_BODY = {
    "ProjectKey" : "Meiro"
}

BATCH_SIZE = 1000
logger = getLogger(__name__)


class ShowAdsFacade:
    def __init__(self):
        self.access_token = None

    def handle_custommers_data(self, customers):
        logger.info(f"Handeling customers of size: {len(customers)}") 
        
        if self.access_token is None:
            self.access_token = self.get_access_token()
            logger.info(f"Fetched new access token {self.access_token}")
            
        for i in range(0, len(customers), BATCH_SIZE):
            customers_batch = customers[i:i + BATCH_SIZE]
            self.post_customers_data(customers_batch)
        
    def post_customers_data(self, customers):
        logger.info(f"Handeling batch of size: {len(customers)}")
        
        headers = self.create_authorization_header()
        body = self.create_show_bulk_body(customers)

        response = requests.post(SHOW_BULK_URL, headers=headers, json=body)
        logger.info(f"Batch ended with: {response.status_code} and response: {response.content}")
            
    def get_access_token(self):
        response = requests.post(AUTH_URL, json=AUTH_BODY)
        if response.status_code == 200:
            return response.json().get("AccessToken")
        
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