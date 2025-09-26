from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime
from decimal import Decimal
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

class BovinoWithLastMedicion(BaseModel):
    """Bovino con su última medición"""
    model_config = ConfigDict(from_attributes=True)
    
    id: str  # Cambiado a str para coincidir con BovinoResponse
    id_bovino: str
    sexo: Optional[str] = None
    raza: Optional[str] = None
    finca_id: str  # Cambiado a str para coincidir con BovinoResponse
    created_at: datetime
    
    # Última medición
    ultima_medicion: Optional[dict] = None

class FincaWithBovinosAndMediciones(BaseModel):
    """Finca completa con bovinos y sus últimas mediciones"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    nombre: str
    propietario_id: uuid.UUID
    created_at: datetime
    
    # Bovinos con sus últimas mediciones
    bovinos: List[BovinoWithLastMedicion] = []
    
    # Estadísticas adicionales
    total_bovinos: int = 0
    bovinos_con_mediciones_recientes: int = 0
