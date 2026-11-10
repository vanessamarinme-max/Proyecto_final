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
                datos_adoptante = {
                    "nombre": datos.get("nombre"),
                    "documento": documento_adoptante,
                    "correo": datos.get("correo"),
                    "celular": datos.get("celular"),
                    "tipo_vivienda": datos.get("tipo_vivienda"),
                    "cantidad_mascotas": datos.get("cantidad_mascotas")
                }

                coleccion_adoptantes = db["adoptantes"]
                
                adoptante_existente = coleccion_adoptantes.find_one({"documento": documento_adoptante})

                if adoptante_existente:
                    adoptante_id = adoptante_existente["_id"]
                    coleccion_adoptantes.update_one(
                        {"_id": adoptante_id},
                        {"$set": datos_adoptante}
                    )
                else:
                    resultado_adoptante = coleccion_adoptantes.insert_one(datos_adoptante)
                    adoptante_id = resultado_adoptante.inserted_id

                datos["adoptante_id"] = adoptante_id

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


# =====================================
# CONSULTAS ANALÍTICAS Y REPORTES (AGREGACIONES)
# =====================================

@crud_bp.route("/api/reportes/tienda-por-categoria", methods=["GET"])
def reporte_tienda_categoria():
    """Calcula el stock total y valor potencial del inventario agrupado por categoría en la tienda."""
    try:
        pipeline = [
            {
                "$group": {
                    "_id": "$categoria",
                    "total_stock": {"$sum": "$stock"},
                    "valor_inventario_potencial": {"$sum": {"$multiply": ["$precio", "$stock"]}},
                    "cantidad_productos": {"$sum": 1}
                }
            },
            {"$sort": {"valor_inventario_potencial": -1}}
        ]
        resultado = list(db["tienda"].aggregate(pipeline))
        return jsonify(convertir_json(resultado)), 200
    except PyMongoError as error:
        return jsonify({"error": str(error)}), 500


@crud_bp.route("/api/reportes/solicitudes-detalladas", methods=["GET"])
def reporte_solicitudes_detalladas():
    """Realiza un JOIN ($lookup) entre solicitudes de adopción y los datos del adoptante."""
    try:
        pipeline = [
            {
                "$lookup": {
                    "from": "adoptantes",
                    "localField": "adoptante_id",
                    "foreignField": "_id",
                    "as": "info_adoptante"
                }
            },
            {"$unwind": "$info_adoptante"}
        ]
        resultado = list(db["solicitudesAdopcion"].aggregate(pipeline))
        return jsonify(convertir_json(resultado)), 200
    except PyMongoError as error:
        return jsonify({"error": str(error)}), 500


@crud_bp.route("/api/reportes/perritos-por-tamano", methods=["GET"])
def reporte_perritos_tamano():
    """Agrupa y cuenta los perritos disponibles según su tamaño."""
    try:
        pipeline = [
            {
                "$group": {
                    "_id": "$tamano",
                    "total_perritos": {"$sum": 1}
                }
            },
            {"$sort": {"total_perritos": -1}}
        ]
        resultado = list(db["perros"].aggregate(pipeline))
        return jsonify(convertir_json(resultado)), 200
    except PyMongoError as error:
        return jsonify({"error": str(error)}), 500
