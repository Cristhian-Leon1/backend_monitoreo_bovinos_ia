from fastapi import APIRouter, HTTPException, status, Depends
from app.models.auth import UserRegister, UserLogin, TokenResponse, PerfilUpdate, PerfilResponse
from app.services.auth_service import auth_service
from fastapi.security import HTTPAuthorizationCredentials  # 👈 Añade esto
from app.middleware.auth import get_current_user, get_current_user_id, security  # Añadir security
from typing import Dict, Any

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Registra un nuevo usuario en el sistema
    """
    try:
        result = await auth_service.register_user(user_data)
        
        user_response = {
            "id": result["user"].id,
            "email": result["user"].email,
            "created_at": result["user"].created_at
        }
        
        return TokenResponse(
            access_token=result["session"].access_token,
            refresh_token=result["session"].refresh_token,
            expires_in=result["session"].expires_in,
            user=user_response
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    """
    Autentica un usuario y devuelve tokens de acceso
    """
    try:
        result = await auth_service.login_user(user_data)
        
        user_response = {
            "id": result["user"].id,
            "email": result["user"].email,
            "created_at": result["user"].created_at,
            "perfil": result["perfil"]
        }
        
        return TokenResponse(
            access_token=result["session"].access_token,
            refresh_token=result["session"].refresh_token,
            expires_in=result["session"].expires_in,
            user=user_response
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Cierra la sesión del usuario actual"""
    try:
        token = credentials.credentials  # Obtener el token real
        await auth_service.logout_user(token)
        return {"message": "Sesión cerrada exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=PerfilResponse)
async def get_current_user_profile(user_id: str = Depends(get_current_user_id)):
    """
    Obtiene el perfil del usuario actual
    """
    try:
        perfil = await auth_service.get_user_profile(user_id)
        
        if not perfil:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil no encontrado"
            )
        
        return perfil
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/me", response_model=PerfilResponse)
async def update_current_user_profile(
    profile_data: PerfilUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """
    Actualiza el perfil del usuario actual
    """
    try:
        updated_profile = await auth_service.update_user_profile(user_id, profile_data)
        return updated_profile
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/verify")
async def verify_token(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Verifica si el token actual es válido
    """
    return {
        "valid": True,
        "user_id": current_user.get("id"),
        "email": current_user.get("email")
    }
