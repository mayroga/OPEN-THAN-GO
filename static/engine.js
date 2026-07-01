/* =========================================================
   ENGINE: SISTEMA DE ACTIVACIÓN DE BIENESTAR (TVid)
   MOTOR: COMUNICACIÓN CON MAIN.PY
========================================================= */

const app = document.getElementById('app');

// Función inicial: Presenta el centro de activación
async function iniciarApp() {
    app.innerHTML = `
        <h1>CENTRO DE ACTIVACIÓN</h1>
        <p>Selecciona tu estado actual para recibir un protocolo de bienestar inmediato:</p>
        <button class="btn-action" onclick="solicitarProtocolo(true)">NECESITO ESCAPAR (Salir)</button>
        <button class="btn-action btn-secondary" onclick="solicitarProtocolo(false)">SISTEMA DE CASA (10 min)</button>
    `;
}

// Función que solicita el protocolo al motor en Python (main.py)
async function solicitarProtocolo(salir) {
    try {
        const res = await fetch(`/api/get-protocol?salir=${salir}`);
        const data = await res.json();
        
        if (data.modo === 'casa') {
            renderCasa(data.protocolos);
        } else {
            renderSalida(data.protocolo);
        }
    } catch (error) {
        app.innerHTML = `<h1>Error de Sistema</h1><p>Intenta nuevamente.</p><button class="btn-action" onclick="iniciarApp()">Volver</button>`;
    }
}

// Renderizado para modo Casa: Divide en 2 fases de 5 minutos
function renderCasa(protocolos) {
    app.innerHTML = `
        <h2>PROTOCOLO DE 10 MINUTOS</h2>
        <div id="protocol-display">
            <p><strong>Fase 1 (5 min):</strong><br>${protocolos[0].nombre}<br><em>Acción: ${protocolos[0].accion}</em></p>
            <p><strong>Fase 2 (5 min):</strong><br>${protocolos[1].nombre}<br><em>Acción: ${protocolos[1].accion}</em></p>
        </div>
        <button class="btn-action" onclick="iniciarApp()">Misión Cumplida</button>
    `;
}

// Renderizado para modo Salida: Misión de entorno
function renderSalida(protocolo) {
    app.innerHTML = `
        <h2>PROTOCOLO DE SALIDA</h2>
        <div id="protocol-display">
            <p><strong>Tu Misión:</strong><br>${protocolo.nombre}</p>
            <p><strong>Acción de Activación:</strong><br>${protocolo.accion}</p>
        </div>
        <p><small>Al terminar, regresa para documentar tu bienestar.</small></p>
        <button class="btn-action" onclick="iniciarApp()">Finalizar</button>
    `;
}

// Inicializar al cargar
iniciarApp();
