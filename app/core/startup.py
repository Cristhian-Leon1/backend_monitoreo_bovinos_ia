"""
Sistema de inicialización con feedback visual para el servidor
"""
import logging
from typing import Dict, Any

# Configurar colores para terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_status(message: str, status: bool = True, emoji_success: str = "✅", emoji_error: str = "❌"):
    """Imprime un mensaje de estado con color y emoji"""
    if status:
        print(f"{Colors.GREEN}{emoji_success} {message}{Colors.RESET}")
    else:
        print(f"{Colors.RED}{emoji_error} {message}{Colors.RESET}")

def print_info(message: str, emoji: str = "📋"):
    """Imprime información general"""
    print(f"{Colors.CYAN}{emoji} {message}{Colors.RESET}")

def print_warning(message: str, emoji: str = "⚠️"):
    """Imprime una advertencia"""
    print(f"{Colors.YELLOW}{emoji} {message}{Colors.RESET}")

def print_header():
    """Imprime el header del sistema"""
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}🐄 BACKEND MONITOREO BOVINOS IA - INICIANDO 🤖{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*60}{Colors.RESET}\n")

async def check_database_connection():
    """Verifica la conexión a la base de datos"""
    try:
        from app.config.database import supabase, supabase_admin
        
        print_info("Verificando conexión a base de datos...")
        
        # Test conexión regular
        try:
            result = supabase.table("perfiles").select("id").limit(1).execute()
            print_status("Conexión a Supabase (usuario): OK")
        except Exception as e:
            print_status(f"Conexión a Supabase (usuario): Error - {str(e)[:50]}", False)
            return False
        
        # Test conexión admin
        try:
            buckets = supabase_admin.storage.list_buckets()
            print_status("Conexión a Supabase (admin): OK")
        except Exception as e:
            print_status(f"Conexión a Supabase (admin): Error - {str(e)[:50]}", False)
            return False
            
        return True
        
    except Exception as e:
        print_status(f"Error en verificación de BD: {str(e)[:50]}", False)
        return False

async def check_environment_variables():
    """Verifica las variables de entorno"""
    try:
        from app.config.settings import settings
        
        print_info("Verificando variables de entorno...")
        
        # Verificar variables críticas
        if not settings.supabase_url:
            print_status("Variable SUPABASE_URL: No encontrada", False)
            return False
        print_status("Variable SUPABASE_URL: OK")
        
        if not settings.supabase_anon_key:
            print_status("Variable SUPABASE_ANON_KEY: No encontrada", False)
            return False
        print_status("Variable SUPABASE_ANON_KEY: OK")
        
        if not settings.supabase_service_role_key:
            print_status("Variable SUPABASE_SERVICE_ROLE_KEY: No encontrada", False)
            return False
        print_status("Variable SUPABASE_SERVICE_ROLE_KEY: OK")
        
        if not settings.secret_key:
            print_status("Variable SECRET_KEY: No encontrada", False)
            return False
        print_status("Variable SECRET_KEY: OK")
        
        return True
        
    except Exception as e:
        print_status(f"Error verificando variables: {str(e)[:50]}", False)
        return False

async def check_models():
    """Verifica los modelos Pydantic"""
    try:
        print_info("Verificando modelos de datos...")
        
        from app.models.auth_models import PerfilResponse
        from app.models.finca_models import FincaResponse
        from app.models.bovino_models import BovinoResponse
        from app.models.medicion_models import MedicionResponse
        
        print_status("Modelo Perfil: OK")
        print_status("Modelo Finca: OK")
        print_status("Modelo Bovino: OK")
        print_status("Modelo Medicion: OK")
        
        # Resolver referencias
        from app.models.resolver_models import resolve_model_references
        resolve_model_references()
        print_status("Referencias de modelos: Resueltas")
        
        return True
        
    except Exception as e:
        print_status(f"Error en modelos: {str(e)[:50]}", False)
        return False

async def check_routes():
    """Verifica que las rutas estén cargadas"""
    try:
        print_info("Verificando rutas de la API...")
        
        from app.views.api_router import api_router
        
        route_count = len(api_router.routes)
        if route_count > 0:
            print_status(f"Rutas de API: {route_count} endpoints cargados")
            return True
        else:
            print_status("Rutas de API: No se encontraron rutas", False)
            return False
            
    except Exception as e:
        print_status(f"Error verificando rutas: {str(e)[:50]}", False)
        return False

async def startup_checks() -> Dict[str, bool]:
    """Ejecuta todas las verificaciones de inicio"""
    print_header()
    
    results = {}
    
    # Verificar variables de entorno
    results['env'] = await check_environment_variables()
    
    # Verificar modelos
    results['models'] = await check_models()
    
    # Verificar rutas
    results['routes'] = await check_routes()
    
    # Verificar base de datos
    results['database'] = await check_database_connection()
    
    # Resumen final
    print(f"\n{Colors.BOLD}{Colors.BLUE}📊 RESUMEN DE INICIALIZACIÓN:{Colors.RESET}")
    
    all_good = True
    for service, status in results.items():
        service_names = {
            'env': 'Variables de entorno',
            'models': 'Modelos de datos',
            'routes': 'Rutas de API',
            'database': 'Base de datos'
        }
        print_status(f"{service_names[service]}: {'Funcionando' if status else 'Con errores'}", status)
        if not status:
            all_good = False
    
    if all_good:
        print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 ¡TODOS LOS SERVICIOS INICIADOS CORRECTAMENTE!{Colors.RESET}")
        print(f"{Colors.GREEN}🚀 Servidor listo para recibir peticiones{Colors.RESET}\n")
    else:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}⚠️  ALGUNOS SERVICIOS TIENEN PROBLEMAS{Colors.RESET}")
        print(f"{Colors.YELLOW}🔧 El servidor puede funcionar con limitaciones{Colors.RESET}\n")
    
    return results
