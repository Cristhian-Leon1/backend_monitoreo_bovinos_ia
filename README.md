# 🐄 Monitoreo Bovinos IA - Sistema Completo 🤖

Sistema completo de monitoreo de ganado bovino con inteligencia artificial.

## 📁 Estructura del Proyecto

```
backend_monitoreo_bovinos_IA/
├── backend/                 # API Backend (FastAPI + Supabase)
├── .venv/                  # Entorno virtual Python (no incluido en repo)
└── README.md               # Este archivo
```

## 🚀 Inicio Rápido

### 1. Clonar el repositorio
```bash
git clone [tu-repo-url]
cd backend_monitoreo_bovinos_IA
```

### 2. Configurar el backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales de Supabase
```

### 4. Iniciar el backend
```bash
python run.py
```

## 📚 Documentación

- [Backend API](./backend/README.md) - Documentación completa del backend
- [API Docs](http://localhost:8000/docs) - Documentación interactiva (cuando el servidor esté corriendo)

## 🛠️ Tecnologías

- **Backend**: FastAPI, Python 3.11+
- **Base de datos**: PostgreSQL (Supabase)
- **Autenticación**: JWT con Supabase Auth
- **Storage**: Supabase Storage
- **Tests**: pytest
- **Documentación**: Swagger/OpenAPI

## 🔒 Seguridad

Este proyecto incluye:
- Variables de entorno protegidas
- Autenticación JWT
- Políticas de acceso a base de datos (RLS)
- Validación de datos con Pydantic
- Archivos sensibles excluidos del repositorio

## 📞 Soporte

Para reportar problemas o solicitar características, crear un issue en el repositorio.

---
Desarrollado con ❤️ para el monitoreo inteligente de ganado bovino
