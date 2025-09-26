from fastapi import APIRouter
from app.views import (
    auth_views,
    finca_views,
    bovino_views,
    medicion_views,
    image_views
)

# Router principal para todas las rutas de la API
api_router = APIRouter()

# Incluir todas las vistas
api_router.include_router(auth_views.router)
api_router.include_router(finca_views.router)
api_router.include_router(bovino_views.router)
api_router.include_router(medicion_views.router)
api_router.include_router(image_views.router)
