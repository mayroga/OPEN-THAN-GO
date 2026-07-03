// OPEN THAN GO SYSTEM - Frontend Voice & Somatic Engine
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
        btn_trigger: "ACTIVAR MANDO",
        loader: "Sincronizando frecuencias de bienestar...",
        btn_continue: "CONTINUAR",
        btn_gps: "ABRIR MAPA EN GPS",
        tipo_casa: "Protocolo Doméstico Activado",
        tipo_salida: "Protocolo de Exploración Abierto",
        txt_correcto: "<strong>¡Excelente elección!</strong><br>",
        txt_incorrecto: "<strong>Analiza esto con calma:</strong><br>",
        inspira: "Inhala / Inspira",
        expira: "Exhala / Expira"
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
        btn_trigger: "ACTIVAR MANDO",
        loader: "Synchronizing wellness frequencies...",
        btn_continue: "CONTINUE",
        btn_gps: "OPEN MAP IN GPS",
        tipo_casa: "Domestic Protocol Activated",
        tipo_salida: "Exploration Protocol Opened",
        txt_correcto: "<strong>Excellent choice!</strong><br>",
        txt_incorrecto: "<strong>Analyze this calmly:</strong><br>",
        inspira: "Inhale",
        expira: "Exhale"
    }
};

function hablarTexto(texto) {
    window.speechSynthesis.cancel();
    if (!texto) return;
    const lectura = new SpeechSynthesisUtterance(texto);
    lectura.lang = idiomaActual === 'es' ? 'es-US' : 'en-US';
    lectura.rate = 0.90;
    window.speechSynthesis.speak(lectura);
}

function cambiarIdioma(lang) {
    idiomaActual = lang;
    document.getElementById('lang-es').classList.toggle('active', lang === 'es');
    document.getElementById('lang-en').classList.toggle('active', lang === 'en');
   
    // Verificación de protección de elementos del formulario para evitar congelamientos
    if(document.getElementById('txt-subtitle')) document.getElementById('txt-subtitle').innerText = traducciones[lang].subtitle;
    if(document.getElementById('lbl-state')) document.getElementById('lbl-state').innerText = traducciones[lang].state;
    if(document.getElementById('lbl-region')) document.getElementById('lbl-region').innerText = traducciones[lang].region;
    if(document.getElementById('lbl-zip')) document.getElementById('lbl-zip').innerText = traducciones[lang].zip;
    if(document.getElementById('lbl-budget')) document.getElementById('lbl-budget').innerText = traducciones[lang].budget;
    if(document.getElementById('lbl-mode')) document.getElementById('lbl-mode').innerText = traducciones[lang].mode;
    if(document.getElementById('lbl-desahogo')) document.getElementById('lbl-desahogo').innerText = traducciones[lang].desahogo;
    if(document.getElementById('inp-text')) document.getElementById('inp-text').placeholder = traducciones[lang].placeholder_text;
   
    // Sincronización automática del botón disparador según tu HTML actual
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
           
            const areaLugar = document.getElementById('interactive-location');
            if (tipoEscapeGlobal === "Salida" && datosLugarGlobal) {
                areaLugar.innerHTML = `
                    <div class="card-lugar">
                        <h3>${datosLugarGlobal.name}</h3>
                        <p>${datosLugarGlobal.address}</p>
                    </div>
                `;
                areaLugar.style.display = 'block';
            } else {
                areaLugar.style.display = 'none';
            }

            procesarPasoMision();
        } else {
            alert(data.message || "Error al procesar la sesión.");
            document.getElementById('wrapper-form').style.display = 'block';
        }
    } catch (error) {
        alert("Error de conexión con el servidor.");
        document.getElementById('wrapper-form').style.display = 'block';
        document.getElementById('wrapper-loader').style.display = 'none';
    }
}

function procesarPasoMision() {
    clearInterval(intervaloRespiracion);
    window.speechSynthesis.cancel();
   
    const contenedorPasos = document.getElementById('step-content');
    const botonContinuar = document.getElementById('btn-next');
    const botonGps = document.getElementById('btn-maps-action');
   
    botonContinuar.style.display = 'none';
    botonGps.style.display = 'none';

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

    if (paso.t === "v" || paso.t === "h") {
        let textoLabel = typeof paso.tx === 'object' ? paso.tx[idiomaActual] : paso.tx;
        contenedorPasos.innerHTML = `<h3 style="color:var(--secondary); margin:20px 0; font-size:18px;">${textoLabel}</h3>`;
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
                <p style="font-weight:600; margin-top:15px; font-size:15px;">${paso.tx[idiomaActual]}</p>
                <p class="breath-inf">${paso.inf[idiomaActual]}</p>
            </div>
        `;
        hablarTexto(paso.tx[idiomaActual]);

        intervaloRespiracion = setInterval(() => {
            tiempoRestante--;
            const circulo = document.getElementById('circulo-pulso');
            const indicadorTexto = document.getElementById('txt-pulmon-accion');
            if (circulo) circulo.innerText = `${tiempoRestante}s`;
           
            if (indicadorTexto) {
                let cicloSegundo = tiempoRestante % 8;
                if (cicloSegundo >= 4) {
                    if (indicadorTexto.innerText !== traducciones[idiomaActual].inspira) {
                        indicadorTexto.innerText = traducciones[idiomaActual].inspira;
                        indicadorTexto.style.color = "#00bcd4";
                        hablarTexto(traducciones[idiomaActual].inspira);
                    }
                } else {
                    if (indicadorTexto.innerText !== traducciones[idiomaActual].expira) {
                        indicadorTexto.innerText = traducciones[idiomaActual].expira;
                        indicadorTexto.style.color = "#d84315";
                        hablarTexto(traducciones[idiomaActual].expira);
                    }
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
            opcionesHtml += `<button class="btn-opcion" onclick="evaluarRespuestaTrivia(${index}, ${paso.c}, '${paso.ex[index][idiomaActual].replace(/'/g, "\\'")}')"> ${opcion[idiomaActual]} </button>`;
        });
        contenedorPasos.innerHTML = `
            <div class="bloque-decision">
                <p style="font-weight:700; font-size:14px; color:var(--primary); line-height:1.4;">${paso.q[idiomaActual]}</p>
                <div class="contenedor-opciones">${opcionesHtml}</div>
                <div id="box-feedback" class="feedback-box"></div>
            </div>`;
        hablarTexto(paso.q[idiomaActual]);
    }
    else if (paso.t === "r") {
        contenedorPasos.innerHTML = `
            <div style="margin:25px 0;">
                <span style="font-size:45px;">💎</span>
                <h2 style="color:var(--accent); margin:10px 0;">${paso.tx}</h2>
            </div>`;
        botonContinuar.style.display = 'block';
    }
    else if (paso.t === "c") {
        contenedorPasos.innerHTML = `<div style="padding:20px; background:#fffde7; border-radius:10px; margin:15px 0; border:1px dashed #fbc02d;"><p style="font-style:italic; font-size:15px; margin:0; font-weight:500;">"${paso.tx[idiomaActual]}"</p></div>`;
        hablarTexto(paso.tx[idiomaActual]);
        botonContinuar.style.display = 'block';
    }
    else if (paso.t === "sil") {
        contenedorPasos.innerHTML = `
            <div style="text-align:left; background:#f3e5f5; padding:16px; border-radius:10px; border:1px solid #e1bee7;">
                <p style="font-size:14px; margin:0 0 10px 0; line-height:1.4;"><strong>Misión:</strong> ${paso.tx[idiomaActual]}</p>
                <small style="color:#4a148c; display:block; font-weight:600;">💡 Enfoque: ${paso.inf[idiomaActual]}</small>
            </div>`;
        hablarTexto(paso.tx[idiomaActual] + ". Enfoque mental: " + paso.inf[idiomaActual]);
        botonContinuar.style.display = 'block';
    }
}

function evaluarRespuestaTrivia(indiceSeleccionado, indiceCorrecto, explicacionTexto) {
    const contenedorFeedback = document.getElementById('box-feedback');
    if (!contenedorFeedback) return;
    const botones = document.querySelectorAll('.btn-opcion');
    botones.forEach(btn => btn.disabled = true);

    const esCorrecto = indiceSeleccionado === indiceCorrecto;
    contenedorFeedback.className = esCorrecto ? "feedback-box fb-correcto" : "feedback-box fb-incorrecto";
    contenedorFeedback.innerHTML = (esCorrecto ? traducciones[idiomaActual].txt_correcto : traducciones[idiomaActual].txt_incorrecto) + explicacionTexto;

    const textoLimpioExplicacion = explicacionTexto.replace(/<[^>]*>/g, '');
    hablarTexto((esCorrecto ? "Excelente. " : "Analiza esto. ") + textoLimpioExplicacion);
    document.getElementById('btn-next').style.display = 'block';
}

function siguienteComando() {
    indicePasoActual++;
    procesarPasoMision();
}
