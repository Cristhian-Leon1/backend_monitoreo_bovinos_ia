from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.models.bovino import BovinoCreate, BovinoUpdate, BovinoResponse, BovinoWithMediciones
from app.services.bovino_service import bovino_service
from app.middleware.auth import get_current_user_id
from typing import List, Optional
import uuid

router = APIRouter(prefix="/bovinos", tags=["Bovinos"])

@router.post("/", response_model=BovinoResponse, status_code=status.HTTP_201_CREATED)
async def create_bovino(
    bovino_data: BovinoCreate,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Crea un nuevo bovino en una finca del usuario actual
    """
    try:
        bovino = await bovino_service.create_bovino(bovino_data, current_user_id)
        return bovino
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/finca/{finca_id}", response_model=List[BovinoResponse])
async def get_bovinos_by_finca(
    finca_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene todos los bovinos de una finca específica
    """
    try:
        bovinos = await bovino_service.get_bovinos_by_finca(finca_id, current_user_id)
        return bovinos
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{bovino_id}", response_model=BovinoResponse)
async def get_bovino_by_id(
    bovino_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene un bovino específico del usuario actual
    """
    try:
        bovino = await bovino_service.get_bovino_by_id(bovino_id, current_user_id)
        
        if not bovino:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bovino no encontrado"
            )
        
        return bovino
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{bovino_id}", response_model=BovinoResponse)
async def update_bovino(
    bovino_id: str,
    bovino_data: BovinoUpdate,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Actualiza un bovino del usuario actual
    """
    try:
        updated_bovino = await bovino_service.update_bovino(bovino_id, bovino_data, current_user_id)
        return updated_bovino
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{bovino_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bovino(
    bovino_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Elimina un bovino del usuario actual
    """
    try:
        deleted = await bovino_service.delete_bovino(bovino_id, current_user_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bovino no encontrado"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{bovino_id}/with-mediciones", response_model=BovinoWithMediciones)
async def get_bovino_with_mediciones(
    bovino_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene un bovino con todas sus mediciones
    """
    try:
        bovino = await bovino_service.get_bovino_with_mediciones(bovino_id, current_user_id)
        
        if not bovino:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bovino no encontrado"
            )
        
        return bovino
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/search/by-id", response_model=List[BovinoResponse])
async def search_bovinos_by_id(
    id_bovino: str = Query(..., description="ID del bovino (placa/arete) a buscar"),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Busca bovinos por ID de bovino (placa/arete)
    """
    try:
        bovinos = await bovino_service.search_bovinos_by_id(id_bovino, current_user_id)
        return bovinos
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
