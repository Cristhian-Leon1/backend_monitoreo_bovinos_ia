from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from datetime import date
from app.models.medicion import MedicionCreate, MedicionUpdate, MedicionResponse
from app.services.medicion_service import medicion_service
from app.middleware.auth import get_current_user_id
import logging

# Configurar logger para el controlador
logger = logging.getLogger(__name__)

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
        logger.info(f"Creando medición para bovino: {medicion_data.bovino_id}")
        medicion = await medicion_service.create_medicion(medicion_data, current_user_id)
        logger.info(f"Medición creada exitosamente con ID: {medicion.get('id', 'unknown')}")
        return medicion
    
    except ValueError as e:
        logger.warning(f"Error de validación al crear medición: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error de validación: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error inesperado al crear medición: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/bovino/{bovino_id}", response_model=List[MedicionResponse])
async def get_mediciones_by_bovino(
    bovino_id: str,
    limit: int = Query(default=50, ge=1, le=100, description="Número máximo de mediciones a devolver"),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene todas las mediciones de un bovino específico con paginación
    """
    try:
        logger.info(f"Obteniendo mediciones para bovino: {bovino_id}, limit: {limit}")
        mediciones = await medicion_service.get_mediciones_by_bovino(bovino_id, current_user_id)
        
        # Aplicar límite de resultados
        mediciones_limitadas = mediciones[:limit] if mediciones else []
        
        logger.info(f"Devolviendo {len(mediciones_limitadas)} mediciones de {len(mediciones)} totales")
        return mediciones_limitadas
    
    except Exception as e:
        logger.error(f"Error al obtener mediciones del bovino {bovino_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener mediciones: {str(e)}"
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
        logger.info(f"Obteniendo medición: {medicion_id}")
        medicion = await medicion_service.get_medicion_by_id(medicion_id, current_user_id)
        
        if not medicion:
            logger.warning(f"Medición no encontrada: {medicion_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medición no encontrada"
            )
        
        logger.info(f"Medición encontrada: {medicion_id}")
        return medicion
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener medición {medicion_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
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
        logger.info(f"Actualizando medición: {medicion_id}")
        updated_medicion = await medicion_service.update_medicion(medicion_id, medicion_data, current_user_id)
        logger.info(f"Medición actualizada exitosamente: {medicion_id}")
        return updated_medicion
    
    except ValueError as e:
        logger.warning(f"Error de validación al actualizar medición {medicion_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error de validación: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error al actualizar medición {medicion_id}: {str(e)}")
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
        logger.info(f"Eliminando medición: {medicion_id}")
        deleted = await medicion_service.delete_medicion(medicion_id, current_user_id)
        
        if not deleted:
            logger.warning(f"Medición no encontrada para eliminar: {medicion_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medición no encontrada"
            )
        
        logger.info(f"Medición eliminada exitosamente: {medicion_id}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar medición {medicion_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
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
        # Validar que la fecha de inicio no sea posterior a la fecha de fin
        if fecha_inicio > fecha_fin:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="La fecha de inicio no puede ser posterior a la fecha de fin"
            )
        
        logger.info(f"Obteniendo mediciones de {bovino_id} del {fecha_inicio} al {fecha_fin}")
        mediciones = await medicion_service.get_mediciones_by_fecha_range(
            bovino_id, fecha_inicio, fecha_fin, current_user_id
        )
        
        logger.info(f"Encontradas {len(mediciones)} mediciones en el rango especificado")
        return mediciones
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener mediciones por rango: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
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
        logger.info(f"Obteniendo última medición de bovino: {bovino_id}")
        medicion = await medicion_service.get_ultima_medicion_bovino(bovino_id, current_user_id)
        
        if not medicion:
            logger.warning(f"No se encontraron mediciones para el bovino: {bovino_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron mediciones para este bovino"
            )
        
        logger.info(f"Última medición encontrada para bovino {bovino_id}: {medicion.get('fecha', 'unknown')}")
        return medicion
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener última medición: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )

# NUEVOS ENDPOINTS ADICIONALES

@router.get("/bovino/{bovino_id}/estadisticas")
async def get_estadisticas_mediciones_bovino(
    bovino_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene estadísticas de las mediciones de un bovino
    """
    try:
        logger.info(f"Obteniendo estadísticas de mediciones para bovino: {bovino_id}")
        estadisticas = await medicion_service.get_estadisticas_mediciones_bovino(bovino_id, current_user_id)
        logger.info(f"Estadísticas calculadas para bovino {bovino_id}")
        return estadisticas
    
    except Exception as e:
        logger.error(f"Error al obtener estadísticas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al calcular estadísticas: {str(e)}"
        )

@router.post("/bovino/{bovino_id}/batch", response_model=List[MedicionResponse], status_code=status.HTTP_201_CREATED)
async def create_mediciones_batch(
    bovino_id: str,
    mediciones_data: List[MedicionCreate],
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Crea múltiples mediciones para un bovino de una vez
    """
    try:
        if len(mediciones_data) > 50:  # Límite de mediciones por lote
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No se pueden crear más de 50 mediciones por lote"
            )
        
        logger.info(f"Creando {len(mediciones_data)} mediciones en lote para bovino: {bovino_id}")
        
        mediciones_creadas = []
        errores = []
        
        for i, medicion_data in enumerate(mediciones_data):
            try:
                # Verificar que el bovino_id coincida
                if str(medicion_data.bovino_id) != bovino_id:
                    errores.append(f"Medición {i+1}: bovino_id no coincide")
                    continue
                
                medicion = await medicion_service.create_medicion(medicion_data, current_user_id)
                mediciones_creadas.append(medicion)
            except Exception as e:
                errores.append(f"Medición {i+1}: {str(e)}")
        
        if errores and not mediciones_creadas:
            # Si todas fallaron
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se pudo crear ninguna medición. Errores: {'; '.join(errores)}"
            )
        elif errores:
            # Si algunas fallaron
            logger.warning(f"Se crearon {len(mediciones_creadas)} de {len(mediciones_data)} mediciones. Errores: {errores}")
        
        logger.info(f"Lote completado: {len(mediciones_creadas)} mediciones creadas")
        return mediciones_creadas
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en creación de lote: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno en creación de lote: {str(e)}"
        )

@router.get("/bovino/{bovino_id}/export")
async def export_mediciones_bovino(
    bovino_id: str,
    formato: str = Query(default="json", regex="^(json|csv)$", description="Formato de exportación: json o csv"),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Exporta todas las mediciones de un bovino en formato JSON o CSV
    """
    try:
        logger.info(f"Exportando mediciones de bovino {bovino_id} en formato {formato}")
        mediciones = await medicion_service.get_mediciones_by_bovino(bovino_id, current_user_id)
        
        if formato == "csv":
            # Para implementación futura de CSV
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Exportación CSV no implementada aún"
            )
        
        # Formato JSON (por defecto)
        export_data = {
            "bovino_id": bovino_id,
            "total_mediciones": len(mediciones),
            "fecha_exportacion": date.today().isoformat(),
            "mediciones": mediciones
        }
        
        logger.info(f"Exportación completada: {len(mediciones)} mediciones")
        return export_data
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en exportación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en exportación: {str(e)}"
        )
