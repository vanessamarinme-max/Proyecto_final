
from config import db
from datetime import datetime
from bson import ObjectId


# Colección de adoptantes
coleccion_adoptantes = db["adoptantes"]


# CREAR ADOPTANTE
def crear_adoptante(datos):

    adoptante = {
        "nombre": datos.get("nombre"),
        "documento": datos.get("documento"),
        "telefono": datos.get("telefono"),
        "correo": datos.get("correo"),
        "direccion": datos.get("direccion"),
        "mascota": datos.get("mascota"),
        "vivienda": datos.get("vivienda"),
        "motivo": datos.get("motivo"),
        "estado_solicitud": "Pendiente",
        "fecha_solicitud": datetime.now()
    }

    resultado = coleccion_adoptantes.insert_one(adoptante)

    return str(resultado.inserted_id)


# CONSULTAR TODOS LOS ADOPTANTES
def obtener_adoptantes():

    adoptantes = list(coleccion_adoptantes.find())

    for adoptante in adoptantes:
        adoptante["_id"] = str(adoptante["_id"])

    return adoptantes


# CONSULTAR UN ADOPTANTE POR ID
def obtener_adoptante(id):

    if not ObjectId.is_valid(id):
        return None

    adoptante = coleccion_adoptantes.find_one({
        "_id": ObjectId(id)
    })

    if adoptante:
        adoptante["_id"] = str(adoptante["_id"])

    return adoptante


# ACTUALIZAR ESTADO DE SOLICITUD
def actualizar_estado(id, nuevo_estado):

    if not ObjectId.is_valid(id):
        return False

    resultado = coleccion_adoptantes.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"estado_solicitud": nuevo_estado}}
    )

    return resultado.modified_count > 0


# ELIMINAR ADOPTANTE
def eliminar_adoptante(id):

    if not ObjectId.is_valid(id):
        return False

    resultado = coleccion_adoptantes.delete_one({
        "_id": ObjectId(id)
    })

    return resultado.deleted_count > 0
