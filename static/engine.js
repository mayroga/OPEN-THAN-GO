// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.6.5.0
// Company: May Roga LLC
// File: static/engine.js - SECCIÓN 1 DE 3 (NÚCLEO CONVERSACIONAL SECUENCIAL)

const KERNEL = {
    timer: null,
    timeLeft: 600,
    isLocked: false,
    idiomaActual: 'es',
    pasosMisiones: [],
    indiceMision: 0,
    datosLugarGlobal: null,
    tipoEscapeGlobal: "",
    
    // Variables de Control de Tiempo e Impaciencia SOLDADAS
    relojRealSegundos: 600,
    contadorToques: 0,
    secuenciaAdelantos:,

    // ARQUITECTURA ADICTIVA: 8 Bloques Secuenciales Fijos de 6 Preguntas (De Menor a Mayor Complejidad)
    bloqueActual: 0,
    conteoInaccion: 0, // Rastreador de Congelamiento para no cargar el sistema
    
    CATALOGO_PREGUNTAS: [
        // Bloque 1: Rutina Diaria General
        "¿La rutina de la semana te está consumiendo?",
        "¿Sientes que tus días son una copia del anterior?",
        "¿Pasas el día libre mirando la pantalla sin hacer nada?",
        "¿Te cuesta levantarte de la cama aunque ya descansaste?",
        "¿Sientes pereza de salir de tu zona de confort hoy?",
        "¿El piloto automático tomó el control de tus decisiones?",

        // Bloque 2: Presión Financiera e Impulso Corporativo
        "¿Trabajas mucho y sientes que no avanzas económicamente?",
        "¿Tienes miedo constante a perder tu empleo en este país?",
        "¿Sientes que lo que te pagan no es suficiente para tus gastos?",
        "¿Ganas bien pero no te atreves a hacer algo diferente?",
        "¿Abres Amazon o Walmart para gastar por aburrimiento?",
        "¿Los biles y las deudas bloquean tu paz mental?",

        // Bloque 3: Aislamiento Social y Entorno Familiar
        "¿Discutes seguido con tus hijos o tu familia?",
        "¿Sientes que están separados o aislados viviendo bajo el mismo techo?",
        "¿Las inconveniencias y diferencias familiares te agobian?",
        "¿Extrañas demasiado a tus familiares que están lejos?",
        "¿Sientes que estás solo contigo mismo enfrentando todo?",
        "¿Te rodea mucha gente pero te sientes incomprendido?",

        // Bloque 4: Relaciones de Pareja y Desamor
        "¿Es difícil encontrar a alguien que de verdad te quiera aquí?",
        "¿Estás pasando por un divorcio o separación dolorosa?",
        "¿No tienes pareja y el peso de la soledad te asfixia hoy?",
        "¿Tu relación actual se volvió monótona y sin motivos?",
        "¿Discutes por dinero o por biles con tu pareja?",
        "¿Prefieres esconderte en el teléfono antes de hablar con alguien?",

        // Bloque 5: Parálisis por Comodidad o Abundancia Vacía
        "¿Tienes todo a nivel material pero no te conformas con nada?",
        "¿Quieres hacer algo diferente hoy pero no sabes qué es?",
        "¿Sientes que el dinero no está llenando tu vacío interno?",
        "¿Te compras cosas innecesarias que luego dejas guardadas?",
        "¿La comodidad te mantiene encerrado en tu propia casa?",
        "¿Has perdido los motivos reales para sonreír de corazón?",

        // Bloque 6: Desgaste Físico, Mental y Salud
        "¿Quieres estar bien de salud pero no encuentras la energía?",
        "¿Sientes tensión acumulada en tus hombros y espalda ahora?",
        "¿Tus ojos te arden por culpa de la luz artificial?",
        "¿Tu mente no para de dar vueltas pensando en el mañana?",
        "¿Sientes el pecho apretado por la prisa de la ciudad?",
        "¿Has olvidado cuándo fue la última vez que respiraste aire puro?",

        // Bloque 7: Crisis de Identidad y Miedos Ocultos
        "¿Te da miedo perder el control si dejas la rutina?",
        "¿Sientes que el sistema te quiere dormido y consumiendo?",
        "¿Te comparas con lo que ves en las redes de otros?",
        "¿Crees que tu vida es solo trabajar y pagar biles?",
        "¿Te da pánico equivocarte si tomas una decisión nueva?",
        "¿Sientes que el tiempo vuela y tú sigues estancado?",

        // Bloque 8: Quiebre Biopsicosocial Profundo
        "¿Tu mente se convirtió en tu mayor prisión en este momento?",
        "¿Quieres ayudar a tu familia pero te sientes impotente?",
        "¿Ganas lo suficiente pero te da miedo perder tu estatus?",
        "¿Sientes que estás perdiendo los mejores años de tu vida?",
        "¿Te cuesta creer que las cosas puedan mejorar para ti hoy?",
        "¿Estás listo para dejar que el mando rompa tu encierro mental?"
    ],

    obtenerPerfilLocal() {
        let perfil = localStorage.getItem("otg_perfil_dinamico");
        if (!perfil) {
            perfil = {
                "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50, 
                "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50, 
                "juego": 50, "contemplacion": 50, "trabajo": 50, "descanso": 50, "organizacion": 50, 
                "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50,
                "indicador_ansiedad": 0
            };
            localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
        }
        return typeof perfil === "string" ? JSON.parse(perfil) : perfil;
    },

    init() {
        const btnMando = document.getElementById('btn-mando');
        if (btnMando) btnMando.onclick = () => this.ejecutar();
        
        // Carga secuencial automática del Bloque 1 desde la memoria local del smartphone
        this.bloqueActual = parseInt(localStorage.getItem("otg_bloque_secuencial")) || 0;
    },

    despertarInicial() {
        document.getElementById('pantalla-bienvenida').style.display = 'none';
        document.getElementById('wrapper-form').classList.remove('hidden');
        this.inyectarBloquePreguntas();
        
        const saludos = [
            "Bienvenido a ópen dán go. Tu escape inteligente. Escucha mis preguntas en pantalla.",
            "ópen dán go está activo. No rellenes casillas de biles. Mira las opciones en tu pantalla ya.",
            "Entraste a ópen dán go. Rompamos tu piloto automático ahora mismo. Toca lo que sientes hoy."
        ];
        this.hablar(saludos[Math.floor(Math.random() * saludos.length)]);
        
        // Inicializa el temporizador de inacción de contingencia local (Acción-Reacción)
        this.iniciarMonitoreoInaccion();
    },

    inyectarBloquePreguntas() {
        const grid = document.getElementById('contenedor-preguntas-oraculo');
        if (!grid) return;
        
        grid.innerHTML = "";
        let inicioIdx = this.bloqueActual * 6;
        
        // Si el usuario superó los 8 bloques secuenciales, reinicia de menor a mayor
        if (inicioIdx >= this.CATALOGO_PREGUNTAS.length) {
            this.bloqueActual = 0;
            inicioIdx = 0;
            localStorage.setItem("otg_bloque_secuencial", 0);
        }

        for (let i = 0; i < 6; i++) {
            let preguntaTexto = this.CATALOGO_PREGUNTAS[inicioIdx + i];
            if (!preguntaTexto) break;

            let btn = document.createElement('button');
            btn.className = 'btn-pregunta-crisis';
            btn.innerText = `${i + 1}. ${preguntaTexto}`;
            btn.onclick = () => this.reaccionarPreguntaSeleccionada(preguntaTexto);
            grid.appendChild(btn);
        }
    },

    iniciarMonitoreoInaccion() {
        clearInterval(this.timer);
        this.conteoInaccion = 0;
        
        // Monitorea el comportamiento del hardware cada 10 segundos para no saturar procesos
        this.timer = setInterval(() => {
            this.conteoInaccion++;
            
            // ESTADO 1 Y 2: Si pasa el tiempo sin responder, avanza al siguiente bloque para picar su curiosidad
            if (this.conteoInaccion === 1 || this.conteoInaccion === 2) {
                this.bloqueActual++;
                this.inyectarBloquePreguntas();
                this.hablar("Veo que estás dudando. Mira estas otras opciones en tu pantalla. Rompe la indecisión.");
            } 
            // ESTADO 3 (CONGELAMIENTO CRÓNICO): Se detiene de forma respetuosa y le da su tiempo
            else if (this.conteoInaccion >= 3) {
                clearInterval(this.timer);
                this.hablar("Disculpa. Te daré tu tiempo. Sé que tu mente está cansada. Estaré aquí esperando a que estés listo para salir del encierro.");
                
                // Muta la visual a un estado de pausa amigable
                const instruccion = document.getElementById('lbl-oraculo-instruccion');
                if (instruccion) instruccion.innerText = "Tomando un respiro. Toca cuando estés listo...";
            }
        }, 10000); // Ventanas exactas de 10 segundos
    },
    reaccionarPreguntaSeleccionada(textoPregunta) {
        // Detiene el temporizador de inacción en el segundo en que hay Reacción
        clearInterval(this.timer);
        
        // Guarda el avance secuencial de menor a mayor para su próxima visita
        this.bloqueActual++;
        localStorage.setItem("otg_bloque_secuencial", this.bloqueActual);

        // Mapea la pregunta seleccionada al input oculto de desahogo
        const inputOculto = document.getElementById('inp-text-invisible');
        if (inputOculto) inputOculto.value = textoPregunta;

        // Dispara la ejecución satelital de inmediato
        this.ejecutar();
    },

    hablar(texto) {
        if (!texto) return;
        window.speechSynthesis.cancel();
        let fx = texto.replace(/OPEN THAN GO/gi, "OPEN DAN GO").replace(/<[^>]*>/g, '');
        const msg = new SpeechSynthesisUtterance(fx);
        msg.lang = 'es-US'; 
        msg.rate = 1.20; 
        window.speechSynthesis.speak(msg);
    },

// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.6.5.0
// Company: May Roga LLC
// File: static/engine.js - SECCIÓN 2 DE 2 (EJECUCIÓN DISRUPTIVA Y RELOJ INTEGRAL)

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;

        const payload = {
            zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
            modo: document.getElementById('modo-selector') ? document.getElementById('modo-selector').value : "SALIR",
            desahogo: document.getElementById('inp-text-invisible') ? document.getElementById('inp-text-invisible').value : "",
            lang: this.idiomaActual,
            perfil_local: this.obtenerPerfilLocal()
        };

        const container = document.getElementById('wrapper-interactive');
        document.getElementById('wrapper-form').classList.add('hidden');
        container.innerHTML = `<div style='text-align:center; padding:40px 0;'><h2 style='color:#fff; font-size:1.1rem;'>CONECTANDO...</h2></div>`;
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

    procesarFlujoSecuencial(container) {
        clearInterval(this.timer);
        window.speechSynthesis.cancel();

        const t = {
            es: { inspira: "Inhala ahora", expira: "Exhala ahora", fin: "Protocolo completado. Borrando rastro.", listen: "ESCUCHA MI GUÍA", launch: "ABRIR CANAL BIG TECH YA" },
            en: { inspira: "Inhale now", expira: "Exhale now", fin: "Protocol completed. Clearing tracks.", listen: "LISTEN TO THE GUIDE", launch: "OPEN BIG TECH CHANNEL NOW" }
        }[this.idiomaActual];

        // MODO SALIR (ACCION_CAMPO) - RETENCION BIOLÓGICA DE 35S
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
                                try {
                                    let perfil = KERNEL.obtenerPerfilLocal();
                                    let token = KERNEL.datosLugarGlobal.token_entorno || "general";
                                    if (perfil) {
                                        if (token.includes("árbol") || token.includes("Sombra")) perfil["naturaleza"] = Math.min(perfil["naturaleza"] + 10, 100);
                                        else if (token.includes("Caminata") || token.includes("subida")) perfil["movimiento"] = Math.min(perfil["movimiento"] + 10, 100);
                                        else if (token.includes("Paseo") || token.includes("colores")) perfil["creatividad"] = Math.min(perfil["creatividad"] + 10, 100);
                                        localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
                                    }
                                } catch (e) {}
                                window.open(this.datosLugarGlobal.destino_coordenadas_gps, '_blank');
                                KERNEL.destruirYReiniciar();
                            };
                        }
                    }
                }, 1000);
                return;
            }
        }

        // MODO CASA - TRANSICIÓN HACIA EL RELOJ CLÍNICO MANDATORIO
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
        window.speechSynthesis.cancel();
        let msg = this.idiomaActual === 'es' ? "Iniciamos diez minutos de limpieza mental profunda. Respira." : "Starting ten minutes of deep mental clearing. Breathe.";
        this.hablar(msg);
        
        container.innerHTML = `
        <div style="text-align:center; width:100%;">
            <div id="breath-circle" style="cursor:pointer;" title="Toca para enfocar tu mente"></div>
            <div id="timer">10:00</div>
            <p id="txt-pulmon">INHALA / INHALE</p>
        </div>`;

        this.timeLeft = 600;
        this.relojRealSegundos = 600;
        this.contadorToques = 0;
        this.secuenciaAdelantos =;

        const circleElement = document.getElementById('breath-circle');
        const timerDiv = document.getElementById('timer');
        const pulmonDiv = document.getElementById('txt-pulmon');

        // CATÁLOGO DE 30 AUDIOS SECUENCIALES FIJOS (Cada 20 segundos sin repetir de menor a mayor profundidad)
        const AUDIOS_SECUENCIALES_CASA = [
            "Sigue el pulso en tu pantalla. Concéntrate. Estás conmigo hoy.",
            "Suelta los hombros despacio. Deja caer todo el peso físico de la semana.",
            "No mires tus biles ahora. No mires tu cartera. Respira ya.",
            "Mantén el ritmo constante. Siente el aire fresco limpiando tu pecho.",
            "Te estoy acompañando en silencio. No estás solo en esta habitación.",
            "Siente tus pies firmes apoyados en el suelo. La tierra te sostiene gratis.",
            "El piloto automático corporativo está apagado en este segundo. Continúa así.",
            "Quédate justo en este instante. El pasado ya pasó, el presente es tuyo.",
            "Suelta la mandíbula ahora. Libera esa carga que aprietas sin darte cuenta.",
            "Tu mente está despertando poco a poco. Estás ganando control real.",
            "Eres mucho más grande que tus deudas. Respira hondo y despacio.",
            "Rompe el zombi que el sistema quiere que seas. Quédate en la sala conmigo.",
            "Escucha mi voz. Nota cómo tu respiración se vuelve más profunda y limpia.",
            "Tus ojos están descansando finalmente de las luces artificiales de la pantalla.",
            "Siente los latidos de tu pecho. Es tu motor vivo latiendo para ti.",
            "Siente el peso fuera de tu espalda. Imagina que dejas caer tu mochila.",
            "No dejes que los pensamientos rápidos te saquen de este momento de paz.",
            "Abandona la prisa de la ciudad hoy. Aquí el tiempo es tuyo.",
            "El dinero regresará a tus bolsillos, pero este segundo de calma no se repite.",
            "Siente cómo tus pulmones se llenan de fuerza con cada ciclo de aire azul.",
            "Tu familia necesita que estés fuerte por dentro. Recupérate ahora.",
            "Olvídate de las aplicaciones de compras. Tu mente está por encima del consumo.",
            "Estás borrando el ruido del día. Quédate en la sala respirando conmigo.",
            "La rutina diaria se ha roto. Tú gobiernas tus decisiones en este instante.",
            "El suelo está firme debajo tuyo. Siente la estabilidad de la tierra.",
            "Tu pecho está libre de agobios ahora. Expulsa todo lo malo de golpe.",
            "Estás recuperando tu centro biopsicosocial. Sigue la luz del círculo.",
            "Tu mente es fuerte. Has domado el miedo a perder el trabajo hoy.",
            "Faltan pocos segundos para el reinicio definitivo. Siente la esperanza.",
            "Estás completamente a salvo aquí. Quédate en paz absoluta en este segundo."
        ];

        if (circleElement) {
            circleElement.onclick = () => {
                if (this.contadorToques < 10) {
                    let adelantoSegundos = this.secuenciaAdelantos[this.contadorToques];
                    this.timeLeft = Math.max(this.timeLeft - adelantoSegundos, 0);
                    this.contadorToques++;
                    try {
                        let perfil = this.obtenerPerfilLocal();
                        perfil["indicador_ansiedad"] = Math.min((perfil["indicador_ansiedad"] || 0) + 10, 100);
                        localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
                    } catch (e) {}
                    let m = Math.floor(this.timeLeft / 60);
                    let s = this.timeLeft % 60;
                    if (timerDiv) {
                        timerDiv.innerText = `${m}:${s.toString().padStart(2, '0')}`;
                    }
                }
            };
        }

        this.timer = setInterval(() => {
            this.relojRealSegundos--;

            if (this.timeLeft > 0) {
                this.timeLeft--;
            }
            let m = Math.floor(this.timeLeft / 60);
            let s = this.timeLeft % 60;
            if (timerDiv) timerDiv.innerText = `${m}:${s.toString().padStart(2, '0')}`;
            
            if (pulmonDiv) {
                let ciclo = this.relojRealSegundos % 8;
                if (ciclo >= 4) {
                    pulmonDiv.innerText = t.inspira.toUpperCase();
                    pulmonDiv.style.color = "#00bcd4";
                } else {
                    pulmonDiv.innerText = t.expira.toUpperCase();
                    pulmonDiv.style.color = "#d84315";
                }
            }

            // CONTROL Y DISPARO SECUENCIAL FIJO MAESTRO CADA 20 SEGUNDOS DESDE EL SEGUNDO CERO
            if (this.relojRealSegundos < 600 && this.relojRealSegundos % 20 === 0) {
                let pasoAudioIdx = Math.floor((600 - this.relojRealSegundos) / 20) - 1;
                let recordatorioTexto = AUDIOS_SECUENCIALES_CASA[pasoAudioIdx];
                if (recordatorioTexto) {
                    window.speechSynthesis.cancel(); // Purga forzada instantánea para mantener limpio el hardware
                    let msgFlotante = new SpeechSynthesisUtterance(recordatorioTexto);
                    msgFlotante.lang = 'es-US';
                    msgFlotante.rate = 1.20;
                    window.speechSynthesis.speak(msgFlotante);
                }
            }

            if (this.relojRealSegundos <= 0) {
                clearInterval(this.timer);
                window.speechSynthesis.cancel();
                if (circleElement) {
                    circleElement.style.animation = "none";
                    circleElement.style.transform = "scale(1)";
                }
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
        sessionStorage.clear();
        location.reload();
    }
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());
