// OPEN THAN GO SYSTEM - Frontend Voice & Somatic Engine
// Company: May Roga LLC
// File: static/engine.js

// Variables de estado global de la sesión interactiva
let idiomaActual = 'es';
let presupuestoActual = 'cero';
let modalidadSalir = true; 
let pasosMisionGlobal = [];
let indicePasoActual = 0;
let datosLugarGlobal = null;
let tipoEscapeGlobal = "";
let intervaloRespiracion = null;

const traducciones = {
    es: {
        subtitle: "Tu escape emocional inteligente",
        state: "Estado", region: "Región / Condado", zip: "ZIP Code", budget: "Presupuesto Disponible",
        mode: "¿Salir o quedarte en casa?", desahogo: "Desahogo Opcional (Filtro Emocional)",
        placeholder_text: "Escribe libremente cómo te sientes hoy...", btn_trigger: "GENERAR ESCAPE",
        loader: "Calculando tu vector de escape ideal...", btn_continue: "CONTINUAR", btn_gps: "ABRIR MAPA EN GPS",
        tipo_casa: "Protocolo Doméstico Activado", tipo_salida: "Protocolo de Exploración Abierto",
        txt_correcto: "<strong>¡Excelente elección!</strong><br>", txt_incorrecto: "<strong>Analiza esto con calma:</strong><br>",
        inspira: "Inhala / Inspira", expira: "Exhala / Expira"
    },
    en: {
        subtitle: "Your intelligent emotional escape",
        state: "State", region: "Region / County", zip: "ZIP Code", budget: "Available Budget",
        mode: "Go out or stay at home?", desahogo: "Optional Venting (Emotional Filter)",
        placeholder_text: "Write freely about how you feel today...", btn_trigger: "GENERATE ESCAPE",
        loader: "Calculating your ideal escape vector...", btn_continue: "CONTINUE", btn_gps: "OPEN MAP IN GPS",
        tipo_casa: "Domestic Protocol Activated", tipo_salida: "Exploration Protocol Opened",
        txt_correcto: "<strong>Excellent choice!</strong><br>", txt_incorrecto: "<strong>Analyze this calmly:</strong><br>",
        inspira: "Inhale", expira: "Exhale"
    }
};

// ----------------------------------------------------
// MOTOR DE AUDIO (SÍNTESIS DE VOZ NATIIVA)
// ----------------------------------------------------
function hablarTexto(texto) {
    window.speechSynthesis.cancel();
    if (!texto) return;
    
    const lectura = new SpeechSynthesisUtterance(texto);
    lectura.lang = idiomaActual === 'es' ? 'es-US' : 'en-US'; 
    lectura.rate = 0.95; 
    lectura.pitch = 1.0; 
    window.speechSynthesis.speak(lectura);
}

// ----------------------------------------------------
// INTERFAZ DE USUARIO Y CONFIGURACIÓN
// ----------------------------------------------------
function cambiarIdioma(lang) {
    idiomaActual = lang;
    document.getElementById('lang-es').classList.toggle('active', lang === 'es');
    document.getElementById('lang-en').classList.toggle('active', lang === 'en');
    
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
        if (elemento) elemento.classList.toggle('active', id === `b-${opcion}`);
    });
}

function cambiarModalidad(esSalir) {
    modalidadSalir = esSalir;
    document.getElementById('m-salir').classList.toggle('active', esSalir === true);
    document.getElementById('m-casa').classList.toggle('active', esSalir === false);
    
    const displayGeografia = esSalir ? 'block' : 'none';
    document.getElementById('inp-state').parentElement.style.display = displayGeografia;
    document.getElementById('inp-region').parentElement.style.display = displayGeografia;
    document.getElementById('inp-zip').parentElement.style.display = displayGeografia;
}

// ----------------------------------------------------
// PETICIÓN ASÍNCRONA UNIFICADA AL BACKEND
// ----------------------------------------------------
async function solicitarEscape() {
    // UNIFICACIÓN DE VARIABLES: Sincronizado al 100% con main.py
    const payload = {
        decision: modalidadSalir ? "salir" : "casa",
        lang: idiomaActual,
        budget_level: presupuestoActual,
        zip_code: document.getElementById('inp-zip').value.trim(),
        estado: document.getElementById('inp-state').value,
        region: document.getElementById('inp-region').value,
        desahogo: document.getElementById('inp-text').value.trim()
    };

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

        setTimeout(() => {
            document.getElementById('wrapper-loader').style.display = 'none';

            if (data.status === 'success' && data.mision && data.mision.b) {
                pasosMisionGlobal = data.mision.b;
                datosLugarGlobal = data.lugar || null;
                tipoEscapeGlobal = data.tipo;
                indicePasoActual = 0;

                document.getElementById('interactive-title').innerText = "OPEN THAN GO";
                document.getElementById('interactive-subtitle').innerText = 
                    tipoEscapeGlobal === "Casa" ? traducciones[idiomaActual].tipo_casa : traducciones[idiomaActual].tipo_salida;

                document.getElementById('wrapper-interactive').style.display = 'block';
                
                const areaLugar = document.getElementById('interactive-location');
                if (tipoEscapeGlobal === "Salida" && datosLugarGlobal) {
                    areaLugar.innerHTML = `
                        <div class="card-lugar">
                            <h3>📍 ${datosLugarGlobal.name}</h3>
                            <p>${datosLugarGlobal.address}</p>
                        </div>
                    `;
                    areaLugar.style.display = 'block';
                } else {
                    areaLugar.style.display = 'none';
                }

                procesarPasoMision();
            } else {
                alert(data.message || "Error al sincronizar con el servidor.");
                document.getElementById('wrapper-form').style.display = 'block';
            }
        }, 1200);

    } catch (error) {
        console.error("Error crítico de comunicación:", error);
        alert("Error de conexión. Reconectando con Open Than Go...");
        document.getElementById('wrapper-form').style.display = 'block';
        document.getElementById('wrapper-loader').style.display = 'none';
    }
}

// ----------------------------------------------------
// PROCESADOR SECUENCIAL AUTOMÁTICO DE PASOS
// ----------------------------------------------------
function procesarPasoMision() {
    clearInterval(intervaloRespiracion);
    window.speechSynthesis.cancel();
    
    const botonContinuar = document.getElementById('btn-next');
    const botonGps = document.getElementById('btn-maps-action');
    
    botonContinuar.style.display = 'none';
    botonGps.style.display = 'none';

    // BLINDAJE DE CONTENEDOR: Crea dinámicamente el lienzo de texto si no existe en el HTML
    let contenedorPasos = document.getElementById('step-content');
    if (!contenedorPasos) {
        contenedorPasos = document.createElement('div');
        contenedorPasos.id = 'step-content';
        const wrapperInteractive = document.getElementById('wrapper-interactive');
        wrapperInteractive.insertBefore(contenedorPasos, botonContinuar);
    }

    if (indicePasoActual >= pasosMisionGlobal.length) {
        if (tipoEscapeGlobal === "Salida" && datosLugarGlobal) {
            botonGps.href = datosLugarGlobal.gps_link;
            botonGps.style.display = 'block';
        } else {
            location.reload();
        }
        return;
    }

    const paso = pasosMisionGlobal[indicePasoActual];

    // Evaluar etiquetas de tus archivos JSON
    if (paso.t === "v" || paso.t === "h") {
        contenedorPasos.innerHTML = `<h3 style="color:var(--secondary); margin:20px 0;">${paso.tx[idiomaActual]}</h3>`;
        hablarTexto(paso.tx[idiomaActual]);
        botonContinuar.style.display = 'block';
    }
    
    else if (paso.story) {
        contenedorPasos.innerHTML = `
            <div class="screen-story">
                <p>${paso.story[idiomaActual]}</p>
            </div>
        `;
        hablarTexto(paso.story[idiomaActual]);
        botonContinuar.style.display = 'block';
    }
    
    else if (paso.t === "breath_auto") {
        let tiempoRestante = paso.d;
        contenedorPasos.innerHTML = `
            <div class="wrapper-circle">
                <div class="breath-circle animar-respiracion" id="circulo-pulso">${tiempoRestante}s</div>
                <div class="txt-instruccion-pulmon" id="txt-pulmon-accion">---</div>
                }

