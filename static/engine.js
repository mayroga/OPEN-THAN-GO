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
let relojSecuencialAutomatico = null;
let cronometroMaestro10Min = null;
let tiempoRestanteMaestro = 600; // 10 minutos exactos en segundos

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
        fin_casa: "Protocolo doméstico terminado. El sistema se apaga automáticamente por tu paz.",
        reloj_maestro_prefijo: "⏱️ Tiempo de Estabilización Restante: "
    },
    en: {
        subtitle: "Your intelligent emotional escape",
        state: "State", region: "Region / County", zip: "ZIP Code", budget: "Available Budget",
        mode: "Go out or stay at home?", desahogo: "Optional Venting (Emotional Filter)",
        placeholder_text: "Write freely about how you feel today...", btn_trigger: "ACTIVATE CONTROL",
        loader: "Synchronizing wellness frequencies...", btn_continue: "CONTINUE", btn_gps: "OPEN MAP IN GPS",
        tipo_casa: "10-Minute Domestic Protocol Activated", tipo_salida: "Exploration Guide Opened",
        txt_correcto: "<strong>TRUE ANSWER!</strong><br>", txt_incorrecto: "<strong>FAILURE ANALYSIS:</strong><br>",
        inspira: "Inhale", expira: "Exhale",
        alerta_35s: "Field preparation active for 35 seconds. Listen to the suggestions carefully before opening the route.",
        fin_casa: "Domestic protocol completed. The system automatically shuts down to preserve your peace.",
        reloj_maestro_prefijo: "⏱️ Remaining Stabilization Time: "
    }
};
function hablarTexto(texto) {
    if (!texto) return;
    window.speechSynthesis.cancel(); // Rompe lecturas anteriores limpiamente
    const lectura = new SpeechSynthesisUtterance(texto);
    lectura.lang = idiomaActual === 'es' ? 'es-US' : 'en-US';
    lectura.rate = 0.88; // Velocidad clínica calmada
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
    const btnTrigger = document.getElementById('btn-main-trigger');
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
        zip_code: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
        estado: document.getElementById('inp-state') ? document.getElementById('inp-state').value : "FL",
        region: document.getElementById('inp-region') ? document.getElementById('inp-region').value : "",
        desahogo: document.getElementById('inp-text') ? document.getElementById('inp-text').value.trim() : ""
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
            document.getElementById('interactive-subtitle').innerText = tipoEscapeGlobal === "Casa" ? traducciones[idiomaActual].tipo_casa : traducciones[idiomaActual].tipo_salida;
            document.getElementById('wrapper-interactive').style.display = 'block';
            // CRONÓMETRO MAESTRO DE CONTROL DE 10 MINUTOS FIJOS EN CASA
            if (tipoEscapeGlobal === "Casa") {
                document.getElementById('wrapper-global-timer').style.display = 'block';
                tiempoRestanteMaestro = 600; 
                ejecutarRelojMaestro10Min();             
                clearTimeout(temporizadorClinicoCasa);
                temporizadorClinicoCasa = setTimeout(() => {
                    hablarTexto(traducciones[idiomaActual].fin_casa);
                    alert(traducciones[idiomaActual].fin_casa);
                    destruirMemoriaYReiniciar();
                }, 600000);
            } else {
                document.getElementById('wrapper-global-timer').style.display = 'none';
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
function ejecutarRelojMaestro10Min() {
    clearInterval(cronometroMaestro10Min);
    const displayGlobal = document.getElementById('global-timer-txt');
    const t = traducciones[idiomaActual];
    cronometroMaestro10Min = setInterval(() => {
        tiempoRestanteMaestro--;
        let mins = Math.floor(tiempoRestanteMaestro / 60);
        let secs = tiempoRestanteMaestro % 60;
        displayGlobal.innerText = `${t.reloj_maestro_prefijo}${mins}:${secs < 10 ? '0' : ''}${secs}`;
        if (tiempoRestanteMaestro <= 0) {
            clearInterval(cronometroMaestro10Min);
            destruirMemoriaYReiniciar();
        }
    }, 1000);
}
function procesarPaoMision() {
    clearInterval(intervaloRespiracion);
    clearTimeout(relojSecuencialAutomatico);    
    const contenedorPasos = document.getElementById('step-content');
        const botonContinuar = document.getElementById('btn-next');
        const botonGps = document.getElementById('btn-maps-action');
        contenedorPasos.innerHTML = "";
        botonContinuar.style.display = 'none';
        botonGps.style.display = 'none';
        if (indicePasoActual >= pasosMisionGlobal.length) {
            if (tipoEscapeGlobal === "Casa") {
                // REQUERIMIENTO AUTOMÁTICO PARA CASA: Sigue corriendo en bucle hasta cumplir los 10 minutos
                indicePasoActual = 0; 
                procesarPaoMision();
                return;
            }
            if (tipoEscapeGlobal === "Salida" && datosLugarGlobal) {
                contenedorPasos.innerHTML = `
                    <div class="card-lugar" style="margin-top:20px;">
                        <h3 style="color:var(--accent); font-weight:800; text-transform:uppercase;">🧭 Protocolo de Despliegue</h3>
                        <p style="font-size:14px; margin:8px 0; line-height:1.4;">${datosLugarGlobal.address}</p>
                        <hr style="border:0; border-top:1px dashed #ddd; margin:10px 0;">
                        <p style="font-size:13px; font-weight:700; color:var(--primary); margin-bottom:5px;">Sugerencia de Enfoque en tus 3 Puntos Críticos:</p>
                        <p style="font-size:13px; line-height:1.4; font-style:italic; color:#444;">${datosLugarGlobal.analisis_sugerido}</p>
                    </div>`;
                let cuentaRegresivaSalir = 35;
                botonContinuar.innerText = `${cuentaRegresivaSalir}s`;
                botonContinuar.disabled = true;
                botonContinuar.style.display = 'block';
                hablarTexto(traducciones[idiomaActual].alerta_35s + " . Tres sugerencias de enfoque: " + datosLugarGlobal.analisis_sugerido);
                let relojSalida = setInterval(() => {
                    cuentaRegresivaSalir--;
                    botonContinuar.innerText = cuentaRegresivaSalir + "s";
                    if(cuentaRegresivaSalir <= 0) {
                        clearInterval(relojSalida);
                        botonContinuar.style.display = 'none';
                        botonGps.href = datosLugarGlobal.gps_link;
                        botonGps.style.display = 'block';
                    }
                }, 1000);
            } else {
                destruirMemoriaYReiniciar();
            }
            return;
        }
        const paso = pasosMisionGlobal[indicePasoActual];
        if (paso.t === "v" || paso.t === "h") {
            let textoLabel = paso.tx;
            contenedorPasos.innerHTML = `<h3 style="color:var(--secondary); margin:20px 0; font-size:18px; font-weight:800;">${textoLabel}</h3>`;
            hablarTexto(textoLabel);
            
            if (tipoEscapeGlobal === "Casa") {
                relojSecuencialAutomatico = setTimeout(() => { siguienteComando(); }, 8000);
            } else {
                botonContinuar.style.display = 'block';
            }
        } else if (paso.story) {
            contenedorPasos.innerHTML = `<div class="screen-story"><p>${paso.story}</p></div>`;
            hablarTexto(paso.story);
            
            if (tipoEscapeGlobal === "Casa") {
                relojSecuencialAutomatico = setTimeout(() => { siguienteComando(); }, 12000);
            } else {
                botonContinuar.style.display = 'block';
            }
        } else if (paso.t === "breath_auto") {
            let tiempoRestante = paso.d;
            contenedorPasos.innerHTML = `
                <div class="wrapper-circle">
                    <div class="breath-circle expand" id="circulo-pulso">
                        <span id="txt-segundos-circulo">${tiempoRestante}s</span>
                        <div class="txt-instruccion-pulmon" id="txt-pulmon-accion">INHALA</div>
                    </div>
                    <p style="font-weight:600; margin-top:25px; font-size:15px; color:var(--primary);">${paso.tx}</p>
                    <p class="breath-inf" style="font-size:12px; color:#666; max-width:90%; margin:5px auto; line-height:1.4;">${paso.inf}</p>
                </div>`;
            hablarTexto(paso.tx + " . " + paso.inf);
            let circulo = document.getElementById('circulo-pulso');
            let indicadorTexto = document.getElementById('txt-pulmon-accion');
            let modoExpansion = true;
            intervaloRespiracion = setInterval(() => {
                tiempoRestante--;
                if (document.getElementById('txt-segundos-circulo')) {
                    document.getElementById('txt-segundos-circulo').innerText = `${tiempoRestante}s`;
                }
                // Ciclo somático visual de expansión pulmonar cada 4 segundos
                let cicloSegundo = tiempoRestante % 8;
                if (cicloSegundo >= 4) {
                    if(circulo) circulo.className = "breath-circle expand";
                    if(indicadorTexto) circulo.innerText = idiomaActual === 'es' ? "INHALA" : "BREATHE IN";
                } else {
                    if(circulo) circulo.className = "breath-circle contract";
                    if(indicadorTexto) circulo.innerText = idiomaActual === 'es' ? "EXHALA" : "BREATHE OUT";
                }
                if (tiempoRestante <= 0) {
                    clearInterval(intervaloRespiracion);
                    siguienteComando();
                }
            }, 1000);
        } else if (paso.t === "d") {
            // SOLUCIÓN BRUTAL DE LA MONOTONÍA POSICIONAL: Mapeo y Shuffling aleatorio
            let mapeoOpciones = paso.op.map((texto, idx) => ({ texto: texto, idxOriginal: idx }));
            mapeoOpciones.sort(() => Math.random() - 0.5);
            let opcionesHtml = "";
            mapeoOpciones.forEach((item) => {
                let explicacionSanada = paso.ex[item.idxOriginal].replace(/'/g, "\\'");
                opcionesHtml += `<button class="btn-opcion" id="opt-${item.idxOriginal}" onclick="evaluarTriviaMargenReintento(${item.idxOriginal}, ${paso.c}, '${explicacionSanada}')"> ${item.texto} </button>`;
            });
            contenedorPasos.innerHTML = `
                <div class="bloque-decision">
                    <p style="font-weight:700; font-size:15px; color:var(--primary); line-height:1.4; margin-bottom:15px; text-align:left;">${paso.q}</p>
                    <div class="contenedor-opciones">${opcionesHtml}</div>
                    <div id="box-feedback" class="feedback-box"></div>
                </div>`;
            hablarTexto(paso.q);
        } else if (paso.t === "r") {
            contenedorPasos.innerHTML = `
                <div style="margin:25px 0; text-align:center;">
                    <span style="font-size:50px;">💎</span>
                    <h2 style="color:var(--accent); margin:10px 0; font-weight:800;">${paso.tx}</h2>
                </div>`;
            hablarTexto(paso.tx);            
            if (tipoEscapeGlobal === "Casa") {
                relojSecuencialAutomatico = setTimeout(() => { siguienteComando(); }, 4000);
            } else {
                botonContinuar.style.display = 'block';
            }
        } else if (paso.t === "c") {
            contenedorPasos.innerHTML = `<div style="padding:20px; background:#fffde7; border-radius:10px; margin:15px 0; border:1px dashed #fbc02d;"><p style="font-style:italic; font-size:15px; margin:0; font-weight:500; line-height:1.4;">"${paso.tx}"</p></div>`;
            hablarTexto(paso.tx);           
            if (tipoEscapeGlobal === "Casa") {
                relojSecuencialAutomatico = setTimeout(() => { siguienteComando(); }, 8000);
            } else {
                botonContinuar.style.display = 'block';
            }
        } else if (paso.t === "sil") {
            contenedorPasos.innerHTML = `
                <div style="text-align:left; background:#f3e5f5; padding:16px; border-radius:10px; border:1px solid #e1bee7;">
                    <p style="font-size:14px; margin:0 0 10px 0; line-height:1.4;"><strong>Misión Práctica:</strong> ${paso.tx}</p>
                    <small style="color:#4a148c; display:block; font-weight:600;">💡 Enfoque: ${paso.inf}</small>
                </div>`;
            hablarTexto(paso.tx + " . Enfoque mental: " + paso.inf);           
            if (tipoEscapeGlobal === "Casa") {
                relojSecuencialAutomatico = setTimeout(() => { siguienteComando(); }, 12000);
            } else {
                botonContinuar.style.display = 'block';
            }
        }
    }
    function evaluarTriviaMargenReintento(indiceSeleccionado, indiceCorrecto, explicacionTexto) {
        const contenedorFeedback = document.getElementById('box-feedback');
        if (!contenedorFeedback) return;        
        const esCorrecto = indiceSeleccionado === indiceCorrecto;
        contenedorFeedback.className = esCorrecto ? "feedback-box fb-correcto" : "feedback-box fb-incorrecto";        
        // REQUERIMIENTO EXPLICACIÓN OBLIGATORIA: Define por qué está bien o mal en su idioma nativo
        const prefijo = esCorrecto ? traducciones[idiomaActual].txt_correcto : traducciones[idiomaActual].txt_incorrecto;
        contenedorFeedback.innerHTML = prefijo + explicacionTexto;
        contenedorFeedback.style.display = "block";
        const textoLimpioExplicacion = explicacionTexto.replace(/<[^>]*>/g, '');
        // PERMITE DAR CLIC EN TODAS LAS PREGUNTAS: No bloquea las opciones incorrectas, solo las atenúa
        if (esCorrecto) {
            const botones = document.querySelectorAll('.btn-opcion');
            botones.forEach(btn => btn.disabled = true); // Bloquea tras ganar para pasar de nivel
            hablarTexto((idiomaActual === 'es' ? "Verdadero. " : "True. ") + textoLimpioExplicacion);
            document.getElementById('btn-next').style.display = 'block';
        } else {
                    document.getElementById(`opt-${indiceSeleccionado}`).style.opacity = "0.4";
        hablarTexto((idiomaActual === 'es' ? "Falso. " : "False. ") + textoLimpioExplicacion);
    }
}
function destruirMemoriaYReiniciar() {
    clearTimeout(temporizadorClinicoCasa);
    clearInterval(intervaloRespiracion);
    clearInterval(cronometroMaestro10Min);
    clearTimeout(relojSecuencialAutomatico);
    pasosMisionGlobal = [];
    datosLugarGlobal = null;
    indicePasoActual = 0;
    location.reload();
}
function siguienteComando() {
    clearTimeout(relojSecuencialAutomatico);
    indicePasoActual++;
    procesarPaoMision();
}

