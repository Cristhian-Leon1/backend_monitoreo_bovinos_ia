from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
import uuid

class BovinoBase(BaseModel):
    id_bovino: str = Field(..., min_length=1, max_length=50)
    sexo: Optional[str] = Field(None, pattern="^[MH]$")
    raza: Optional[str] = Field(None, max_length=100)

class BovinoCreate(BovinoBase):
    finca_id: uuid.UUID

class BovinoUpdate(BaseModel):
    id_bovino: Optional[str] = Field(None, min_length=1, max_length=50)
    sexo: Optional[str] = Field(None, pattern="^[MH]$")
    raza: Optional[str] = Field(None, max_length=100)

class BovinoResponse(BovinoBase):
    id: uuid.UUID
    finca_id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class BovinoWithMediciones(BovinoResponse):
    mediciones: List[dict] = []
