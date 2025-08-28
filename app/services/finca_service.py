from supabase import Client
from app.config.database import supabase
from app.models.finca import FincaCreate, FincaUpdate
from typing import List, Dict, Any, Optional
import uuid

class FincaService:
    def __init__(self, db_client: Client = supabase):
        self.db = db_client
    
    async def create_finca(self, finca_data: FincaCreate, propietario_id: str) -> Dict[str, Any]:
        """Crea una nueva finca"""
        try:
            insert_data = finca_data.dict()
            insert_data['propietario_id'] = propietario_id
            
            response = self.db.table('fincas').insert(insert_data).execute()
            
            if response.data:
                return response.data[0]
            else:
                raise Exception("Error creando finca")
                
        except Exception as e:
            raise Exception(f"Error creando finca: {str(e)}")
    
    async def get_fincas_by_user(self, propietario_id: str) -> List[Dict[str, Any]]:
        """Obtiene todas las fincas de un usuario"""
        try:
            response = self.db.table('fincas').select('*').eq('propietario_id', propietario_id).execute()
            return response.data if response.data else []
            
        except Exception as e:
            raise Exception(f"Error obteniendo fincas: {str(e)}")
    
    async def get_finca_by_id(self, finca_id: str, propietario_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una finca específica"""
        try:
            response = self.db.table('fincas').select('*').eq('id', finca_id).eq('propietario_id', propietario_id).execute()
            
            if response.data:
                return response.data[0]
            return None
            
        except Exception as e:
            raise Exception(f"Error obteniendo finca: {str(e)}")
    
    async def update_finca(self, finca_id: str, finca_data: FincaUpdate, propietario_id: str) -> Dict[str, Any]:
        """Actualiza una finca"""
        try:
            update_data = finca_data.dict(exclude_unset=True)
            
            response = self.db.table('fincas').update(update_data).eq('id', finca_id).eq('propietario_id', propietario_id).execute()
            
            if response.data:
                return response.data[0]
            else:
                raise Exception("Finca no encontrada o sin permisos")
                
        except Exception as e:
            raise Exception(f"Error actualizando finca: {str(e)}")
    
    async def delete_finca(self, finca_id: str, propietario_id: str) -> bool:
        """Elimina una finca"""
        try:
            response = self.db.table('fincas').delete().eq('id', finca_id).eq('propietario_id', propietario_id).execute()
            
            return len(response.data) > 0
            
        except Exception as e:
            raise Exception(f"Error eliminando finca: {str(e)}")
    
    async def get_finca_with_bovinos(self, finca_id: str, propietario_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una finca con sus bovinos"""
        try:
            # Obtener finca
            finca_response = self.db.table('fincas').select('*').eq('id', finca_id).eq('propietario_id', propietario_id).execute()
            
            if not finca_response.data:
                return None
            
            finca = finca_response.data[0]
            
            # Obtener bovinos de la finca
            bovinos_response = self.db.table('bovinos').select('*').eq('finca_id', finca_id).execute()
            
            finca['bovinos'] = bovinos_response.data if bovinos_response.data else []
            
            return finca
            
        except Exception as e:
            raise Exception(f"Error obteniendo finca con bovinos: {str(e)}")

# Instancia global del servicio
finca_service = FincaService()
