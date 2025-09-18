from pydantic import BaseModel, Field
from typing import Optional

class ProfileImageUploadRequest(BaseModel):
    """Modelo para subir imagen de perfil en base64"""
    image_base64: str = Field(..., description="Imagen codificada en base64")
    file_name: Optional[str] = Field(None, description="Nombre del archivo (opcional)")

class ProfileImageUploadResponse(BaseModel):
    """Respuesta de subida de imagen de perfil"""
    url: str
    public_url: str
    file_name: str
    profile_updated: bool
