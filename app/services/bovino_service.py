from supabase import Client
from app.config.database import supabase_admin  # ✅ Cambiar a admin
from app.models.bovino import BovinoCreate, BovinoUpdate
from typing import List, Dict, Any, Optional
import uuid

class BovinoService:
    def __init__(self, db_client: Client = supabase_admin):  # ✅ Usar admin
        self.db = db_client
    
    async def create_bovino(self, bovino_data: BovinoCreate, propietario_id: str) -> Dict[str, Any]:
        """Crea un nuevo bovino"""
        try:
            # Verificar que la finca pertenece al usuario
            finca_response = self.db.table('fincas').select('id').eq('id', str(bovino_data.finca_id)).eq('propietario_id', propietario_id).execute()
            
            if not finca_response.data:
                raise Exception("Finca no encontrada o sin permisos")
            
            # ✅ CORREGIR: Convertir UUID a string antes de insertar
            insert_data = bovino_data.dict()
            insert_data['finca_id'] = str(insert_data['finca_id'])  # Convertir UUID a string
            
            response = self.db.table('bovinos').insert(insert_data).execute()
            
            if response.data:
                return response.data[0]
            else:
                raise Exception("Error creando bovino")
                
        except Exception as e:
            raise Exception(f"Error creando bovino: {str(e)}")
    
    async def get_bovinos_by_finca(self, finca_id: str, propietario_id: str) -> List[Dict[str, Any]]:
        """Obtiene todos los bovinos de una finca"""
        try:
            # Verificar permisos
            finca_response = self.db.table('fincas').select('id').eq('id', finca_id).eq('propietario_id', propietario_id).execute()
            
            if not finca_response.data:
                raise Exception("Finca no encontrada o sin permisos")
            
            response = self.db.table('bovinos').select('*').eq('finca_id', finca_id).execute()
            return response.data if response.data else []
            
        except Exception as e:
            raise Exception(f"Error obteniendo bovinos: {str(e)}")
    
    async def get_bovino_by_id(self, bovino_id: str, propietario_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un bovino específico"""
        try:
            response = self.db.table('bovinos').select('*, fincas!inner(propietario_id)').eq('id', bovino_id).execute()
            
            if response.data and response.data[0]['fincas']['propietario_id'] == propietario_id:
                return response.data[0]
            return None
            
        except Exception as e:
            raise Exception(f"Error obteniendo bovino: {str(e)}")
    
    async def update_bovino(self, bovino_id: str, bovino_data: BovinoUpdate, propietario_id: str) -> Dict[str, Any]:
        """Actualiza un bovino"""
        try:
            # Verificar permisos
            bovino_actual = await self.get_bovino_by_id(bovino_id, propietario_id)
            if not bovino_actual:
                raise Exception("Bovino no encontrado o sin permisos")
            
            update_data = bovino_data.dict(exclude_unset=True)
            
            response = self.db.table('bovinos').update(update_data).eq('id', bovino_id).execute()
            
            if response.data:
                return response.data[0]
            else:
                raise Exception("Error actualizando bovino")
                
        except Exception as e:
            raise Exception(f"Error actualizando bovino: {str(e)}")
    
    async def delete_bovino(self, bovino_id: str, propietario_id: str) -> bool:
        """Elimina un bovino"""
        try:
            # Verificar permisos
            bovino_actual = await self.get_bovino_by_id(bovino_id, propietario_id)
            if not bovino_actual:
                raise Exception("Bovino no encontrado o sin permisos")
            
            response = self.db.table('bovinos').delete().eq('id', bovino_id).execute()
            
            return len(response.data) > 0
            
        except Exception as e:
            raise Exception(f"Error eliminando bovino: {str(e)}")
    
    async def get_bovino_with_mediciones(self, bovino_id: str, propietario_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un bovino con sus mediciones"""
        try:
            # Obtener bovino
            bovino = await self.get_bovino_by_id(bovino_id, propietario_id)
            
            if not bovino:
                return None
            
            # Obtener mediciones del bovino
            mediciones_response = self.db.table('mediciones_bovinos').select('*').eq('bovino_id', bovino_id).order('fecha', desc=True).execute()
            
            bovino['mediciones'] = mediciones_response.data if mediciones_response.data else []
            
            return bovino
            
        except Exception as e:
            raise Exception(f"Error obteniendo bovino con mediciones: {str(e)}")
    
    async def search_bovinos_by_id(self, id_bovino: str, propietario_id: str) -> List[Dict[str, Any]]:
        """Busca bovinos por ID de bovino (placa/arete)"""
        try:
            response = self.db.table('bovinos').select('*, fincas!inner(propietario_id)').ilike('id_bovino', f'%{id_bovino}%').execute()
            
            # Filtrar por propietario
            bovinos = [bovino for bovino in response.data if bovino['fincas']['propietario_id'] == propietario_id]
            
            return bovinos
            
        except Exception as e:
            raise Exception(f"Error buscando bovinos: {str(e)}")

# Instancia global del servicio
bovino_service = BovinoService()
