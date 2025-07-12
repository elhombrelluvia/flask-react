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
- [Frontend Demo](#frontend-demo)
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
- Frontend demo incluido para probar la funcionalidad.
- Modularidad y separación clara de responsabilidades.
- Soporte CORS para integración con frontend.

---

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/elhombrelluvia/flask-react
   cd flask-react
   ```

2. Navega al directorio del backend:
   ```bash
   cd backend
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno (ver sección [Configuración](#configuración)).

---

## Configuración

### Variables de Entorno

Crea o actualiza el archivo `.env` en el directorio `backend/` con la siguiente configuración:

```properties
MONGO_URI=mongodb://usuario_api:inacap123@<IP_MAQUINA_VIRTUAL>:27017/comerciotech
```

**Importante:** Reemplaza `<IP_MAQUINA_VIRTUAL>` con la IP real de tu máquina virtual donde está corriendo MongoDB.

### Base de Datos

- **Base de datos:** `comerciotech`
- **Usuario:** `usuario_api`
- **Contraseña:** `inacap123`
- **Puerto:** `27017`

---

## Estructura del Proyecto

```
/
├── backend/                # API Flask
│   ├── app.py             # Punto de entrada principal
│   ├── db.py              # Conexión a MongoDB
│   ├── config.py          # (Reservado para configuración avanzada)
│   ├── requirements.txt   # Dependencias del proyecto
│   ├── .env               # Variables de entorno
│   │
│   ├── controllers/       # Lógica de negocio y validaciones
│   │   ├── clientes_controller.py
│   │   ├── productos_controller.py
│   │   └── pedidos_controller.py
│   │
│   └── routes/            # Definición de rutas y blueprints
│       ├── clientes_routes.py
│       ├── productos_routes.py
│       └── pedidos_routes.py
│
├── frontend/              # Frontend demo
│   ├── index.html         # Página principal
│   ├── css/
│   │   └── style.css      # Estilos
│   └── js/
│       ├── main.js        # Funciones principales
│       ├── clientes.js    # Gestión de clientes
│       ├── productos.js   # Gestión de productos
│       └── pedidos.js     # Gestión de pedidos
│
└── README.md              # Este archivo
```

---

## Uso

### Iniciar el Backend

1. Navega al directorio del backend:
   ```bash
   cd backend
   ```

2. Inicia la API:
   ```bash
   python app.py
   ```

3. La API estará disponible en: `http://localhost:5000/`

### Usar el Frontend Demo

1. Asegúrate de que el backend esté corriendo.

2. Abre el archivo `frontend/index.html` en tu navegador web.

3. Usa la interfaz para:
   - Crear, listar y buscar clientes
   - Crear, listar y buscar productos
   - Crear y listar pedidos
   - Ver historial de compras de productos

---

## Endpoints Principales

### Clientes

- `POST   /api/clientes/`           - Crear cliente
- `GET    /api/clientes/`           - Listar todos los clientes
- `GET    /api/clientes/<id>`       - Obtener cliente por ID
- `GET    /api/clientes/rut/<rut>`  - Buscar cliente por RUT
- `PUT    /api/clientes/rut/<rut>`  - Actualizar cliente
- `DELETE /api/clientes/rut/<rut>`  - Eliminar cliente

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

## Frontend Demo

El proyecto incluye un frontend demo que permite interactuar con la API de manera visual:

### Funcionalidades del Frontend

- **Navegación por pestañas:** Clientes, Productos, Pedidos
- **Gestión de Clientes:**
  - Crear nuevos clientes con validación de RUT
  - Listar todos los clientes
  - Buscar clientes por RUT
  - Eliminar clientes
- **Gestión de Productos:**
  - Crear productos con validación de código de barra
  - Listar todos los productos
  - Buscar productos por código de barra
  - Ver historial de compras
  - Eliminar productos
- **Gestión de Pedidos:**
  - Crear pedidos seleccionando cliente y productos
  - Gestión automática de stock
  - Listar todos los pedidos
  - Eliminar pedidos

### Características del Frontend

- **Diseño Responsivo:** Funciona en dispositivos móviles y desktop
- **Interfaz Moderna:** Diseño con gradientes y efectos glassmorphism
- **Validación de Datos:** Validación client-side antes de enviar datos
- **Manejo de Errores:** Mensajes claros de error y éxito
- **Actualización Automática:** Las listas se actualizan automáticamente después de operaciones


## Notas de Seguridad

- **Validación de datos:** Todos los endpoints validan tipos y unicidad.
- **Integridad:** Los historiales y stocks se actualizan automáticamente.
- **CORS:** Configurado para permitir solicitudes desde el frontend.
- **Autenticación:** Actualmente la API no requiere autenticación. Para producción, se recomienda agregar JWT o similar.

---

## Mejoras Sugeridas

- Agregar autenticación y roles de usuario.
- Implementar paginación para grandes volúmenes de datos.
- Soporte para imágenes de productos.
- Reportes y estadísticas.
- Implementar logging y monitoreo.

---

## Solución de Problemas

### Error de Conexión a MongoDB

Si recibes errores de conexión, verifica:
1. La IP de la máquina virtual está correcta en el archivo `.env`
2. MongoDB está corriendo en la máquina virtual
3. El usuario `usuario_api` tiene los permisos necesarios
4. El puerto 27017 está abierto

### Error CORS en el Frontend

Si tienes problemas de CORS, asegúrate de que:
1. El backend esté corriendo en `http://localhost:5000`
2. Flask-CORS esté instalado y configurado correctamente

---

## Licencia

Este proyecto es de uso académico y puede ser adaptado libremente.

---

**¡Gracias por usar ComercioTech API!**