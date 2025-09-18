from supabase import create_client, Client
from supabase.client import ClientOptions
from app.config.settings import settings
import ssl
import httpx

# Configurar opciones del cliente para manejar SSL de manera más robusta
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Cliente HTTP con SSL configurado
http_client = httpx.Client(verify=False)

# Opciones del cliente
client_options = ClientOptions(
    httpx_client=http_client,
    schema="public"
)

# Cliente de Supabase
try:
    supabase: Client = create_client(
        settings.supabase_url,
        settings.supabase_anon_key,
        options=client_options
    )
    print(f"✅ Cliente Supabase creado exitosamente")
    print(f"   URL base: {settings.supabase_url}")
    print(f"   Storage endpoint: {settings.supabase_url}/storage/v1")
except Exception as e:
    print(f"Error creando cliente Supabase: {e}")
    # Fallback sin opciones específicas
    supabase: Client = create_client(
        settings.supabase_url,
        settings.supabase_anon_key
    )

# Cliente de Supabase con permisos de servicio (para operaciones administrativas)
try:
    supabase_admin: Client = create_client(
        settings.supabase_url,
        settings.supabase_service_role_key,
        options=client_options
    )
    print(f"✅ Cliente Supabase admin creado exitosamente")
except Exception as e:
    print(f"Error creando cliente Supabase admin: {e}")
    # Fallback sin opciones específicas
    supabase_admin: Client = create_client(
        settings.supabase_url,
        settings.supabase_service_role_key
    )
