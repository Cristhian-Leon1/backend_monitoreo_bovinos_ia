from supabase import Client
from app.config.database import supabase
from app.models.finca import FincaCreate, FincaUpdate, FincaWithBovinosAndMediciones, BovinoWithLastMedicion
from typing import List, Dict, Any, Optional
from datetime import datetime
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

    async def get_finca_with_bovinos_and_mediciones(self, finca_id: str, propietario_id: str) -> Optional[FincaWithBovinosAndMediciones]:
        """
        Obtiene una finca con todos sus bovinos y la última medición de cada uno
        """
        try:
            # Obtener datos de la finca
            finca_response = self.db.table('fincas')\
                .select('*')\
                .eq('id', finca_id)\
                .eq('propietario_id', propietario_id)\
                .execute()
            
            if not finca_response.data:
                return None
            
            finca_data = finca_response.data[0]
            
            # Obtener bovinos de la finca
            bovinos_response = self.db.table('bovinos')\
                .select('*')\
                .eq('finca_id', finca_id)\
                .execute()
            
            bovinos_with_mediciones = []
            bovinos_con_mediciones_recientes = 0
            
            for bovino_data in bovinos_response.data:
                # Obtener la última medición de cada bovino
                medicion_response = self.db.table('mediciones_bovinos')\
                    .select('*')\
                    .eq('bovino_id', bovino_data['id'])\
                    .order('fecha', desc=True)\
                    .limit(1)\
                    .execute()
                
                ultima_medicion = None
                if medicion_response.data:
                    ultima_medicion = medicion_response.data[0]
                    # Considerar medición reciente si es de los últimos 30 días
                    try:
                        fecha_medicion_str = ultima_medicion['fecha']
                        if isinstance(fecha_medicion_str, str):
                            # La fecha viene como string "YYYY-MM-DD"
                            from datetime import date
                            fecha_medicion = datetime.strptime(fecha_medicion_str, '%Y-%m-%d').date()
                            fecha_actual = datetime.now().date()
                            dias_diferencia = (fecha_actual - fecha_medicion).days
                        else:
                            # La fecha ya es un objeto date
                            fecha_actual = datetime.now().date()
                            dias_diferencia = (fecha_actual - fecha_medicion_str).days
                        
                        if dias_diferencia <= 30:
                            bovinos_con_mediciones_recientes += 1
                    except Exception as e:
                        # Si hay error parseando fecha, no cuenta como reciente
                        print(f"Error parseando fecha de medición: {e}")
                        pass
                
                # Crear objeto bovino con última medición
                bovino_with_medicion = BovinoWithLastMedicion(
                    **bovino_data,
                    ultima_medicion=ultima_medicion
                )
                bovinos_with_mediciones.append(bovino_with_medicion)
            
            # Crear objeto finca completo
            finca_completa = FincaWithBovinosAndMediciones(
                **finca_data,
                bovinos=bovinos_with_mediciones,
                total_bovinos=len(bovinos_with_mediciones),
                bovinos_con_mediciones_recientes=bovinos_con_mediciones_recientes
            )
            
            return finca_completa
            
        except Exception as e:
            print(f"Error al obtener finca con bovinos y mediciones: {e}")
            raise Exception(f"Error al obtener datos completos de la finca: {str(e)}")

# Instancia global del servicio
finca_service = FincaService()
