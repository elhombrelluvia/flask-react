from flask import Blueprint
from controllers.productos_controller import (
    crear_producto,
    obtener_productos,
    actualizar_producto_por_codigo_barra,
    eliminar_producto_por_codigo_barra,
    historial_compras_producto_por_codigo_barra,
    actualizar_stock_por_codigo_barra,
    buscar_producto_por_codigo_barra
)

productos_bp = Blueprint("productos", __name__)

# Rutas CRUD generales
productos_bp.route("/", methods=["POST"])(crear_producto)
productos_bp.route("/", methods=["GET"])(obtener_productos)
productos_bp.route("/<codigo_barra>", methods=["PUT"])(actualizar_producto_por_codigo_barra)
productos_bp.route("/<codigo_barra>", methods=["DELETE"])(eliminar_producto_por_codigo_barra)
productos_bp.route("/codigo_barra/<codigo_barra>", methods=["GET"])(buscar_producto_por_codigo_barra)

# Rutas específicas
productos_bp.route("/<codigo_barra>/historial", methods=["GET"])(historial_compras_producto_por_codigo_barra)
productos_bp.route("/<codigo_barra>/stock", methods=["PATCH"])(actualizar_stock_por_codigo_barra)