from supabase import Client
from app.config.database import supabase
from app.config.settings import settings
from fastapi import UploadFile
from typing import List, Dict, Any
import uuid
import os
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

# Instancia global del servicio
image_service = ImageService()
