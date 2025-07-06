from pymongo import MongoClient

# Conexión a MongoDB local (ajusta el URI si es necesario)
client = MongoClient("mongodb://localhost:27017/")
db = client["comerciotech"]
clientes_collection = db["clientes"]

clientes_seed = [
    {
        "rut": "123456785",
        "nombre": "Juan",
        "apellido": "Pérez",
        "pedidos_activos": 2,
        "historial_pedidos": [1001, 1002]
    },
    {
        "rut": "234567892",
        "nombre": "María",
        "apellido": "González",
        "pedidos_activos": 0,
        "historial_pedidos": [1003]
    },
    {
        "rut": "345678901",
        "nombre": "Pedro",
        "apellido": "Ramírez",
        "pedidos_activos": 1,
        "historial_pedidos": [1004, 1005, 1006]
    }
]

# Limpia la colección antes de insertar (opcional)
clientes_collection.delete_many({})

# Inserta los clientes de ejemplo
clientes_collection.insert_many(clientes_seed)

print("Seed de clientes insertada correctamente.")