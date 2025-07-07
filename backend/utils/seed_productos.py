from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["comerciotech"]
productos_collection = db["productos"]

productos_seed = [
    {
        "nombre": "Notebook Lenovo",
        "categoria": "Tecnología",
        "precio": 500000,
        "stock": 10,
        "codigo_barra": "12345678",
        "historial_compras": []
    },
    {
        "nombre": "Mouse Logitech",
        "categoria": "Tecnología",
        "precio": 15000,
        "stock": 20,
        "codigo_barra": "23456789",
        "historial_compras": []
    },
    {
        "nombre": "Silla Oficina",
        "categoria": "Muebles",
        "precio": 80000,
        "stock": 5,
        "codigo_barra": "34567890",
        "historial_compras": []
    }
]

productos_collection.delete_many({})
productos_collection.insert_many(productos_seed)
print("Productos insertados.")