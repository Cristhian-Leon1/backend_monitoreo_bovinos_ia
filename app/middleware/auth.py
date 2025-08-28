from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import auth_service
from typing import Optional, Dict, Any
import uuid

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Middleware para obtener el usuario actual desde el token JWT
    """
    try:
        token = credentials.credentials
        user = await auth_service.verify_token(token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user_id(current_user: Dict[str, Any] = Depends(get_current_user)) -> str:
    """
    Obtiene solo el ID del usuario actual
    """
    return current_user.get("id")

class AuthMiddleware:
    """
    Middleware personalizado para manejo de autenticación
    """
    
    @staticmethod
    async def verify_user_owns_resource(user_id: str, resource_owner_id: str) -> bool:
        """
        Verifica que el usuario sea propietario del recurso
        """
        return user_id == resource_owner_id
    
    @staticmethod
    async def require_admin(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        """
        Requiere que el usuario sea administrador
        """
        # Aquí puedes implementar lógica adicional para verificar roles de admin
        # Por ahora, todos los usuarios autenticados tienen acceso
        return current_user
    
    @staticmethod
    async def optional_auth(credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))) -> Optional[Dict[str, Any]]:
        """
        Autenticación opcional - no falla si no hay token
        """
        if not credentials:
            return None
        
        try:
            token = credentials.credentials
            user = await auth_service.verify_token(token)
            return user
        except:
            return None
