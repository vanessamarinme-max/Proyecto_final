from flask import Blueprint, request, jsonify
from bson import ObjectId
from pymongo.errors import PyMongoError

from config import db
from utils.helpers import convertir_json


crud_bp = Blueprint("crud_bp", __name__)

# Colecciones permitidas
COLECCIONES = [
    "adoptantes",
    "perros",
    "tienda",
    "registrosVeterinarios",
    "seguimientosPostAdopcion",
    "solicitudesAdopcion",
]


# =====================================
# VALIDAR COLECCION
# =====================================

def obtener_coleccion(nombre):

    if nombre not in COLECCIONES:
        return None

    return db[nombre]


# =====================================
# CREATE - CREAR REGISTRO (CON SEPARACIÓN AUTOMÁTICA)
# =====================================

@crud_bp.route("/api/<nombre>", methods=["POST"])
def crear_registro(nombre):

    coleccion = obtener_coleccion(nombre)

    if coleccion is None:
        return jsonify({"error": "Colección no válida"}), 404

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict) or not datos:
        return jsonify({"error": "Debes enviar datos válidos"}), 400

    try:
        # Convertir referencias terminadas en _id
        for campo, valor in datos.items():

            if campo.endswith("_id") and valor:
                if not ObjectId.is_valid(valor):
                    return jsonify({
                        "error": f"El identificador {campo} no es válido"
                    }), 400

                datos[campo] = ObjectId(valor)

        # ========================================================
        # LÓGICA ESPECIAL: SI ES SOLICITUD DE ADOPCIÓN
        # Separamos y guardamos al adoptante en su propia colección
        # ========================================================
        if nombre == "solicitudesAdopcion":
            documento_adoptante = datos.get("documento")

            if documento_adoptante:
                # Estructura de los datos que irán a la colección 'adoptantes'
                datos_adoptante = {
                    "nombre": datos.get("nombre"),
                    "documento": documento_adoptante,
                    "correo": datos.get("correo"),
                    "celular": datos.get("celular"),
                    "tipo_vivienda": datos.get("tipo_vivienda"),
                    "cantidad_mascotas": datos.get("cantidad_mascotas")
                }

                coleccion_adoptantes = db["adoptantes"]
                
                # Buscamos si el adoptante ya existe por su número de documento
                adoptante_existente = coleccion_adoptantes.find_one({"documento": documento_adoptante})

                if adoptante_existente:
                    # Si ya existe, actualizamos sus datos por si cambió de teléfono o correo
                    adoptante_id = adoptante_existente["_id"]
                    coleccion_adoptantes.update_one(
                        {"_id": adoptante_id},
                        {"$set": datos_adoptante}
                    )
                else:
                    # Si es nuevo, lo insertamos en la colección 'adoptantes'
                    resultado_adoptante = coleccion_adoptantes.insert_one(datos_adoptante)
                    adoptante_id = resultado_adoptante.inserted_id

                # Guardamos la relación (ObjectId) dentro de la solicitud de adopción
                datos["adoptante_id"] = adoptante_id

        # Insertamos el registro principal en su respectiva colección
        resultado = coleccion.insert_one(datos)

        return jsonify({
            "mensaje": "Registro creado y datos separados correctamente",
            "id": str(resultado.inserted_id)
        }), 201

    except PyMongoError as error:
        return jsonify({"error": str(error)}), 500


# =====================================
# READ - CONSULTAR TODOS
# =====================================

@crud_bp.route("/api/<nombre>", methods=["GET"])
def consultar_registros(nombre):

    coleccion = obtener_coleccion(nombre)

    if coleccion is None:
        return jsonify({"error": "Colección no válida"}), 404

    try:
        registros = list(coleccion.find())

        return jsonify(convertir_json(registros)), 200

    except PyMongoError as error:
        return jsonify({"error": str(error)}), 500


# =====================================
# READ - CONSULTAR UNO POR ID
# =====================================

@crud_bp.route("/api/<nombre>/<identificador>", methods=["GET"])
def consultar_registro(nombre, identificador):

    coleccion = obtener_coleccion(nombre)

    if coleccion is None:
        return jsonify({"error": "Colección no válida"}), 404

    if not ObjectId.is_valid(identificador):
        return jsonify({"error": "Identificador no válido"}), 400

    try:
        registro = coleccion.find_one({
            "_id": ObjectId(identificador)
        })

        if registro is None:
            return jsonify({"error": "Registro no encontrado"}), 404

        return jsonify(convertir_json(registro)), 200

    except PyMongoError as error:
        return jsonify({"error": str(error)}), 500


# =====================================
# UPDATE - ACTUALIZAR REGISTRO
# =====================================

@crud_bp.route("/api/<nombre>/<identificador>", methods=["PUT"])
def actualizar_registro(nombre, identificador):

    coleccion = obtener_coleccion(nombre)

    if coleccion is None:
        return jsonify({"error": "Colección no válida"}), 404

    if not ObjectId.is_valid(identificador):
        return jsonify({"error": "Identificador no válido"}), 400

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict) or not datos:
        return jsonify({"error": "Debes enviar datos para actualizar"}), 400

    # Evitar modificar el identificador
    datos.pop("_id", None)

    try:
        for campo, valor in datos.items():

            if campo.endswith("_id") and valor:
                if not ObjectId.is_valid(valor):
                    return jsonify({
                        "error": f"El identificador {campo} no es válido"
                    }), 400

                datos[campo] = ObjectId(valor)

        resultado = coleccion.update_one(
            {"_id": ObjectId(identificador)},
            {"$set": datos}
        )

        if resultado.matched_count == 0:
            return jsonify({"error": "Registro no encontrado"}), 404

        return jsonify({
            "mensaje": "Registro actualizado correctamente"
        }), 200

    except PyMongoError as error:
        return jsonify({"error": str(error)}), 500


# =====================================
# DELETE - ELIMINAR REGISTRO
# =====================================

@crud_bp.route("/api/<nombre>/<identificador>", methods=["DELETE"])
def eliminar_registro(nombre, identificador):

    coleccion = obtener_coleccion(nombre)

    if coleccion is None:
        return jsonify({"error": "Colección no válida"}), 404

    if not ObjectId.is_valid(identificador):
        return jsonify({"error": "Identificador no válido"}), 400

    try:
        resultado = coleccion.delete_one({
            "_id": ObjectId(identificador)
        })

        if resultado.deleted_count == 0:
            return jsonify({"error": "Registro no encontrado"}), 404

        return jsonify({
            "mensaje": "Registro eliminado correctamente"
        }), 200

    except PyMongoError as error:
        return jsonify({"error": str(error)}), 500
