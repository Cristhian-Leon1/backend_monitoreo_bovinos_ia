# 🚀 Guía de Despliegue en Render

## 📋 Archivos Necesarios

**SOLO necesitas estos archivos en tu repositorio:**
- ✅ `requirements.txt` (OBLIGATORIO - lista de dependencias)
- ✅ `runtime.txt` (RECOMENDADO - versión de Python)
- ✅ Todo tu código en `/app/`

**NO necesitas:** Procfile, render.yaml, build.sh, start.sh (se configuran en el dashboard)

## 🚀 Pasos para Desplegar en Render

### 1. Preparación del Repositorio

Asegúrate de que tienes estos archivos en GitHub:
- ✅ `requirements.txt`
- ✅ `runtime.txt` 
- ✅ Tu aplicación en `/app/`
- ✅ `.env.example` (plantilla de variables)

### 2. Crear Cuenta en Render

1. Ve a [render.com](https://render.com)
2. Regístrate con tu cuenta de GitHub
3. Autoriza el acceso a tus repositorios

### 3. Crear Nuevo Web Service

1. En el dashboard de Render, click "New +"
2. Selecciona "Web Service"
3. Conecta tu repositorio GitHub
4. Selecciona el repositorio `backend_monitoreo_bovinos_ia`

### 4. Configuración del Servicio

**Configuración Básica:**
- **Name**: `backend-monitoreo-bovinos-ia`
- **Region**: `Oregon (US West)` o el más cercano
- **Branch**: `main`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Plan:**
- Selecciona el plan gratuito para empezar

### 5. Variables de Entorno

En la sección "Environment Variables", agrega:

```
SUPABASE_URL=https://txmwxmonhadrnivthzkh.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR4bXd4bW9uaGFkcm5pdnRoemtoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYzMjI1ODksImV4cCI6MjA3MTg5ODU4OX0.9u-elC3451i9JXdm3QpgsocHYRr6nkbxSGVwvFs032Y
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR4bXd4bW9uaGFkcm5pdnRoemtoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjMyMjU4OSwiZXhwIjoyMDcxODk4NTg5fQ.Hi1k0DVY-Thb6Hy_NjxnDSCyUDHGyIr4MxfHuSpDgQo
SECRET_KEY=monitoreo_bovinos_IA_super_secret_key_2025_secure_production
APP_NAME=Monitoreo Bovinos IA Backend
APP_VERSION=1.0.0
DEBUG=False
BUCKET_NAME=monitoreo_bovinos_IA
```

### 6. Configuración Avanzada

**Auto-Deploy:**
- ✅ Habilitar auto-deploy desde `main` branch

**Health Check:**
- **Health Check Path**: `/health`

### 7. Desplegar

1. Click "Create Web Service"
2. Render automáticamente:
   - Clonará tu repositorio
   - Instalará dependencias
   - Ejecutará el build
   - Iniciará tu aplicación

### 8. Verificar Despliegue

Una vez completado:
- Tu API estará disponible en: `https://tu-app.onrender.com`
- Documentación: `https://tu-app.onrender.com/docs`
- Health check: `https://tu-app.onrender.com/health`

## 🔧 Solución de Problemas

### Build Failures
- Verificar `requirements.txt`
- Revisar logs de build en Render

### Start Failures
- Verificar variables de entorno
- Revisar logs de aplicación

### Database Connection
- Verificar credenciales de Supabase
- Confirmar que Supabase permite conexiones externas

## 📊 Monitoreo

Render proporciona:
- ✅ Logs en tiempo real
- ✅ Métricas de CPU/Memoria
- ✅ Health checks automáticos
- ✅ SSL certificates automáticos

## 🔄 Actualizaciones

Para actualizar tu aplicación:
1. Push cambios a `main` branch
2. Render automáticamente detectará y desplegará

## 💰 Costos

**Plan Gratuito:**
- 750 horas/mes
- Aplicación se duerme después de 15 min sin uso
- Perfecto para desarrollo y demos

**Plan Pagado:**
- $7/mes por servicio
- Sin hibernación
- Mejor para producción
