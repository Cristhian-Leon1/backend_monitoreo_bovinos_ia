from supabase import Client
from app.config.database import supabase
from app.config.settings import settings
from fastapi import UploadFile
from typing import List, Dict, Any
import uuid
import os
import base64
import io
from datetime import datetime

class ImageService:
    def __init__(self, db_client: Client = supabase):
        self.db = db_client
        self.bucket_name = settings.bucket_name
    
    async def upload_image(self, file: UploadFile, folder: str = "bovinos") -> Dict[str, Any]:
        """Sube una imagen al bucket de Supabase"""
        try:
            # Generar nombre único para el archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = os.path.splitext(file.filename)[1] if file.filename else '.jpg'
            unique_filename = f"{folder}/{timestamp}_{uuid.uuid4().hex[:8]}{file_extension}"
            
            # Leer contenido del archivo
            file_content = await file.read()
            
            # Usar el cliente admin para subir archivos (evita problemas de RLS)
            from app.config.database import supabase_admin
            
            try:
                # Subir archivo al bucket
                response = supabase_admin.storage.from_(self.bucket_name).upload(
                    path=unique_filename,
                    file=file_content,
                    file_options={
                        "content-type": file.content_type or "image/jpeg",
                        "cache-control": "3600"
                    }
                )
                
                # Obtener URL pública
                public_url = supabase_admin.storage.from_(self.bucket_name).get_public_url(unique_filename)
                
                return {
                    "url": unique_filename,
                    "public_url": public_url,
                    "file_name": file.filename or "uploaded_image.jpg"
                }
                
            except Exception as upload_error:
                raise Exception(f"Error subiendo a bucket: {str(upload_error)}")
                
        except Exception as e:
            raise Exception(f"Error en upload de imagen: {str(e)}")
    
    async def upload_multiple_images(self, files: List[UploadFile], folder: str = "bovinos") -> Dict[str, Any]:
        """Sube múltiples imágenes al bucket"""
        uploaded_files = []
        failed_files = []
        
        for file in files:
            try:
                result = await self.upload_image(file, folder)
                uploaded_files.append(result)
            except Exception as e:
                failed_files.append(f"{file.filename}: {str(e)}")
        
        return {
            "uploaded_files": uploaded_files,
            "failed_files": failed_files,
            "total_uploaded": len(uploaded_files),
            "total_failed": len(failed_files)
        }
    
    async def delete_image(self, file_path: str) -> bool:
        """Elimina una imagen del bucket"""
        try:
            from app.config.database import supabase_admin
            response = supabase_admin.storage.from_(self.bucket_name).remove([file_path])
            return True  # Si no hay excepción, asumimos éxito
        except Exception as e:
            raise Exception(f"Error eliminando imagen: {str(e)}")
    
    async def get_image_url(self, file_path: str) -> str:
        """Obtiene la URL pública de una imagen"""
        try:
            from app.config.database import supabase_admin
            return supabase_admin.storage.from_(self.bucket_name).get_public_url(file_path)
        except Exception as e:
            raise Exception(f"Error obteniendo URL: {str(e)}")
    
    async def list_images_in_folder(self, folder: str = "bovinos") -> List[Dict[str, Any]]:
        """Lista todas las imágenes en una carpeta"""
        try:
            response = self.db.storage.from_(self.bucket_name).list(folder)
            return response if response else []
        except Exception as e:
            raise Exception(f"Error listando imágenes: {str(e)}")

    async def upload_profile_image_base64(self, image_base64: str, user_id: str, file_name: str = None) -> Dict[str, Any]:
        """Sube una imagen de perfil desde base64 y actualiza la tabla perfiles"""
        try:
            # Validar que el base64 tenga el formato correcto
            if not image_base64 or not image_base64.startswith('data:image/'):
                raise Exception("Formato de imagen base64 inválido. Debe incluir el data URL completo.")
            
            # Extraer el tipo de contenido y los datos base64
            header, encoded = image_base64.split(',', 1)
            content_type = header.split(';')[0].split(':')[1]
            
            # Validar tipo de contenido
            allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
            if content_type not in allowed_types:
                raise Exception(f"Tipo de imagen no permitido. Tipos válidos: {', '.join(allowed_types)}")
            
            # Decodificar base64
            try:
                image_data = base64.b64decode(encoded)
            except Exception as decode_error:
                raise Exception(f"Error decodificando imagen base64: {str(decode_error)}")
            
            # Validar tamaño (máximo 10MB)
            max_size = 10 * 1024 * 1024  # 10MB
            if len(image_data) > max_size:
                raise Exception("La imagen es demasiado grande. Máximo 10MB")
            
            # Generar nombre único para el archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            extension = ".jpg" if content_type == "image/jpeg" else ".png"
            if content_type == "image/webp":
                extension = ".webp"
            
            unique_filename = f"perfiles/{user_id}_{timestamp}_{uuid.uuid4().hex[:8]}{extension}"
            
            # Usar el cliente admin para subir archivos
            from app.config.database import supabase_admin
            
            try:
                # Subir archivo al bucket
                response = supabase_admin.storage.from_(self.bucket_name).upload(
                    path=unique_filename,
                    file=image_data,
                    file_options={
                        "content-type": content_type,
                        "cache-control": "3600"
                    }
                )
                
                # Obtener URL pública
                public_url = supabase_admin.storage.from_(self.bucket_name).get_public_url(unique_filename)
                
                # Actualizar tabla perfiles con la nueva imagen
                try:
                    update_response = self.db.table('perfiles')\
                        .update({'imagen_perfil': public_url})\
                        .eq('id', user_id)\
                        .execute()
                    
                    profile_updated = len(update_response.data) > 0
                    
                except Exception as update_error:
                    # Si hay error actualizando perfil, eliminar la imagen subida
                    try:
                        supabase_admin.storage.from_(self.bucket_name).remove([unique_filename])
                    except:
                        pass
                    raise Exception(f"Error actualizando perfil: {str(update_error)}")
                
                return {
                    "url": unique_filename,
                    "public_url": public_url,
                    "file_name": file_name or f"profile_image{extension}",
                    "profile_updated": profile_updated
                }
                
            except Exception as upload_error:
                raise Exception(f"Error subiendo imagen a bucket: {str(upload_error)}")
                
        except Exception as e:
            raise Exception(f"Error en upload de imagen de perfil: {str(e)}")

# Instancia global del servicio
image_service = ImageService()
