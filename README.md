# ComercioTech API

API RESTful para la gestión de clientes, productos y pedidos de un sistema de ventas, desarrollada con Flask y MongoDB.

---

## Tabla de Contenidos

- [Características](#características)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Uso](#uso)
- [Endpoints Principales](#endpoints-principales)
- [Seeds de Datos](#seeds-de-datos)
- [Notas de Seguridad](#notas-de-seguridad)
- [Mejoras Sugeridas](#mejoras-sugeridas)
- [Licencia](#licencia)

---

## Características

- CRUD completo para **clientes**, **productos** y **pedidos**.
- Validación robusta de datos y unicidad (RUT para clientes, código de barra para productos).
- Gestión de stock y actualización automática de historiales.
- Consultas rápidas y filtros por cliente, categoría y precio.
- Seeds para poblar la base de datos con datos de prueba.
- Modularidad y separación clara de responsabilidades.

---

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/elhombrelluvia/flask-react
   cd flask-react
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Asegúrate de tener MongoDB corriendo y configura la URI en el archivo `.env`:
   ```
   MONGO_URI=mongodb://localhost:27017/
   ```

---

## Configuración

- El archivo `.env` debe contener la variable `MONGO_URI`.
- La base de datos utilizada es `comerciotech` (puedes cambiarlo en `db.py`).

---

## Estructura del Proyecto

```
backend/
│
├── app.py                  # Punto de entrada principal de la API
├── db.py                   # Conexión a MongoDB
├── config.py               # (Reservado para configuración avanzada)
├── requirements.txt        # Dependencias del proyecto
│
├── controllers/            # Lógica de negocio y validaciones
│   ├── clientes_controller.py
│   ├── productos_controller.py
│   └── pedidos_controller.py
│
├── routes/                 # Definición de rutas y blueprints
│   ├── clientes_routes.py
│   ├── productos_routes.py
│   └── pedidos_routes.py
│
├── utils/                  # Scripts de seeds para poblar la base de datos
│   ├── seed_clientes.py
│   ├── seed_productos.py
│   └── seed_pedidos.py
│
└── .env                    # Variables de entorno (no subir al repo)
```

---

## Uso

1. Inicia la API:
   ```bash
   python app.py
   ```

2. Accede a la API en:  
   `http://localhost:5000/`  
   Los endpoints están bajo el prefijo `/api/` (ejemplo: `/api/clientes/`).

---

## Endpoints Principales

### Clientes

- `POST   /api/clientes/`           - Crear cliente
- `GET    /api/clientes/`           - Listar todos los clientes
- `GET    /api/clientes/<id>`       - Obtener cliente por ID
- `GET    /api/clientes/rut/<rut>`  - Buscar cliente por RUT
- `PUT    /api/clientes/rut/<rut>`       - Actualizar cliente
- `DELETE /api/clientes/rut/<rut>`       - Eliminar cliente

### Productos

- `POST   /api/productos/`                  - Crear producto
- `GET    /api/productos/`                  - Listar todos los productos
- `GET    /api/productos/codigo_barra/<cb>` - Buscar producto por código de barra
- `PUT    /api/productos/<cb>`              - Actualizar producto
- `DELETE /api/productos/<cb>`              - Eliminar producto
- `GET    /api/productos/<cb>/historial`    - Ver historial de compras del producto
- `PATCH  /api/productos/<cb>/stock`        - Actualizar stock

### Pedidos

- `POST   /api/pedidos/`           - Crear pedido (usando RUT y códigos de barra)
- `GET    /api/pedidos/`           - Listar todos los pedidos
- `GET    /api/pedidos/<id>`       - Obtener pedido por ID
- `PUT    /api/pedidos/<id>`       - Actualizar pedido
- `DELETE /api/pedidos/<id>`       - Eliminar pedido
- `GET    /api/pedidos/buscar`     - Buscar pedidos por filtros (cliente, categoría, precio)

---

## Seeds de Datos

Para poblar la base de datos con datos de prueba, ejecuta:

```bash
python utils/seed_clientes.py
python utils/seed_productos.py
```

---

## Notas de Seguridad

- **Validación de datos:** Todos los endpoints validan tipos y unicidad.
- **Integridad:** Los historiales y stocks se actualizan automáticamente.
- **Autenticación:** Actualmente la API no requiere autenticación. Para producción, se recomienda agregar JWT o similar.

---

## Mejoras Sugeridas

- Agregar autenticación y roles de usuario.
- Soporte para imágenes de productos.
- Reportes y estadísticas.

---

## Licencia

Este proyecto es de uso académico y puede ser adaptado libremente.

---

**¡Gracias por usar ComercioTech API!**