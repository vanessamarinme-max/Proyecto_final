import certifi
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Obtener configuración
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "HuellitasDeAmor")

# Crear conexión
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

# Seleccionar base de datos
db = client[DATABASE_NAME]


def probar_conexion():
    try:
        client.admin.command("ping")
        print("Conexión exitosa con MongoDB")
        print("Base de datos:", DATABASE_NAME)
        return True

    except Exception as error:
        print("Error de conexión:", error)
        return False
