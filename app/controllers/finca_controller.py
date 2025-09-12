from fastapi import APIRouter, HTTPException, status, Depends
from app.models.finca import FincaCreate, FincaUpdate, FincaResponse, FincaWithBovinos, FincaWithBovinosAndMediciones
from app.services.finca_service import finca_service
from app.middleware.auth import get_current_user_id
from typing import List
import uuid

router = APIRouter(prefix="/fincas", tags=["Fincas"])

@router.post("/", response_model=FincaResponse, status_code=status.HTTP_201_CREATED)
async def create_finca(
    finca_data: FincaCreate,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Crea una nueva finca para el usuario actual
    """
    try:
        finca = await finca_service.create_finca(finca_data, current_user_id)
        return finca
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[FincaResponse])
async def get_my_fincas(current_user_id: str = Depends(get_current_user_id)):
    """
    Obtiene todas las fincas del usuario actual
    """
    try:
        fincas = await finca_service.get_fincas_by_user(current_user_id)
        return fincas
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{finca_id}", response_model=FincaResponse)
async def get_finca_by_id(
    finca_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene una finca específica del usuario actual
    """
    try:
        finca = await finca_service.get_finca_by_id(finca_id, current_user_id)
        
        if not finca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Finca no encontrada"
            )
        
        return finca
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{finca_id}", response_model=FincaResponse)
async def update_finca(
    finca_id: str,
    finca_data: FincaUpdate,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Actualiza una finca del usuario actual
    """
    try:
        updated_finca = await finca_service.update_finca(finca_id, finca_data, current_user_id)
        return updated_finca
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{finca_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_finca(
    finca_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Elimina una finca del usuario actual
    """
    try:
        deleted = await finca_service.delete_finca(finca_id, current_user_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Finca no encontrada"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{finca_id}/with-bovinos", response_model=FincaWithBovinos)
async def get_finca_with_bovinos(
    finca_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene una finca con todos sus bovinos
    """
    try:
        finca = await finca_service.get_finca_with_bovinos(finca_id, current_user_id)
        
        if not finca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Finca no encontrada"
            )
        
        return finca
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{finca_id}/complete", response_model=FincaWithBovinosAndMediciones)
async def get_finca_complete(
    finca_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene una finca completa con todos sus bovinos y la última medición de cada uno
    """
    try:
        finca_completa = await finca_service.get_finca_with_bovinos_and_mediciones(finca_id, current_user_id)
        
        if not finca_completa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Finca no encontrada"
            )
        
        return finca_completa
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
