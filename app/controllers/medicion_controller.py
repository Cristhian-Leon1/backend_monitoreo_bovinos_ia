from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.models.medicion import MedicionCreate, MedicionUpdate, MedicionResponse
from app.services.medicion_service import medicion_service
from app.middleware.auth import get_current_user_id
from typing import List, Optional
from datetime import date
import uuid

router = APIRouter(prefix="/mediciones", tags=["Mediciones"])

@router.post("/", response_model=MedicionResponse, status_code=status.HTTP_201_CREATED)
async def create_medicion(
    medicion_data: MedicionCreate,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Crea una nueva medición para un bovino del usuario actual
    """
    try:
        medicion = await medicion_service.create_medicion(medicion_data, current_user_id)
        return medicion
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/bovino/{bovino_id}", response_model=List[MedicionResponse])
async def get_mediciones_by_bovino(
    bovino_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene todas las mediciones de un bovino específico
    """
    try:
        mediciones = await medicion_service.get_mediciones_by_bovino(bovino_id, current_user_id)
        return mediciones
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{medicion_id}", response_model=MedicionResponse)
async def get_medicion_by_id(
    medicion_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene una medición específica del usuario actual
    """
    try:
        medicion = await medicion_service.get_medicion_by_id(medicion_id, current_user_id)
        
        if not medicion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medición no encontrada"
            )
        
        return medicion
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{medicion_id}", response_model=MedicionResponse)
async def update_medicion(
    medicion_id: str,
    medicion_data: MedicionUpdate,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Actualiza una medición del usuario actual
    """
    try:
        updated_medicion = await medicion_service.update_medicion(medicion_id, medicion_data, current_user_id)
        return updated_medicion
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{medicion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medicion(
    medicion_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Elimina una medición del usuario actual
    """
    try:
        deleted = await medicion_service.delete_medicion(medicion_id, current_user_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medición no encontrada"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/bovino/{bovino_id}/range", response_model=List[MedicionResponse])
async def get_mediciones_by_date_range(
    bovino_id: str,
    fecha_inicio: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_fin: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene mediciones de un bovino en un rango de fechas
    """
    try:
        mediciones = await medicion_service.get_mediciones_by_fecha_range(
            bovino_id, fecha_inicio, fecha_fin, current_user_id
        )
        return mediciones
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/bovino/{bovino_id}/ultima", response_model=MedicionResponse)
async def get_ultima_medicion_bovino(
    bovino_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene la última medición de un bovino
    """
    try:
        medicion = await medicion_service.get_ultima_medicion_bovino(bovino_id, current_user_id)
        
        if not medicion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron mediciones para este bovino"
            )
        
        return medicion
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
