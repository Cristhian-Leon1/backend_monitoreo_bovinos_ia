from supabase import Client
from app.config.database import supabase, supabase_admin
from app.models.auth import UserRegister, UserLogin, PerfilCreate, PerfilUpdate
from typing import Optional, Dict, Any
import uuid

class AuthService:
    def __init__(self, db_client: Client = supabase):
        self.db = db_client
        self.admin_db = supabase_admin
    
    async def register_user(self, user_data: UserRegister) -> Dict[str, Any]:
        """Registra un nuevo usuario"""
        try:
            # Registrar usuario en Supabase Auth
            auth_response = self.db.auth.sign_up({
                "email": user_data.email,
                "password": user_data.password,
                "options": {
                    "data": {
                        "nombre_completo": user_data.nombre_completo
                    }
                }
            })
            
            if auth_response.user:
                return {
                    "user": auth_response.user,
                    "session": auth_response.session
                }
            else:
                raise Exception("Error al registrar usuario")
                
        except Exception as e:
            raise Exception(f"Error en registro: {str(e)}")
    
    async def login_user(self, user_data: UserLogin) -> Dict[str, Any]:
        """Autentica un usuario"""
        try:
            auth_response = self.db.auth.sign_in_with_password({
                "email": user_data.email,
                "password": user_data.password
            })
            
            if auth_response.user and auth_response.session:
                # Obtener perfil del usuario
                perfil = await self.get_user_profile(auth_response.user.id)
                
                return {
                    "user": auth_response.user,
                    "session": auth_response.session,
                    "perfil": perfil
                }
            else:
                raise Exception("Credenciales inválidas")
                
        except Exception as e:
            raise Exception(f"Error en login: {str(e)}")
    
    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene el perfil de un usuario"""
        try:
            response = self.db.table('perfiles').select('*').eq('id', user_id).execute()
            
            if response.data:
                return response.data[0]
            return None
            
        except Exception as e:
            raise Exception(f"Error obteniendo perfil: {str(e)}")
    
    async def update_user_profile(self, user_id: str, profile_data: PerfilUpdate) -> Dict[str, Any]:
        """Actualiza el perfil de un usuario"""
        try:
            update_data = profile_data.dict(exclude_unset=True)
            update_data['updated_at'] = 'now()'
            
            response = self.db.table('perfiles').update(update_data).eq('id', user_id).execute()
            
            if response.data:
                return response.data[0]
            else:
                raise Exception("Error actualizando perfil")
                
        except Exception as e:
            raise Exception(f"Error actualizando perfil: {str(e)}")
    
    async def logout_user(self, access_token: str) -> bool:
        """Cierra sesión de usuario"""
        try:
            self.db.auth.sign_out()
            return True
        except Exception as e:
            raise Exception(f"Error en logout: {str(e)}")
    
    async def verify_token(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Verifica un token de acceso"""
        try:
            user_response = self.db.auth.get_user(access_token)
            if user_response.user:
                return user_response.user
            return None
        except Exception as e:
            return None

# Instancia global del servicio
auth_service = AuthService()
