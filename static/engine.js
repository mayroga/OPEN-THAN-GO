// OPEN THAN GO SYSTEM - Somatic Voice Engine
// Company: May Roga LLC
// File: static/engine.js

let idiomaActual = 'es';
let presupuestoActual = 'cero';
let modalidadSalir = true; 
let pasosMisionGlobal = [];
let indicePasoActual = 0;
let datosLugarGlobal = null;
let tipoEscapeGlobal = "";
let intervaloRespiracion = null;
let temporizadorClinicoCasa = null;

const traducciones = {
    es: {
        subtitle: "Tu escape emocional inteligente",
        state: "Estado", region: "Región / Condado", zip: "ZIP Code", budget: "Presupuesto Disponible",
        mode: "¿Salir o quedarte en casa?", desahogo: "Desahogo Opcional (Filtro Emocional)",
        placeholder_text: "Escribe libremente cómo te sientes hoy...", btn_trigger: "ACTIVAR MANDO",
        loader: "Sincronizando frecuencias de bienestar...", btn_continue: "CONTINUAR", btn_gps: "ABRIR MAPA EN GPS",
        tipo_casa: "Protocolo Doméstico de 10 Minutos Activado", tipo_salida: "Guía de Exploración Abierta",
        txt_correcto: "<strong>¡RESPUESTA VERDADERA!</strong><br>", txt_incorrecto: "<strong>ANÁLISIS DE FALLO:</strong><br>",
        inspira: "Inhala / Inspira", expira: "Exhala / Expira",
        alerta_35s: "Preparación de campo activa por 35 segundos. Escucha las sugerencias atentamente antes de abrir la ruta.",
        fin_casa: "Protocolo doméstico terminado. El sistema se apaga automáticamente por tu paz."
    },
    en: {
        subtitle: "Your intelligent emotional escape",
        state: "State", region: "Region / County", zip: "ZIP Code", budget: "Available Budget",
        mode: "Go out or stay at home?", desahogo: "Optional Venting (Emotional Filter)",
        placeholder_text: "Write freely about how you feel today...", btn_trigger: "ACTIVAR MANDO",
        loader: "Synchronizing wellness frequencies...", btn_continue: "CONTINUE", btn_gps: "OPEN MAP IN GPS",
        tipo_casa: "10-Minute Domestic Protocol Activated", tipo_salida: "Exploration Guide Opened",
        txt_correcto: "<strong>TRUE ANSWER!</strong><br>", txt_incorrecto: "<strong>FAILURE ANALYSIS:</strong><br>",
        inspira: "Inhale", expira: "Exhale",
        alerta_35s: "Field preparation active for 35 seconds. Listen to the suggestions carefully before opening the route.",
        fin_casa: "Domestic protocol completed. The system automatically shuts down to preserve your peace."
    }
};

function hablarTexto(texto) {
    if (!texto) return;
    // Detiene lecturas viejas solo al invocar un NUEVO paso, nunca por segundo
    window.speechSynthesis.cancel(); 
    
    const lectura = new SpeechSynthesisUtterance(texto);
    lectura.lang = idiomaActual === 'es' ? 'es-US' : 'en-US';
    lectura.rate = 0.88; 
    lectura.pitch = 1.0;
    window.speechSynthesis.speak(lectura);
}

function cambiarIdioma(lang) {
    idiomaActual = lang;
    document.getElementById('lang-es').classList.toggle('active', lang === 'es');
    document.getElementById('lang-en').classList.toggle('active', lang === 'en');
    
    if(document.getElementById('txt-subtitle')) document.getElementById('txt-subtitle').innerText = traducciones[lang].subtitle;
    if(document.getElementById('lbl-state')) document.getElementById('lbl-state').innerText = traducciones[lang].state;
    if(document.getElementById('lbl-region')) document.getElementById('lbl-region').innerText = traducciones[lang].region;
    if(document.getElementById('lbl-zip')) document.getElementById('lbl-zip').innerText = traducciones[lang].zip;
    if(document.getElementById('lbl-budget')) document.getElementById('lbl-budget').innerText = traducciones[lang].budget;
    if(document.getElementById('lbl-mode')) document.getElementById('lbl-mode').innerText = traducciones[lang].mode;
    if(document.getElementById('lbl-desahogo')) document.getElementById('lbl-desahogo').innerText = traducciones[lang].desahogo;
    if(document.getElementById('inp-text')) document.getElementById('inp-text').placeholder = traducciones[lang].placeholder_text;
    
    const btnTrigger = document.getElementById('btn-main-trigger') || document.querySelector('.btn-trigger');
    if(btnTrigger) btnTrigger.innerText = traducciones[lang].btn_trigger;
    
    if(document.getElementById('txt-loader')) document.getElementById('txt-loader').innerText = traducciones[lang].loader;
    if(document.getElementById('btn-next')) document.getElementById('btn-next').innerText = traducciones[lang].btn_continue;
    if(document.getElementById('btn-maps-action')) document.getElementById('btn-maps-action').innerText = traducciones[lang].btn_gps;
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
    if(document.getElementById('inp-state')) document.getElementById('inp-state').parentElement.style.display = displayGeografia;
    if(document.getElementById('inp-region')) document.getElementById('inp-region').parentElement.style.display = displayGeografia;
    if(document.getElementById('inp-zip')) document.getElementById('inp-zip').parentElement.style.display = displayGeografia;
}

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
            
            // Reloj clínico estricto de 10 minutos en casa para apagarse solo
            if (tipoEscapeGlobal === "Casa") {
                clearTimeout(temporizadorClinicoCasa);
                temporizadorClinicoCasa = setTimeout(() => {
                    hablarTexto(traducciones[idiomaActual].fin_casa);
                    alert(traducciones[idiomaActual].fin_casa);
                    destruirMemoriaYReiniciar();
                }, 600000); 
            }

            procesarPaoMision();
        } else {
            alert(data.message || "Error al sincronizar canales emocionales.");
            document.getElementById('wrapper-form').style.display = 'block';
        }
    } catch (error) {
        alert("Error de enlace con el servidor.");
        document.getElementById('wrapper-form').style.display = 'block';
        document.getElementById('wrapper-loader').style.display = 'none';
    }
}

function procesarPaoMision() {
    clearInterval(intervaloRespiracion);
    
    const contenedorPasos = document.getElementById('step-content');
    const botonContinuar = document.getElementById('btn-next');
    const botonGps = document.getElementById('btn-maps-action');
    
    // Limpieza de memoria visual de escritura previa para evitar bloqueos
    contenedorPasos.innerHTML = "";
    botonContinuar.style.display = 'none';
    botonGps.style.display = 'none';

    if (indicePasoActual >= pasosMisionGlobal.length) {
        if (tipoEscapeGlobal === "Salida" && datosLugarGlobal) {
            contenedorPasos.innerHTML = `
                <div class="card-lugar" style="margin-top:20px;">
                    <h3 style="color:var(--accent); font-weight:800; text-transform:uppercase;">🧭 Protocolo de Despliegue</h3>
                    <p style="font-size:14px; margin:8px 0; line-height:1.4;">${datosLugarGlobal.address}</p>
                    <hr style="border:0; border-top:1px dashed #ddd; margin:10px 0;">
                    <p style="font-size:13px; font-weight:700; color:var(--primary); margin-bottom:5px;">Sugerencia de Enfoque en tus 3 Puntos Críticos:</p>
                    <p style="font-size:13px; line-height:1.4; font-style:italic; color:#444;">${datosLugarGlobal.analisis_sugerido}</p>
                </div>
            `;
            
            let cuentaRegresivaSalir = 35;
            botonContinuar.innerText = `${cuentaRegresivaSalir}s`;
            botonContinuar.disabled = true;
            botonContinuar.style.display = 'block';
            
            // La voz lee obligatoriamente la guía explicativa completa sin cortarse
            hablarTexto(traducciones[idiomaActual].alerta_35s + " . Tres sugerencias de enfoque: " + datosLugarGlobal.analisis_sugerido);
            
                let relojSalida = setInterval(() => {
                cuentaRegresivaSalir--;
                botonContinuar.innerText = cuentaRegresivaSalir + "s";
                if(cuentaRegresivaSalir <= 0) {
                    clearInterval(relojSalida);
                    botonContinuar.style.display = 'none';
                    
                    // DESPLIEGUE OBLIGATORIO DE MAPA EN VIVO SIN MARCHA ATRÁS
                    botonGps.href = datosLugarGlobal.gps_link;
                    botonGps.style.display = 'block';
                    
                    // Corrección definitiva para abrir la app nativa de Google Maps en el celular
                    window.open(datosLugarGlobal.gps_link, '_blank');
                }
            }, 1000);

        } else {
            destruirMemoriaYReiniciar();
        }
        return;
    }

    const paso = pasosMisionGlobal[indicePasoActual];

    if (paso.t === "v" || paso.t === "h") {
        let textoLabel = typeof paso.tx === 'object' ? paso.tx[idiomaActual] : paso.tx;
        contenedorPasos.innerHTML = `<h3 style="color:var(--secondary); margin:20px 0; font-size:18px; font-weight:800;">${textoLabel}</h3>`;
        hablarTexto(textoLabel);
        botonContinuar.style.display = 'block';
    }
    
    else if (paso.story) {
        contenedorPasos.innerHTML = `<div class="screen-story"><p>${paso.story[idiomaActual]}</p></div>`;
        hablarTexto(paso.story[idiomaActual]);
        botonContinuar.style.display = 'block';
    }
    
    else if (paso.t === "breath_auto") {
        let tiempoRestante = paso.d;
        contenedorPasos.innerHTML = `
            <div class="wrapper-circle"> 
                <div class="breath-circle animar-respiracion" id="circulo-pulso">${tiempoRestante}s</div> 
                <div class="txt-instruccion-pulmon" id="txt-pulmon-accion">---</div> 
                <p style="font-weight:600; margin-top:15px; font-size:15px; color:var(--primary);">${paso.tx[idiomaActual]}</p> 
                <p class="breath-inf">${paso.inf[idiomaActual]}</p> 
            </div>`;
            
        // CORRECCIÓN CLÍNICA: La voz lee todo el texto continuo de la respiración de corrido sin interrupción
        hablarTexto(paso.tx[idiomaActual] + " . " + paso.inf[idiomaActual]);

        intervaloRespiracion = setInterval(() => {
            tiempoRestante--;
            const circulo = document.getElementById('circulo-pulso');
            const indicadorTexto = document.getElementById('txt-pulmon-accion');
            if (circulo) circulo.innerText = `${tiempoRestante}s`;
            
            // Control visual del pulmón en pantalla (In/Out) sin invocar SpeechSynthesis interno que corte el audio anterior
            if (indicadorTexto) {
                let cicloSegundo = tiempoRestante % 8;
                if (cicloSegundo >= 4) {
                    indicadorTexto.innerText = traducciones[idiomaActual].inspira;
                    indicadorTexto.style.color = "#00bcd4";
                } else {
                    indicadorTexto.innerText = traducciones[idiomaActual].expira;
                    indicadorTexto.style.color = "#d84315";
                }
            }
            if (tiempoRestante <= 0) {
                clearInterval(intervaloRespiracion);
                botonContinuar.style.display = 'block';
            }
        }, 1000);
    }
    
    else if (paso.t === "d") {
        let opcionesHtml = "";
        paso.op.forEach((opcion, index) => {
            opcionesHtml += `<button class="btn-opcion" id="opt-${index}" onclick="evaluarTriviaMargenReintento(${index}, ${paso.c}, '${paso.ex[index][idiomaActual].replace(/'/g, "\\'")}')"> ${opcion[idiomaActual]} </button>`;
        });
        contenedorPasos.innerHTML = `
            <div class="bloque-decision"> 
                <p style="font-weight:700; font-size:14px; color:var(--primary); line-height:1.4; margin-bottom:12px;">${paso.q[idiomaActual]}</p> 
                <div class="contenedor-opciones">${opcionesHtml}</div> 
                <div id="box-feedback" class="feedback-box"></div> 
            </div>`;
        hablarTexto(paso.q[idiomaActual]);
    }
    
    else if (paso.t === "r") {
        contenedorPasos.innerHTML = `
            <div style="margin:25px 0; text-align:center;"> 
                <span style="font-size:50px;">💎</span> 
                <h2 style="color:var(--accent); margin:10px 0; font-weight:800;">${paso.tx}</h2> 
            </div>`;
        hablarTexto(paso.tx);
        botonContinuar.style.display = 'block';
    }
    
    else if (paso.t === "c") {
        contenedorPasos.innerHTML = `<div style="padding:20px; background:#fffde7; border-radius:10px; margin:15px 0; border:1px dashed #fbc02d;"><p style="font-style:italic; font-size:15px; margin:0; font-weight:500; line-height:1.4;">"${paso.tx[idiomaActual]}"</p></div>`;
        hablarTexto(paso.tx[idiomaActual]);
        botonContinuar.style.display = 'block';
    }
    
    else if (paso.t === "sil") {
        contenedorPasos.innerHTML = `
            <div style="text-align:left; background:#f3e5f5; padding:16px; border-radius:10px; border:1px solid #e1bee7;"> 
                <p style="font-size:14px; margin:0 0 10px 0; line-height:1.4;"><strong>Misión Práctica:</strong> ${paso.tx[idiomaActual]}</p> 
                <small style="color:#4a148c; display:block; font-weight:600;">💡 Enfoque: ${paso.inf[idiomaActual]}</small> 
            </div>`;
        hablarTexto(paso.tx[idiomaActual] + " . Enfoque mental: " + paso.inf[idiomaActual]);
        botonContinuar.style.display = 'block';
    }
}

// MARGEN DE REINTENTO: Explica fallos con voz, oculta malas opciones y obliga a tocar la correcta
function evaluarTriviaMargenReintento(indiceSeleccionado, indiceCorrecto, explicacionTexto) {
    const contenedorFeedback = document.getElementById('box-feedback');
    if (!contenedorFeedback) return;
    const esCorrecto = indiceSeleccionado === indiceCorrecto;
    contenedorFeedback.className = esCorrecto ? "feedback-box fb-correcto" : "feedback-box fb-incorrecto";
    
    const prefijo = esCorrecto ? traducciones[idiomaActual].txt_correcto : traducciones[idiomaActual].txt_incorrecto;
    contenedorFeedback.innerHTML = prefijo + explicacionTexto;
    const textoLimpioExplicacion = explicacionTexto.replace(/<[^>]*>/g, '');
    
    if (esCorrecto) {
        const botones = document.querySelectorAll('.btn-opcion');
        botones.forEach(btn => btn.disabled = true);
        hablarTexto((idiomaActual === 'es' ? "Verdadero. " : "True. ") + textoLimpioExplicacion);
        document.getElementById('btn-next').style.display = 'block';
    } else {
        document.getElementById(`opt-${indiceSeleccionado}`).style.opacity = "0.4";
        document.getElementById(`opt-${indiceSeleccionado}`).style.pointerEvents = "none";
        hablarTexto((idiomaActual === 'es' ? "Falso. " : "False. ") + textoLimpioExplicacion);
    }
}

function destruirMemoriaYReiniciar() {
    clearTimeout(temporizadorClinicoCasa);
    clearInterval(intervaloRespiracion);
    pasosMisionGlobal = [];
    datosLugarGlobal = null;
    indicePasoActual = 0;
    location.reload(); // Borra la caché visual del navegador de forma instantánea
}

function siguienteComando() {
    indicePasoActual++;
    procesarPaoMision();
}
