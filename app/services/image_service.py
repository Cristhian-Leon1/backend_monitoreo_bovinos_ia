from supabase import Client
from app.config.database import supabase_admin  # ✅ Cambiar a admin
from app.config.database import supabase
from app.config.settings import settings
from fastapi import UploadFile
from typing import List, Dict, Any
import uuid
import base64
from datetime import datetime

class ImageService:
    def __init__(self, db_client: Client = supabase_admin):  # ✅ Usar admin
        self.db = db_client
        self.bucket_name = settings.bucket_name

    async def upload_profile_image_base64(self, image_base64: str, user_id: str, file_name: str = None) -> Dict[str, Any]:
        """Sube una imagen de perfil desde base64 y actualiza la tabla perfiles"""
        try:
            print(f"🔍 === SERVICIO: Iniciando upload ===")
            print(f"👤 user_id recibido: {user_id}")
            print(f"📄 file_name recibido: {file_name}")
            print(f"📏 Longitud image_base64: {len(image_base64) if image_base64 else 'None'}")
            
            # Validar que el base64 tenga el formato correcto
            if not image_base64:
                print("❌ SERVICIO: image_base64 está vacío o es None")
                raise Exception("image_base64 no puede estar vacío")
                
            if not image_base64.startswith('data:image/'):
                print(f"❌ SERVICIO: Formato incorrecto. Comienza con: {image_base64[:30]}...")
                raise Exception("Formato de imagen base64 inválido. Debe incluir el data URL completo.")
            
            print("✅ SERVICIO: Formato base64 inicial válido")
            
            # Extraer el tipo de contenido y los datos base64
            try:
                if ',' not in image_base64:
                    print("❌ SERVICIO: No se encontró coma separadora")
                    raise Exception("Formato base64 inválido: falta coma separadora")
                    
                header, encoded = image_base64.split(',', 1)
                print(f"📝 SERVICIO: Header extraído: {header}")
                print(f"📏 SERVICIO: Longitud datos encoded: {len(encoded)}")
                
                if ';' not in header or ':' not in header:
                    print(f"❌ SERVICIO: Header malformado: {header}")
                    raise Exception("Header base64 malformado")
                    
                content_type = header.split(';')[0].split(':')[1]
                print(f"📝 SERVICIO: Content-type detectado: {content_type}")
                
            except Exception as parse_error:
                print(f"❌ SERVICIO: Error parseando header: {str(parse_error)}")
                raise Exception(f"Error parseando header base64: {str(parse_error)}")
            
            # Validar tipo de contenido
            allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
            if content_type not in allowed_types:
                print(f"❌ SERVICIO: Tipo no permitido: {content_type}")
                print(f"📝 SERVICIO: Tipos permitidos: {allowed_types}")
                raise Exception(f"Tipo de imagen no permitido. Tipos válidos: {', '.join(allowed_types)}")
            
            print("✅ SERVICIO: Tipo de contenido válido")
            
            # Decodificar base64
            try:
                print("🔄 SERVICIO: Intentando decodificar base64...")
                image_data = base64.b64decode(encoded)
                print(f"📏 SERVICIO: Tamaño imagen decodificada: {len(image_data)} bytes")
            except Exception as decode_error:
                print(f"❌ SERVICIO: Error decodificando: {str(decode_error)}")
                print(f"📝 SERVICIO: Primeros 50 chars del encoded: {encoded[:50]}")
                raise Exception(f"Error decodificando imagen base64: {str(decode_error)}")
            
            # Validar tamaño (máximo 10MB)
            max_size = 10 * 1024 * 1024  # 10MB
            if len(image_data) > max_size:
                print(f"❌ SERVICIO: Imagen muy grande: {len(image_data)} bytes (máx: {max_size})")
                raise Exception("La imagen es demasiado grande. Máximo 10MB")
            
            print("✅ SERVICIO: Tamaño de imagen válido")
            
            # Validar que el user_id es un UUID válido
            try:
                uuid.UUID(user_id)
                print("✅ SERVICIO: user_id es UUID válido")
            except ValueError:
                print(f"❌ SERVICIO: user_id inválido: {user_id}")
                raise Exception(f"El user_id '{user_id}' no es un UUID válido")
            
            # Generar nombre único para el archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            extension = ".jpg" if content_type == "image/jpeg" else ".png"
            if content_type == "image/webp":
                extension = ".webp"
            
            unique_filename = f"perfiles/{user_id}_{timestamp}_{uuid.uuid4().hex[:8]}{extension}"
            print(f"📁 SERVICIO: Nombre archivo: {unique_filename}")
            
            # Usar el cliente admin para subir archivos
            from app.config.database import supabase_admin
            
            try:
                print("🚀 SERVICIO: Iniciando subida al bucket...")
                
                # Nota: Saltamos la verificación del bucket para evitar URLs incorrectas
                print(f"📦 SERVICIO: Bucket configurado: {self.bucket_name}")
                print("✅ SERVICIO: Procediendo directamente con upload via HTTP")
                
                # Subir archivo al bucket
                print(f"📤 SERVICIO: Subiendo archivo: {unique_filename}")
                print(f"📦 SERVICIO: Bucket: {self.bucket_name}")
                print(f"📏 SERVICIO: Tamaño datos: {len(image_data)} bytes")
                
                try:
                    # Usar directamente la API HTTP de Supabase Storage ya que el cliente tiene problemas con URLs
                    from app.config.settings import settings
                    import httpx
                    
                    storage_url = f"{settings.supabase_url}/storage/v1"
                    upload_url = f"{storage_url}/object/{self.bucket_name}/{unique_filename}"
                    
                    print(f"🌐 SERVICIO: URL directa para upload: {upload_url}")
                    
                    headers = {
                        "Authorization": f"Bearer {settings.supabase_service_role_key}",
                        "Content-Type": content_type,
                        "Cache-Control": "3600"
                    }
                    
                    print(f"🔐 SERVICIO: Headers: {headers}")
                    
                    # Hacer request HTTP directo
                    with httpx.Client(timeout=30.0) as client:
                        response = client.post(upload_url, content=image_data, headers=headers)
                        
                        print(f"🌐 SERVICIO: Status code: {response.status_code}")
                        print(f"🌐 SERVICIO: Response headers: {dict(response.headers)}")
                        print(f"🌐 SERVICIO: Response text: {response.text}")
                        
                        if response.status_code == 200:
                            print("✅ SERVICIO: Upload directo exitoso")
                            try:
                                response_data = response.json()
                                print(f"� SERVICIO: Response JSON: {response_data}")
                            except:
                                print("📊 SERVICIO: Response no es JSON válido")
                                response_data = {"message": "Upload successful"}
                                
                        elif response.status_code == 409:
                            print("⚠️ SERVICIO: Archivo ya existe, intentando con upsert...")
                            # Intentar con upsert usando PUT
                            put_response = client.put(upload_url, content=image_data, headers=headers)
                            print(f"� SERVICIO: PUT Status: {put_response.status_code}")
                            print(f"🔄 SERVICIO: PUT Response: {put_response.text}")
                            
                            if put_response.status_code in [200, 201]:
                                print("✅ SERVICIO: Upload con PUT exitoso")
                                response = put_response
                                try:
                                    response_data = response.json()
                                except:
                                    response_data = {"message": "Upload successful"}
                            else:
                                raise Exception(f"Upload falló con PUT: {put_response.status_code} - {put_response.text}")
                        
                        elif response.status_code in [400, 404]:
                            print(f"❌ SERVICIO: Error del cliente: {response.status_code}")
                            print(f"🔍 SERVICIO: Posible problema con bucket o permisos")
                            
                            # Verificar si el bucket existe usando GET
                            bucket_check_url = f"{storage_url}/bucket/{self.bucket_name}"
                            bucket_response = client.get(bucket_check_url, headers={
                                "Authorization": f"Bearer {settings.supabase_service_role_key}"
                            })
                            print(f"🔍 SERVICIO: Bucket check status: {bucket_response.status_code}")
                            print(f"🔍 SERVICIO: Bucket check response: {bucket_response.text}")
                            
                            raise Exception(f"Upload falló: {response.status_code} - {response.text}")
                        
                        else:
                            raise Exception(f"Upload falló: {response.status_code} - {response.text}")
                        
                except Exception as upload_exception:
                    print(f"❌ SERVICIO: Exception en upload directo: {str(upload_exception)}")
                    print(f"🔍 SERVICIO: Exception type: {type(upload_exception).__name__}")
                    
                    if hasattr(upload_exception, 'args') and upload_exception.args:
                        print(f"📝 SERVICIO: Exception args: {upload_exception.args}")
                    
                    # Re-lanzar la excepción
                    raise upload_exception
                
                print(f"✅ SERVICIO: Imagen subida exitosamente")
                
                # Obtener URL pública directamente, sin usar el cliente de Supabase
                from app.config.settings import settings
                public_url = f"{settings.supabase_url}/storage/v1/object/public/{self.bucket_name}/{unique_filename}"
                print(f"🔗 SERVICIO: URL pública construida: {public_url}")
                
                # Verificar que la URL pública funciona
                try:
                    import httpx
                    with httpx.Client(timeout=10.0) as client:
                        test_response = client.head(public_url)
                        print(f"� SERVICIO: Test URL pública - Status: {test_response.status_code}")
                        if test_response.status_code == 200:
                            print("✅ SERVICIO: URL pública accesible")
                        else:
                            print(f"⚠️ SERVICIO: URL pública retorna: {test_response.status_code}")
                except Exception as test_error:
                    print(f"⚠️ SERVICIO: No se pudo verificar URL pública: {str(test_error)}")
                    # Continuar de todos modos
                
                # Actualizar tabla perfiles con la nueva imagen
                profile_updated = False
                try:
                    print("💾 SERVICIO: Actualizando tabla perfiles...")
                    print(f"👤 SERVICIO: user_id para actualizar: {user_id}")
                    print(f"🔗 SERVICIO: URL para guardar: {public_url}")
                    
                    # USAR CLIENTE ADMIN para evitar problemas de RLS
                    print("🔐 SERVICIO: Usando cliente admin para actualizar perfiles...")
                    
                    # Primero verificar si el perfil existe
                    print("🔍 SERVICIO: Verificando si el perfil existe...")
                    check_response = supabase_admin.table('perfiles')\
                        .select('id, imagen_perfil')\
                        .eq('id', user_id)\
                        .execute()
                    
                    print(f"📊 SERVICIO: Perfiles encontrados: {len(check_response.data)}")
                    if check_response.data:
                        existing_profile = check_response.data[0]
                        print(f"✅ SERVICIO: Perfil existe - ID: {existing_profile.get('id')}")
                        print(f"🖼️ SERVICIO: Imagen actual: {existing_profile.get('imagen_perfil', 'NULL')}")
                    else:
                        print("❌ SERVICIO: No se encontró perfil existente")
                    
                    # Intentar actualizar el perfil existente CON CLIENTE ADMIN
                    print("🔄 SERVICIO: Intentando actualizar perfil con admin...")
                    update_response = supabase_admin.table('perfiles')\
                        .update({'imagen_perfil': public_url})\
                        .eq('id', user_id)\
                        .execute()
                    
                    print(f"📊 SERVICIO: Respuesta update - data: {update_response.data}")
                    print(f"📊 SERVICIO: Respuesta update - count: {getattr(update_response, 'count', 'N/A')}")
                    profile_updated = len(update_response.data) > 0
                    print(f"✅ SERVICIO: Filas actualizadas: {len(update_response.data)}")
                    
                    if profile_updated:
                        print("🎉 SERVICIO: Perfil actualizado exitosamente")
                        # Verificar que realmente se actualizó
                        verify_response = supabase_admin.table('perfiles')\
                            .select('imagen_perfil')\
                            .eq('id', user_id)\
                            .execute()
                        
                        if verify_response.data:
                            updated_url = verify_response.data[0].get('imagen_perfil')
                            print(f"✅ SERVICIO: Verificación - URL guardada: {updated_url}")
                            if updated_url == public_url:
                                print("🎯 SERVICIO: URL coincide perfectamente")
                            else:
                                print("⚠️ SERVICIO: URL no coincide exactamente")
                    
                    if not profile_updated:
                        print("🔄 SERVICIO: Update falló, intentando crear perfil...")
                        try:
                            print(f"➕ SERVICIO: Creando perfil para user_id: {user_id}")
                            create_response = supabase_admin.table('perfiles')\
                                .insert({
                                    'id': user_id, 
                                    'imagen_perfil': public_url
                                })\
                                .execute()
                            
                            print(f"📊 SERVICIO: Respuesta create - data: {create_response.data}")
                            profile_updated = len(create_response.data) > 0
                            
                            if profile_updated:
                                print("🎉 SERVICIO: Perfil creado exitosamente")
                            else:
                                print("❌ SERVICIO: No se pudo crear el perfil")
                                
                        except Exception as create_error:
                            print(f"❌ SERVICIO: Error creando perfil: {str(create_error)}")
                            print(f"🔍 SERVICIO: Tipo error create: {type(create_error).__name__}")
                            
                            # Verificar si es problema de foreign key
                            if "violates foreign key" in str(create_error).lower():
                                print("🔑 SERVICIO: Error FK - el user_id no existe en auth.users")
                            
                            profile_updated = False
                    
                except Exception as update_error:
                    print(f"❌ SERVICIO: Error en actualización de perfil: {str(update_error)}")
                    print(f"🔍 SERVICIO: Tipo de error update: {type(update_error).__name__}")
                    
                    # Análisis específico del error
                    error_str = str(update_error).lower()
                    if "relation" in error_str and "does not exist" in error_str:
                        print("📋 SERVICIO: La tabla 'perfiles' no existe")
                    elif "column" in error_str and "does not exist" in error_str:
                        print("📋 SERVICIO: La columna 'imagen_perfil' no existe")
                    elif "violates" in error_str:
                        print("🔑 SERVICIO: Violación de constraaint de BD")
                    
                    profile_updated = False
                
                result = {
                    "url": unique_filename,
                    "public_url": public_url,
                    "file_name": file_name or f"profile_image{extension}",
                    "profile_updated": profile_updated
                }
                
                print("✅ SERVICIO: Upload completado exitosamente")
                print(f"🔍 === SERVICIO: Fin upload ===")
                return result
                
            except Exception as upload_error:
                print(f"❌ SERVICIO: Error en upload a bucket: {str(upload_error)}")
                print(f"🔍 SERVICIO: Tipo de error upload: {type(upload_error).__name__}")
                
                # Intentar obtener más detalles del error
                error_detail = str(upload_error)
                
                if hasattr(upload_error, 'message'):
                    print(f"📝 SERVICIO: Error message: {upload_error.message}")
                    error_detail = upload_error.message
                elif hasattr(upload_error, 'detail'):
                    print(f"📝 SERVICIO: Error detail: {upload_error.detail}")
                    error_detail = upload_error.detail
                elif hasattr(upload_error, 'args') and upload_error.args:
                    print(f"📝 SERVICIO: Error args: {upload_error.args}")
                    error_detail = str(upload_error.args[0]) if upload_error.args else str(upload_error)
                
                # Si es KeyError, mostrar qué clave falta
                if isinstance(upload_error, KeyError):
                    print(f"� SERVICIO: KeyError - Clave faltante: {upload_error}")
                    error_detail = f"Clave faltante en respuesta de Supabase: {upload_error}"
                
                # Información adicional para debugging
                print(f"📋 SERVICIO: Dir del error: {[attr for attr in dir(upload_error) if not attr.startswith('_')]}")
                
                # Verificar si es problema de bucket
                if "404" in str(upload_error) or "Not Found" in str(upload_error):
                    error_detail = f"Bucket '{self.bucket_name}' no encontrado o no accesible. Verificar configuración de Supabase Storage."
                elif "401" in str(upload_error) or "Unauthorized" in str(upload_error):
                    error_detail = f"Sin permisos para acceder al bucket '{self.bucket_name}'. Verificar SERVICE_ROLE_KEY."
                elif "403" in str(upload_error) or "Forbidden" in str(upload_error):
                    error_detail = f"Operación prohibida en bucket '{self.bucket_name}'. Verificar políticas RLS del bucket."
                    
                raise Exception(f"Error subiendo imagen a bucket: {error_detail}")
                
        except Exception as e:
            print(f"❌ SERVICIO: Error general: {str(e)}")
            print(f"🔍 SERVICIO: Tipo de error general: {type(e).__name__}")
            print(f"🔍 === SERVICIO: Fin upload (ERROR) ===")
            raise Exception(f"Error en upload de imagen de perfil: {str(e)}")

# Instancia global del servicio
image_service = ImageService()
