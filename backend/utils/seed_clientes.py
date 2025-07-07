from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["comerciotech"]
clientes_collection = db["clientes"]

clientes_seed = [
    {
        "rut": "123456785",
        "nombre": "Juan",
        "apellido": "Pérez",
        "historial_pedidos": []
    },
    {
        "rut": "234567892",
        "nombre": "María",
        "apellido": "González",
        "historial_pedidos": []
    }
]

clientes_collection.delete_many({})
clientes_collection.insert_many(clientes_seed)
print("Clientes insertados.")