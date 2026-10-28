# api-incidencias

API sencilla para gestionar incidencias informáticas de la empresa ficticia TechSupport, desarrollada con Python y FastAPI como proyecto integrador de RA6.f.

## Requisitos

- Git y una cuenta de GitHub con acceso al repositorio
- Clave SSH configurada en tu cuenta
- Python 3.12 o superior

## Puesta en marcha

1. Clonar el repositorio por SSH:

   git clone git@github.com:Roles-PruebaProyecto/api-incidencias.git
   cd api-incidencias

2. Crear y activar el entorno virtual (Git Bash en Windows):

   python -m venv .venv
   source .venv/Scripts/activate

   En Linux o macOS: source .venv/bin/activate

3. Instalar las dependencias:

   pip install -r requirements.txt

4. Crear tu archivo de configuración local a partir de la plantilla:

   cp .env.example .env

   Rellena ADMIN_TOKEN con un valor de prueba propio. El archivo .env no se sube nunca al repositorio.

5. Arrancar la API:

   uvicorn app.main:app --reload

6. Abrir la documentación interactiva en http://127.0.0.1:8000/docs

## Endpoints

| Método | Ruta | Función |
|---|---|---|
| GET | /incidencias | Listar todas las incidencias |
| GET | /incidencias/{id} | Consultar una incidencia |
| POST | /incidencias | Crear una incidencia |
| PUT | /incidencias/{id} | Modificar una incidencia |
| DELETE | /incidencias/{id} | Eliminar una incidencia (requiere ADMIN_TOKEN) |

## Estructura

app/main.py:       **Código de la API**
requirements.txt:  **Dependencias**
.env.example:      **Plantilla de configuración, sin secretos**
SECURITY.md:       **Política de seguridad**

## Flujo de trabajo

- main está protegida: no se escribe directamente en ella.
- Cada cambio parte de una Issue, se hace en una rama feature y entra mediante Pull Request revisada.

## Seguridad

No se suben contraseñas, tokens, claves privadas ni archivos .env reales. Consulta SECURITY.md para comunicar un problema de seguridad.