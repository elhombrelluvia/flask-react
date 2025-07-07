from flask import Blueprint
from controllers.pedidos_controller import (
    crear_pedido,
    obtener_pedidos,
    obtener_pedido_por_id,
    actualizar_pedido,
    eliminar_pedido,
    buscar_pedidos
)

pedidos_bp = Blueprint("pedidos", __name__)

# Rutas CRUD generales
pedidos_bp.route("/", methods=["POST"])(crear_pedido)
pedidos_bp.route("/", methods=["GET"])(obtener_pedidos)
pedidos_bp.route("/<pedido_id>", methods=["GET"])(obtener_pedido_por_id)
pedidos_bp.route("/<pedido_id>", methods=["PUT"])(actualizar_pedido)
pedidos_bp.route("/<pedido_id>", methods=["DELETE"])(eliminar_pedido)

# Ruta para consultas rápidas con filtros
pedidos_bp.route("/buscar", methods=["GET"])(buscar_pedidos)