// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.5.5.0
// Company: May Roga LLC
// File: static/engine.js - SECCIÓN 1 DE 2

const KERNEL = {
    timer: null,
    timeLeft: 600,
    isLocked: false,
    idiomaActual: 'es',
    pasosMisiones: [],
    indiceMision: 0,
    datosLugarGlobal: null,
    tipoEscapeGlobal: "",

    // MOTOR DE PREFERENCIAS IMPLÍCITAS LOCAL: Inicializa los contadores de las 19 necesidades en la RAM del teléfono
    obtenerPerfilLocal() {
        let perfil = localStorage.getItem("otg_perfil_dinamico");
        if (!perfil) {
            perfil = {
                "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50, 
                "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50, 
                "juego": 50, "contemplacion": 50, "trabajo": 50, "descanso": 50, "organizacion": 50, 
                "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50
            };
            localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
        }
        return JSON.stringify(perfil) === "{}" ? JSON.parse(localStorage.getItem("otg_perfil_dinamico")) : JSON.parse(perfil);
    },

    init() {
        const btnMando = document.getElementById('btn-mando');
        if (btnMando) btnMando.onclick = () => this.ejecutar();
    },

    despertarInicial() {
        document.getElementById('pantalla-bienvenida').style.display = 'none';
        document.getElementById('wrapper-form').classList.remove('hidden');

        // Oraciones sencillas de acción directa claras para todos
        const saludos = [
            "Bienvenido a ópen dán go. Tu escape inteligente. Pon tus datos en el mando ya.",
            "ópen dán go está activo. Olvida tus biles un momento. Usa el mando ahora.",
            "Entraste a ópen dán go. El despertador está encendido. Vamos a sacarte de la rutina gris."
        ];
        this.hablar(saludos[Math.floor(Math.random() * saludos.length)]);
    },

    hablar(texto) {
        if (!texto) return;
        window.speechSynthesis.cancel();
        let fx = texto.replace(/OPEN THAN GO/gi, "OPEN DAN GO").replace(/<[^>]*>/g, '');
        const msg = new SpeechSynthesisUtterance(fx);
        
        // RECTIFICACIÓN MÁXIMA DE IDIOMA: La voz siempre se mantiene en español nativo por estabilidad
        msg.lang = 'es-US';
        msg.rate = 1.20; // Velocidad de acción rápida y despierta
        window.speechSynthesis.speak(msg);
    },

    cambiarIdioma(lang) {
        this.idiomaActual = lang;
        document.getElementById('lang-es').classList.toggle('active', lang === 'es');
        document.getElementById('lang-en').classList.toggle('active', lang === 'en');

        // TRADUCCIÓN REAL E INMEDIATA DE TODO EL CONTENEDOR VISUAL (La voz no cambia, se mantiene en español)
        const t = {
            es: { title: "OPEN THAN GO", zip: "Código Postal", mode: "Modo de Operación", mente: "Estado Mental", budget: "Presupuesto", perfil: "Perfil", desahogo: "Desahogo", placeholder: "Escribe libremente cómo te sientes hoy...", btn: "ACTIVAR MANDO", alert: "Idioma cambiado a español." },
            en: { title: "OPEN THAN GO", zip: "ZIP Code", mode: "Operation Mode", mente: "Mental State", budget: "Budget Available", perfil: "Profile", desahogo: "Venting Layer", placeholder: "Write freely how you feel today...", btn: "ACTIVATE CONTROL", alert: "Idioma de pantalla cambiado a inglés." }
        }[lang];

        document.getElementById('txt-app-title').innerText = t.title;
        document.getElementById('lbl-zip').innerText = t.zip;
        document.getElementById('lbl-mode').innerText = t.mode;
        document.getElementById('lbl-mente').innerText = t.mente;
        document.getElementById('lbl-budget').innerText = t.budget;
        document.getElementById('lbl-perfil').innerText = t.perfil;
        document.getElementById('lbl-desahogo').innerText = t.desahogo;
        document.getElementById('inp-text').placeholder = t.placeholder;
        document.getElementById('btn-mando').innerText = t.btn;
        
        this.hablar(t.alert);
    },

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;

        // Extrae las métricas dinámicas acumuladas de clics en local antes de despachar al servidor
        const perfilDinamicLocal = this.obtenerPerfilLocal();

        const payload = {
            zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
            mente: document.getElementById('inp-mente') ? document.getElementById('inp-mente').value : "agotado",
            modo: document.getElementById('modo-selector') ? document.getElementById('modo-selector').value : "SALIR",
            budget: document.getElementById('inp-budget') ? document.getElementById('inp-budget').value : "0",
            perfil: document.getElementById('inp-perfil') ? document.getElementById('inp-perfil').value : "solo",
            desahogo: document.getElementById('inp-text') ? document.getElementById('inp-text').value.trim() : "",
            lang: this.idiomaActual,
            perfil_local: perfilDinamicLocal // Inyectamos la lectura implícita de la mente
        };

        const container = document.getElementById('wrapper-interactive');
        document.getElementById('wrapper-form').classList.add('hidden');
        container.innerHTML = `<div style='text-align:center; padding:40px 0;'><h2 style='color:#fff; font-size:1.1rem; letter-spacing:1px;'>CONECTANDO...</h2></div>`;
        container.classList.remove('hidden');

        try {
            const r = await fetch("/api/mando-integral", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await r.json();

            this.datosLugarGlobal = data;
            this.tipoEscapeGlobal = data.DIRECCIONAMIENTO_MASTER;
            this.indiceMision = 0;

            if (this.tipoEscapeGlobal === "INTERVENCION_DOMESTICA") {
                this.pasosMisiones = data.misiones.slice(0, 3);
            } else {
                this.pasosMisiones = [];
            }
            this.procesarFlujoSecuencial(container);
        } catch (error) {
            alert("Error.");
            document.getElementById('wrapper-form').classList.remove('hidden');
            container.classList.add('hidden');
            this.isLocked = false;
        }
    },
// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.5.5.0
// Company: May Roga LLC
// File: static/engine.js - SECCIÓN 2 DE 2

    procesarFlujoSecuencial(container) {
        clearInterval(this.timer);
        const t = {
            es: { inspira: "Inhala ahora", expira: "Exhala ahora", fin: "Protocolo completado. Borrando rastro.", listen: "ESCUCHA MI GUÍA", launch: "ABRIR CANAL BIG TECH YA" },
            en: { inspira: "Inhale now", expira: "Exhale now", fin: "Protocol completed. Clearing tracks.", listen: "LISTEN TO THE GUIDE", launch: "OPEN BIG TECH CHANNEL NOW" }
        }[this.idiomaActual];

        // MODO SALIR (ACCION_CAMPO) - SECUESTRO DIRECTO DE PLATAFORMAS TRILLONARIAS
        if (this.tipoEscapeGlobal === "ACCION_CAMPO") {
            if (this.datosLugarGlobal) {
                let textoFormateado = this.datosLugarGlobal.destino_instruccion.replace(/\n/g, '<br>');
                container.innerHTML = `
                <div class="mision-card">
                    <small>${this.idiomaActual === 'es' ? 'Acción de Campo' : 'Field Action'}</small>
                    <h2>${this.datosLugarGlobal.destino_titulo}</h2>
                    <div class="instruccion-text">${textoFormateado}</div>
                    <button id="btn-countdown-salida" style="width:100%; background:#222; color:#aaa; padding:17px; font-weight:bold; margin-top:15px; border:none; text-transform:uppercase; border-radius:4px; font-size:0.9rem;" disabled>35s ${t.listen}</button>
                    <button id="btn-gps-action" class="hidden" style="width:100%; background:#0d47a1; color:#fff; padding:17px; font-weight:bold; margin-top:15px; border:none; text-transform:uppercase; border-radius:4px; cursor:pointer; font-size:0.95rem; letter-spacing:0.5px;">${t.launch}</button>
                </div>`;

                this.hablar(this.datosLugarGlobal.destino_instruccion);
                
                let retencion = 35;
                const btnCount = document.getElementById('btn-countdown-salida');
                const btnGps = document.getElementById('btn-gps-action');
                
                this.timer = setInterval(() => {
                    retencion--;
                    if (btnCount) btnCount.innerText = `${retencion}s ${t.listen}`;
                    if (retencion <= 0) {
                        clearInterval(this.timer);
                        if (btnCount) btnCount.style.display = 'none';
                        if (btnGps) {
                            btnGps.classList.remove('hidden');
                            btnGps.onclick = () => {
                                // APRENDIZAJE IMPLÍCITO: Registra la elección antes de saltar a la plataforma externa
                                try {
                                    let perfil = JSON.parse(localStorage.getItem("otg_perfil_dinamico"));
                                    let token = KERNEL.datosLugarGlobal.token_entorno || "general";
                                    
                                    if (perfil) {
                                        // Si elige un entorno natural, suma peso al indicador correspondiente para la siguiente consulta
                                        if (token.toLowerCase().includes("árbol") || token.toLowerCase().includes("sombra")) {
                                            perfil["naturaleza"] = Math.min(perfil["naturaleza"] + 10, 100);
                                            perfil["silencio"] = Math.min(perfil["silencio"] + 5, 100);
                                        } else if (token.toLowerCase().includes("caminata") || token.toLowerCase().includes("subida")) {
                                            perfil["movimiento"] = Math.min(perfil["movimiento"] + 10, 100);
                                            perfil["aire_fresco"] = Math.min(perfil["aire_fresco"] + 5, 100);
                                        } else if (token.toLowerCase().includes("paseo") || token.toLowerCase().includes("colores")) {
                                            perfil["creatividad"] = Math.min(perfil["creatividad"] + 10, 100);
                                            perfil["esperanza"] = Math.min(perfil["esperanza"] + 5, 100);
                                        }
                                        // Guarda el avance sin bases de datos pesadas de forma segura y anónima
                                        localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
                                    }
                                } catch (e) {
                                    console.log("[Kernel] Error en registro de preferencia implícita.");
                                }

                                // Secuestra el comportamiento: Abre la app nativa (YouTube, Spotify, Maps) de golpe en el celular
                                window.open(this.datosLugarGlobal.destino_coordenadas_gps, '_blank');
                                this.destruirYReiniciar(); // Purga todo rastro del teléfono al saltar al escape
                            };
                        }
                    }
                }, 1000);
                return;
            }
        }

        // MODO CASA - ACCIONES SECUENCIALES CORTAS
        if (this.indiceMision >= this.pasosMisiones.length) {
            this.iniciarRelojClinicoCasa(container, t);
            return;
        }

        const paso = this.pasosMisiones[this.indiceMision];
        container.innerHTML = `
        <div class="mision-card">
            <small>${this.idiomaActual === 'es' ? 'Misión Interna' : 'Internal Mission'}</small>
            <h3>${paso.titulo}</h3>
            <p>${paso.descripcion}</p>
            <button id="btn-next" style="width:100%; background:#2e7d32; color:#fff; padding:16px; font-weight:bold; text-transform:uppercase; border-radius:6px; cursor:pointer; border:none; margin-top:15px; font-size:0.95rem;">${this.idiomaActual === 'es' ? 'HAZLO AHORA' : 'DO IT NOW'}</button>
        </div>`;

        this.hablar(paso.titulo + " . " + paso.descripcion);
        document.getElementById('btn-next').onclick = () => this.avanzarPaso();
    },

    iniciarRelojClinicoCasa(container, t) {
        let msg = this.idiomaActual === 'es' ? "Iniciamos diez minutos de limpieza mental profunda. Respira." : "Starting ten minutes of deep mental clearing. Breathe.";
        this.hablar(msg);
        
        container.innerHTML = `
        <div style="text-align:center; width:100%;">
            <div id="breath-circle"></div>
            <div id="timer">10:00</div>
            <p id="txt-pulmon">INHALA / INHALE</p>
        </div>`;

        this.timeLeft = 600;
        this.timer = setInterval(() => {
            this.timeLeft--;
            let m = Math.floor(this.timeLeft / 60);
            let s = this.timeLeft % 60;
            
            const timerDiv = document.getElementById('timer');
            const pulmonDiv = document.getElementById('txt-pulmon');
            
            if (timerDiv) timerDiv.innerText = `${m}:${s.toString().padStart(2, '0')}`;
            if (pulmonDiv) {
                // SINCRO CLÍNICA NATURAL: 4 segundos arriba y 4 segundos abajo (Ciclos regulares de 8 segundos)
                let ciclo = this.timeLeft % 8;
                if (cycle >= 4) {
                    pulmonDiv.innerText = t.inspira.toUpperCase();
                    pulmonDiv.style.color = "#00bcd4";
                } else {
                    pulmonDiv.innerText = t.expira.toUpperCase();
                    pulmonDiv.style.color = "#d84315";
                }
            }

            if (this.timeLeft > 0 && this.timeLeft % 20 === 0) {
                let recordatorios = this.idiomaActual === 'es' ? [
                    "Sigue el pulso. Estás conmigo.", "No mires tus biles. Respira ya.",
                    "Mantén el ritmo ahora.", "Siente el peso fuera de tus hombros.",
                    "Te estoy acompañando. Hazlo conmigo.", "Siente el aire limpiando tu pecho."
                ] : [
                    "Follow the rhythm. You are with me.", "Forget your bills. Breathe now.",
                    "Keep the pace.", "Feel the weight leave your shoulders.",
                    "I am with you. Do it now.", "Feel the air clearing your chest."
                ];
                KERNEL.hablar(recordatorios[Math.floor(Math.random() * recordatorios.length)]);
            }

            if (this.timeLeft <= 0) {
                clearInterval(this.timer);
                this.hablar(t.fin);
                alert(t.fin);
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
        
        // Mantiene guardado el perfil dinámico pero limpia estados volátiles de sesión por privacidad
        sessionStorage.clear();
        location.reload();
    }
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());
