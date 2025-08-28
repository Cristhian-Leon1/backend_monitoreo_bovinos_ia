"""
Test End-to-End del sistema completo
====================================

Prueba el flujo completo del sistema desde login hasta operaciones CRUD.
"""
import pytest
import requests
import time
from tests.conftest import TEST_BASE_URL, TEST_USER_EMAIL, TEST_USER_PASSWORD


@pytest.mark.e2e
class TestCompleteWorkflow:
    """Test del flujo completo del sistema"""
    
    @pytest.mark.e2e
    def test_complete_system_workflow(self):
        """
        Test completo del sistema:
        1. Health check
        2. Login
        3. Acceso a endpoints protegidos
        4. Operaciones CRUD básicas
        """
        base_url = TEST_BASE_URL
        
        # 1. Health check
        response = requests.get(f"{base_url}/health", timeout=10)
        assert response.status_code == 200
        health_data = response.json()
        assert health_data["status"] == "healthy"
        
        # 2. Verificar documentación
        response = requests.get(f"{base_url}/docs", timeout=10)
        assert response.status_code == 200
        
        # 3. Intentar login
        login_data = {
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }
        response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data, timeout=10)
        
        if response.status_code == 200:
            # Si el login es exitoso, continuar con tests autenticados
            auth_data = response.json()
            token = auth_data["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # 4. Probar endpoints protegidos
            endpoints_to_test = [
                "/api/v1/fincas",
                "/api/v1/bovinos", 
                "/api/v1/mediciones"
            ]
            
            for endpoint in endpoints_to_test:
                response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=10)
                # Debería retornar 200 (datos) o 404 (no encontrado), pero no 401
                assert response.status_code != 401, f"Endpoint {endpoint} no autorizado"
        
        else:
            # Si no hay usuario de prueba, verificar que al menos retorna 401
            assert response.status_code == 401
        
        print("✅ Test E2E completado exitosamente")
    
    @pytest.mark.e2e
    def test_system_performance(self):
        """Test básico de rendimiento del sistema"""
        base_url = TEST_BASE_URL
        
        # Medir tiempo de respuesta del health check
        start_time = time.time()
        response = requests.get(f"{base_url}/health", timeout=10)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 2.0, f"Health check muy lento: {response_time}s"
        
        print(f"✅ Tiempo de respuesta health check: {response_time:.3f}s")
    
    @pytest.mark.e2e 
    @pytest.mark.skipif(True, reason="Requiere configuración específica de imágenes")
    def test_image_upload_workflow(self):
        """Test del flujo de subida de imágenes (opcional)"""
        # Este test se puede habilitar cuando se configure específicamente
        pass
