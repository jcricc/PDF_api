# c:/Users/jritc/Downloads/OctInk/octinkapi/src/tests/test_api/test_dependencies.py
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.dependencies import write_data_to_gcs, read_data_from_gcs

async def test_write_and_read_data_from_gcs():
    url = await write_data_to_gcs("test.txt", "Test Data")
    data = await read_data_from_gcs(url)
    assert data == "Test Data"

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
    try:
        read_data_from_gcs("test.txt")
    except HTTPException as exc_info:
        read_data_from_gcs("test.txt")
    assert "File test.txt not found in GCS" in str(exc_info.value.detail)

@patch("app.dependencies.gcp_storage_client")
def test_write_data_to_gcs(mock_gcp_storage_client):
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_bucket.blob.return_value = mock_blob
    mock_gcp_storage_client.bucket.return_value = mock_bucket


