from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración de la aplicación usando variables de entorno"""
    
    # Chatwoot
    chatwoot_api_key: str
    chatwoot_base_url: str
    
    # Google Cloud
    google_application_credentials: str
    gcp_project_id: str
    bigquery_dataset: str
    bigquery_table: str
    
    # Gemini
    gemini_api_key: str
    
    # Speech-to-Text
    stt_provider: str = "google"  # "google" o "openai"
    openai_api_key: str | None = None
    
    # Dashboard
    dashboard_url: str
    
    # Server
    port: int = 8000
    host: str = "0.0.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Obtiene la configuración (singleton)"""
    return Settings()
