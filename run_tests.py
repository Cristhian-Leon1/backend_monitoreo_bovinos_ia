#!/usr/bin/env python3
"""
🧪 Script para ejecutar tests del Backend de Monitoreo Bovino con IA
Ejecuta todas las pruebas con configuración optimizada y reporte detallado
"""

import subprocess
import sys
import os
from pathlib import Path

def print_banner():
    """Muestra el banner de inicio de tests"""
    print("\n" + "="*60)
    print("🧪 EJECUTANDO TESTS - BACKEND MONITOREO BOVINO IA 🐄")
    print("="*60)

def run_tests():
    """Ejecuta todos los tests con pytest"""
    try:
        # Configurar variables de entorno para tests
        test_env = os.environ.copy()
        test_env['PYTHONPATH'] = str(Path(__file__).parent)
        
        print("\n🔍 Ejecutando suite completa de tests...")
        
        # Comando pytest con configuración optimizada
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",  # Verbose
            "--tb=short",  # Traceback corto
            "--strict-markers",  # Strict markers
            "--disable-warnings",  # Deshabilitar warnings
            "-x",  # Parar en el primer error
            "--color=yes"  # Colorear output
        ]
        
        # Ejecutar tests
        result = subprocess.run(cmd, env=test_env, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("\n✅ ¡Todos los tests pasaron exitosamente!")
            print("🎉 El backend está funcionando correctamente")
        else:
            print("\n❌ Algunos tests fallaron")
            print("🔧 Revisa los errores anteriores")
            
        return result.returncode
        
    except Exception as e:
        print(f"\n💥 Error ejecutando tests: {e}")
        return 1

def run_specific_test_type(test_type):
    """Ejecuta un tipo específico de test"""
    valid_types = ['unit', 'integration', 'e2e']
    
    if test_type not in valid_types:
        print(f"❌ Tipo de test inválido: {test_type}")
        print(f"Tipos válidos: {', '.join(valid_types)}")
        return 1
    
    try:
        test_env = os.environ.copy()
        test_env['PYTHONPATH'] = str(Path(__file__).parent)
        
        print(f"\n🎯 Ejecutando tests {test_type.upper()}...")
        
        cmd = [
            sys.executable, "-m", "pytest",
            f"tests/{test_type}/",
            "-v",
            "--tb=short",
            "--disable-warnings",
            "--color=yes"
        ]
        
        result = subprocess.run(cmd, env=test_env, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(f"\n✅ Tests {test_type.upper()} completados exitosamente!")
        else:
            print(f"\n❌ Tests {test_type.upper()} fallaron")
            
        return result.returncode
        
    except Exception as e:
        print(f"\n💥 Error ejecutando tests {test_type}: {e}")
        return 1

def main():
    """Función principal"""
    print_banner()
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        return run_specific_test_type(test_type)
    else:
        return run_tests()

if __name__ == "__main__":
    print("\n🚀 Iniciando sistema de tests...")
    exit_code = main()
    print(f"\n📊 Tests completados con código: {exit_code}")
    sys.exit(exit_code)
