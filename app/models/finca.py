from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
import uuid

class FincaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)

class FincaCreate(FincaBase):
    pass

class FincaUpdate(FincaBase):
    pass

class FincaResponse(FincaBase):
    id: uuid.UUID
    propietario_id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

# Modelo simplificado para evitar referencias circulares por ahora
class FincaWithBovinos(FincaResponse):
    bovinos: List[dict] = []
