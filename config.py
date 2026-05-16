"""
Configuration management for DevAssist API
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration
    app_name: str = "DevAssist"
    gemini_api_key: str= "AIzaSyAVNIc85mtqQOmm9tXUO_KlyUkC1xWD27U"

    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Security
    api_keys: str = "dev-key-123,test-key-456"
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:8080"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @property
    def api_keys_list(self) -> List[str]:
        """Parse comma-separated API keys into a list"""
        return [key.strip() for key in self.api_keys.split(",") if key.strip()]
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse comma-separated CORS origins into a list"""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


# Global settings instance
settings = Settings()

# Made with Bob
