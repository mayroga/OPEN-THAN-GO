// OPEN THAN GO SYSTEM - Frontend Engine
// Company: May Roga LLC
// File: static/engine.js

// Variables de estado global de la sesión interactiva
let idiomaActual = 'es';
let presupuestoActual = 'cero';
let modalidadSalir = true; // true = Salir, false = Casa
let pasosMisionGlobal = [];
let indicePasoActual = 0;
let datosLugarGlobal = null;
let tipoEscapeGlobal = "";
let intervaloRespiracion = null;

// Diccionario de traducción básico para la interfaz estática
const traducciones = {
    es: {
        subtitle: "Tu escape emocional inteligente",
        state: "Estado",
        region: "Región / Condado",
        zip: "ZIP Code",
        budget: "Presupuesto Disponible",
        mode: "¿Salir o quedarte en casa?",
        desahogo: "Desahogo Opcional (Filtro Emocional)",
        placeholder_text: "Escribe libremente cómo te sientes hoy...",
        btn_trigger: "GENERAR ESCAPE",
        loader: "Calculando tu vector de escape ideal...",
        btn_continue: "CONTINUAR",
        btn_gps: "ABRIR MAPA EN GPS",
        tipo_casa: "Protocolo Doméstico Activado",
        tipo_salida: "Protocolo de Exploración Abierto",
        txt_correcto: "<strong>¡Excelente elección!</strong><br>",
        txt_incorrecto: "<strong>Analiza esto con calma:</strong><br>"
    },
    en: {
        subtitle: "Your intelligent emotional escape",
        state: "State",
        region: "Region / County",
        zip: "ZIP Code",
        budget: "Available Budget",
        mode: "Go out or stay at home?",
        desahogo: "Optional Venting (Emotional Filter)",
        placeholder_text: "Write freely about how you feel today...",
        btn_trigger: "GENERATE ESCAPE",
        loader: "Calculating your ideal escape vector...",
        btn_continue: "CONTINUE",
        btn_gps: "OPEN MAP IN GPS",
        tipo_casa: "Domestic Protocol Activated",
        tipo_salida: "Exploration Protocol Opened",
        txt_correcto: "<strong>Excellent choice!</strong><br>",
        txt_incorrecto: "<strong>Analyze this calmly:</strong><br>"
    }
};

// ----------------------------------------------------
// MANEJO DE INTERFAZ Y CAPTURA DE CONFIGURACIÓN
// ----------------------------------------------------
function cambiarIdioma(lang) {
    idiomaActual = lang;
    document.getElementById('lang-es').classList.toggle('active', lang === 'es');
    document.getElementById('lang-en').classList.toggle('active', lang === 'en');
    
    // Cambiar textos del formulario dinámicamente
    document.getElementById('txt-subtitle').innerText = traducciones[lang].subtitle;
    document.getElementById('lbl-state').innerText = traducciones[lang].state;
    document.getElementById('lbl-region').innerText = traducciones[lang].region;
    document.getElementById('lbl-zip').innerText = traducciones[lang].zip;
    document.getElementById('lbl-budget').innerText = traducciones[lang].budget;
    document.getElementById('lbl-mode').innerText = traducciones[lang].mode;
    document.getElementById('lbl-desahogo').innerText = traducciones[lang].desahogo;
    document.getElementById('inp-text').placeholder = traducciones[lang].placeholder_text;
    document.getElementById('btn-main-trigger').innerText = traducciones[lang].btn_trigger;
    document.getElementById('txt-loader').innerText = traducciones[lang].loader;
    document.getElementById('btn-next').innerText = traducciones[lang].btn_continue;
    document.getElementById('btn-maps-action').innerText = traducciones[lang].btn_gps;
}

function cambiarBolsillo(opcion) {
    presupuestoActual = opcion;
    const ids = ['b-cero', 'b-minimo', 'b-moderado', 'b-libre'];
    ids.forEach(id => {
        const elemento = document.getElementById(id);
        if (elemento) {
            elemento.classList.toggle('active', id === `b-${opcion}`);
        }
    });
}

function cambiarModalidad(esSalir) {
    modalidadSalir = esSalir;
    document.getElementById('m-salir').classList.toggle('active', esSalir === true);
    document.getElementById('m-casa').classList.toggle('active', esSalir === false);
    
    // Ocultar selectores geográficos si se queda en casa para simplificar la UX
    const displayGeografia = esSalir ? 'block' : 'none';
    document.getElementById('inp-state').parentElement.style.display = displayGeografia;
    document.getElementById('inp-region').parentElement.style.display = displayGeografia;
    document.getElementById('inp-zip').parentElement.style.display = displayGeografia;
}

// ----------------------------------------------------
// PETICIÓN ASÍNCRONA AL BACKEND (MAIN.PY)
// ----------------------------------------------------
async function solicitarEscape() {
    const payload = {
        decision: modalidadSalir ? "salir" : "casa",
        lang: idiomaActual,
        budget_level: presupuestoActual,
        zip_code: document.getElementById('inp-zip').value.trim(),
        estado: document.getElementById('inp-state').value,
        region: document.getElementById('inp-region').value,
        desahogo: document.getElementById('inp-text').value.trim()
    };

    // Control de pantallas (Mostrar Loader)
    document.getElementById('wrapper-form').style.display = 'none';
    document.getElementById('wrapper-loader').style.display = 'flex';
    document.getElementById('wrapper-interactive').style.display = 'none';

    try {
        const respuesta = await fetch('/api/open-than-go', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await respuesta.json();

        // Pausa intencional de 1.8 segundos para bajar las revoluciones mentales del usuario
        setTimeout(() => {
            document.getElementById('wrapper-loader').style.display = 'none';

            if (data.status === 'success') {
                // Inicializar variables del juego / terapia oculta
                pasosMisionGlobal = data.mision.b;
                datosLugarGlobal = data.lugar || null;
                tipoEscapeGlobal = data.tipo; // "Casa" o "Salida"
                indicePasoActual = 0;

                // Configurar cabeceras de la sección interactiva
                document.getElementById('interactive-title').innerText = "OPEN THAN GO";
                document.getElementById('interactive-subtitle').innerText = 
                    tipoEscapeGlobal === "Casa" ? traducciones[idiomaActual].txt_tipo_casa : traducciones[idiomaActual].txt_tipo_salida;

                document.getElementById('wrapper-interactive').style.display = 'block';
                
                // Si es salida, inyectamos la tarjeta del lugar de inmediato
                const areaLugar = document.getElementById('interactive-location');
                if (tipoEscapeGlobal === "Salida" && datosLugarGlobal) {
                    areaLugar.innerHTML = `
                        <div class="card-lugar">
                            <h3>📍 Destino Asignado: ${datosLugarGlobal.name}</h3>
                            <p>${datosLugarGlobal.address}</p>
                        </div>
                    `;
                    areaLugar.style.display = 'block';
                } else {
                    areaLugar.style.display = 'none';
                }

                // Arrancar el procesador secuencial de pasos
                procesarPasoMision();
            } else {
                alert(data.message);
                document.getElementById('wrapper-form').style.display = 'block';
            }
        }, 1800);

    } catch (error) {
        console.error("Error del sistema:", error);
        alert("Error de conexión con Open Than Go Server.");
        document.getElementById('wrapper-form').style.display = 'block';
        document.getElementById('wrapper-loader').style.display = 'none';
    }
}

// ----------------------------------------------------
// MOTOR DE PROCESAMIENTO SECUENCIAL (PASO A PASO)
// ----------------------------------------------------
function procesarPasoMision() {
    clearInterval(intervaloRespiracion); // Limpiar cualquier reloj previo
    
    const contenedorPasos = document.getElementById('step-content');
    const botonContinuar = document.getElementById('btn-next');
    const botonGps = document.getElementById('btn-maps-action');
    
    // Ocultar controles por defecto hasta evaluar el tipo de paso
    botonContinuar.style.display = 'none';
    botonGps.style.display = 'none';

    // Validación: Si terminamos todos los bloques de la misión
    if (indicePasoActual >= pasosMisionGlobal.length) {
        if (tipoEscapeGlobal === "Salida" && datosLugarGlobal) {
            // Fin de la misión en exteriores: habilitar GPS definitivo
            botonGps.href = datosLugarGlobal.gps_link;
            botonGps.style.display = 'block';
        } else {
            // Fin de la misión en casa: recargar para permitir otra sesión
            location.reload();
        }
        return;
    }

    const paso = pasosMisionGlobal[indicePasoActual];

    // EVALUACIÓN DE ETIQUETA DINÁMICA DE TU JSON
    
    // 1. Cabeceras decorativas sueltas (v o h)
    if (paso.t === "v" || paso.t === "h") {
        contenedorPasos.innerHTML = `<h3 style="color:var(--secondary); margin:20px 0;">${paso.tx[idiomaActual]}</h3>`;
        botonContinuar.style.display = 'block';
    }
    
    // 2. Bloque de Narrativa Contextual (story)
    else if (paso.story) {
        contenedorPasos.innerHTML = `
            <div class="screen-story">
                <p>${paso.story[idiomaActual]}</p>
            </div>
        `;
        botonContinuar.style.display = 'block';
    }
    
    // 3. Bloque de Regulación Biológica (breath_auto)
    else if (paso.t === "breath_auto") {
        let tiempoRestante = paso.d;
        contenedorPasos.innerHTML = `
            <div class="wrapper-circle">
                <div class="breath-circle" id="circulo-pulso">${tiempoRestante}s</div>
                function evaluarRespuestaTrivia(indiceSeleccionado, indiceCorrecto, explicacionTexto) {
    const contenedorFeedback = document.getElementById('box-feedback');
    if (!contenedorFeedback) return;

    // Deshabilitar el resto de opciones para evitar doble clic
    const botones = document.querySelectorAll('.btn-opcion');
    botones.forEach(btn => btn.disabled = true);

    const esCorrecto = indiceSeleccionado === indiceCorrecto;
    contenedorFeedback.className = esCorrecto ? "feedback-box fb-correcto" : "feedback-box fb-incorrecto";
    
    const prefijo = esCorrecto ? traducciones[idiomaActual].txt_correcto : traducciones[idiomaActual].txt_incorrecto;
    contenedorFeedback.innerHTML = prefijo + explicacionTexto;

    // Habilitar el botón de continuar una vez que el usuario procesó la retroalimentación
    document.getElementById('btn-next').style.display = 'block';
}

function siguienteComando() {
    indicePasoActual++;
    procesarPasoMision();
}

