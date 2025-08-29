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
    debug: bool = False  # Cambiar a False para producción
    secret_key: str
    
    # Configuración del servidor
    host: str = "0.0.0.0"
    port: int = int(os.getenv("PORT", 8000))  # Usar PORT de Render
    
    # Configuración de CORS - Agregar dominio de Render
    cors_origins: List[str] = [
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://*.onrender.com",  # Permitir dominios de Render
        "https://monitoreo-bovinos-ia.onrender.com"  # Tu dominio específico
    ]
    
    # Configuración del bucket
    bucket_name: str = "monitoreo_bovinos_IA"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Instancia global de configuración
settings = Settings()
