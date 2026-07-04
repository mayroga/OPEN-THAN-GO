// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.3.0.0
// Company: May Roga LLC
// File: static/engine.js

const KERNEL = {
    timer: null,
    timeLeft: 600,
    isLocked: false,
    idiomaActual: 'es',
    pasosMisiones: [],
    indiceMision: 0,
    datosLugarGlobal: null,
    tipoEscapeGlobal: "",

    init() {
        const btnMando = document.getElementById('btn-mando') || document.getElementById('btn-main-trigger');
        if (btnMando) {
            btnMando.onclick = () => this.ejecutar();
        }
    },

    hablar(texto) {
        if (!texto) return;
        // Corta de inmediato la voz anterior únicamente al cambiar de fase, nunca por segundo
        window.speechSynthesis.cancel(); 
        
        const textoLimpio = texto.replace(/<[^>]*>/g, '');
        const msg = new SpeechSynthesisUtterance(textoLimpio);
        msg.lang = this.idiomaActual === 'es' ? 'es-US' : 'en-US';
        msg.rate = 0.88; // Velocidad pausada somática para romper el modo zombi
        msg.pitch = 1.0;
        window.speechSynthesis.speak(msg);
    },

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;

        // Captura instantánea de variables biosociales del HTML
        const payload = {
            zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "33167",
            mente: document.getElementById('inp-mente') ? document.getElementById('inp-mente').value : "aburrido",
            modo: document.getElementById('modo-selector') ? document.getElementById('modo-selector').value : "SALIR",
            budget: document.getElementById('inp-budget') ? document.getElementById('inp-budget').value : "0",
            perfil: document.getElementById('inp-perfil') ? document.getElementById('inp-perfil').value : "solo",
            desahogo: document.getElementById('inp-text') ? document.getElementById('inp-text').value.trim() : ""
        };

        // Control visual inmediato en el teléfono del cliente (Costo cero de procesamiento)
        document.getElementById('wrapper-form').classList.add('hidden');
        const container = document.getElementById('wrapper-interactive');
        container.innerHTML = `<div style='text-align:center; padding:40px 0;'><h2 style='color:#fff;'>Sincronizando frecuencias de bienestar...</h2></div>`;
        container.classList.remove('hidden');

        try {
            const respuesta = await fetch("/api/mando-integral", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await respuesta.json();
            
            this.pasosMisiones = data.misiones || (data.mision ? data.mision.b : []);
            this.datosLugarGlobal = data.lugar || null;
            this.tipoEscapeGlobal = data.modo || data.tipo;
            this.indiceMision = 0;

            // Iniciar el procesador secuencial del KERNEL
            this.procesarFlujoSecuencial(container);
        } catch (error) {
            alert("Error de enlace satelital con el servidor.");
            document.getElementById('wrapper-form').classList.remove('hidden');
            container.classList.add('hidden');
            this.isLocked = false;
        }
    },

    procesarFlujoSecuencial(container) {
        clearInterval(this.timer);
        
        // REGLA DE CIERRE: Si terminamos todas las misiones del JSON o Catálogo
        if (this.indiceMision >= this.pasosMisiones.length) {
            if (this.tipoEscapeGlobal === "SALIR" && this.datosLugarGlobal) {
                // Despliega la Guía Absoluta en Campo con los 3 puntos mínimos sugeridos
                container.innerHTML = `
                    <div class="mision-card" style="border: 1px solid #333; padding: 20px; text-align: center; background: #0a0a0a; border-radius: 12px;">
                        <h2 style="color:#d84315; font-weight:900;">${this.datosLugarGlobal.name}</h2>
                        <p style="font-size:13px; color:#aaa; margin:5px 0;">${this.datosLugarGlobal.address}</p>
                        <hr style="border:0; border-top:1px dashed #333; margin:15px 0;">
                        <p style="text-align:left; font-size:14px; line-height:1.45; background:#111; padding:12px; border-radius:6px; border-left:4px solid #2e7d32; color:#fff;">
                            <strong>GUÍA ABSOLUTA DE ACCIÓN:</strong><br>${this.datosLugarGlobal.analisis_sugerido}
                        </p>
                        <button id="btn-countdown-salida" style="width:100%; background:#222; color:#aaa; padding:16px; font-weight:bold; margin-top:15px;" disabled>35s ANCLAJE SOMÁTICO</button>
                        <button id="btn-gps-action" class="hidden" style="width:100%; background:#4285f4; color:#fff; padding:16px; font-weight:bold; margin-top:15px;">ABRIR ENLACE DE MAPA</button>
                    </div>
                `;

                this.hablar(this.datosLugarGlobal.name + " . Escucha las indicaciones de campo: " + this.datosLugarGlobal.analisis_sugerido);

                let retencion = 35;
                const btnCount = document.getElementById('btn-countdown-salida');
                const btnGps = document.getElementById('btn-gps-action');

                let relojSalida = setInterval(() => {
                    retencion--;
                    if (btnCount) btnCount.innerText = `${retencion}s PREPARACIÓN DE ENTORNO`;
                    
                    if (retencion <= 0) {
                        clearInterval(relojSalida);
                        if (btnCount) btnCount.style.display = 'none';
                        if (btnGps) {
                            btnGps.classList.remove('hidden');
                            // Clic voluntario del cliente que salta el antivirus de ventanas emergentes de Apple y Android
                            btnGps.onclick = () => { window.open(this.datosLugarGlobal.gps, '_blank'); };
                        }
                    }
                }, 1000);
            } else {
                // Modo CASA: Al terminar las fases secuenciales, arranca el pulmón de 10:00 minutos fijos
                this.iniciarRelojClinicoCasa(container);
            }
            return;
        }

        const paso = this.pasosMisiones[this.indiceMision];

        // 1. Títulos decorativos del JSON ("v" o "h")
        if (paso.t === "v" || paso.t === "h") {
            let textoLabel = typeof paso.tx === 'object' ? paso.tx[this.idiomaActual] : paso.tx;
            container.innerHTML = `
                <div class="mision-card" style="background:#0a0a0a; border:1px solid #333; padding:25px; border-radius:12px;">
                    <h3 style="color:#2e7d32; font-size:1.3rem; font-weight:800; text-transform:uppercase;">${textoLabel}</h3>
                    <button id="btn-next" style="width:100%; background:#222; color:#fff; padding:14px; font-weight:bold; margin-top:20px;">CONTINUAR</button>
                </div>`;
            this.hablar(textoLabel);
            document.getElementById('btn-next').onclick = () => this.avanzarPaso();
        }
        
        // 2. Narrativa clínica camuflada ("story")
        else if (paso.story) {
            let textoStory = paso.story[this.idiomaActual];
            container.innerHTML = `
                <div class="mision-card" style="background:#0a0a0a; border:1px solid #333; padding:25px; border-radius:12px; text-align:left;">
                    <p style="font-size:1.05rem; line-height:1.6; color:#ccc; border-left:4px solid #2e7d32; padding-left:15px;">${textoStory}</p>
                    <button id="btn-next" style="width:100%; background:#2e7d32; color:#fff; padding:14px; font-weight:bold; margin-top:20px; text-transform:uppercase;">CONTINUAR</button>
                </div>`;
            this.hablar(textoStory);
            document.getElementById('btn-next').onclick = () => this.avanzarPaso();
        }
        
        // 3. Regulación pulmonar rítmica ("breath_auto")
        else if (paso.t === "breath_auto" || paso.descripcion) {
            // Adaptar tanto si lee de tu JSON original como del nuevo formato simplificado
            let tiempoPulmon = paso.d || 25;
            let textoInstruccion = paso.tx ? paso.tx[this.idiomaActual] : paso.titulo;
            let textoDetalle = paso.inf ? paso.inf[this.idiomaActual] : paso.descripcion;

            container.innerHTML = `
                <div class="mision-card" style="background:#0a0a0a; border:1px solid #333; padding:25px; border-radius:12px;">
                    <div id="breath-circle"></div>
                    <div id="circulo-pulso" style="font-size:2rem; font-weight:800; margin-top:10px;">${tiempoPulmon}s</div>
                    <div id="txt-pulmon-accion" style="font-size:1.3rem; font-weight:bold; color:#00bcd4; margin-top:10px; text-transform:uppercase;">INHALA / INSPIRA</div>
                    <p style="font-weight:600; margin-top:15px; color:#fff;">${textoInstruccion}</p>
                    <p style="font-size:12px; color:#777; line-height:1.4;">${textoDetalle}</p>
                    <button id="btn-next" class="hidden" style="width:100%; background:#2e7d32; color:#fff; padding:14px; font-weight:bold; margin-top:15px;">AVANZAR</button>
                </div>`;
            
            this.hablar(textoInstruccion + " . " + textoDetalle);

            let relojPulmon = setInterval(() => {
                tiempoPulmon--;
                const divContador = document.getElementById('circulo-pulso');
                const divAccion = document.getElementById('txt-pulmon-accion');
                
                if (divContador) divContador.innerText = `${tiempoPulmon}s`;
                
                if (divAccion) {
                    let ciclo = tiempoPulmon % 8;
                    if (ciclo >= 4) {
                        divAccion.innerText = "INHALA / INSPIRA";
                        divAccion.style.color = "#00bcd4";
} else {
    divAccion.innerText = "EXHALA / EXPIRA";
    divAccion.style.color = "#d84315";
}
}

if (tiempoPulmon <= 0) {
    clearInterval(relojPulmon);
    const btnNext = document.getElementById('btn-next');
    if (btnNext) btnNext.classList.remove('hidden');
}
}, 1000);

document.getElementById('btn-next').onclick = () => this.avanzarPaso();
}

// 4. Cuestionario conductual interactivo ("d") con margen de reintento ilimitado
else if (paso.t === "d") {
    let opcionesHtml = "";

    paso.op.forEach((opcion, index) => {
        opcionesHtml += `<button class="btn-opcion" id="opt-${index}" style="width:100%; text-align:left; padding:12px; margin-top:8px; background:#111; color:#fff; border:1px solid #333; cursor:pointer;" onclick="KERNEL.evaluarRespuestaTrivia(${index}, ${paso.c}, '${paso.ex[index][this.idiomaActual].replace(/'/g, "\\'")}')">${opcion[this.idiomaActual]}</button>`;
    });

    container.innerHTML = `
        <div class="mision-card" style="background:#0a0a0a; border:1px solid #333; padding:20px; border-radius:12px; text-align:left;">
            <p style="font-weight:700; font-size:14.5px; color:#fff; line-height:1.4;">${paso.q[this.idiomaActual]}</p>
            <div style="margin-top:10px;">${opcionesHtml}</div>
            <div id="box-feedback" class="feedback-box" style="margin-top:12px; padding:12px; border-radius:8px; display:none; font-size:13px; line-height:1.4;"></div>
            <button id="btn-next" class="hidden" style="width:100%; background:#2e7d32; color:#fff; padding:14px; font-weight:bold; margin-top:15px; text-transform:uppercase;">CONTINUAR</button>
        </div>`;

    this.hablar(paso.q[this.idiomaActual]);
    document.getElementById('btn-next').onclick = () => this.avanzarPaso();
}

// 5. Puntos de enfoque ("r")
else if (paso.t === "r") {
    container.innerHTML = `
        <div class="mision-card" style="background:#0a0a0a; border:1px solid #333; padding:30px; border-radius:12px;">
            <span style="font-size:50px;">💎</span>
            <h2 style="color:#d84315; font-weight:900; margin:15px 0;">${paso.tx}</h2>
            <button id="btn-next" style="width:100%; background:#222; color:#fff; padding:14px; font-weight:bold;">ACEPTAR ENFOQUE</button>
        </div>`;

    this.hablar(paso.tx);
    document.getElementById('btn-next').onclick = () => this.avanzarPaso();
}

// 6. Compromiso mental ("c")
else if (paso.t === "c") {
    let textoCompromiso = typeof paso.tx === 'object'
        ? paso.tx[this.idiomaActual]
        : paso.tx;

    container.innerHTML = `
        <div class="mision-card" style="background:#0a0a0a; border:1px solid #333; padding:25px; border-radius:12px;">
            <div style="padding:20px; background:#111; border-radius:8px; border:1px dashed #fbc02d; margin-bottom:15px;">
                <p style="font-style:italic; font-size:15px; margin:0; color:#fff; line-height:1.4;">"${textoCompromiso}"</p>
            </div>
            <button id="btn-next" style="width:100%; background:#2e7d32; color:#fff; padding:14px; font-weight:bold;">ME COMPROMETO</button>
        </div>`;

    this.hablar(textoCompromiso);
    document.getElementById('btn-next').onclick = () => this.avanzarPaso();
}

// 7. Misión práctica final en silencio ("sil")
else if (paso.t === "sil") {
    container.innerHTML = `
        <div class="mision-card" style="background:#0a0a0a; border:1px solid #333; padding:20px; border-radius:12px; text-align:left;">
            <p style="font-size:14px; line-height:1.4; color:#fff;">
                <strong>MISIÓN DE ENTORNO:</strong><br>${paso.tx[this.idiomaActual]}
            </p>
            <small style="color:#00bcd4; font-weight:600; margin-top:5px; display:block;">
                💡 FOCO: ${paso.inf[this.idiomaActual]}
            </small>
            <button id="btn-next" style="width:100%; background:#2e7d32; color:#fff; padding:14px; font-weight:bold; margin-top:15px; text-transform:uppercase;">
                EJECUTAR
            </button>
        </div>`;

    this.hablar(
        paso.tx[this.idiomaActual] +
        " . Enfoque mental: " +
        paso.inf[this.idiomaActual]
    );

    document.getElementById('btn-next').onclick = () => this.avanzarPaso();
}
},

evaluarRespuestaTrivia(seleccionado, correcto, explicacion) {
    const box = document.getElementById('box-feedback');
    if (!box) return;

    const esCorrecto = seleccionado === correcto;

    box.style.display = "block";
    box.className = esCorrecto
        ? "feedback-box fb-correcto"
        : "feedback-box fb-incorrecto";

    const prefijo = esCorrecto
        ? "¡RESPUESTA VERDADERA!"
        : "ANÁLISIS DE FALLO:";

    box.innerHTML = prefijo + explicacion;

    if (esCorrecto) {
        // Deshabilita reintentos al acertar y revela el pase de sección voluntario
        document.querySelectorAll('.btn-opcion').forEach(btn => btn.disabled = true);

        this.hablar(
            (this.idiomaActual === 'es' ? "Verdadero. " : "True. ") +
            explicacion
        );

        document.getElementById('btn-next').classList.remove('hidden');
    } else {
        // Deja margen de reintento atenuando el botón erróneo
        const btnFallo = document.getElementById(`opt-${seleccionado}`);

        if (btnFallo) {
            btnFallo.style.opacity = "0.35";
            btnFallo.style.pointerEvents = "none";
        }

        this.hablar(
            (this.idiomaActual === 'es' ? "Falso. " : "False. ") +
            explicacion
        );
    }
},

iniciarRelojClinicoCasa(container) {
    this.hablar(
        "Fase educativa completada. Iniciando reloj clínico de diez minutos. Sincroniza tu respiración."
    );

    container.innerHTML = `
        <div id="breath-circle"></div>
        <div id="timer" style="font-weight:900; text-align:center; font-size:2.8rem; margin:15px 0;">10:00</div>
        <p id="txt-pulmon" style="font-size:14px; text-transform:uppercase; font-weight:bold; color:#00bcd4; text-align:center; letter-spacing:2px;">
            INHALA / INSPIRA
        </p>`;

    this.timeLeft = 600;

    this.timer = setInterval(() => {
        this.timeLeft--;

        let m = Math.floor(this.timeLeft / 60);
        let s = this.timeLeft % 60;

        const timerDiv = document.getElementById('timer');
        const pulmonDiv = document.getElementById('txt-pulmon');

        if (timerDiv) {
            timerDiv.innerText = `${m}:${s.toString().padStart(2, '0')}`;
        }

        if (pulmonDiv) {
            let ciclo = this.timeLeft % 8;

            if (ciclo >= 4) {
                pulmonDiv.innerText = "INHALA / INSPIRA";
                pulmonDiv.style.color = "#00bcd4";
            } else {
                pulmonDiv.innerText = "EXHALA / EXPIRA";
                pulmonDiv.style.color = "#d84315";
            }
        }

        if (this.timeLeft <= 0) {
            clearInterval(this.timer);
            this.hablar("Protocolo terminado. Ejecutando borrado de rastro automático.");
            alert("Protocolo completado. Borrando rastro de sesión.");
            this.destruirYReiniciar();
        }
    }, 1000);
},

avanzarPaso() {
    this.indiceMision++;
    const container = document.getElementById('wrapper-interactive');
    this.procesarFlujoSecuencial(container);
},

destruirYReiniciar() {
    clearInterval(this.timer);
    window.speechSynthesis.cancel();
    this.pasosMisiones = [];
    this.indiceMision = 0;
    this.isLocked = false;
    location.reload(); // Autodestrucción absoluta de caché e hilos en el hardware del cliente
}
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());
