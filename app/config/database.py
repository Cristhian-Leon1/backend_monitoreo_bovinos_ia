from supabase import create_client, Client
from supabase.client import ClientOptions
from app.config.settings import settings
import ssl
import httpx

# Configurar opciones del cliente
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

http_client = httpx.Client(verify=False)

client_options = ClientOptions(
    httpx_client=http_client,
    schema="public"
)

# ✅ Cliente anon - SOLO para autenticación temporal
try:
    supabase: Client = create_client(
        settings.supabase_url,
        settings.supabase_anon_key,
        options=client_options
    )
    print(f"✅ Cliente Supabase anon creado")
except Exception as e:
    print(f"Error creando cliente Supabase: {e}")
    supabase: Client = create_client(
        settings.supabase_url,
        settings.supabase_anon_key
    )

# ✅ Cliente admin - Para TODAS las operaciones de datos
try:
    supabase_admin: Client = create_client(
        settings.supabase_url,
        settings.supabase_service_role_key,
        options=client_options
    )
    print(f"✅ Cliente Supabase admin creado")
except Exception as e:
    print(f"Error creando cliente Supabase admin: {e}")
    supabase_admin: Client = create_client(
        settings.supabase_url,
        settings.supabase_service_role_key
    )