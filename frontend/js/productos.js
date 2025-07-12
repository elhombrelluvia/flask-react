// Funciones para gestión de productos

function mostrarFormProducto() {
    document.getElementById('form-producto').style.display = 'block';
}

async function listarProductos() {
    try {
        const productos = await makeRequest(`${API_BASE_URL}/productos/`);
        mostrarProductos(productos);
    } catch (error) {
        // Error ya manejado en makeRequest
    }
}

async function crearProducto() {
    const nombre = document.getElementById('producto-nombre').value;
    const categoria = document.getElementById('producto-categoria').value;
    const precio = parseFloat(document.getElementById('producto-precio').value);
    const stock = parseInt(document.getElementById('producto-stock').value);
    const codigo = document.getElementById('producto-codigo').value;
    
    if (!nombre || !categoria || !precio || !stock || !codigo) {
        mostrarMensaje('Todos los campos son obligatorios', 'error');
        return;
    }
    if (stock < 0) {
        mostrarMensaje('El stock no puede ser negativo', 'error');
        return;
    }
    if (precio < 0) {
        mostrarMensaje('El precio no puede ser negativo', 'error');
        return;
    }
   
    try {
        const producto = await makeRequest(`${API_BASE_URL}/productos/`, {
            method: 'POST',
            body: JSON.stringify({
                nombre: nombre,
                categoria: categoria,
                precio: precio,
                stock: stock,
                codigo_barra: codigo,
                historial_compras: []
            })
        });
        
        mostrarMensaje('Producto creado exitosamente');
        cancelarForm();
        listarProductos();
        
        // Limpiar formulario
        document.getElementById('producto-nombre').value = '';
        document.getElementById('producto-categoria').value = '';
        document.getElementById('producto-precio').value = '';
        document.getElementById('producto-stock').value = '';
        document.getElementById('producto-codigo').value = '';
    } catch (error) {
        // Error ya manejado en makeRequest
    }
}

async function buscarProducto() {
    const codigo = document.getElementById('buscar-codigo').value;
    
    if (!codigo) {
        mostrarMensaje('Ingrese un código de barra para buscar', 'error');
        return;
    }
    
    try {
        const producto = await makeRequest(`${API_BASE_URL}/productos/codigo_barra/${codigo}`);
        mostrarProductos([producto]);
    } catch (error) {
        // Error ya manejado en makeRequest
    }
}

async function eliminarProducto(codigoBarra) {
    if (!confirm('¿Está seguro que desea eliminar este producto?')) {
        return;
    }
    
    try {
        await makeRequest(`${API_BASE_URL}/productos/${codigoBarra}`, {
            method: 'DELETE'
        });
        
        mostrarMensaje('Producto eliminado exitosamente');
        listarProductos();
    } catch (error) {
        // Error ya manejado en makeRequest
    }
}

async function verHistorialProducto(codigoBarra) {
    try {
        const historial = await makeRequest(`${API_BASE_URL}/productos/${codigoBarra}/historial`);
        mostrarHistorial(historial.historial_compras, codigoBarra);
    } catch (error) {
        // Error ya manejado en makeRequest
    }
}

function mostrarHistorial(historial, codigoBarra) {
    const resultado = document.getElementById('resultado-productos');
    
    let html = `<h3>Historial de Compras - Código: ${codigoBarra}</h3>`;
    
    if (!historial || historial.length === 0) {
        html += '<p>No hay historial de compras para este producto.</p>';
    } else {
        html += '<div class="historial-list">';
        historial.forEach(compra => {
            html += `
                <div class="historial-item">
                    <p><strong>Cliente:</strong> ${compra.nombre}</p>
                    <p><strong>RUT:</strong> ${compra.rut}</p>
                </div>
            `;
        });
        html += '</div>';
    }
    
    html += '<button onclick="listarProductos()" class="button-back">Volver a la lista</button>';
    resultado.innerHTML = html;
}

function mostrarProductos(productos) {
    const resultado = document.getElementById('resultado-productos');
    
    if (!productos || productos.length === 0) {
        resultado.innerHTML = '<p>No se encontraron productos.</p>';
        return;
    }
    
    let html = '<h3>Productos:</h3>';
    productos.forEach(producto => {
        html += `
            <div class="item">
                <h4>${producto.nombre}</h4>
                <p><strong>Categoría:</strong> ${producto.categoria}</p>
                <p><strong>Precio:</strong> $${producto.precio.toLocaleString()}</p>
                <p><strong>Stock:</strong> ${producto.stock}</p>
                <p><strong>Código:</strong> ${producto.codigo_barra}</p>
                <p><strong>Compras:</strong> ${producto.historial_compras.length}</p>
                <div class="item-actions">
                    <button onclick="verHistorialProducto('${producto.codigo_barra}')" class="button-info">
                        Ver Historial
                    </button>
                    <button onclick="eliminarProducto('${producto.codigo_barra}')" class="button-danger">
                        Eliminar
                    </button>
                </div>
            </div>
        `;
    });
    
    resultado.innerHTML = html;
}