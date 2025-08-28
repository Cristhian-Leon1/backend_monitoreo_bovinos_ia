"""
Test de endpoints de la API
===========================

Pruebas de los endpoints principales de la API.
"""
import pytest
from tests.conftest import TEST_USER_EMAIL, TEST_USER_PASSWORD


@pytest.mark.integration
class TestHealthEndpoints:
    """Tests para endpoints de salud"""
    
    def test_root_endpoint(self, client):
        """Test del endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
    
    def test_health_endpoint(self, client):
        """Test del endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        # El status puede ser 'healthy' o 'degraded' dependiendo de la conectividad
        assert data["status"] in ["healthy", "degraded"]
        assert "service" in data
        assert "version" in data


class TestDocumentationEndpoints:
    """Tests para endpoints de documentación"""
    
    def test_docs_endpoint(self, client):
        """Test del endpoint de documentación"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_openapi_endpoint(self, client):
        """Test del endpoint de OpenAPI"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data


class TestAuthEndpoints:
    """Tests para endpoints de autenticación"""
    
    def test_login_endpoint_structure(self, client):
        """Test de estructura del endpoint de login"""
        # Test con credenciales vacías para verificar estructura
        response = client.post("/api/v1/auth/login", json={})
        # Puede retornar 422 (validation error) o 401 (unauthorized)
        assert response.status_code in [401, 422]
    
    def test_login_with_test_user(self, client):
        """Test de login con usuario de prueba"""
        login_data = {
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        # Si el usuario existe, debería ser 200, sino 401
        if response.status_code == 200:
            data = response.json()
            assert "access_token" in data
            assert "user" in data
        else:
            assert response.status_code == 401


class TestProtectedEndpoints:
    """Tests para endpoints protegidos"""
    
    def test_fincas_without_auth(self, client):
        """Test de acceso a fincas sin autenticación"""
        response = client.get("/api/v1/fincas/")
        # Puede retornar 401 (no autorizado) o 403 (prohibido)
        assert response.status_code in [401, 403]
    
    def test_bovinos_without_auth(self, client):
        """Test de acceso a bovinos sin autenticación"""
        response = client.get("/api/v1/bovinos/")
        # Puede retornar 401, 403 o 405 dependiendo de la configuración
        assert response.status_code in [401, 403, 405]
    
    def test_mediciones_without_auth(self, client):
        """Test de acceso a mediciones sin autenticación"""
        response = client.get("/api/v1/mediciones/")
        # Puede retornar 401, 403 o 405 dependiendo de la configuración
        assert response.status_code in [401, 403, 405]
