from fastapi.testclient import TestClient, HTTPException
from app.main import app  # Adjust according to your project structure
from app.dependencies import read_data_from_gcs, write_data_to_gcs  # Adjust import paths as necessary
from unittest.mock import patch, MagicMock
import os
import pytest

client = TestClient(app)

@patch("app.dependencies.gcp_storage_client")
def test_read_data_from_gcs(mock_gcp_storage_client):
    mock_blob = MagicMock()
    mock_blob.download_as_text.return_value = "Test Data"
    mock_bucket = MagicMock()
    mock_bucket.get_blob.return_value = mock_blob
    mock_gcp_storage_client.bucket.return_value = mock_bucket

    data = read_data_from_gcs("test.txt")
    assert data == "Test Data"

    mock_bucket.get_blob.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        read_data_from_gcs("test.txt")
    assert "File test.txt not found in GCS" in str(exc_info.value.detail)

@patch("app.dependencies.gcp_storage_client")
def test_write_data_to_gcs(mock_gcp_storage_client):
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_bucket.blob.return_value = mock_blob
    mock_gcp_storage_client.bucket.return_value = mock_bucket

    expected_bucket_name = os.getenv('GCP_BUCKET_NAME')
    url = write_data_to_gcs("test.txt", "Test Data")
    assert url == f"https://storage.googleapis.com/{expected_bucket_name}/test.txt"
