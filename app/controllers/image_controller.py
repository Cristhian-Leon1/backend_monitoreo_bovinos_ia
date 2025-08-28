from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from app.models.common import ImageUploadResponse, BulkUploadResponse
from app.services.image_service import image_service
from app.middleware.auth import get_current_user_id
from typing import List, Optional
import uuid

router = APIRouter(prefix="/images", tags=["Imágenes"])

@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    folder: str = Form("bovinos"),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Sube una imagen al bucket de almacenamiento
    """
    try:
        # Validar tipo de archivo
        allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de archivo no permitido. Tipos válidos: {', '.join(allowed_types)}"
            )
        
        # Validar tamaño (máximo 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        file_content = await file.read()
        if len(file_content) > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo es demasiado grande. Máximo 10MB"
            )
        
        # Resetear el archivo para la subida
        await file.seek(0)
        
        result = await image_service.upload_image(file, folder)
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error subiendo imagen: {str(e)}"
        )

@router.post("/upload-multiple", response_model=BulkUploadResponse)
async def upload_multiple_images(
    files: List[UploadFile] = File(...),
    folder: str = Form("bovinos"),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Sube múltiples imágenes al bucket de almacenamiento
    """
    try:
        # Validar cantidad de archivos
        max_files = 20
        if len(files) > max_files:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Máximo {max_files} archivos permitidos"
            )
        
        # Validar cada archivo
        allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
        max_size = 10 * 1024 * 1024  # 10MB
        
        for file in files:
            if file.content_type not in allowed_types:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Archivo {file.filename}: tipo no permitido"
                )
            
            file_content = await file.read()
            if len(file_content) > max_size:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Archivo {file.filename}: demasiado grande (máximo 10MB)"
                )
            
            await file.seek(0)  # Resetear para la subida
        
        result = await image_service.upload_multiple_images(files, folder)
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error subiendo imágenes: {str(e)}"
        )

@router.delete("/{file_path:path}")
async def delete_image(
    file_path: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Elimina una imagen del bucket de almacenamiento
    """
    try:
        deleted = await image_service.delete_image(file_path)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Imagen no encontrada"
            )
        
        return {"message": "Imagen eliminada exitosamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error eliminando imagen: {str(e)}"
        )

@router.get("/url/{file_path:path}")
async def get_image_url(
    file_path: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene la URL pública de una imagen
    """
    try:
        url = await image_service.get_image_url(file_path)
        return {"public_url": url}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo URL: {str(e)}"
        )

@router.get("/list/{folder}")
async def list_images_in_folder(
    folder: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Lista todas las imágenes en una carpeta específica
    """
    try:
        images = await image_service.list_images_in_folder(folder)
        return {"images": images}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listando imágenes: {str(e)}"
        )
