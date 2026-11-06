
print("iniciando proceso")


from flask import Flask, jsonify
from flask_cors import CORS

from config import probar_conexion
from routes.crud import crud_bp
from routes.analytics import analytics


# Crear aplicación Flask
app = Flask(__name__)

# Permitir conexión con el frontend
CORS(app)


# Registrar rutas
app.register_blueprint(crud_bp)
app.register_blueprint(analytics)


# Página principal de la API
@app.route("/", methods=["GET"])
def inicio():

    return jsonify({
        "mensaje": "Bienvenido a Huellitas de Amor",
        "estado": "Servidor funcionando",
        "baseDatos": "HuellitasDeAmor"
    })


# Verificar funcionamiento del servidor
@app.route("/api/estado", methods=["GET"])
def estado():

    conexion = probar_conexion()

    if conexion:
        return jsonify({
            "servidor": "Funcionando",
            "mongodb": "Conectado"
        }), 200

    return jsonify({
        "servidor": "Funcionando",
        "mongodb": "Desconectado"
    }), 500


# Iniciar servidor
if __name__ == "__main__":
    print("iniciando servidor")
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
