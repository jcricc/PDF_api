from fastapi import HTTPException, Header, Request
from google.cloud import storage
from google.oauth2 import service_account
import os
import asyncio

# Load environment variables
GCP_SERVICE_ACCOUNT_FILE = os.getenv('GCP_SERVICE_ACCOUNT_FILE')
GCP_BUCKET_NAME = os.getenv('GCP_BUCKET_NAME')

if not GCP_SERVICE_ACCOUNT_FILE:
    raise ValueError("GCP_SERVICE_ACCOUNT_FILE environment variable is not set")
if not GCP_BUCKET_NAME:
    raise ValueError("GCP_BUCKET_NAME environment variable is not set")

# Initialize Google Cloud Storage Client
credentials = service_account.Credentials.from_service_account_file(GCP_SERVICE_ACCOUNT_FILE)
gcp_storage_client = storage.Client(credentials=credentials, project=credentials.project_id)

async def write_data_to_gcs(filename: str, data: str) -> str:
    """
    Writes data to a specified file in Google Cloud Storage asynchronously and returns the file's URL.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _write_data_to_gcs_sync, filename, data)

def _write_data_to_gcs_sync(filename: str, data: str) -> str:
    try:
        bucket = gcp_storage_client.bucket(GCP_BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(data)
        return f"https://storage.googleapis.com/{GCP_BUCKET_NAME}/{filename}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing data to GCS: {str(e)}")

async def read_data_from_gcs(filename: str) -> str:
    """
    Reads data from a specified file in Google Cloud Storage asynchronously.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _read_data_from_gcs_sync, filename)

def _read_data_from_gcs_sync(filename: str) -> str:
    try:
        bucket = gcp_storage_client.bucket(GCP_BUCKET_NAME)
        blob = bucket.get_blob(filename)
        if blob:
            return blob.download_as_text()
        else:
            raise HTTPException(status_code=404, detail=f"File {filename} not found in GCS.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading data from GCS: {str(e)}")

async def verify_token(token: str = Header(...)):
    """
    Async dependency to verify access tokens. Implement your token validation logic here.
    """
    # Placeholder for demonstration; replace with your token validation logic.
    if token != "expected_token":
        raise HTTPException(status_code=401, detail="Invalid access token")
    return token

async def get_query_validator(request: Request) -> str:
    """
    Validates and manipulates query parameters asynchronously.
    """
    query_param = request.query_params.get('q', '').strip()
    if not query_param:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is missing or empty")
    return query_param
