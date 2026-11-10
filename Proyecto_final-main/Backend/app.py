print("iniciando proceso")

from flask import Flask, jsonify, request
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


# =====================================
# RUTA DE LOGIN PARA EL ADMINISTRADOR
# =====================================
@app.route("/api/login", methods=["POST"])
def login_admin():
    datos = request.get_json(silent=True)

    if not datos:
        return jsonify({"error": "No se enviaron datos"}), 400

    correo = datos.get("correo")
    password = datos.get("password")

    # Validar las credenciales fijas solicitadas
    if correo == "huellitas@amor.com" and password == "Huellitas_Amor":
        return jsonify({
            "mensaje": "Inicio de sesión exitoso",
            "usuario": correo
        }), 200
    else:
        return jsonify({
            "error": "Correo o contraseña incorrectos"
        }), 401


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
