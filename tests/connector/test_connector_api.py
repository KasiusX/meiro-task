import os
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.connector.connector_api import app
from src.exceptions.ConnectorErrorException import ConnectorErrorException
from src.exceptions.ConnectorInvalidInputException import ConnectorInvalidInputException

client = TestClient(app)

def test_valid_data_file():
    _test_upload("data_100.csv", 200, {"message": "Data send successfully"})
    
def test_non_csv_file():
    _test_upload("data_non_csv.txt", 400, {"detail": "Uploaded file is not a CSV file."})
    
def test_handle_connctor_error_exception():
    with patch("src.connector.connector_api.handle_csv_file", side_effect=ConnectorErrorException("Connector error")):
        _test_upload("data_100.csv", 500, {"detail": "Connector error"})
        
def test_handle_connctor_invalid_input_exception():
    with patch("src.connector.connector_api.handle_csv_file", side_effect=ConnectorInvalidInputException("Invalid input")):
        _test_upload("data_100.csv", 400, {"detail": "Invalid input"})
    
def _test_upload(file_name: str, expected_status: int, expected_body: dict):
    response = _upload_file(file_name)
    assert response.status_code == expected_status
    assert response.json() == expected_body

def _upload_file(file_name: str):
    file_path = os.path.join(os.path.dirname(__file__), "..", "test_files", file_name)
    with patch("src.connector.connector.show_ads_facade.handle_customers_data", return_value=None):
        with open(file_path, "rb") as f:
            return client.post("/upload-csv", files={"file": (file_name, f, "text/csv")})
