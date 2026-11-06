
from config import db
from datetime import datetime
from bson import ObjectId


# Colección de mascotas
coleccion_mascotas = db["mascotas"]


# CREAR MASCOTA
def crear_mascota(datos):

    mascota = {
        "nombre": datos.get("nombre"),
        "especie": datos.get("especie"),
        "edad": datos.get("edad"),
        "sexo": datos.get("sexo"),
        "descripcion": datos.get("descripcion"),
        "imagen": datos.get("imagen"),
        "estado": "Disponible",
        "fecha_registro": datetime.now()
    }

    resultado = coleccion_mascotas.insert_one(mascota)

    return str(resultado.inserted_id)


# CONSULTAR TODAS LAS MASCOTAS
def obtener_mascotas():

    mascotas = list(coleccion_mascotas.find())

    for mascota in mascotas:
        mascota["_id"] = str(mascota["_id"])

    return mascotas


# CONSULTAR MASCOTAS DISPONIBLES
def obtener_mascotas_disponibles():

    mascotas = list(
        coleccion_mascotas.find({"estado": "Disponible"})
    )

    for mascota in mascotas:
        mascota["_id"] = str(mascota["_id"])

    return mascotas


# CONSULTAR UNA MASCOTA POR ID
def obtener_mascota(id):

    if not ObjectId.is_valid(id):
        return None

    mascota = coleccion_mascotas.find_one({
        "_id": ObjectId(id)
    })

    if mascota:
        mascota["_id"] = str(mascota["_id"])

    return mascota


# ACTUALIZAR INFORMACIÓN DE UNA MASCOTA
def actualizar_mascota(id, datos):

    if not ObjectId.is_valid(id):
        return False

    datos_actualizados = {
        "nombre": datos.get("nombre"),
        "especie": datos.get("especie"),
        "edad": datos.get("edad"),
        "sexo": datos.get("sexo"),
        "descripcion": datos.get("descripcion"),
        "imagen": datos.get("imagen")
    }

    resultado = coleccion_mascotas.update_one(
        {"_id": ObjectId(id)},
        {"$set": datos_actualizados}
    )

    return resultado.matched_count > 0


# ACTUALIZAR ESTADO DE UNA MASCOTA
def actualizar_estado_mascota(id, nuevo_estado):

    if not ObjectId.is_valid(id):
        return False

    resultado = coleccion_mascotas.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"estado": nuevo_estado}}
    )

    return resultado.modified_count > 0


# ELIMINAR MASCOTA
def eliminar_mascota(id):

    if not ObjectId.is_valid(id):
        return False

    resultado = coleccion_mascotas.delete_one({
        "_id": ObjectId(id)
    })

    return resultado.deleted_count > 0
