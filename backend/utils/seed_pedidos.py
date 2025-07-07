from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["comerciotech"]
pedidos_collection = db["pedidos"]

pedidos_seed = [
    {
        # Pedido de Juan
        "cliente_id": "cl1",
        "productos": [
            {"producto_id": "pr1", "cantidad": 1},
            {"producto_id": "pr2", "cantidad": 2}
        ]
    },
    {
        # Pedido de María
        "cliente_id": "cl2",
        "productos": [
            {"producto_id": "pr3", "cantidad": 1}
        ]
    }
]

pedidos_collection.delete_many({})
pedidos_collection.insert_many(pedidos_seed)
print("Pedidos insertados.")