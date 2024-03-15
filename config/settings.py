from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "OctInk"
    google_cloud_credentials: str = "C:\Users\jritc\Downloads\OctInk\octink-64f9c59ad601.json"

    class Config:
        env_file = ".env"

settings = Settings()