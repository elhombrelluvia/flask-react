from flask import Blueprint
from controllers.clientes_controller import (
    crear_cliente,
    obtener_clientes,
    obtener_cliente_por_id,
    actualizar_cliente_por_rut,
    eliminar_cliente_por_rut,
    buscar_cliente_por_rut
)

clientes_bp = Blueprint("clientes", __name__)

# Rutas específicas primero para evitar conflictos con rutas dinámicas
clientes_bp.route("/rut/<rut>", methods=["GET"])(buscar_cliente_por_rut)

# Rutas CRUD generales
clientes_bp.route("/", methods=["POST"])(crear_cliente)
clientes_bp.route("/", methods=["GET"])(obtener_clientes)
clientes_bp.route("/<cliente_id>", methods=["GET"])(obtener_cliente_por_id)
clientes_bp.route("/rut/<rut>", methods=["PUT"])(actualizar_cliente_por_rut)
clientes_bp.route("/rut/<rut>", methods=["DELETE"])(eliminar_cliente_por_rut)