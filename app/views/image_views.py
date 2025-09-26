from fastapi import APIRouter, HTTPException, status, Depends
from app.models.common import  ProfileImageUploadRequest, ProfileImageUploadResponse
from app.controllers.image_controller import image_controller
from app.middleware.auth import get_current_user_id

router = APIRouter(prefix="/images", tags=["Imágenes"])

@router.post("/upload-profile", response_model=ProfileImageUploadResponse)
async def upload_profile_image(
    request: ProfileImageUploadRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Sube una imagen de perfil desde base64 y actualiza la tabla perfiles
    """
    try:
        print("🚀 === INICIO UPLOAD IMAGEN PERFIL ===")
        print(f"👤 Usuario autenticado: {current_user_id}")
        print(f"📝 Tipo de request: {type(request)}")
        print(f"📄 Archivo especificado: {request.file_name}")
        
        # Validar que image_base64 existe y tiene contenido
        if not hasattr(request, 'image_base64') or not request.image_base64:
            print("❌ ERROR: No se recibió image_base64 o está vacío")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El campo image_base64 es requerido y no puede estar vacío"
            )
        
        # Logs sobre el contenido base64
        image_b64_length = len(request.image_base64)
        print(f"📏 Longitud de image_base64: {image_b64_length} caracteres")
        
        # Verificar que comience con data:image/
        if request.image_base64.startswith('data:image/'):
            header_part = request.image_base64.split(',')[0] if ',' in request.image_base64 else request.image_base64[:50]
            print(f"✅ Header base64 correcto: {header_part}")
        else:
            print(f"❌ Header base64 incorrecto. Primeros 50 chars: {request.image_base64[:50]}")
        
        # Verificar que tenga la coma separadora
        if ',' not in request.image_base64:
            print("❌ ERROR: Falta la coma separadora en el base64")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato base64 inválido: falta la coma separadora después del header"
            )
        
        print("📤 Enviando a controlador de imagen...")
        
        result = await image_controller.upload_profile_image_base64(
            image_base64=request.image_base64,
            user_id=current_user_id,
            file_name=request.file_name
        )
        
        print("✅ Imagen subida exitosamente")
        print(f"🔗 URL generada: {result['public_url']}")
        print("🚀 === FIN UPLOAD IMAGEN PERFIL ===")
        
        return result
    
    except HTTPException as http_ex:
        print(f"❌ HTTPException capturada: {http_ex.detail}")
        print("🚀 === FIN UPLOAD IMAGEN PERFIL (ERROR HTTP) ===")
        raise
    except Exception as e:
        print(f"❌ Exception general capturada: {str(e)}")
        print(f"🔍 Tipo de error: {type(e).__name__}")
        print("🚀 === FIN UPLOAD IMAGEN PERFIL (ERROR GENERAL) ===")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )