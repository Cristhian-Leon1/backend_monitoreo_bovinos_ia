from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import uuid

class PerfilBase(BaseModel):
    nombre_completo: Optional[str] = None
    imagen_perfil: Optional[str] = None

class PerfilCreate(PerfilBase):
    pass

class PerfilUpdate(PerfilBase):
    pass

class PerfilResponse(PerfilBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    nombre_completo: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    created_at: datetime
    perfil: Optional[PerfilResponse] = None
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: str
    user: UserResponse
