"""
Test de configuración del sistema
================================

Verifica que la configuración del sistema esté correcta.
"""
import pytest
from app.config.settings import settings
from app.config.database import supabase, supabase_admin


@pytest.mark.unit
class TestConfiguration:
    """Tests de configuración del sistema"""
    
    def test_environment_variables(self):
        """Verifica que las variables de entorno estén configuradas"""
        assert settings.supabase_url is not None
        assert settings.supabase_anon_key is not None
        assert settings.supabase_service_role_key is not None
        assert settings.secret_key is not None
        assert settings.app_name is not None
        
    def test_supabase_url_format(self):
        """Verifica que la URL de Supabase tenga el formato correcto"""
        assert settings.supabase_url.startswith("https://")
        assert ".supabase.co" in settings.supabase_url
        
    def test_database_clients_creation(self):
        """Verifica que los clientes de base de datos se puedan crear"""
        assert supabase is not None
        assert supabase_admin is not None
        
    def test_app_settings(self):
        """Verifica configuración de la aplicación"""
        assert settings.app_name == "Monitoreo Bovinos IA Backend"
        assert settings.app_version == "1.0.0"
        assert isinstance(settings.debug, bool)
        assert isinstance(settings.host, str)
        assert isinstance(settings.port, int)
