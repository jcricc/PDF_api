from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "OctInk"
    GOOGLE_APPLICATION_CREDENTIALS="C:\Users\jritc\Downloads\OctInk\octink-64f9c59ad601.json"

    class Config:
        env_file = ".env"

settings = Settings()