# 🐄 Backend Monitoreo Bovinos IA 🤖

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-orange.svg)](https://supabase.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Sistema completo de monitoreo de ganado bovino con inteligencia artificial.**

Backend desarrollado con **arquitectura MVC**, **FastAPI** y **Supabase** para el monitoreo inteligente y automatizado de ganado bovino, proporcionando análisis de datos en tiempo real y gestión integral de fincas.

## 🚀 Características Principales

- 🔐 **Autenticación JWT** con Supabase Auth
- 📊 **API RESTful** completa con documentación automática
- 🐄 **Gestión de Bovinos** con tracking completo
- 🏡 **Administración de Fincas** multi-usuario
- 📈 **Mediciones y Análisis** de datos bovinos
- 🧪 **Suite de Tests** completa (Unit, Integration, E2E)
- 🎨 **Sistema de Arranque Visual** con feedback en tiempo real
- 📱 **Documentación Interactiva** con Swagger/OpenAPI

## 📁 Estructura del Proyecto

```
backend_monitoreo_bovinos_IA/
├── 📁 app/                    # Código principal (Arquitectura MVC)
│   ├── 📁 config/            # Configuraciones de la aplicación
│   ├── 📁 controllers/       # Controladores (Lógica de negocio)
│   ├── 📁 core/             # Sistema de arranque y configuración core
│   ├── 📁 middleware/       # Middlewares personalizados
│   ├── 📁 models/           # Modelos de datos (Pydantic)
│   ├── 📁 services/         # Servicios de negocio
│   ├── 📁 views/            # Rutas y endpoints de la API
│   └── 📄 main.py           # Aplicación principal FastAPI
├── 📁 tests/                 # Suite completa de pruebas
│   ├── 📁 unit/             # Pruebas unitarias
│   ├── 📁 integration/      # Pruebas de integración
│   ├── 📁 e2e/             # Pruebas end-to-end
│   └── 📄 conftest.py      # Configuración de pytest
├── 📄 .env.example          # Plantilla de variables de entorno
├── 📄 .gitignore            # Configuración de archivos ignorados
├── 📄 pyproject.toml        # Configuración del proyecto Python
├── 📄 requirements.txt      # Dependencias del proyecto
├── 📄 run.py               # Script de ejecución del servidor
└── 📄 run_tests.py         # Script de ejecución de tests
```

## 🛠️ Tecnologías

| Categoría | Tecnología | Versión | Propósito |
|-----------|------------|---------|-----------|
| **Framework** | FastAPI | 0.104+ | API REST de alto rendimiento |
| **Base de Datos** | PostgreSQL | Latest | Base de datos relacional (via Supabase) |
| **ORM/Cliente** | Supabase | 2.0+ | Cliente de base de datos y autenticación |
| **Validación** | Pydantic | 2.5+ | Validación de datos y modelos |
| **Testing** | pytest | Latest | Framework de testing |
| **Servidor** | Uvicorn | 0.24+ | Servidor ASGI |
| **Autenticación** | JWT | - | Tokens de autenticación |
| **Storage** | Supabase Storage | - | Almacenamiento de archivos |

## ⚡ Inicio Rápido

### 1. Prerrequisitos

- Python 3.11 o superior
- Cuenta en [Supabase](https://supabase.com)
- Git

### 2. Clonar el repositorio

```bash
git clone https://github.com/Cristhian-Leon1/backend_monitoreo_bovinos_ia.git
cd backend_monitoreo_bovinos_IA
```

### 3. Configurar entorno virtual

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

```bash
# Copiar plantilla de configuración
cp .env.example .env

# Editar .env con tus credenciales de Supabase
# SUPABASE_URL=tu_url_de_supabase
# SUPABASE_ANON_KEY=tu_clave_anonima
# SUPABASE_SERVICE_ROLE_KEY=tu_clave_de_servicio
# SECRET_KEY=tu_clave_secreta_super_segura
```

### 6. Ejecutar el servidor

```bash
# Iniciar servidor con arranque visual
python run.py

# El servidor estará disponible en:
# http://localhost:8000
```

## 🧪 Ejecutar Tests

### Ejecutar todos los tests
```bash
python run_tests.py
```

### Ejecutar tests específicos
```bash
# Tests unitarios
python run_tests.py unit

# Tests de integración
python run_tests.py integration

# Tests end-to-end
python run_tests.py e2e
```

### Ejecutar con pytest directamente
```bash
# Todos los tests
pytest tests/

# Tests específicos
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Con cobertura
pytest tests/ --cov=app
```

## 📖 API Endpoints

### Documentación Interactiva

Una vez que el servidor esté ejecutándose:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Salud del sistema |
| `GET` | `/health` | Estado del servidor |
| `POST` | `/auth/login` | Iniciar sesión |
| `POST` | `/auth/register` | Registrar usuario |
| `GET` | `/fincas/` | Listar fincas |
| `POST` | `/fincas/` | Crear finca |
| `GET` | `/bovinos/` | Listar bovinos |
| `POST` | `/bovinos/` | Registrar bovino |
| `GET` | `/mediciones/` | Obtener mediciones |
| `POST` | `/mediciones/` | Crear medición |

## 🏗️ Arquitectura

### Patrón MVC (Model-View-Controller)

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   MODELS    │◄──►│ CONTROLLERS  │◄──►│    VIEWS    │
│  (Pydantic) │    │   (Lógica)   │    │   (Rutas)   │
└─────────────┘    └──────────────┘    └─────────────┘
       ▲                   ▲                   ▲
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  SERVICES   │    │ MIDDLEWARE   │    │   CONFIG    │
│ (Supabase)  │    │ (Auth/CORS)  │    │ (Settings)  │
└─────────────┘    └──────────────┘    └─────────────┘
```

### Base de Datos (Supabase)

- **perfiles**: Información de usuarios
- **fincas**: Datos de las fincas
- **bovinos**: Registro de ganado
- **mediciones**: Datos de monitoreo
- **Storage**: Imágenes y archivos

## 🔒 Seguridad

### Configuraciones de Seguridad Implementadas

- ✅ **Variables de entorno** protegidas (.env ignorado en Git)
- ✅ **Autenticación JWT** con tokens seguros
- ✅ **Row Level Security (RLS)** en Supabase
- ✅ **Validación de datos** con Pydantic
- ✅ **CORS configurado** para dominios específicos
- ✅ **Sanitización de inputs** automática
- ✅ **Rate limiting** implementado
- ✅ **Headers de seguridad** configurados

### Archivos Sensibles Protegidos

El `.gitignore` está configurado para proteger:
- Archivos `.env` y credenciales
- Claves API y tokens
- Certificados y llaves privadas
- Archivos de configuración sensibles

## 🤝 Contribuir

### Proceso de Contribución

1. **Fork** el repositorio
2. **Crear** una nueva rama (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** los cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Crear** un Pull Request

### Estándares de Código

- Seguir **PEP 8** para estilo de código Python
- Escribir **tests** para nuevas funcionalidades
- Documentar **funciones y clases**
- Usar **type hints** en Python

## 📝 Changelog

### [1.0.0] - 2025-08-28

#### Agregado
- ✅ Arquitectura MVC completa
- ✅ Autenticación JWT con Supabase
- ✅ CRUD completo para Fincas, Bovinos y Mediciones
- ✅ Sistema de arranque visual
- ✅ Suite completa de tests (Unit, Integration, E2E)
- ✅ Documentación interactiva con Swagger
- ✅ Configuración de seguridad robusta

## 📞 Soporte y Contacto

### Reportar Problemas

- **Issues**: [GitHub Issues](https://github.com/Cristhian-Leon1/backend_monitoreo_bovinos_ia/issues)
- **Bugs**: Usar la plantilla de bug report
- **Características**: Usar la plantilla de feature request

### Documentación Adicional

- 📚 **[Wiki del Proyecto](https://github.com/Cristhian-Leon1/backend_monitoreo_bovinos_ia/wiki)**
- 🔗 **[API Reference](http://localhost:8000/docs)** (servidor corriendo)
- 📖 **[Guía de Desarrollo](docs/DEVELOPMENT.md)**

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

<div align="center">

**Desarrollado con ❤️ para el monitoreo inteligente de ganado bovino**

[![GitHub](https://img.shields.io/badge/GitHub-Cristhian--Leon1-black.svg)](https://github.com/Cristhian-Leon1)
[![Supabase](https://img.shields.io/badge/Powered_by-Supabase-green.svg)](https://supabase.com)
[![FastAPI](https://img.shields.io/badge/Built_with-FastAPI-009485.svg)](https://fastapi.tiangolo.com)

</div>
