import os
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.connector.connector_api import app

client = TestClient(app)

def test_valid_data_file():
    _test_upload("data_100.csv", 200, {"message": "Data send successfully"})
    
def test_invalid_value_file():
    _test_upload("data_invalid_value.csv", 200, {"message": "Data send successfully"})
    
def test_missing_value_file():
    _test_upload("data_missing_value.csv", 200, {"message": "Data send successfully"})
    
def test_empty_file():
    _test_upload("data_empty.csv", 400, {"detail": "No valid customers data found"})
    
def test_non_csv_file():
    _test_upload("data_non_csv.txt", 400, {"detail": "Uploaded file is not a CSV file."})
    
def test_missing_header_file():
    _test_upload("data_missing_header.csv", 400, {"detail": "No valid customers data found"})
    
def _test_upload(file_name: str, expected_status: int, expected_body: dict):
    response = _upload_file(file_name)
    assert response.status_code == expected_status
    assert response.json() == expected_body
    
# should test 500

def _upload_file(file_name: str):
    file_path = os.path.join(os.path.dirname(__file__), "..", "test_files", file_name)
    with patch("src.connector.connector.show_ads_facade.handle_customers_data", return_value=None):
        with open(file_path, "rb") as f:
            return client.post("/upload-csv", files={"file": (file_name, f, "text/csv")})
