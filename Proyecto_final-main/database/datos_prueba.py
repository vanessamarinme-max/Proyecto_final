import certifi
from pymongo import MongoClient

# 1. Reemplaza con tu URI real de MongoDB Atlas
MONGO_URI = "mongodb+srv://samuelsalazarmo_db_user:vFLbpXoIA83mE5sw@huellitasdeamor.wuoxemk.mongodb.net/"
# 2. Conectar al cliente
client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where()
)

db = client["HuellitasDeAmor"]

# Prueba de conexión rápida
try:
    print("Colecciones en la base de datos:", db.list_collection_names())
    print("¡Conexión exitosa!")
except Exception as e:
    print("Error:", e)

# 4. Datos a insertar (en Python usas diccionarios y listas)
refugios_data = [
    {
        "nombre": "Huellitas Felices",
        "direccion": "Medellín",
        "telefono": "3001234567",
        "correo": "huellitas@gmail.com"
    },
    {
        "nombre": "Amigos Peludos",
        "direccion": "Envigado",
        "telefono": "3007654321",
        "correo": "amigos@gmail.com"
    }
]

adoptantes_data = [
    {
        "nombre": "Carlos Pérez",
        "documento": "123456789",
        "telefono": "3001112233",
        "correo": "carlos@gmail.com",
        "direccion": "Medellín",
        "fechaRegistro": "2026-11-01"
    },
    {
        "nombre": "María Gómez",
        "documento": "987654321",
        "telefono": "3004445566",
        "correo": "maria@gmail.com",
        "direccion": "Envigado",
        "fechaRegistro": "2026-11-02"
    }
]

# 5. Insertar en las colecciones
res_refugios = db.refugios.insert_many(refugios_data)
print(f"Refugios insertados con IDs: {res_refugios.inserted_ids}")

res_adoptantes = db.adoptantes.insert_many(adoptantes_data)
print(f"Adoptantes insertados con IDs: {res_adoptantes.inserted_ids}")