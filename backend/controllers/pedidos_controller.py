from flask import request, jsonify
from bson.objectid import ObjectId
from bson.errors import InvalidId
from db import db
from datetime import datetime


pedidos_collection = db["pedidos"]
productos_collection = db["productos"]

def serializar_pedido(pedido):
    pedido["_id"] = str(pedido["_id"])
    # Si el pedido tiene fecha_hora, conviértela a string ISO
    if "fecha_hora" in pedido and isinstance(pedido["fecha_hora"], datetime):
        pedido["fecha_hora"] = pedido["fecha_hora"].isoformat()
    return pedido

def crear_pedido():
    """
    Crea un nuevo pedido usando el RUT del cliente y códigos de barra de productos.
    """
    data = request.get_json()
    cliente_rut = data.get("cliente_rut")
    productos_solicitados = data.get("productos", [])

    if not cliente_rut or not isinstance(productos_solicitados, list) or not productos_solicitados:
        return jsonify({"error": "Datos de pedido incompletos"}), 400

    # Obtener datos del cliente por RUT
    cliente = db["clientes"].find_one({"rut": cliente_rut})
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    productos_final = []
    productos_obj = []
    for item in productos_solicitados:
        producto = productos_collection.find_one({"codigo_barra": item["codigo_barra"]})
        if not producto:
            return jsonify({"error": f"Producto {item['codigo_barra']} no encontrado"}), 404
        if producto["stock"] < item["cantidad"]:
            return jsonify({"error": f"Stock insuficiente para {producto['nombre']}"}), 400
        productos_final.append({
            "codigo_barra": producto["codigo_barra"],
            "nombre": producto["nombre"],
            "cantidad": item["cantidad"]
        })
        productos_obj.append(producto)

    # Descontar stock y actualizar historial de compras de productos
    for idx, item in enumerate(productos_solicitados):
        productos_collection.update_one(
            {"codigo_barra": item["codigo_barra"]},
            {
                "$inc": {"stock": -item["cantidad"]},
                "$addToSet": {
                    "historial_compras": {
                        "rut": cliente["rut"],
                        "nombre": f"{cliente['nombre']} {cliente['apellido']}"
                    }
                }
            }
        )

    # Crear el pedido con información adicional
    pedido_data = {
        "cliente_id": str(cliente["_id"]),
        "cliente_rut": cliente["rut"],
        "cliente_nombre": cliente["nombre"],
        "cliente_apellido": cliente["apellido"],
        "fecha_hora": datetime.now(),
        "productos": productos_final
    }
    result = pedidos_collection.insert_one(pedido_data)
    nuevo_pedido = pedidos_collection.find_one({"_id": result.inserted_id})

    # Agregar el id del pedido al historial_pedidos del cliente
    db["clientes"].update_one(
        {"_id": cliente["_id"]},
        {"$addToSet": {"historial_pedidos": str(nuevo_pedido["_id"])}}
    )

    return jsonify(serializar_pedido(nuevo_pedido)), 201

def obtener_pedidos():
    """
    Obtiene todos los pedidos.
    """
    pedidos = [serializar_pedido(p) for p in pedidos_collection.find()]
    return jsonify(pedidos), 200

def obtener_pedido_por_id(pedido_id):
    """
    Obtiene un pedido por su ID.
    """
    try:
        pedido = pedidos_collection.find_one({"_id": ObjectId(pedido_id)})
    except (InvalidId, TypeError):
        return jsonify({"error": "ID inválido"}), 400

    if pedido:
        return jsonify(serializar_pedido(pedido)), 200
    return jsonify({"error": "Pedido no encontrado"}), 404

def actualizar_pedido(pedido_id):
    """
    Actualiza los datos de un pedido existente (no gestiona stock).
    """
    data = request.get_json()
    try:
        resultado = pedidos_collection.update_one(
            {"_id": ObjectId(pedido_id)},
            {"$set": data}
        )
    except (InvalidId, TypeError):
        return jsonify({"error": "ID inválido"}), 400

    if resultado.matched_count == 0:
        return jsonify({"error": "Pedido no encontrado"}), 404

    pedido_actualizado = pedidos_collection.find_one({"_id": ObjectId(pedido_id)})
    return jsonify(serializar_pedido(pedido_actualizado)), 200

def eliminar_pedido(pedido_id):
    """
    Elimina un pedido por su ID.
    """
    try:
        resultado = pedidos_collection.delete_one({"_id": ObjectId(pedido_id)})
    except (InvalidId, TypeError):
        return jsonify({"error": "ID inválido"}), 400

    if resultado.deleted_count == 0:
        return jsonify({"error": "Pedido no encontrado"}), 404

    return jsonify({"mensaje": "Pedido eliminado correctamente"}), 200

def buscar_pedidos():
    """
    Consulta pedidos por filtros: categoría, precio o cliente.
    Parámetros por query string: cliente_id, categoria, precio_min, precio_max
    """
    query = {}
    cliente_id = request.args.get("cliente_id")
    categoria = request.args.get("categoria")
    precio_min = request.args.get("precio_min", type=float)
    precio_max = request.args.get("precio_max", type=float)

    if cliente_id:
        query["cliente_id"] = cliente_id

    pedidos = list(pedidos_collection.find(query))

    # Filtros por categoría y precio (requiere buscar productos relacionados)
    if categoria or precio_min is not None or precio_max is not None:
        pedidos_filtrados = []
        for pedido in pedidos:
            productos_ok = []
            for item in pedido.get("productos", []):
                producto = productos_collection.find_one({"_id": ObjectId(item["producto_id"])})
                if not producto:
                    continue
                if categoria and producto.get("categoria") != categoria:
                    continue
                if precio_min is not None and producto.get("precio", 0) < precio_min:
                    continue
                if precio_max is not None and producto.get("precio", 0) > precio_max:
                    continue
                productos_ok.append(item)
            if productos_ok:
                pedido["productos"] = productos_ok
                pedidos_filtrados.append(serializar_pedido(pedido))
        return jsonify(pedidos_filtrados), 200

    return jsonify([serializar_pedido(p) for p in pedidos]), 200