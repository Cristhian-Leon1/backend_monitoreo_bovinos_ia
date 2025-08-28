from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Configuración de Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    
    # Configuración de la aplicación
    app_name: str = "Monitoreo Bovinos IA Backend"
    app_version: str = "1.0.0"
    debug: bool = True
    secret_key: str
    
    # Configuración del servidor
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Configuración de CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Configuración del bucket
    bucket_name: str = "monitoreo_bovinos_IA"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Instancia global de configuración
settings = Settings()
