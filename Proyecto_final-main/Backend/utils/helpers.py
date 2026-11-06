
from bson import ObjectId
from datetime import datetime, date


def convertir_json(documento):

    if isinstance(documento, list):
        return [convertir_json(item) for item in documento]

    if isinstance(documento, dict):
        nuevo = {}

        for clave, valor in documento.items():

            if isinstance(valor, ObjectId):
                nuevo[clave] = str(valor)

            elif isinstance(valor, (datetime, date)):
                nuevo[clave] = valor.isoformat()

            else:
                nuevo[clave] = convertir_json(valor)

        return nuevo

    return documento
