from google.cloud import storage
from google.oauth2 import service_account
import json

def upload_to_gcs(file_path: str, file_name: str) -> str:
    # Use your Google Cloud credentials
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(open('your-service-account.json', 'r').read()),
    )
    client = storage.Client(credentials=credentials)
    bucket = client.get_bucket('your-bucket-name')
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_path)
    return blob.public_url
