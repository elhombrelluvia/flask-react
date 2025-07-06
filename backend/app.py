from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Crear la app
app = Flask(__name__)
CORS(app)

# Conexión a MongoDB
from db import db

# Importar y registrar rutas
from routes.clientes_routes import clientes_bp

app.register_blueprint(clientes_bp, url_prefix="/api/clientes")

# Ruta base
@app.route("/")
def home():
    return {"message": "API ComercioTech en funcionamiento"}

# Iniciar app
if __name__ == "__main__":
    app.run(debug=True)
