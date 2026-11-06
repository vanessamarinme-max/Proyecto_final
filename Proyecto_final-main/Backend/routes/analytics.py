
from flask import Blueprint, jsonify
from pymongo.errors import PyMongoError

from config import db


analytics = Blueprint("analytics", __name__)


# =====================================
# 1. RESUMEN GENERAL
# =====================================

@analytics.route("/api/analitica/resumen", methods=["GET"])
def resumen_general():

    try:
        resultado = {
            "totalAdoptantes": db.adoptantes.count_documents({}),
            "totalPerros": db.perros.count_documents({}),
            "perrosDisponibles": db.perros.count_documents({
                "estado": "Disponible"
            }),
            "perrosAdoptados": db.perros.count_documents({
                "estado": "Adoptado"
            }),
            "totalRefugios": db.refugios.count_documents({}),
            "totalSolicitudes": db.solicitudesAdopcion.count_documents({})
        }

        return jsonify(resultado), 200

    except PyMongoError as error:
        return jsonify({"error": str(error)}), 500


# =====================================
# 2. SOLICITUDES POR ESTADO
# =====================================

@analytics.route("/api/analitica/solicitudes-estado", methods=["GET"])
def solicitudes_por_estado():

    try:

        pipeline = [

            {
                "$group": {
                    "_id": "$estado",
                    "cantidad": {"$sum": 1}
                }
            },

            {
                "$project": {
                    "_id": 0,
                    "estado": "$_id",
                    "cantidad": 1
                }
            },

            {
                "$sort": {
                    "cantidad": -1
                }
            }

        ]

        resultado = list(
            db.solicitudesAdopcion.aggregate(pipeline)
        )

        return jsonify(resultado), 200

    except PyMongoError as error:
        return jsonify({"error": str(error)}), 500


# =====================================
# 3. ADOPCIONES POR MES
# =====================================

@analytics.route("/api/analitica/adopciones-mes", methods=["GET"])
def adopciones_por_mes():

    try:

        pipeline = [

            {
                "$match": {
                    "estado": "Aprobada",
                    "fechaSolicitud": {"$type": "string"}
                }
            },

            {
                "$project": {
                    "mes": {
                        "$substr": ["$fechaSolicitud", 0, 7]
                    }
                }
            },

            {
                "$group": {
                    "_id": "$mes",
                    "totalAdopciones": {"$sum": 1}
                }
            },

            {
                "$sort": {
                    "_id": 1
                }
            },

            {
                "$project": {
                    "_id": 0,
                    "mes": "$_id",
                    "totalAdopciones": 1
                }
            }

        ]

        resultado = list(
            db.solicitudesAdopcion.aggregate(pipeline)
        )

        return jsonify(resultado), 200

    except PyMongoError as error:
        return jsonify({"error": str(error)}), 500


# =====================================
# 4. PERROS POR REFUGIO
# =====================================

@analytics.route("/api/analitica/perros-refugio", methods=["GET"])
def perros_por_refugio():

    try:

        pipeline = [

            {
                "$lookup": {
                    "from": "refugios",
                    "localField": "refugio_id",
                    "foreignField": "_id",
                    "as": "informacionRefugio"
                }
            },

            {
                "$unwind": {
                    "path": "$informacionRefugio",
                    "preserveNullAndEmptyArrays": False
                }
            },

            {
                "$group": {
                    "_id": "$informacionRefugio._id",
                    "nombreRefugio": {
                        "$first": "$informacionRefugio.nombre"
                    },
                    "totalPerros": {"$sum": 1},
                    "disponibles": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$estado", "Disponible"]},
                                1,
                                0
                            ]
                        }
                    },
                    "adoptados": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$estado", "Adoptado"]},
                                1,
                                0
                            ]
                        }
                    }
                }
            },

            {
                "$sort": {
                    "totalPerros": -1
                }
            },

            {
                "$project": {
                    "_id": 0,
                    "nombreRefugio": 1,
                    "totalPerros": 1,
                    "disponibles": 1,
                    "adoptados": 1
                }
            }

        ]

        resultado = list(db.perros.aggregate(pipeline))

        return jsonify(resultado), 200

    except PyMongoError as error:
        return jsonify({"error": str(error)}), 500


# =====================================
# 5. REGISTROS VETERINARIOS
# =====================================

@analytics.route("/api/analitica/atenciones-veterinarias", methods=["GET"])
def atenciones_veterinarias():

    try:

        pipeline = [

            {
                "$group": {
                    "_id": "$tipo",
                    "totalAtenciones": {"$sum": 1}
                }
            },

            {
                "$sort": {
                    "totalAtenciones": -1
                }
            },

            {
                "$limit": 10
            },

            {
                "$project": {
                    "_id": 0,
                    "tipoAtencion": "$_id",
                    "totalAtenciones": 1
                }
            }

        ]

        resultado = list(
            db.registrosVeterinarios.aggregate(pipeline)
        )

        return jsonify(resultado), 200

    except PyMongoError as error:
        return jsonify({"error": str(error)}), 500


# =====================================
# 6. SEGUIMIENTOS POST ADOPCION
# =====================================

@analytics.route("/api/analitica/seguimientos", methods=["GET"])
def analizar_seguimientos():

    try:

        pipeline = [

            {
                "$group": {
                    "_id": "$estado",
                    "cantidad": {"$sum": 1}
                }
            },

            {
                "$project": {
                    "_id": 0,
                    "estado": "$_id",
                    "cantidad": 1
                }
            },

            {
                "$sort": {
                    "cantidad": -1
                }
            }

        ]

        resultado = list(
            db.seguimientosPostAdopcion.aggregate(pipeline)
        )

        return jsonify(resultado), 200

    except PyMongoError as error:
        return jsonify({"error": str(error)}), 500


# =====================================
# 7. SOLICITUDES CON INFORMACION RELACIONADA
# =====================================

@analytics.route("/api/analitica/solicitudes-detalle", methods=["GET"])
def solicitudes_detalle():

    try:

        pipeline = [

            {
                "$lookup": {
                    "from": "adoptantes",
                    "localField": "adoptante_id",
                    "foreignField": "_id",
                    "as": "adoptante"
                }
            },

            {
                "$lookup": {
                    "from": "perros",
                    "localField": "perro_id",
                    "foreignField": "_id",
                    "as": "perro"
                }
            },

            {
                "$unwind": {
                    "path": "$adoptante",
                    "preserveNullAndEmptyArrays": True
                }
            },

            {
                "$unwind": {
                    "path": "$perro",
                    "preserveNullAndEmptyArrays": True
                }
            },

            {
                "$project": {
                    "_id": 0,
                    "estado": 1,
                    "fechaSolicitud": 1,
                    "motivo": 1,
                    "nombreAdoptante": "$adoptante.nombre",
                    "correoAdoptante": "$adoptante.correo",
                    "nombrePerro": "$perro.nombre"
                }
            },

            {
                "$sort": {
                    "fechaSolicitud": -1
                }
            }

        ]

        resultado = list(
            db.solicitudesAdopcion.aggregate(pipeline)
        )

        return jsonify(resultado), 200

    except PyMongoError as error:
        return jsonify({"error": str(error)}), 500
