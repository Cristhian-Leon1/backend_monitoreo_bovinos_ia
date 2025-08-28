from fastapi import APIRouter
from app.controllers import (
    auth_controller,
    finca_controller,
    bovino_controller,
    medicion_controller,
    image_controller
)

# Router principal para todas las rutas de la API
api_router = APIRouter()

# Incluir todos los controladores
api_router.include_router(auth_controller.router)
api_router.include_router(finca_controller.router)
api_router.include_router(bovino_controller.router)
api_router.include_router(medicion_controller.router)
api_router.include_router(image_controller.router)
