import re
from flask import request, jsonify
from bson.objectid import ObjectId
from bson.errors import InvalidId
from db import db

productos_collection = db["productos"]

def validar_campos_producto(data):
    """
    Valida los campos obligatorios y tipos de datos básicos para un producto.
    """
    campos_obligatorios = ["nombre", "categoria", "precio", "stock", "codigo_barra", "historial_compras"]
    for campo in campos_obligatorios:
        if campo not in data:
            return False, f"Falta el campo obligatorio: {campo}"
    if not isinstance(data["nombre"], str):
        return False, "El nombre debe ser un string"
    if not isinstance(data["categoria"], str):
        return False, "La categoría debe ser un string"
    if not isinstance(data["precio"], (int, float)) or data["precio"] < 0:
        return False, "El precio debe ser un número positivo"
    if not isinstance(data["stock"], int) or data["stock"] < 0:
        return False, "El stock debe ser un entero no negativo"
    if not isinstance(data["codigo_barra"], str) or not re.fullmatch(r"\d{8,13}", data["codigo_barra"]):
        return False, "El código de barra debe ser un string numérico de 8 a 13 dígitos"
    if not isinstance(data["historial_compras"], list):
        return False, "El historial de compras debe ser una lista"
    return True, ""

def serializar_producto(producto):
    producto["_id"] = str(producto["_id"])
    return producto

def crear_producto():
    """
    Crea un nuevo producto en la base de datos.
    """
    data = request.get_json()
    valido, mensaje = validar_campos_producto(data)
    if not valido:
        return jsonify({"error": mensaje}), 400

    # Validar que no exista un producto con el mismo código de barra
    if productos_collection.find_one({"codigo_barra": data["codigo_barra"]}):
        return jsonify({"error": "Ya existe un producto con ese código de barra"}), 400

    result = productos_collection.insert_one(data)
    nuevo_producto = productos_collection.find_one({"_id": result.inserted_id})
    return jsonify(serializar_producto(nuevo_producto)), 201

def obtener_productos():
    """
    Obtiene todos los productos.
    """
    productos = [serializar_producto(p) for p in productos_collection.find()]
    return jsonify(productos), 200


def actualizar_producto_por_codigo_barra(codigo_barra):
    """
    Actualiza los datos de un producto existente usando el código de barra.
    """
    data = request.get_json()
    try:
        resultado = productos_collection.update_one(
            {"codigo_barra": codigo_barra},
            {"$set": data}
        )
    except Exception:
        return jsonify({"error": "Error al actualizar el producto"}), 400

    if resultado.matched_count == 0:
        return jsonify({"error": "Producto no encontrado"}), 404

    producto_actualizado = productos_collection.find_one({"codigo_barra": codigo_barra})
    return jsonify(serializar_producto(producto_actualizado)), 200

def eliminar_producto_por_codigo_barra(codigo_barra):
    """
    Elimina un producto por su código de barra.
    """
    try:
        resultado = productos_collection.delete_one({"codigo_barra": codigo_barra})
    except Exception:
        return jsonify({"error": "Error al eliminar el producto"}), 400

    if resultado.deleted_count == 0:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({"mensaje": "Producto eliminado correctamente"}), 200

def historial_compras_producto_por_codigo_barra(codigo_barra):
    """
    Visualiza el historial de compras de un producto usando el código de barra.
    """
    producto = productos_collection.find_one({"codigo_barra": codigo_barra})
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({"historial_compras": producto.get("historial_compras", [])}), 200

def actualizar_stock_por_codigo_barra(codigo_barra):
    """
    Actualiza el stock de un producto usando el código de barra.
    """
    data = request.get_json()
    nuevo_stock = data.get("stock")
    if not isinstance(nuevo_stock, int) or nuevo_stock < 0:
        return jsonify({"error": "El stock debe ser un entero no negativo"}), 400

    try:
        resultado = productos_collection.update_one(
            {"codigo_barra": codigo_barra},
            {"$set": {"stock": nuevo_stock}}
        )
    except Exception:
        return jsonify({"error": "Error al actualizar el stock"}), 400

    if resultado.matched_count == 0:
        return jsonify({"error": "Producto no encontrado"}), 404

    producto_actualizado = productos_collection.find_one({"codigo_barra": codigo_barra})
    return jsonify(serializar_producto(producto_actualizado)), 200

def buscar_producto_por_codigo_barra(codigo_barra):
    """
    Busca un producto por su código de barra.
    """
    producto = productos_collection.find_one({"codigo_barra": codigo_barra})
    if producto:
        return jsonify(serializar_producto(producto)), 200
    return jsonify({"error": "Producto no encontrado"}), 404