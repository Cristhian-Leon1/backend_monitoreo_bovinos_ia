from supabase import Client
from app.config.database import supabase
from app.models.medicion import MedicionCreate, MedicionUpdate
from typing import List, Dict, Any, Optional
from datetime import date
import uuid

class MedicionService:
    def __init__(self, db_client: Client = supabase):
        self.db = db_client
    
    async def create_medicion(self, medicion_data: MedicionCreate, propietario_id: str) -> Dict[str, Any]:
        """Crea una nueva medición"""
        try:
            # Verificar que el bovino pertenece al usuario
            bovino_response = self.db.table('bovinos').select('*, fincas!inner(propietario_id)').eq('id', str(medicion_data.bovino_id)).execute()
            
            if not bovino_response.data or bovino_response.data[0]['fincas']['propietario_id'] != propietario_id:
                raise Exception("Bovino no encontrado o sin permisos")
            
            insert_data = medicion_data.dict()
            insert_data['fecha'] = str(insert_data['fecha'])  # Convertir fecha a string
            
            response = self.db.table('mediciones_bovinos').insert(insert_data).execute()
            
            if response.data:
                return response.data[0]
            else:
                raise Exception("Error creando medición")
                
        except Exception as e:
            raise Exception(f"Error creando medición: {str(e)}")
    
    async def get_mediciones_by_bovino(self, bovino_id: str, propietario_id: str) -> List[Dict[str, Any]]:
        """Obtiene todas las mediciones de un bovino"""
        try:
            # Verificar permisos
            bovino_response = self.db.table('bovinos').select('*, fincas!inner(propietario_id)').eq('id', bovino_id).execute()
            
            if not bovino_response.data or bovino_response.data[0]['fincas']['propietario_id'] != propietario_id:
                raise Exception("Bovino no encontrado o sin permisos")
            
            response = self.db.table('mediciones_bovinos').select('*').eq('bovino_id', bovino_id).order('fecha', desc=True).execute()
            return response.data if response.data else []
            
        except Exception as e:
            raise Exception(f"Error obteniendo mediciones: {str(e)}")
    
    async def get_medicion_by_id(self, medicion_id: str, propietario_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una medición específica"""
        try:
            response = self.db.table('mediciones_bovinos').select('*, bovinos!inner(*, fincas!inner(propietario_id))').eq('id', medicion_id).execute()
            
            if response.data and response.data[0]['bovinos']['fincas']['propietario_id'] == propietario_id:
                return response.data[0]
            return None
            
        except Exception as e:
            raise Exception(f"Error obteniendo medición: {str(e)}")
    
    async def update_medicion(self, medicion_id: str, medicion_data: MedicionUpdate, propietario_id: str) -> Dict[str, Any]:
        """Actualiza una medición"""
        try:
            # Verificar permisos
            medicion_actual = await self.get_medicion_by_id(medicion_id, propietario_id)
            if not medicion_actual:
                raise Exception("Medición no encontrada o sin permisos")
            
            update_data = medicion_data.dict(exclude_unset=True)
            if 'fecha' in update_data:
                update_data['fecha'] = str(update_data['fecha'])
            
            response = self.db.table('mediciones_bovinos').update(update_data).eq('id', medicion_id).execute()
            
            if response.data:
                return response.data[0]
            else:
                raise Exception("Error actualizando medición")
                
        except Exception as e:
            raise Exception(f"Error actualizando medición: {str(e)}")
    
    async def delete_medicion(self, medicion_id: str, propietario_id: str) -> bool:
        """Elimina una medición"""
        try:
            # Verificar permisos
            medicion_actual = await self.get_medicion_by_id(medicion_id, propietario_id)
            if not medicion_actual:
                raise Exception("Medición no encontrada o sin permisos")
            
            response = self.db.table('mediciones_bovinos').delete().eq('id', medicion_id).execute()
            
            return len(response.data) > 0
            
        except Exception as e:
            raise Exception(f"Error eliminando medición: {str(e)}")
    
    async def get_mediciones_by_fecha_range(self, bovino_id: str, fecha_inicio: date, fecha_fin: date, propietario_id: str) -> List[Dict[str, Any]]:
        """Obtiene mediciones de un bovino en un rango de fechas"""
        try:
            # Verificar permisos
            bovino_response = self.db.table('bovinos').select('*, fincas!inner(propietario_id)').eq('id', bovino_id).execute()
            
            if not bovino_response.data or bovino_response.data[0]['fincas']['propietario_id'] != propietario_id:
                raise Exception("Bovino no encontrado o sin permisos")
            
            response = self.db.table('mediciones_bovinos').select('*').eq('bovino_id', bovino_id).gte('fecha', str(fecha_inicio)).lte('fecha', str(fecha_fin)).order('fecha', desc=True).execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            raise Exception(f"Error obteniendo mediciones por rango: {str(e)}")
    
    async def get_ultima_medicion_bovino(self, bovino_id: str, propietario_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene la última medición de un bovino"""
        try:
            mediciones = await self.get_mediciones_by_bovino(bovino_id, propietario_id)
            
            if mediciones:
                return mediciones[0]  # Ya están ordenadas por fecha desc
            return None
            
        except Exception as e:
            raise Exception(f"Error obteniendo última medición: {str(e)}")

# Instancia global del servicio
medicion_service = MedicionService()
