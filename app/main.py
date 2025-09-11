from supabase import Client
from typing import Dict, Any, List, Optional
from datetime import date
from decimal import Decimal
import uuid
from app.models.medicion_model import MedicionCreate, MedicionUpdate
from app.config.database import supabase

class MedicionService:
    def __init__(self, db_client: Client = supabase):
        self.db = db_client
    
    def _convert_decimals_to_float(self, data: dict) -> dict:
        """Convierte valores Decimal a float para evitar problemas de serialización"""
        if not isinstance(data, dict):
            return data
            
        converted = {}
        for key, value in data.items():
            if isinstance(value, Decimal):
                converted[key] = float(value) if value is not None else None
            elif isinstance(value, dict):
                converted[key] = self._convert_decimals_to_float(value)
            elif isinstance(value, list):
                converted[key] = [self._convert_decimals_to_float(item) if isinstance(item, dict) else 
                                (float(item) if isinstance(item, Decimal) else item) for item in value]
            else:
                converted[key] = value
        return converted
    
    def _prepare_insert_data(self, medicion_data: MedicionCreate) -> dict:
        """Prepara los datos para inserción en la base de datos"""
        insert_data = medicion_data.dict()
        
        # Convertir fecha a string
        if 'fecha' in insert_data and insert_data['fecha']:
            insert_data['fecha'] = str(insert_data['fecha'])
        
        # Convertir UUID a string
        if 'bovino_id' in insert_data:
            insert_data['bovino_id'] = str(insert_data['bovino_id'])
        
        # Convertir Decimals a float
        insert_data = self._convert_decimals_to_float(insert_data)
        
        return insert_data
    
    def _prepare_update_data(self, medicion_data: MedicionUpdate) -> dict:
        """Prepara los datos para actualización en la base de datos"""
        update_data = medicion_data.dict(exclude_unset=True)
        
        # Convertir fecha a string si está presente
        if 'fecha' in update_data and update_data['fecha']:
            update_data['fecha'] = str(update_data['fecha'])
        
        # Convertir Decimals a float
        update_data = self._convert_decimals_to_float(update_data)
        
        return update_data
    
    async def create_medicion(self, medicion_data: MedicionCreate, propietario_id: str) -> Dict[str, Any]:
        """Crea una nueva medición"""
        try:
            # Verificar que el bovino pertenece al usuario
            bovino_response = self.db.table('bovinos').select('*, fincas!inner(propietario_id)').eq('id', str(medicion_data.bovino_id)).execute()
            
            if not bovino_response.data or bovino_response.data[0]['fincas']['propietario_id'] != propietario_id:
                raise Exception("Bovino no encontrado o sin permisos")
            
            # Preparar datos para inserción
            insert_data = self._prepare_insert_data(medicion_data)
            
            print(f"DEBUG - Insertando medición con datos: {insert_data}")
            
            response = self.db.table('mediciones_bovinos').insert(insert_data).execute()
            
            if response.data:
                # Convertir la respuesta también para evitar problemas de serialización
                result = self._convert_decimals_to_float(response.data[0])
                print(f"DEBUG - Medición creada exitosamente: {result}")
                return result
            else:
                raise Exception("Error creando medición - No se recibieron datos")
                
        except Exception as e:
            print(f"ERROR - Error en create_medicion: {str(e)}")
            raise Exception(f"Error creando medición: {str(e)}")
    
    async def get_mediciones_by_bovino(self, bovino_id: str, propietario_id: str) -> List[Dict[str, Any]]:
        """Obtiene todas las mediciones de un bovino"""
        try:
            # Verificar permisos
            bovino_response = self.db.table('bovinos').select('*, fincas!inner(propietario_id)').eq('id', bovino_id).execute()
            
            if not bovino_response.data or bovino_response.data[0]['fincas']['propietario_id'] != propietario_id:
                raise Exception("Bovino no encontrado o sin permisos")
            
            response = self.db.table('mediciones_bovinos').select('*').eq('bovino_id', bovino_id).order('fecha', desc=True).execute()
            
            # Convertir Decimals en todas las mediciones
            if response.data:
                return [self._convert_decimals_to_float(medicion) for medicion in response.data]
            else:
                return []
            
        except Exception as e:
            raise Exception(f"Error obteniendo mediciones: {str(e)}")
    
    async def get_medicion_by_id(self, medicion_id: str, propietario_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una medición específica"""
        try:
            response = self.db.table('mediciones_bovinos').select('*, bovinos!inner(*, fincas!inner(propietario_id))').eq('id', medicion_id).execute()
            
            if response.data and response.data[0]['bovinos']['fincas']['propietario_id'] == propietario_id:
                # Convertir Decimals en la respuesta
                return self._convert_decimals_to_float(response.data[0])
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
            
            # Preparar datos para actualización
            update_data = self._prepare_update_data(medicion_data)
            
            print(f"DEBUG - Actualizando medición con datos: {update_data}")
            
            response = self.db.table('mediciones_bovinos').update(update_data).eq('id', medicion_id).execute()
            
            if response.data:
                # Convertir la respuesta
                result = self._convert_decimals_to_float(response.data[0])
                print(f"DEBUG - Medición actualizada exitosamente: {result}")
                return result
            else:
                raise Exception("Error actualizando medición - No se recibieron datos")
                
        except Exception as e:
            print(f"ERROR - Error en update_medicion: {str(e)}")
            raise Exception(f"Error actualizando medición: {str(e)}")
    
    async def delete_medicion(self, medicion_id: str, propietario_id: str) -> bool:
        """Elimina una medición"""
        try:
            # Verificar permisos
            medicion_actual = await self.get_medicion_by_id(medicion_id, propietario_id)
            if not medicion_actual:
                raise Exception("Medición no encontrada o sin permisos")
            
            response = self.db.table('mediciones_bovinos').delete().eq('id', medicion_id).execute()
            
            print(f"DEBUG - Medición eliminada: {len(response.data) > 0}")
            return len(response.data) > 0
            
        except Exception as e:
            print(f"ERROR - Error en delete_medicion: {str(e)}")
            raise Exception(f"Error eliminando medición: {str(e)}")
    
    async def get_mediciones_by_fecha_range(self, bovino_id: str, fecha_inicio: date, fecha_fin: date, propietario_id: str) -> List[Dict[str, Any]]:
        """Obtiene mediciones de un bovino en un rango de fechas"""
        try:
            # Verificar permisos
            bovino_response = self.db.table('bovinos').select('*, fincas!inner(propietario_id)').eq('id', bovino_id).execute()
            
            if not bovino_response.data or bovino_response.data[0]['fincas']['propietario_id'] != propietario_id:
                raise Exception("Bovino no encontrado o sin permisos")
            
            response = self.db.table('mediciones_bovinos').select('*').eq('bovino_id', bovino_id).gte('fecha', str(fecha_inicio)).lte('fecha', str(fecha_fin)).order('fecha', desc=True).execute()
            
            # Convertir Decimals en todas las mediciones
            if response.data:
                return [self._convert_decimals_to_float(medicion) for medicion in response.data]
            else:
                return []
            
        except Exception as e:
            raise Exception(f"Error obteniendo mediciones por rango: {str(e)}")
    
    async def get_ultima_medicion_bovino(self, bovino_id: str, propietario_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene la última medición de un bovino"""
        try:
            mediciones = await self.get_mediciones_by_bovino(bovino_id, propietario_id)
            
            if mediciones:
                # Ya está convertida por get_mediciones_by_bovino
                return mediciones[0]  # Ya están ordenadas por fecha desc
            return None
            
        except Exception as e:
            raise Exception(f"Error obteniendo última medición: {str(e)}")
    
    async def get_estadisticas_mediciones_bovino(self, bovino_id: str, propietario_id: str) -> Dict[str, Any]:
        """Obtiene estadísticas de las mediciones de un bovino"""
        try:
            mediciones = await self.get_mediciones_by_bovino(bovino_id, propietario_id)
            
            if not mediciones:
                return {
                    "total_mediciones": 0,
                    "primera_medicion": None,
                    "ultima_medicion": None,
                    "promedio_altura": None,
                    "promedio_peso": None
                }
            
            # Calcular estadísticas
            alturas = [m['altura_cm'] for m in mediciones if m.get('altura_cm') is not None]
            pesos = [m['peso_bascula_kg'] for m in mediciones if m.get('peso_bascula_kg') is not None]
            
            estadisticas = {
                "total_mediciones": len(mediciones),
                "primera_medicion": mediciones[-1]['fecha'] if mediciones else None,  # Última en lista ordenada desc
                "ultima_medicion": mediciones[0]['fecha'] if mediciones else None,    # Primera en lista ordenada desc
                "promedio_altura": sum(alturas) / len(alturas) if alturas else None,
                "promedio_peso": sum(pesos) / len(pesos) if pesos else None
            }
            
            return self._convert_decimals_to_float(estadisticas)
            
        except Exception as e:
            raise Exception(f"Error obteniendo estadísticas: {str(e)}")

# Instancia global del servicio
medicion_service = MedicionService()