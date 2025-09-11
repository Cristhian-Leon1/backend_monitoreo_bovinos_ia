from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from app.config.settings import settings
from app.views.api import api_router
from app.core.startup import startup_checks, print_status, print_info
import logging
import time
import asyncio
import json
from decimal import Decimal
from datetime import datetime, date
import uuid

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variable global para almacenar resultados de startup
startup_results = {}

# JSON Encoder personalizado para manejar Decimals
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convertir Decimal a float
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)

# Función helper para respuestas JSON personalizadas
def custom_json_response(content, status_code: int = 200):
    """Crea una respuesta JSON usando el encoder personalizado"""
    return JSONResponse(
        content=json.loads(json.dumps(content, cls=CustomJSONEncoder)),
        status_code=status_code
    )

# Crear instancia de FastAPI
app = FastAPI(
    title=settings.app_name,
    description="Backend para el sistema de Monitoreo Bovinos con IA",
    version=settings.app_version,
    debug=settings.debug
)

# Eventos de ciclo de vida
@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar el servidor"""
    global startup_results
    startup_results = await startup_checks()

@app.on_event("shutdown")
async def shutdown_event():
    """Evento que se ejecuta al cerrar el servidor"""
    print_info("🛑 Cerrando servidor...")
    print_status("Servidor detenido correctamente", True, "👋")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejadores de errores globales ACTUALIZADOS
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Manejador personalizado para HTTPException"""
    content = {
        "error": True,
        "detail": exc.detail,
        "status_code": exc.status_code
    }
    return custom_json_response(content, exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Manejador para errores de validación"""
    content = {
        "error": True,
        "detail": "Error de validación",
        "errors": exc.errors()
    }
    return custom_json_response(content, 422)

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Manejador para errores generales"""
    logger.error(f"Error no manejado: {str(exc)}")
    content = {
        "error": True,
        "detail": "Error interno del servidor",
        "message": str(exc) if settings.debug else "Ha ocurrido un error inesperado"
    }
    return custom_json_response(content, 500)

# Rutas de salud y información ACTUALIZADAS
@app.get("/")
async def root():
    """Ruta raíz de la API"""
    content = {
        "message": "Bienvenido al Backend de Monitoreo Bovinos IA",
        "version": settings.app_version,
        "status": "running"
    }
    return custom_json_response(content)

@app.get("/health")
async def health_check():
    """Verificación de salud del servicio"""
    global startup_results
    
    # Estado general basado en los resultados de startup
    overall_status = "healthy"
    if startup_results:
        if not all(startup_results.values()):
            overall_status = "degraded"
    else:
        overall_status = "starting"
    
    content = {
        "status": overall_status,
        "service": settings.app_name,
        "version": settings.app_version,
        "services": startup_results if startup_results else "initializing"
    }
    return custom_json_response(content)

# Incluir todas las rutas de la API
app.include_router(api_router, prefix="/api/v1")

# Middleware personalizado para logging CON SOPORTE DECIMAL
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logging de requests"""
    start_time = time.time()
    
    # Log del request
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log de la respuesta
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - Time: {process_time:.4f}s")
    
    return response

# Middleware para manejar automáticamente las respuestas con Decimals
@app.middleware("http")
async def decimal_json_middleware(request: Request, call_next):
    """Middleware para convertir automáticamente respuestas con Decimals"""
    response = await call_next(request)
    
    # Si la respuesta es JSON y contiene datos, procesarla
    if (response.headers.get("content-type", "").startswith("application/json") and 
        hasattr(response, 'body')):
        try:
            # Solo procesar si no es una respuesta ya procesada por custom_json_response
            if not hasattr(response, '_custom_encoded'):
                body = response.body
                if body:
                    content = json.loads(body)
                    # Re-serializar usando nuestro encoder personalizado
                    new_body = json.dumps(content, cls=CustomJSONEncoder)
                    response.body = new_body.encode()
        except (json.JSONDecodeError, AttributeError):
            # Si no se puede decodificar o procesar, dejar la respuesta como está
            pass
    
    return response