// Funciones para gestión de pedidos

function mostrarFormPedido() {
    document.getElementById('form-pedido').style.display = 'block';
    cargarClientesSelect();
    cargarProductosSelect();
}

async function cargarClientesSelect() {
    try {
        const clientes = await makeRequest(`${API_BASE_URL}/clientes/`);
        const select = document.getElementById('pedido-cliente-select');
        
        select.innerHTML = '<option value="">Seleccione un cliente</option>';
        clientes.forEach(cliente => {
            select.innerHTML += `<option value="${cliente.rut}">${cliente.nombre} ${cliente.apellido} - ${cliente.rut}</option>`;
        });
    } catch (error) {
        mostrarMensaje('Error al cargar clientes', 'error');
    }
}

async function cargarProductosSelect() {
    try {
        const productos = await makeRequest(`${API_BASE_URL}/productos/`);
        window.productosDisponibles = productos;
        
        const select = document.querySelector('.producto-select');
        if (select) {
            actualizarSelectProducto(select);
        }
    } catch (error) {
        mostrarMensaje('Error al cargar productos', 'error');
    }
}

function actualizarSelectProducto(select) {
    select.innerHTML = '<option value="">Seleccione un producto</option>';
    if (window.productosDisponibles) {
        window.productosDisponibles.forEach(producto => {
            if (producto.stock > 0) {
                select.innerHTML += `<option value="${producto.codigo_barra}">${producto.nombre} - ${producto.codigo_barra} (Stock: ${producto.stock})</option>`;
            }
        });
    }
}

function agregarProductoPedido() {
    const container = document.getElementById('productos-pedido');
    const div = document.createElement('div');
    div.className = 'producto-item';
    div.innerHTML = `
        <select class="producto-select">
            <option value="">Seleccione un producto</option>
        </select>
        <input type="number" class="cantidad" placeholder="Cantidad" min="1" max="999">
        <button onclick="this.parentElement.remove()">Eliminar</button>
    `;
    container.appendChild(div);
    
    const nuevoSelect = div.querySelector('.producto-select');
    actualizarSelectProducto(nuevoSelect);
}

async function listarPedidos() {
    try {
        const pedidos = await makeRequest(`${API_BASE_URL}/pedidos/`);
        mostrarPedidos(pedidos);
    } catch (error) {
        // Error ya manejado en makeRequest
    }
}

async function crearPedido() {
    const clienteRut = document.getElementById('pedido-cliente-select').value;
    const productosItems = document.querySelectorAll('.producto-item');
    
    if (!clienteRut) {
        mostrarMensaje('Seleccione un cliente', 'error');
        return;
    }
    
    const productos = [];
    productosItems.forEach(item => {
        const codigo = item.querySelector('.producto-select').value;
        const cantidad = parseInt(item.querySelector('.cantidad').value);

        if (cantidad <= 0) {
            mostrarMensaje('La cantidad debe ser mayor a 0', 'error');
            return;
        }
        if (!codigo) {
            mostrarMensaje('Seleccione un producto', 'error');
            return;
        }
        if (isNaN(cantidad)) {
            mostrarMensaje('Ingrese una cantidad válida', 'error');
            return;
        }
        
        if (codigo && cantidad) {
            productos.push({
                codigo_barra: codigo,
                cantidad: cantidad
            });
        }
    });
    
    if (productos.length === 0) {
        mostrarMensaje('Agregue al menos un producto al pedido', 'error');
        return;
    }
    
    try {
        const pedido = await makeRequest(`${API_BASE_URL}/pedidos/`, {
            method: 'POST',
            body: JSON.stringify({
                cliente_rut: clienteRut,
                productos: productos
            })
        });
        
        mostrarMensaje('Pedido creado exitosamente');
        cancelarForm();
        listarPedidos();
        
        // Limpiar formulario
        document.getElementById('pedido-cliente-select').value = '';
        document.getElementById('productos-pedido').innerHTML = `
            <h4>Productos del pedido:</h4>
            <div class="producto-item">
                <select class="producto-select">
                    <option value="">Seleccione un producto</option>
                </select>
                <input type="number" class="cantidad" placeholder="Cantidad" min="1" max="999">
            </div>
        `;
        
        const selectInicial = document.querySelector('.producto-select');
        if (selectInicial) {
            actualizarSelectProducto(selectInicial);
        }
    } catch (error) {
        // Error ya manejado en makeRequest
    }
}

async function eliminarPedido(pedidoId) {
    if (!confirm('¿Está seguro que desea eliminar este pedido?')) {
        return;
    }
    
    try {
        await makeRequest(`${API_BASE_URL}/pedidos/${pedidoId}`, {
            method: 'DELETE'
        });
        
        mostrarMensaje('Pedido eliminado exitosamente');
        listarPedidos();
    } catch (error) {
        // Error ya manejado en makeRequest
    }
}

function mostrarPedidos(pedidos) {
    const resultado = document.getElementById('resultado-pedidos');
    
    if (!pedidos || pedidos.length === 0) {
        resultado.innerHTML = '<p>No se encontraron pedidos.</p>';
        return;
    }
    
    let html = '<h3>Pedidos:</h3>';
    pedidos.forEach(pedido => {
        html += `
            <div class="item">
                <h4>Pedido ${pedido._id}</h4>
                <p><strong>Cliente:</strong> ${pedido.cliente_nombre} ${pedido.cliente_apellido} (${pedido.cliente_rut})</p>
                <p><strong>Fecha:</strong> ${new Date(pedido.fecha_hora).toLocaleString()}</p>
                <p><strong>Productos:</strong></p>
                <ul>
        `;
        
        pedido.productos.forEach(producto => {
            html += `<li>${producto.nombre} - Cantidad: ${producto.cantidad} - Código: ${producto.codigo_barra}</li>`;
        });
        
        html += `
                </ul>
                <div class="item-actions">
                    <button onclick="eliminarPedido('${pedido._id}')" class="button-danger">
                        Eliminar
                    </button>
                </div>
            </div>
        `;
    });
    
    resultado.innerHTML = html;
}