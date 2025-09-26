from supabase import Client
from app.config.database import supabase
from app.config.settings import settings
from typing import List, Dict, Any
import uuid
import base64
from datetime import datetime

class ImageController:
    def __init__(self, db_client: Client = supabase):
        self.db = db_client
        self.bucket_name = settings.bucket_name

    async def upload_profile_image_base64(self, image_base64: str, user_id: str, file_name: str = None) -> Dict[str, Any]:
        """Sube una imagen de perfil desde base64 y actualiza la tabla perfiles"""
        try:
            print(f"🔍 === CONTROLADOR: Iniciando upload ===")
            print(f"👤 user_id recibido: {user_id}")
            print(f"📄 file_name recibido: {file_name}")
            print(f"📏 Longitud image_base64: {len(image_base64) if image_base64 else 'None'}")
            
            # Validar que el base64 tenga el formato correcto
            if not image_base64:
                print("❌ CONTROLADOR: image_base64 está vacío o es None")
                raise Exception("image_base64 no puede estar vacío")
                
            if not image_base64.startswith('data:image/'):
                print(f"❌ CONTROLADOR: Formato incorrecto. Comienza con: {image_base64[:30]}...")
                raise Exception("Formato de imagen base64 inválido. Debe incluir el data URL completo.")
            
            print("✅ CONTROLADOR: Formato base64 inicial válido")
            
            # Extraer el tipo de contenido y los datos base64
            try:
                if ',' not in image_base64:
                    print("❌ CONTROLADOR: No se encontró coma separadora")
                    raise Exception("Formato base64 inválido: falta coma separadora")
                    
                header, encoded = image_base64.split(',', 1)
                print(f"📝 CONTROLADOR: Header extraído: {header}")
                print(f"📏 CONTROLADOR: Longitud datos encoded: {len(encoded)}")
                
                if ';' not in header or ':' not in header:
                    print(f"❌ CONTROLADOR: Header malformado: {header}")
                    raise Exception("Header base64 malformado")
                    
                content_type = header.split(';')[0].split(':')[1]
                print(f"📝 CONTROLADOR: Content-type detectado: {content_type}")
                
            except Exception as parse_error:
                print(f"❌ CONTROLADOR: Error parseando header: {str(parse_error)}")
                raise Exception(f"Error parseando header base64: {str(parse_error)}")
            
            # Validar tipo de contenido
            allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
            if content_type not in allowed_types:
                print(f"❌ CONTROLADOR: Tipo no permitido: {content_type}")
                print(f"📝 CONTROLADOR: Tipos permitidos: {allowed_types}")
                raise Exception(f"Tipo de imagen no permitido. Tipos válidos: {', '.join(allowed_types)}")
            
            print("✅ CONTROLADOR: Tipo de contenido válido")
            
            # Decodificar base64
            try:
                print("🔄 CONTROLADOR: Intentando decodificar base64...")
                image_data = base64.b64decode(encoded)
                print(f"📏 CONTROLADOR: Tamaño imagen decodificada: {len(image_data)} bytes")
            except Exception as decode_error:
                print(f"❌ CONTROLADOR: Error decodificando: {str(decode_error)}")
                print(f"📝 CONTROLADOR: Primeros 50 chars del encoded: {encoded[:50]}")
                raise Exception(f"Error decodificando imagen base64: {str(decode_error)}")
            
            # Validar tamaño (máximo 10MB)
            max_size = 10 * 1024 * 1024  # 10MB
            if len(image_data) > max_size:
                print(f"❌ CONTROLADOR: Imagen muy grande: {len(image_data)} bytes (máx: {max_size})")
                raise Exception("La imagen es demasiado grande. Máximo 10MB")
            
            print("✅ CONTROLADOR: Tamaño de imagen válido")
            
            # Validar que el user_id es un UUID válido
            try:
                uuid.UUID(user_id)
                print("✅ CONTROLADOR: user_id es UUID válido")
            except ValueError:
                print(f"❌ CONTROLADOR: user_id inválido: {user_id}")
                raise Exception(f"El user_id '{user_id}' no es un UUID válido")
            
            # Generar nombre único para el archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            extension = ".jpg" if content_type == "image/jpeg" else ".png"
            if content_type == "image/webp":
                extension = ".webp"
            
            unique_filename = f"perfiles/{user_id}_{timestamp}_{uuid.uuid4().hex[:8]}{extension}"
            print(f"📁 CONTROLADOR: Nombre archivo: {unique_filename}")
            
            # Usar el cliente admin para subir archivos
            from app.config.database import supabase_admin
            
            try:
                print("🚀 CONTROLADOR: Iniciando subida al bucket...")
                
                # Nota: Saltamos la verificación del bucket para evitar URLs incorrectas
                print(f"📦 CONTROLADOR: Bucket configurado: {self.bucket_name}")
                print("✅ CONTROLADOR: Procediendo directamente con upload via HTTP")
                
                # Subir archivo al bucket
                print(f"📤 CONTROLADOR: Subiendo archivo: {unique_filename}")
                print(f"📦 CONTROLADOR: Bucket: {self.bucket_name}")
                print(f"📏 CONTROLADOR: Tamaño datos: {len(image_data)} bytes")
                
                try:
                    # Usar directamente la API HTTP de Supabase Storage ya que el cliente tiene problemas con URLs
                    from app.config.settings import settings
                    import httpx
                    
                    storage_url = f"{settings.supabase_url}/storage/v1"
                    upload_url = f"{storage_url}/object/{self.bucket_name}/{unique_filename}"
                    
                    print(f"🌐 CONTROLADOR: URL directa para upload: {upload_url}")
                    
                    headers = {
                        "Authorization": f"Bearer {settings.supabase_service_role_key}",
                        "Content-Type": content_type,
                        "Cache-Control": "3600"
                    }
                    
                    print(f"🔐 CONTROLADOR: Headers: {headers}")
                    
                    # Hacer request HTTP directo
                    with httpx.Client(timeout=30.0) as client:
                        response = client.post(upload_url, content=image_data, headers=headers)
                        
                        print(f"🌐 CONTROLADOR: Status code: {response.status_code}")
                        print(f"🌐 CONTROLADOR: Response headers: {dict(response.headers)}")
                        print(f"🌐 CONTROLADOR: Response text: {response.text}")
                        
                        if response.status_code == 200:
                            print("✅ CONTROLADOR: Upload directo exitoso")
                            try:
                                response_data = response.json()
                                print(f"📊 CONTROLADOR: Response JSON: {response_data}")
                            except:
                                print("📊 CONTROLADOR: Response no es JSON válido")
                                response_data = {"message": "Upload successful"}
                                
                        elif response.status_code == 409:
                            print("⚠️ CONTROLADOR: Archivo ya existe, intentando con upsert...")
                            # Intentar con upsert usando PUT
                            put_response = client.put(upload_url, content=image_data, headers=headers)
                            print(f"🔄 CONTROLADOR: PUT Status: {put_response.status_code}")
                            print(f"🔄 CONTROLADOR: PUT Response: {put_response.text}")
                            
                            if put_response.status_code in [200, 201]:
                                print("✅ CONTROLADOR: Upload con PUT exitoso")
                                response = put_response
                                try:
                                    response_data = response.json()
                                except:
                                    response_data = {"message": "Upload successful"}
                            else:
                                raise Exception(f"Upload falló con PUT: {put_response.status_code} - {put_response.text}")
                        
                        elif response.status_code in [400, 404]:
                            print(f"❌ CONTROLADOR: Error del cliente: {response.status_code}")
                            print(f"🔍 CONTROLADOR: Posible problema con bucket o permisos")
                            
                            # Verificar si el bucket existe usando GET
                            bucket_check_url = f"{storage_url}/bucket/{self.bucket_name}"
                            bucket_response = client.get(bucket_check_url, headers={
                                "Authorization": f"Bearer {settings.supabase_service_role_key}"
                            })
                            print(f"🔍 CONTROLADOR: Bucket check status: {bucket_response.status_code}")
                            print(f"🔍 CONTROLADOR: Bucket check response: {bucket_response.text}")
                            
                            raise Exception(f"Upload falló: {response.status_code} - {response.text}")
                        
                        else:
                            raise Exception(f"Upload falló: {response.status_code} - {response.text}")
                        
                except Exception as upload_exception:
                    print(f"❌ CONTROLADOR: Exception en upload directo: {str(upload_exception)}")
                    print(f"🔍 CONTROLADOR: Exception type: {type(upload_exception).__name__}")
                    
                    if hasattr(upload_exception, 'args') and upload_exception.args:
                        print(f"📝 CONTROLADOR: Exception args: {upload_exception.args}")
                    
                    # Re-lanzar la excepción
                    raise upload_exception
                
                print(f"✅ CONTROLADOR: Imagen subida exitosamente")
                
                # Obtener URL pública directamente, sin usar el cliente de Supabase
                from app.config.settings import settings
                public_url = f"{settings.supabase_url}/storage/v1/object/public/{self.bucket_name}/{unique_filename}"
                print(f"🔗 CONTROLADOR: URL pública construida: {public_url}")
                
                # Verificar que la URL pública funciona
                try:
                    import httpx
                    with httpx.Client(timeout=10.0) as client:
                        test_response = client.head(public_url)
                        print(f"✅ CONTROLADOR: Test URL pública - Status: {test_response.status_code}")
                        if test_response.status_code == 200:
                            print("✅ CONTROLADOR: URL pública accesible")
                        else:
                            print(f"⚠️ CONTROLADOR: URL pública retorna: {test_response.status_code}")
                except Exception as test_error:
                    print(f"⚠️ CONTROLADOR: No se pudo verificar URL pública: {str(test_error)}")
                    # Continuar de todos modos
                
                # Actualizar tabla perfiles con la nueva imagen
                profile_updated = False
                try:
                    print("💾 CONTROLADOR: Actualizando tabla perfiles...")
                    print(f"👤 CONTROLADOR: user_id para actualizar: {user_id}")
                    print(f"🔗 CONTROLADOR: URL para guardar: {public_url}")
                    
                    # USAR CLIENTE ADMIN para evitar problemas de RLS
                    print("🔐 CONTROLADOR: Usando cliente admin para actualizar perfiles...")
                    
                    # Primero verificar si el perfil existe
                    print("🔍 CONTROLADOR: Verificando si el perfil existe...")
                    check_response = supabase_admin.table('perfiles')\
                        .select('id, imagen_perfil')\
                        .eq('id', user_id)\
                        .execute()
                    
                    print(f"📊 CONTROLADOR: Perfiles encontrados: {len(check_response.data)}")
                    if check_response.data:
                        existing_profile = check_response.data[0]
                        print(f"✅ CONTROLADOR: Perfil existe - ID: {existing_profile.get('id')}")
                        print(f"🖼️ CONTROLADOR: Imagen actual: {existing_profile.get('imagen_perfil', 'NULL')}")
                    else:
                        print("❌ CONTROLADOR: No se encontró perfil existente")
                    
                    # Intentar actualizar el perfil existente CON CLIENTE ADMIN
                    print("🔄 CONTROLADOR: Intentando actualizar perfil con admin...")
                    update_response = supabase_admin.table('perfiles')\
                        .update({'imagen_perfil': public_url})\
                        .eq('id', user_id)\
                        .execute()
                    
                    print(f"📊 CONTROLADOR: Respuesta update - data: {update_response.data}")
                    print(f"📊 CONTROLADOR: Respuesta update - count: {getattr(update_response, 'count', 'N/A')}")
                    profile_updated = len(update_response.data) > 0
                    print(f"✅ CONTROLADOR: Filas actualizadas: {len(update_response.data)}")
                    
                    if profile_updated:
                        print("🎉 CONTROLADOR: Perfil actualizado exitosamente")
                        # Verificar que realmente se actualizó
                        verify_response = supabase_admin.table('perfiles')\
                            .select('imagen_perfil')\
                            .eq('id', user_id)\
                            .execute()
                        
                        if verify_response.data:
                            updated_url = verify_response.data[0].get('imagen_perfil')
                            print(f"✅ CONTROLADOR: Verificación - URL guardada: {updated_url}")
                            if updated_url == public_url:
                                print("🎯 CONTROLADOR: URL coincide perfectamente")
                            else:
                                print("⚠️ CONTROLADOR: URL no coincide exactamente")
                    
                    if not profile_updated:
                        print("🔄 CONTROLADOR: Update falló, intentando crear perfil...")
                        try:
                            print(f"➕ CONTROLADOR: Creando perfil para user_id: {user_id}")
                            create_response = supabase_admin.table('perfiles')\
                                .insert({
                                    'id': user_id, 
                                    'imagen_perfil': public_url
                                })\
                                .execute()
                            
                            print(f"📊 CONTROLADOR: Respuesta create - data: {create_response.data}")
                            profile_updated = len(create_response.data) > 0
                            
                            if profile_updated:
                                print("🎉 CONTROLADOR: Perfil creado exitosamente")
                            else:
                                print("❌ CONTROLADOR: No se pudo crear el perfil")
                                
                        except Exception as create_error:
                            print(f"❌ CONTROLADOR: Error creando perfil: {str(create_error)}")
                            print(f"🔍 CONTROLADOR: Tipo error create: {type(create_error).__name__}")
                            
                            # Verificar si es problema de foreign key
                            if "violates foreign key" in str(create_error).lower():
                                print("🔑 CONTROLADOR: Error FK - el user_id no existe en auth.users")
                            
                            profile_updated = False
                    
                except Exception as update_error:
                    print(f"❌ CONTROLADOR: Error en actualización de perfil: {str(update_error)}")
                    print(f"🔍 CONTROLADOR: Tipo de error update: {type(update_error).__name__}")
                    
                    # Análisis específico del error
                    error_str = str(update_error).lower()
                    if "relation" in error_str and "does not exist" in error_str:
                        print("📋 CONTROLADOR: La tabla 'perfiles' no existe")
                    elif "column" in error_str and "does not exist" in error_str:
                        print("📋 CONTROLADOR: La columna 'imagen_perfil' no existe")
                    elif "violates" in error_str:
                        print("🔑 CONTROLADOR: Violación de constraaint de BD")
                    
                    profile_updated = False
                
                result = {
                    "url": unique_filename,
                    "public_url": public_url,
                    "file_name": file_name or f"profile_image{extension}",
                    "profile_updated": profile_updated
                }
                
                print("✅ CONTROLADOR: Upload completado exitosamente")
                print(f"🔍 === CONTROLADOR: Fin upload ===")
                return result
                
            except Exception as upload_error:
                print(f"❌ CONTROLADOR: Error en upload a bucket: {str(upload_error)}")
                print(f"🔍 CONTROLADOR: Tipo de error upload: {type(upload_error).__name__}")
                
                # Intentar obtener más detalles del error
                error_detail = str(upload_error)
                
                if hasattr(upload_error, 'message'):
                    print(f"📝 CONTROLADOR: Error message: {upload_error.message}")
                    error_detail = upload_error.message
                elif hasattr(upload_error, 'detail'):
                    print(f"📝 CONTROLADOR: Error detail: {upload_error.detail}")
                    error_detail = upload_error.detail
                elif hasattr(upload_error, 'args') and upload_error.args:
                    print(f"📝 CONTROLADOR: Error args: {upload_error.args}")
                    error_detail = str(upload_error.args[0]) if upload_error.args else str(upload_error)
                
                # Si es KeyError, mostrar qué clave falta
                if isinstance(upload_error, KeyError):
                    print(f"🗝️ CONTROLADOR: KeyError - Clave faltante: {upload_error}")
                    error_detail = f"Clave faltante en respuesta de Supabase: {upload_error}"
                
                # Información adicional para debugging
                print(f"📋 CONTROLADOR: Dir del error: {[attr for attr in dir(upload_error) if not attr.startswith('_')]}")
                
                # Verificar si es problema de bucket
                if "404" in str(upload_error) or "Not Found" in str(upload_error):
                    error_detail = f"Bucket '{self.bucket_name}' no encontrado o no accesible. Verificar configuración de Supabase Storage."
                elif "401" in str(upload_error) or "Unauthorized" in str(upload_error):
                    error_detail = f"Sin permisos para acceder al bucket '{self.bucket_name}'. Verificar SERVICE_ROLE_KEY."
                elif "403" in str(upload_error) or "Forbidden" in str(upload_error):
                    error_detail = f"Operación prohibida en bucket '{self.bucket_name}'. Verificar políticas RLS del bucket."
                    
                raise Exception(f"Error subiendo imagen a bucket: {error_detail}")
                
        except Exception as e:
            print(f"❌ CONTROLADOR: Error general: {str(e)}")
            print(f"🔍 CONTROLADOR: Tipo de error general: {type(e).__name__}")
            print(f"🔍 === CONTROLADOR: Fin upload (ERROR) ===")
            raise Exception(f"Error en upload de imagen de perfil: {str(e)}")

# Instancia global del controlador
image_controller = ImageController()
