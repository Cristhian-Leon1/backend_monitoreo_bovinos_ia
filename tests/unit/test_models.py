"""
Test de modelos Pydantic
========================

Verifica que los modelos de datos funcionen correctamente.
"""
import pytest
import uuid
from datetime import datetime
from app.models.auth import PerfilCreate, PerfilResponse, UserRegister, UserLogin
from app.models.finca import FincaCreate, FincaResponse
from app.models.bovino import BovinoCreate, BovinoResponse
from app.models.medicion import MedicionCreate, MedicionResponse


@pytest.mark.unit
class TestAuthModels:
    """Tests para modelos de autenticación"""
    
    def test_user_register_valid(self):
        """Test de registro de usuario válido"""
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "nombre_completo": "Usuario Test"
        }
        user = UserRegister(**user_data)
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.nombre_completo == "Usuario Test"
    
    def test_user_register_invalid_email(self):
        """Test de registro con email inválido"""
        with pytest.raises(ValueError):
            UserRegister(email="invalid-email", password="password123")
    
    def test_user_register_short_password(self):
        """Test de registro con contraseña muy corta"""
        with pytest.raises(ValueError):
            UserRegister(email="test@example.com", password="123")


class TestFincaModels:
    """Tests para modelos de finca"""
    
    def test_finca_create_valid(self):
        """Test de creación de finca válida"""
        finca_data = {"nombre": "Finca Test"}
        finca = FincaCreate(**finca_data)
        assert finca.nombre == "Finca Test"
    
    def test_finca_create_empty_name(self):
        """Test de creación de finca con nombre vacío"""
        with pytest.raises(ValueError):
            FincaCreate(nombre="")


class TestBovinoModels:
    """Tests para modelos de bovino"""
    
    def test_bovino_create_valid(self):
        """Test de creación de bovino válido"""
        bovino_data = {
            "id_bovino": "COW001",
            "sexo": "M",
            "raza": "Holstein",
            "finca_id": str(uuid.uuid4())
        }
        bovino = BovinoCreate(**bovino_data)
        assert bovino.id_bovino == "COW001"
        assert bovino.sexo == "M"
        assert bovino.raza == "Holstein"
    
    def test_bovino_invalid_sex(self):
        """Test de bovino con sexo inválido"""
        with pytest.raises(ValueError):
            BovinoCreate(
                id_bovino="COW001",
                sexo="X",  # Inválido
                finca_id=str(uuid.uuid4())
            )
