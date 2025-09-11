from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
import uuid
import json

class MedicionBase(BaseModel):
    fecha: date
    altura_cm: Optional[Decimal] = Field(None, ge=0, max_digits=6, decimal_places=2)
    l_torso_cm: Optional[Decimal] = Field(None, ge=0, max_digits=6, decimal_places=2)
    l_oblicua_cm: Optional[Decimal] = Field(None, ge=0, max_digits=6, decimal_places=2)
    l_cadera_cm: Optional[Decimal] = Field(None, ge=0, max_digits=6, decimal_places=2)
    a_cadera_cm: Optional[Decimal] = Field(None, ge=0, max_digits=6, decimal_places=2)
    edad_meses: Optional[int] = Field(None, ge=0)
    peso_bascula_kg: Optional[Decimal] = Field(None, ge=0, max_digits=6, decimal_places=2)

class MedicionCreate(MedicionBase):
    bovino_id: uuid.UUID

class MedicionUpdate(BaseModel):
    fecha: Optional[date] = None
    altura_cm: Optional[Decimal] = Field(None, ge=0, max_digits=6, decimal_places=2)
    l_torso_cm: Optional[Decimal] = Field(None, ge=0, max_digits=6, decimal_places=2)
    l_oblicua_cm: Optional[Decimal] = Field(None, ge=0, max_digits=6, decimal_places=2)
    l_cadera_cm: Optional[Decimal] = Field(None, ge=0, max_digits=6, decimal_places=2)
    a_cadera_cm: Optional[Decimal] = Field(None, ge=0, max_digits=6, decimal_places=2)
    edad_meses: Optional[int] = Field(None, ge=0)
    peso_bascula_kg: Optional[Decimal] = Field(None, ge=0, max_digits=6, decimal_places=2)

class MedicionResponse(MedicionBase):
    id: uuid.UUID
    bovino_id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
        # Agregar configuración para manejar Decimals
        json_encoders = {
            Decimal: lambda v: float(v) if v is not None else None,
            datetime: lambda v: v.isoformat() if v is not None else None,
            date: lambda v: v.isoformat() if v is not None else None,
            uuid.UUID: lambda v: str(v) if v is not None else None,
        }