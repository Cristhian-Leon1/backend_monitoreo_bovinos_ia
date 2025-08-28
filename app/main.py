from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.config.settings import settings
from app.views.api import api_router
from app.core.startup import startup_checks, print_status, print_info
import logging
import time
import asyncio

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variable global para almacenar resultados de startup
startup_results = {}

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

# Manejadores de errores globales
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Manejador personalizado para HTTPException"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Manejador para errores de validación"""
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "detail": "Error de validación",
            "errors": exc.errors()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Manejador para errores generales"""
    logger.error(f"Error no manejado: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "detail": "Error interno del servidor",
            "message": str(exc) if settings.debug else "Ha ocurrido un error inesperado"
        }
    )

# Rutas de salud y información
@app.get("/")
async def root():
    """Ruta raíz de la API"""
    return {
        "message": "Bienvenido al Backend de Monitoreo Bovinos IA",
        "version": settings.app_version,
        "status": "running"
    }

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
    
    return {
        "status": overall_status,
        "service": settings.app_name,
        "version": settings.app_version,
        "services": startup_results if startup_results else "initializing"
    }

# Incluir todas las rutas de la API
app.include_router(api_router, prefix="/api/v1")

# Middleware personalizado para logging
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
