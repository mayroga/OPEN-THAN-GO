// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.3.0.0
// Company: May Roga LLC
// File: static/engine.js
// PARTE 1 DE 4

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
        window.speechSynthesis.cancel(); 
        
        const textoLimpio = texto.replace(/<[^>]*>/g, '');
        const msg = new SpeechSynthesisUtterance(textoLimpio);
        msg.lang = this.idiomaActual === 'es' ? 'es-US' : 'en-US';
        msg.rate = 0.88; 
        msg.pitch = 1.0;
        window.speechSynthesis.speak(msg);
    },
    
// PARTE 2 DE 4: Captura de Datos y Enlace con el Servidor (Sincronizado)

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;

        // Captura exacta de los mandos del formulario sin dejar cabos sueltos
        const payload = {
            zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
            mente: document.getElementById('inp-mente') ? document.getElementById('inp-mente').value : "aburrido",
            modo: document.getElementById('modo-selector') ? document.getElementById('modo-selector').value : "SALIR",
            budget: document.getElementById('inp-budget') ? document.getElementById('inp-budget').value : "0",
            perfil: document.getElementById('inp-perfil') ? document.getElementById('inp-perfil').value : "solo",
            desahogo: document.getElementById('inp-text') ? document.getElementById('inp-text').value.trim() : ""
        };

        const container = document.getElementById('wrapper-interactive');
        document.getElementById('wrapper-form').classList.add('hidden');
        container.innerHTML = `<div style='text-align:center; padding:40px 0;'><h2 style='color:#fff;'>Sincronizando frecuencias de bienestar...</h2></div>`;
        container.classList.remove('hidden');

        try {
            const respuesta = await fetch("/api/mando-integral", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await respuesta.json();
            
            // Asignación elástica del bloque 'b' o misiones puras de tu catálogo
            this.pasosMisiones = data.misiones || (data.mision ? data.mision.b : []);
            this.datosLugarGlobal = data.lugar || null;
            this.tipoEscapeGlobal = data.modo || data.tipo;
            this.indiceMision = 0;

            // Arranca el procesador por pasos del teléfono del cliente
            this.procesarFlujoSecuencial(container);
        } catch (error) {
            alert("Error de enlace satelital con el servidor.");
            document.getElementById('wrapper-form').classList.remove('hidden');
            container.classList.add('hidden');
            this.isLocked = false;
        }
    },

    procesarRespuesta(res) {
        this.isLocked = false;
    },

// PARTE 3 DE 4: Procesador de Misiones, Historias y Pulmón Torácico

    procesarFlujoSecuencial(container) {
        clearInterval(this.timer);
        const traducciones = {
            es: { inspira: "Inhala / Inspira", expira: "Exhala / Expira", txt_correcto: "<strong>¡RESPUESTA VERDADERA!</strong><br>", txt_incorrecto: "<strong>ANÁLISIS DE FALLO:</strong><br>", alerta_35s: "Preparación de campo activa por 35 segundos. Escucha atentamente.", fin_casa: "Protocolo completado. Borrando rastro." },
            en: { inspira: "Inhale", expira: "Exhale", txt_correcto: "<strong>TRUE ANSWER!</strong><br>", txt_incorrecto: "<strong>FAILURE ANALYSIS:</strong><br>", alerta_35s: "Field preparation active for 35 seconds. Listen carefully.", fin_casa: "Protocol completed. Clearing tracks." }
        };
        const traduccion = traducciones[this.idiomaActual];

        if (this.indiceMision >= this.pasosMisiones.length) {
            if (this.tipoEscapeGlobal === "SALIR" && this.datosLugarGlobal) {
                container.innerHTML = `
                    <div class="mision-card">
                        <h2 style="color:#d84315; font-weight:900;">${this.datosLugarGlobal.name}</h2>
                        <p style="font-size:13px; color:#aaa; margin:5px 0;">${this.datosLugarGlobal.address}</p>
                        <hr style="border:0; border-top:1px dashed #333; margin:15px 0;">
                        <p style="text-align:left; font-size:14px; line-height:1.45; background:#111; padding:12px; border-radius:6px; border-left:4px solid #2e7d32; color:#fff;">
                            <strong>GUÍA ABSOLUTA DE ACCIÓN:</strong><br>${this.datosLugarGlobal.analisis_sugerido}
                        </p>
                        <button id="btn-countdown-salida" style="width:100%; background:#222; color:#aaa; padding:16px; font-weight:bold; margin-top:15px;" disabled>35s ANCLAJE SOMÁTICO</button>
                        <button id="btn-gps-action" class="hidden" style="width:100%; background:#4285f4; color:#fff; padding:16px; font-weight:bold; margin-top:15px;">ABRIR ENLACE DE MAPA</button>
                    </div>`;

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
                            btnGps.onclick = () => { window.open(this.datosLugarGlobal.gps, '_blank'); };
                        }
                    }
                }, 1000);
            } else {
                this.iniciarRelojClinicoCasa(container, traduccion);
            }
            return;
        }

        const paso = this.pasosMisiones[this.indiceMision];

        if (paso.t === "v" || paso.t === "h") {
            let textoLabel = typeof paso.tx === 'object' ? paso.tx[this.idiomaActual] : paso.tx;
            container.innerHTML = `
                <div class="mision-card">
                    <h3 style="color:#2e7d32; font-size:1.3rem; font-weight:800; text-transform:uppercase;">${textoLabel}</h3>
                    <button id="btn-next" style="width:100%; background:#222; color:#fff; padding:14px; font-weight:bold; margin-top:20px;">CONTINUAR</button>
                </div>`;
            this.hablar(textoLabel);
            document.getElementById('btn-next').onclick = () => this.avanzarPaso();
        }
        else if (paso.story) {
            let textoStory = paso.story[this.idiomaActual];
            container.innerHTML = `
                <div class="mision-card" style="text-align:left;">
                    <p style="font-size:1.05rem; line-height:1.6; color:#ccc; border-left:4px solid #2e7d32; padding-left:15px;">${textoStory}</p>
                    <button id="btn-next" style="width:100%; background:#2e7d32; color:#fff; padding:14px; font-weight:bold; margin-top:20px; text-transform:uppercase;">CONTINUAR</button>
                </div>`;
            this.hablar(textoStory);
            document.getElementById('btn-next').onclick = () => this.avanzarPaso();
        }
        else if (paso.t === "breath_auto" || paso.descripcion) {
            let tiempoPulmon = paso.d || 25;
            let textoInstruccion = paso.tx ? paso.tx[this.idiomaActual] : paso.titulo;
            let textoDetalle = paso.inf ? paso.inf[this.idiomaActual] : paso.descripcion;

            container.innerHTML = `
                <div class="mision-card">
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
                        divAccion.innerText = traduccion.inspira;
                        divAccion.style.color = "#00bcd4";
                    } else {
                        divAccion.innerText = traduccion.expira;
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
            
// PARTE 4 DE 4: Cuestionario Conductual, Puntos, Compromisos y Autodestrucción de Rastro

        else if (paso.t === "d") {
            let opcionesHtml = "";
            paso.op.forEach((opcion, index) => {
                opcionesHtml += `<button class="btn-opcion" id="opt-${index}" style="width:100%; text-align:left; padding:12px; margin-top:8px; background:#111; color:#fff; border:1px solid #333; cursor:pointer;" onclick="KERNEL.evaluarRespuestaTrivia(${index}, ${paso.c}, '${paso.ex[index][this.idiomaActual].replace(/'/g, "\\'")}', '${traduccion.txt_correcto}', '${traduccion.txt_incorrecto}')">${opcion[this.idiomaActual]}</button>`;
            });

            container.innerHTML = `
                <div class="mision-card" style="text-align:left;">
                    <p style="font-weight:700; font-size:14.5px; color:#fff; line-height:1.4;">${paso.q[this.idiomaActual]}</p>
                    <div style="margin-top:10px;">${opcionesHtml}</div>
                    <div id="box-feedback" class="feedback-box" style="margin-top:12px; padding:12px; border-radius:8px; display:none; font-size:13px; line-height:1.4;"></div>
                    <button id="btn-next" class="hidden" style="width:100%; background:#2e7d32; color:#fff; padding:14px; font-weight:bold; margin-top:15px; text-transform:uppercase;">CONTINUAR</button>
                </div>`;
            this.hablar(paso.q[this.idiomaActual]);
            document.getElementById('btn-next').onclick = () => this.avanzarPaso();
        }
        else if (paso.t === "r") {
            container.innerHTML = `
                <div class="mision-card">
                    <span style="font-size:50px;">💎</span>
                    <h2 style="color:#d84315; font-weight:900; margin:15px 0;">${paso.tx}</h2>
                    <button id="btn-next" style="width:100%; background:#222; color:#fff; padding:14px; font-weight:bold;">ACEPTAR ENFOQUE</button>
                </div>`;
            this.hablar(paso.tx);
            document.getElementById('btn-next').onclick = () => this.avanzarPaso();
        }
        else if (paso.t === "c") {
            let textoCompromiso = typeof paso.tx === 'object' ? paso.tx[this.idiomaActual] : paso.tx;
            container.innerHTML = `
                <div class="mision-card">
                    <div style="padding:20px; background:#111; border-radius:8px; border:1px dashed #fbc02d; margin-bottom:15px;">
                        <p style="font-style:italic; font-size:15px; margin:0; color:#fff; line-height:1.4;">"${textoCompromiso}"</p>
                    </div>
                    <button id="btn-next" style="width:100%; background:#2e7d32; color:#fff; padding:14px; font-weight:bold;">ME COMPROMETO</button>
                </div>`;
            this.hablar(textoCompromiso);
            document.getElementById('btn-next').onclick = () => this.avanzarPaso();
        }
        else if (paso.t === "sil") {
            container.innerHTML = `
                <div class="mision-card" style="text-align:left;">
                    <p style="font-size:14px; line-height:1.4; color:#fff;"><strong>MISIÓN DE ENTORNO:</strong><br>${paso.tx[this.idiomaActual]}</p>
                    <small style="color:#00bcd4; font-weight:600; margin-top:5px; display:block;">💡 FOCO: ${paso.inf[this.idiomaActual]}</small>
                    <button id="btn-next" style="width:100%; background:#2e7d32; color:#fff; padding:14px; font-weight:bold; margin-top:15px; text-transform:uppercase;">EJECUTAR</button>
                </div>`;
            this.hablar(paso.tx[this.idiomaActual] + " . Enfoque mental: " + paso.inf[this.idiomaActual]);
            document.getElementById('btn-next').onclick = () => this.avanzarPaso();
        }
    },

    evaluarRespuestaTrivia(seleccionado, correcto, explicacion, txtCorrecto, txtIncorrecto) {
        const box = document.getElementById('box-feedback');
        if (!box) return;
        const esCorrecto = seleccionado === correcto;
        box.style.display = "block";
        box.className = esCorrecto ? "feedback-box fb-correcto" : "feedback-box fb-incorrecto";
        box.innerHTML = (esCorrecto ? txtCorrecto : txtIncorrecto) + explicacion;

        if (esCorrecto) {
            document.querySelectorAll('.btn-opcion').forEach(btn => btn.disabled = true);
            // CORRECCIÓN: Hablar la explicación real de tu JSON sin mezclar variables
            this.hablar((this.idiomaActual === 'es' ? "Excelente. " : "True. ") + explicacion);
            document.getElementById('btn-next').classList.remove('hidden');
        } else {
            const btnFallo = document.getElementById(`opt-${seleccionado}`);
            if (btnFallo) { btnFallo.style.opacity = "0.35"; btnFallo.style.pointerEvents = "none"; }
            this.hablar((this.idiomaActual === 'es' ? "Analiza esto. " : "False. ") + explicacion);
        }
    },

    iniciarRelojClinicoCasa(container, traduccion) {
        this.hablar("Fase misiones completada. Iniciando reloj clínico de diez minutos. Sincroniza tu respiración.");
        container.innerHTML = `
            <div id="breath-circle"></div>
            <div id="timer" style="font-weight:900; text-align:center; font-size:2.8rem; margin:15px 0;">10:00</div>
            <p id="txt-pulmon" style="font-size:14px; text-transform:uppercase; font-weight:bold; color:#00bcd4; text-align:center; letter-spacing:2px;">INHALA / INSPIRA</p>
        `;
        this.timeLeft = 600;
        this.timer = setInterval(() => {
            this.timeLeft--;
            let m = Math.floor(this.timeLeft / 60);
            let s = this.timeLeft % 60;
            const timerDiv = document.getElementById('timer');
            const pulmonDiv = document.getElementById('txt-pulmon');
            if (timerDiv) timerDiv.innerText = `${m}:${s.toString().padStart(2, '0')}`;
            if (pulmonDiv) {
                let ciclo = this.timeLeft % 8;
                if (ciclo >= 4) { pulmonDiv.innerText = traduccion.inspira; pulmonDiv.style.color = "#00bcd4"; }
                else { pulmonDiv.innerText = traduccion.expira; pulmonDiv.style.color = "#d84315"; }
            }
            if (this.timeLeft <= 0) {
                clearInterval(this.timer);
                this.hablar(traduccion.fin_casa);
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
        location.reload();
    }
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());
