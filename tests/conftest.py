"""
Configuración común para todos los tests
"""
import os
import sys
import pytest
from fastapi.testclient import TestClient

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

# Base URL para tests
TEST_BASE_URL = "http://localhost:8000"

# Cliente de pruebas para FastAPI
@pytest.fixture
def client():
    """Cliente de pruebas para FastAPI"""
    with TestClient(app) as test_client:
        yield test_client

# Configuraciones de test
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "password123"

# Headers comunes
def get_auth_headers(token: str) -> dict:
    """Obtiene headers de autenticación"""
    return {"Authorization": f"Bearer {token}"}

def get_json_headers() -> dict:
    """Obtiene headers para JSON"""
    return {"Content-Type": "application/json"}
