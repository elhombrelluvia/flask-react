// Funciones para gestión de clientes

function mostrarFormCliente() {
    document.getElementById('form-cliente').style.display = 'block';
}

async function listarClientes() {
    try {
        const clientes = await makeRequest(`${API_BASE_URL}/clientes/`);
        mostrarClientes(clientes);
    } catch (error) {
        // Error ya manejado en makeRequest
    }
}

async function crearCliente() {
    const rut = document.getElementById('cliente-rut').value;
    const nombre = document.getElementById('cliente-nombre').value;
    const apellido = document.getElementById('cliente-apellido').value;
    
    if (!rut || !nombre || !apellido) {
        mostrarMensaje('Todos los campos son obligatorios', 'error');
        return;
    }
    
    try {
        const cliente = await makeRequest(`${API_BASE_URL}/clientes/`, {
            method: 'POST',
            body: JSON.stringify({
                rut: rut,
                nombre: nombre,
                apellido: apellido,
                historial_pedidos: []
            })
        });
        
        mostrarMensaje('Cliente creado exitosamente');
        cancelarForm();
        listarClientes();
        
        // Limpiar formulario
        document.getElementById('cliente-rut').value = '';
        document.getElementById('cliente-nombre').value = '';
        document.getElementById('cliente-apellido').value = '';
    } catch (error) {
        // Error ya manejado en makeRequest
    }
}

async function buscarCliente() {
    const rut = document.getElementById('buscar-rut').value;
    
    if (!rut) {
        mostrarMensaje('Ingrese un RUT para buscar', 'error');
        return;
    }
    
    try {
        const cliente = await makeRequest(`${API_BASE_URL}/clientes/rut/${rut}`);
        mostrarClientes([cliente]);
    } catch (error) {
        // Error ya manejado en makeRequest
    }
}

async function eliminarCliente(rut) {
    if (!confirm('¿Está seguro que desea eliminar este cliente?')) {
        return;
    }
    
    try {
        await makeRequest(`${API_BASE_URL}/clientes/rut/${rut}`, {
            method: 'DELETE'
        });
        
        mostrarMensaje('Cliente eliminado exitosamente');
        listarClientes();
    } catch (error) {
        // Error ya manejado en makeRequest
    }
}

function mostrarClientes(clientes) {
    const resultado = document.getElementById('resultado-clientes');
    
    if (!clientes || clientes.length === 0) {
        resultado.innerHTML = '<p>No se encontraron clientes.</p>';
        return;
    }
    
    let html = '<h3>Clientes:</h3>';
    clientes.forEach(cliente => {
        html += `
            <div class="item">
                <h4>${cliente.nombre} ${cliente.apellido}</h4>
                <p><strong>RUT:</strong> ${cliente.rut}</p>
                <p><strong>Pedidos:</strong> ${cliente.historial_pedidos.length}</p>
                <p><strong>ID:</strong> ${cliente._id}</p>
                <div class="item-actions">
                    <button onclick="eliminarCliente('${cliente.rut}')" class="button-danger">
                        Eliminar
                    </button>
                </div>
            </div>
        `;
    });
    
    resultado.innerHTML = html;
}