"""API de incidencias de la empresa ficticia TechSupport.

API sencilla para gestionar incidencias informáticas, desarrollada con
FastAPI. Los datos se guardan en memoria (una lista de Python), por lo que
se pierden al reiniciar el servidor.

Endpoints disponibles:
    GET /: Comprueba que la API está operativa.
    GET /incidencias: Lista todas las incidencias.
    GET /incidencias/{id}: Consulta una incidencia.
    POST /incidencias: Crea una incidencia.
    PUT /incidencias/{id}: Modifica una incidencia.
    DELETE /incidencias/{id}: Elimina una incidencia (requiere token).
"""

import os

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env (si existe) al entorno.
load_dotenv()

#: Token de administrador leído de la variable de entorno ADMIN_TOKEN.
#: Es necesario para eliminar incidencias. Vale None si no está definido.
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

#: Instancia principal de la aplicación FastAPI.
app = FastAPI(title="API de incidencias")


class Incidencia(BaseModel):
    """Modelo completo de una incidencia, tal como se devuelve en las respuestas.

    Attributes:
        id: Identificador único de la incidencia.
        titulo: Título breve de la incidencia.
        descripcion: Descripción detallada del problema.
        estado: Estado actual (por ejemplo, "abierta").
        prioridad: Prioridad asignada (por ejemplo, "alta").
        tecnico: Nombre del técnico responsable.
    """

    id: int
    titulo: str
    descripcion: str
    estado: str
    prioridad: str
    tecnico: str

#: Almacén en memoria de las incidencias. Contiene una incidencia de ejemplo.
incidencias: list[Incidencia] = [
    Incidencia(
        id=1,
        titulo="No arranca el ordenador 12",
        descripcion="El equipo no muestra imagen",
        estado="abierta",
        prioridad="alta",
        tecnico="Ana",
    )
]

class IncidenciaActualizar(BaseModel):
    """Datos necesarios para modificar una incidencia existente (PUT).

    Todos los campos son obligatorios porque la modificación reemplaza la
    incidencia completa. El id no se puede cambiar.

    Attributes:
        titulo: Nuevo título de la incidencia.
        descripcion: Nueva descripción del problema.
        estado: Nuevo estado de la incidencia.
        prioridad: Nueva prioridad.
        tecnico: Nuevo técnico responsable.
    """

    titulo: str
    descripcion: str
    estado: str
    prioridad: str
    tecnico: str

class IncidenciaCrear(BaseModel):
    """Datos necesarios para crear una incidencia nueva (POST).

    No incluye el id porque lo genera la propia API.

    Attributes:
        titulo: Título de la incidencia.
        descripcion: Descripción del problema.
        estado: Estado inicial. Por defecto "abierta".
        prioridad: Prioridad de la incidencia.
        tecnico: Técnico al que se asigna.
    """

    titulo: str
    descripcion: str
    estado: str = "abierta"
    prioridad: str
    tecnico: str

@app.get("/")
def inicio():
    """Comprueba que la API está funcionando.

    Returns:
        dict: Diccionario con un mensaje de estado.
    """
    return {"mensaje": "API de incidencias operativa"}


@app.get("/incidencias", response_model=list[Incidencia])
def listar_incidencias():
    """Devuelve todas las incidencias almacenadas.

    Returns:
        list[Incidencia]: Lista con todas las incidencias (puede estar vacía).
    """

    return incidencias

@app.put("/incidencias/{id}", response_model=Incidencia)
def modificar_incidencia(id: int, datos: IncidenciaActualizar):
    """Modifica por completo una incidencia existente.

    Busca la incidencia por su id y la sustituye por una nueva con los datos
    recibidos, conservando el mismo identificador.

    Args:
        id: Identificador de la incidencia a modificar.
        datos: Nuevos datos de la incidencia.

    Returns:
        Incidencia: La incidencia ya actualizada.

    Raises:
        HTTPException: Con código 404 si no existe ninguna incidencia con ese id.
    """

    # Se guarda también la posición para poder reemplazar el elemento.
    for posicion, incidencia in enumerate(incidencias):
        if incidencia.id == id:
            actualizada = Incidencia(id=id, **datos.model_dump())
            incidencias[posicion] = actualizada
            return actualizada
    # Si el bucle termina sin encontrar el id, la incidencia no existe.
    raise HTTPException(status_code=404, detail=f"No existe la incidencia con id {id}")


@app.delete("/incidencias/{id}")
def eliminar_incidencia(id: int, x_admin_token: str | None = Header(default=None)):
    """Elimina una incidencia. Operación reservada a administradores.

    El token se envía en la cabecera HTTP X-Admin-Token y debe coincidir con
    el valor de la variable de entorno ADMIN_TOKEN.

    Args:
        id: Identificador de la incidencia a eliminar.
        x_admin_token: Token de administrador recibido en la cabecera
            X-Admin-Token.

    Returns:
        dict: Diccionario con un mensaje de confirmación.

    Raises:
        HTTPException: Con código 500 si ADMIN_TOKEN no está configurado en
            el servidor.
        HTTPException: Con código 403 si el token recibido no es válido.
        HTTPException: Con código 404 si no existe ninguna incidencia con ese id.
    """

    # Si el servidor no tiene token configurado, no se permite borrar nada.
    if not ADMIN_TOKEN:
        raise HTTPException(status_code=500, detail="ADMIN_TOKEN no configurado en el entorno")
    # El token de la cabecera debe coincidir con el configurado.
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Token de administrador no válido")
    for posicion, incidencia in enumerate(incidencias):
        if incidencia.id == id:
            incidencias.pop(posicion)
            return {"mensaje": f"Incidencia {id} eliminada"}
    raise HTTPException(status_code=404, detail=f"No existe la incidencia con id {id}")

@app.get("/incidencias/{id}", response_model=Incidencia)
def obtener_incidencia(id: int):
    """Devuelve una incidencia concreta a partir de su identificador.

    Args:
        id: Identificador de la incidencia que se quiere consultar.

    Returns:
        Incidencia: La incidencia encontrada.

    Raises:
        HTTPException: Con código 404 si no existe ninguna incidencia con ese id.
    """

    for incidencia in incidencias:
        if incidencia.id == id:
            return incidencia
    raise HTTPException(status_code=404, detail=f"No existe la incidencia con id {id}")

@app.post("/incidencias", response_model=Incidencia, status_code=201)
def crear_incidencia(datos: IncidenciaCrear):
    """Crea una nueva incidencia y la añade al almacén.

    El identificador se genera automáticamente: es el mayor id existente más
    uno (o 1 si todavía no hay incidencias).

    Args:
        datos: Datos de la incidencia a crear.

    Returns:
        Incidencia: La incidencia creada, con su id asignado (código HTTP 201).
    """

    # max() con default=0 evita un error cuando la lista está vacía.
    nuevo_id = max((i.id for i in incidencias), default=0) + 1
    nueva = Incidencia(id=nuevo_id, **datos.model_dump())
    incidencias.append(nueva)
    return nueva