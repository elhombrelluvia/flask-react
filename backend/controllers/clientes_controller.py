import re
from flask import request, jsonify
from bson.objectid import ObjectId
from bson.errors import InvalidId
from db import db

clientes_collection = db["clientes"]

def es_rut_valido(rut):
    """
    Valida un RUT chileno sin puntos ni guion.
    Ejemplo válido: 123456785 (8 dígitos + dígito verificador)
    """
    if not re.fullmatch(r"\d{8}[0-9kK]", rut):
        return False

    cuerpo = rut[:-1]
    dv = rut[-1].lower()
    suma = 0
    multiplo = 2

    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo += 1
        if multiplo > 7:
            multiplo = 2

    resto = suma % 11
    dv_esperado = 'k' if resto == 1 else '0' if resto == 0 else str(11 - resto)
    return dv == dv_esperado

def validar_campos_cliente(data):
    """
    Valida los campos obligatorios y tipos de datos básicos para un cliente.
    """
    campos_obligatorios = ["rut", "nombre", "apellido", "historial_pedidos"]
    for campo in campos_obligatorios:
        if campo not in data:
            return False, f"Falta el campo obligatorio: {campo}"
    if not isinstance(data["rut"], str):
        return False, "El RUT debe ser un string"
    if not es_rut_valido(data["rut"]):
        return False, "El RUT ingresado no es válido"
    if not isinstance(data["nombre"], str) or not isinstance(data["apellido"], str):
        return False, "Nombre y apellido deben ser strings"
    if not isinstance(data["historial_pedidos"], list):
        return False, "historial_pedidos debe ser una lista"
    return True, ""
def serializar_cliente(cliente):
    """
    Convierte el ObjectId a string y filtra campos sensibles si es necesario.
    """
    cliente["_id"] = str(cliente["_id"])
    return cliente

def crear_cliente():
    """
    Crea un nuevo cliente en la base de datos.
    """
    data = request.get_json()
    valido, mensaje = validar_campos_cliente(data)
    if not valido:
        return jsonify({"error": mensaje}), 400

    # Validar que no exista un cliente con el mismo RUT
    if clientes_collection.find_one({"rut": data["rut"]}):
        return jsonify({"error": "Ya existe un cliente con ese RUT"}), 400

    result = clientes_collection.insert_one(data)
    nuevo_cliente = clientes_collection.find_one({"_id": result.inserted_id})
    return jsonify(serializar_cliente(nuevo_cliente)), 201

def obtener_clientes():
    """
    Obtiene todos los clientes.
    """
    clientes = [serializar_cliente(cliente) for cliente in clientes_collection.find()]
    return jsonify(clientes), 200

def obtener_cliente_por_id(cliente_id):
    """
    Obtiene un cliente por su ID.
    """
    try:
        cliente = clientes_collection.find_one({"_id": ObjectId(cliente_id)})
    except (InvalidId, TypeError):
        return jsonify({"error": "ID inválido"}), 400

    if cliente:
        return jsonify(serializar_cliente(cliente)), 200
    return jsonify({"error": "Cliente no encontrado"}), 404

def actualizar_cliente_por_rut(rut):
    """
    Actualiza los datos de un cliente existente usando el RUT.
    """
    data = request.get_json()
    try:
        resultado = clientes_collection.update_one(
            {"rut": rut},
            {"$set": data}
        )
    except Exception:
        return jsonify({"error": "Error al actualizar el cliente"}), 400

    if resultado.matched_count == 0:
        return jsonify({"error": "Cliente no encontrado"}), 404

    cliente_actualizado = clientes_collection.find_one({"rut": rut})
    return jsonify(serializar_cliente(cliente_actualizado)), 200

def eliminar_cliente_por_rut(rut):
    """
    Elimina un cliente por su RUT.
    """
    try:
        resultado = clientes_collection.delete_one({"rut": rut})
    except Exception:
        return jsonify({"error": "Error al eliminar el cliente"}), 400

    if resultado.deleted_count == 0:
        return jsonify({"error": "Cliente no encontrado"}), 404

    return jsonify({"mensaje": "Cliente eliminado correctamente"}), 200

def buscar_cliente_por_rut(rut):
    """
    Busca un cliente por su RUT.
    """
    cliente = clientes_collection.find_one({"rut": rut})
    if cliente:
        return jsonify(serializar_cliente(cliente)), 200
    return jsonify({"error": "Cliente no encontrado con ese RUT"}), 404