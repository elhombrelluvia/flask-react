const API_BASE_URL = 'http://localhost:5000/api';

// Funciones de navegación
function showSection(sectionName) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(sectionName).style.display = 'block';
}

function cancelarForm() {
    const forms = document.querySelectorAll('.form-container');
    forms.forEach(form => {
        form.style.display = 'none';
    });
}

// Función para mostrar mensajes
function mostrarMensaje(mensaje, tipo = 'success') {
    const div = document.createElement('div');
    div.className = tipo;
    div.textContent = mensaje;
    
    const resultado = document.querySelector('.section:not([style*="display: none"]) .resultado');
    resultado.insertBefore(div, resultado.firstChild);
    
    setTimeout(() => {
        div.remove();
    }, 5000);
}

// Función para hacer peticiones HTTP
async function makeRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Error en la petición');
        }
        
        return data;
    } catch (error) {
        console.error('Error:', error);
        mostrarMensaje(error.message, 'error');
        throw error;
    }
}

// Inicializar la app
document.addEventListener('DOMContentLoaded', () => {
    showSection('clientes');
});