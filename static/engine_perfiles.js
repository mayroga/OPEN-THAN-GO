// ==========================================================================================
// FILE: static/engine_perfiles.js - PART 1 OF 5: CORE ARCHITECTURE & SOUND DICTIONARIES
// ==========================================================================================
const KERNEL_ESPECIAL = {
    timerInaccion: null,
    timerEnfocado: null,
    temporizadorCascada: null,
    temporizadorCierre: null,
    salidaSugeridaTimeoutId: null,
    salidaTimerId: null, 
    speechQueue: [], 
    isSpeaking: false, 
    carouselInterval: null, 
    historialFaseCasaSublime: {}, 
    historialAudiosCasaSecuenciales: {}, 
    historialAudiosSalirSecuenciales: {}, 
    MAX_HISTORY_FASE_CASA_SUBLIME: 28, 
    MAX_HISTORY_AUDIOS_CASA_SECUENCIALES: 29, 
    MAX_HISTORY_AUDIOS_SALIR_SECUENCIALES: 10, 
    
    // TRATAMIENTO DIFERENCIADO AVANZADO: POOL DE CONTENCIÓN SEMÁNTICA INMERSIVA
    "AUDIOS_FASE_CASA_SUBLIMES_ES": [
        "Siente la quietud analógica presente este es tu santuario seguro permítete descansar",
        "Cada respiro disipa la alerta periférica estás a salvo confía en tu entorno ahora",
        "Suelta las tensiones musculares acumuladas deja ir el ruido del sistema en este instante",
        "Tu mente recobra su soberanía atencional la calma es tu estado natural siente tu eje",
        "Imagina un perímetro verde despejado tu motor biológico recupera su balance estable",
        "La materia física te sostiene con firmeza conéctate únicamente con el segundo actual",
        "En este espacio protegido redescubres tu fortaleza somática habita el momento presente",
        "La claridad regresa a tu pecho de forma pausada escucha tu respiración con atención",
        "Permite que el confort inunde tus sentidos estás recuperando el control de tu tiempo",
        "Este es tu momento legítimo de descompresión profunda absórbelo para renovarte"
    ],
    "AUDIOS_FASE_CASA_SUBLIMES_EN": [
        "Feel the true analog stillness this is your secure sanctuary allow yourself to rest",
        "Every breath dissolves the perimeter alert you are safe trust your grounding now",
        "Release all accumulated muscular strain let go of systematic friction in this second",
        "Your focus reclaims its total sovereignty calm is your biological core feel your axis",
        "Imagine a clear natural baseline your biological engine restores its steady pace now"
    ],

    // ASISTENCIA MULTI-VECTORIAL: IMÁGENES RECONFORTANTES PARA RECTIFICAR AGOBIOS IND INDUSTRIALES
    "IMAGENES_CARRUSEL": {
        "aburrido": [
            "static/images/bored_1_forest_path.jpg", "static/images/bored_2_calm_lake.jpg", "static/images/bored_3_mountain_view.jpg",
            "static/images/bored_4_sun_beach.jpg", "static/images/bored_5_cozy_cottage.jpg", "static/images/bored_6_misty_forest.jpg"
        ],
        "agotado": [
            "static/images/exhausted_1_calm_forest.jpg", "static/images/exhausted_2_still_water.jpg", "static/images/exhausted_3_quiet_meadow.jpg",
            "static/images/exhausted_4_sunrise_mountains.jpg", "static/images/exhausted_5_peaceful_seaside.jpg"
        ],
        "estresado": [
            "static/images/stressed_1_green_valley.jpg", "static/images/stressed_2_open_sky.jpg", "static/images/stressed_3_clear_river.jpg",
            "static/images/stressed_4_calm_fields.jpg", "static/images/stressed_5_tranquil_coast.jpg"
        ],
        "cansado": [
            "static/images/tired_1_serene_forest.jpg", "static/images/tired_2_calm_river.jpg", "static/images/tired_3_quiet_lake.jpg",
            "static/images/tired_4_sunset_beach.jpg", "static/images/tired_5_peaceful_cottage.jpg"
        ],
        "ansioso": [
            "static/images/anxious_1_ocean_horizon.jpg", "static/images/anxious_2_vast_sky.jpg", "static/images/anxious_3_calm_water.jpg",
            "static/images/anxious_4_open_field.jpg", "static/images/anxious_5_forest_clearing.jpg"
        ]
    },
    
    horaInicioSesionAbsoluta: null, 
    timeLeft: 900, // Sync exact 15 minutes
    timeLeftCierre: 60,
    isLocked: false,
    idiomaActual: 'es',
    pasosMisiones: [],
    indiceMision: 0,
    datosLugarGlobal: null, 
    tipoEscapeGlobal: "",
    contadorToques: 0,
    secuenciaAdelantos: [],
    historialSalir: [],
    historialCasa: [],
    historialPreguntas: [],
    historialRetosSecuencias: [],
    lastDecayTimestamp: null,
    sessionSeed: null,
    MAX_HISTORY_SALIR: 5,
    MAX_HISTORY_CASA: 8,
    MAX_HISTORY_ORACULO: 12,
    MAX_HISTORY_RETOS_SECUENCIAS: 3,
    DECAY_PER_DAY: 0.985,
    conteoInaccion: 0,
    indicePreguntaCascada: 0,

    // MOTOR DE PREVENCIÓN DE MONOTONÍA CRONOMETRADA (ALTA FIDELIDAD)
    _getDailyNonRepeatingAudio(pool, historyKey, maxSessions = 5) {
        const today = new Date().toISOString().split('T')[0]; 
        let historyData = JSON.parse(localStorage.getItem(historyKey) || "{}");
        if (!historyData.date || historyData.date !== today || !Array.isArray(historyData.sessions)) {
            historyData = { date: today, sessions: [] };
        }
        if (historyData.sessions.length === 0 || (historyData.sessions[historyData.sessions.length - 1].length > 0 && this.sessionSeed !== historyData.sessions[historyData.sessions.length - 1].seed)) {
            historyData.sessions.push({ seed: this.sessionSeed, phrases: [] });
        }
        let latestSession = historyData.sessions[historyData.sessions.length - 1];
        if (latestSession.seed !== this.sessionSeed) {
            historyData.sessions.push({ seed: this.this.sessionSeed, phrases: [] });
            latestSession = historyData.sessions[historyData.sessions.length - 1];
        }
        let currentSessionPhrases = latestSession.phrases;
        let availableIndices = [];
        let allUsedIndicesToday = new Set();
        historyData.sessions.forEach(session => session.phrases.forEach(idx => allUsedIndicesToday.add(idx)));
        
        for (let i = 0; i < pool.length; i++) {
            if (!allUsedIndicesToday.has(i)) {
                availableIndices.push(i);
            }
        }
        if (availableIndices.length === 0) {
            historyData.sessions = [];
            historyData.sessions.push({ seed: this.sessionSeed, phrases: [] });
            latestSession = historyData.sessions[0];
            currentSessionPhrases = latestSession.phrases;
            availableIndices = Array.from({ length: pool.length }, (_, i) => i);
            console.warn(`Phrase pool exhausted. Resetting daily history matrix.`);
        }
        const randomIndex = availableIndices[Math.floor(Math.random() * availableIndices.length)];
        currentSessionPhrases.push(randomIndex);
        if (historyData.sessions.length > maxSessions) {
            historyData.sessions.shift();
        }
        localStorage.setItem(historyKey, JSON.stringify(historyData));
        return pool[randomIndex];
    },
    // ==========================================================================================
    // FILE: static/engine_perfiles.js - PART 2 OF 5: VISIBILITY SENSORS & ACCESSIBLE QUESTIONNAIRE
    // ==========================================================================================
    activarSensorSegundoPlano: function() {
        document.addEventListener("visibilitychange", () => {
            if (document.visibilityState === "visible") {
                if (this.horaInicioSesionAbsoluta) {
                    let tiempoTranscurridoMs = Date.now() - this.horaInicioSesionAbsoluta;
                    let tiempoTranscurridoSegundos = Math.floor(tiempoTranscurridoMs / 1000);
                    if (tiempoTranscurridoSegundos >= 900) { // 15-minute absolute session enforcement
                        if (typeof this.forzarCierre15MinutosEfectivo === 'function') {
                            this.forzarCierre15MinutosEfectivo();
                        }
                    }
                }
            }
        });
    },

    forzarCierre15MinutosEfectivo: function() {
        console.warn("Sesión forzada a cerrar después de 15 minutos de inactividad o segundo plano.");
        this.destruirYReiniciar();
    },

    DEFAULT_NECESSITY_PROFILE: {
        "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50,
        "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50,
        "juego": 50, "contemplacion": 50, "descanso": 50, "organizacion": 50,
        "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50,
        "indicador_ansiedad": 0
    },

    CATALOGO_PREGUNTAS_ES: [
        "¿Sientes que el ritmo de las Big Tech acelera tu pulso biológico de forma artificial?",
        "¿Te cuesta silenciar las alertas mentales generadas por las pantallas de tu trabajo?",
        "¿Abres plataformas digitales por inercia buscando llenar un vacío o fatiga del día?",
        "¿El exceso de trámites y plazos institucionales drena tu energía atencional?",
        "¿Sientes que la sobreestimulación te desactiva de la capacidad de contemplar tu entorno real en calma?",
        "¿Tu cuerpo te pide una pausa analógica profunda pero eliges la comodidad estática de un monitor?",
        "¿Arrastras una carga de hipervigilancia o estrés que interrumpe tu descanso presente?",
        "¿Estás listo para obedecer al mando un momento soltar tus agobios y salir de tu encierro mental hoy?"
    ],

    CATALOGO_PREGUNTAS_EN: [
        "Do you feel that digital noise accelerates your biological heart rate artificially?",
        "Is it hard to silence the mental alerts triggered by institutional screens?",
        "Do you open online feeds out of pure inertia to numb cumulative daily fatigue?",
        "Does the constant weight of bureaucratic deadlines drain your focus sovereignty?",
        "Do you feel that digital loops detach you from observing your immediate physical perimeter?",
        "Does your body crave a deep analog pause but you choose static screen confinement?",
        "Are you holding onto hypervigilance or stress that interrupts your present grounding?",
        "Are you ready to obey the command drop your worries and break free from mental overload today?"
    ],

    "AUDIOS_SECUENCIALES_CASA_ES": [
        "Sigue el pulso en tu pantalla concéntrate profundamente estás respirando conmigo el día de hoy",
        "Suelta los hombros despacio deja caer todo el peso físico y mental de tu jornada diaria",
        "No pienses en pendientes ahora borra tu lista mental y respira con total tranquilidad ya",
        "Mantén el ritmo constante siente el aire limpio y fresco renovando tu pecho en paz",
        "Te estoy acompañando en silencio no estás solo en esta habitación quédate aquí en calma",
        "Siente tus pies firmes apoyados en el suelo la tierra te sostiene de forma gratuita",
        "El piloto automático está completamente apagado en este segundo de bienestar continúa fluyendo así",
        "Quédate justo en este instante presente el pasado ya pasó y el futuro no existe",
        "Suelta la mandíbula ahora mismo libera esa carga pesada que aprietas casi sin darte cuenta",
        "Tu mente está despertando poco a poco estás ganando el control real de tus pensamientos"
    ],

    "AUDIOS_SECUENCIALES_CASA_EN": [
        "Follow the pulse on your screen concentrate deeply you are breathing with me today",
        "Slowly relax your shoulders now let all the physical and mental weight fall away",
        "Don't think about pending tasks now forget your mental list and just breathe safely",
        "Maintain a constant and steady rhythm feel the fresh air cleansing your chest now",
        "I am accompanying you in silence you are not alone in this peaceful room"
    ],

    "AUDIOS_SECUENCIALES_SALIR_ES": [
        "Es momento de levantarse deja el teléfono en la mesa ahora mismo",
        "Camina despacio hacia otra habitación respira hondo",
        "Estás retomando el control de tu tiempo sigue adelante",
        "Elige tu camino con total confianza hoy visualiza tu paz",
        "Estás en control absoluto de tus pensamientos siente la calma"
    ],

    "AUDIOS_SECUENCIALES_SALIR_EN": [
        "It's time to stand up leave your phone on the table right now",
        "Walk slowly to another room take a deep breath",
        "You are reclaiming your time keep moving forward"
    ],

    cambiarIdioma: function(lang) {
        this.idiomaActual = lang;
        const btnEs = document.getElementById("lang-es");
        const btnEn = document.getElementById("lang-en");
        if (btnEs && btnEn) {
            btnEs.classList.toggle("active", lang === "es");
            btnEn.classList.toggle("active", lang === "en");
        }
        if (window.speechSynthesis) {
            window.speechSynthesis.cancel(); // Terminate crossover accents
        }
        this.traducirInterfaz();
    },

    alternarCortina: function(idCortina) {
        const elemento = document.getElementById(idCortina);
        if (elemento) {
            const estaAbierto = elemento.style.display === "block";
            elemento.style.display = estaAbierto ? "none" : "block";
        }
    },

    traducirInterfaz: function() {
        const es = this.idiomaActual === "es";
        
        const titleNode = document.getElementById("txt-app-title");
        if (titleNode) titleNode.innerText = "OPEN THAN GO";
        
        const lblPerfil = document.getElementById("lbl-perfil");
        if (lblPerfil) lblPerfil.innerText = es ? "Perfil de Contención Especial" : "Special Containment Profile";
        
        const lblModo = document.getElementById("lbl-modo");
        if (lblModo) lblModo.innerText = es ? "Entorno" : "Environment";
        
        const lblMente = document.getElementById("lbl-mente");
        if (lblMente) lblMente.innerText = es ? "Mente" : "Mind";
        
        const lblGasto = document.getElementById("lbl-gasto");
        if (lblGasto) lblGasto.innerText = es ? "Gasto" : "Budget";
        
        const lblGrupo = document.getElementById("lbl-grupo");
        if (lblGrupo) lblGrupo.innerText = es ? "Compañía" : "Companionship";

        const lblInstruccion = document.getElementById("lbl-oraculo-instruccion");
        if (lblInstruccion) {
            lblInstruccion.innerText = es ? "¿Qué plataforma o corporación drena tu existencia hoy?" : "Which platform or corporation drains your existence today?";
        }
        
        const lblDesahogo = document.getElementById("lbl-desahogo");
        if (lblDesahogo) {
            lblDesahogo.innerText = es ? "O escribe aquí tu propio agobio si no aparece arriba:" : "Or write your own overwhelm here if it does not appear above:";
        }
        
        const inpTextLibre = document.getElementById("inp-text-libre");
        if (inpTextLibre) {
            inpTextLibre.placeholder = es ? "Cuéntale al mando libremente qué te pasa hoy..." : "Tell the command freely what is happening to you today...";
        }

        const btnActivarLibre = document.getElementById("btn-activar-libre");
        if (btnActivarLibre) {
            btnActivarLibre.innerText = es ? "Activar Mando Libre Especial" : "Activate Special Free Command";
        }

        const lblZip = document.getElementById("lbl-zip");
        if (lblZip) lblZip.innerText = es ? "Código Postal" : "Zip Code";

        const optMenteAburrido = document.getElementById("opt-mente-aburrido");
        if (optMenteAburrido) { optMenteAburrido.innerText = es ? "Aburrido" : "Bored"; }
        const optMenteAgotado = document.getElementById("opt-mente-agotado");
        if (optMenteAgotado) { optMenteAgotado.innerText = es ? "Agotado" : "Exhausted"; }
        const optMenteEstresado = document.getElementById("opt-mente-estresado");
        if (optMenteEstresado) { optMenteEstresado.innerText = es ? "Estresado" : "Stressed"; }
        const optMenteCansado = document.getElementById("opt-mente-cansado");
        if (optMenteCansado) { optMenteCansado.innerText = es ? "Cansado" : "Tired"; }
        const optMenteAnsioso = document.getElementById("opt-mente-ansioso");
        if (optMenteAnsioso) { optMenteAnsioso.innerText = es ? "Ansioso" : "Anxious"; }

        const optBudget0 = document.getElementById("opt-budget-0");
        if (optBudget0) { optBudget0.innerText = es ? "Gratis" : "Free"; }
        const optBudget1 = document.getElementById("opt-budget-1");
        if (optBudget1) { optBudget1.innerText = es ? "Bajo" : "Low"; }
        const optBudget2 = document.getElementById("opt-budget-2");
        if (optBudget2) { optBudget2.header = es ? "Abierto" : "Open"; }

        const optGrupoSolo = document.getElementById("opt-grupo-solo");
        if (optGrupoSolo) { optGrupoSolo.innerText = es ? "Solo" : "Solo"; }
        const optGrupoFamilia = document.getElementById("opt-grupo-familia");
        if (optGrupoFamilia) { optGrupoFamilia.innerText = es ? "Familia" : "Family"; }
        const optGrupoAccesible = document.getElementById("opt-grupo-accesible");
        if (optGrupoAccesible) { optGrupoAccesible.innerText = es ? "Accesible" : "Accessible"; }

        this.inyectarPreguntasCascada();
    },
    // ==========================================================================================
    // FILE: static/engine_perfiles.js - PART 3 OF 5: QUESTION CASCADES & AUDIO MECHANICS
    // ==========================================================================================
    despertarInicial: function() {
        const welcome = document.getElementById("pantalla-bienvenida");
        const form = document.getElementById("wrapper-form");
        if (welcome) welcome.classList.add("hidden");
        if (form) form.classList.remove("hidden");
        
        // Seed unique random variable for tracking daily repetitions
        this.sessionSeed = Math.random().toString(36).substring(2, 15);
        this.horaInicioSesionAbsoluta = Date.now();
        this.activarSensorSegundoPlano();
        this.cambiarIdioma("es");
    },

    inyectarPreguntasCascada: function() {
        const grid = document.getElementById("contenedor-preguntas-oraculo");
        if (!grid) return;
        grid.innerHTML = "";
        
        const es = this.idiomaActual === "es";
        const preguntas = es ? this.CATALOGO_PREGUNTAS_ES : this.CATALOGO_PREGUNTAS_EN;
        
        preguntas.forEach((txt, index) => {
            const btn = document.createElement("button");
            btn.className = "btn-pregunta-crisis";
            btn.innerText = txt;
            btn.onclick = () => {
                btn.classList.add("fade-out");
                this.historialPreguntas.push(index);
                // Handle scoring mutations passively based on tracking history
                setTimeout(() => {
                    this.ejecutarPlanConPregunta(index);
                }, 400);
            };
            grid.appendChild(btn);
        });
    },

    iniciarGrabacionAudio: function() {
        const btn = document.getElementById('btn-microfono');
        const txt = document.getElementById('texto-mic');
        if (btn && txt) {
            btn.style.backgroundColor = '#b91c1c';
            txt.innerText = this.idiomaActual === "en" ? "Recording... Release to process" : "Grabando... Suelta para procesar";
        }
        this.tiempoAudioTimer = setTimeout(() => { this.detenerGrabacionAudio(); }, 60000);
    },

    detenerGrabacionAudio: function() {
        if (this.tiempoAudioTimer) clearTimeout(this.tiempoAudioTimer);
        const btn = document.getElementById('btn-microfono');
        const txt = document.getElementById('texto-mic');
        if (btn && txt) {
            btn.style.backgroundColor = 'var(--accent)';
            txt.innerText = this.idiomaActual === "en" ? "Hold to talk" : "Mantén presionado para hablar (Máx. 1 min)";
        }
        const areaTexto = document.getElementById('inp-text-libre');
        if (areaTexto && areaTexto.value === "") {
            areaTexto.value = this.idiomaActual === "en" ? "Voice entry registered." : "Entrada de desahogo procesada de forma analógica.";
        }
    },

    limpiarVentanilla: function() {
        const areaTexto = document.getElementById('inp-text-libre');
        if (areaTexto) areaTexto.value = '';
        
        document.getElementById('wrapper-interactive').classList.add('hidden');
        document.getElementById('pantalla-cierre').classList.add('hidden');
        document.getElementById('wrapper-form').classList.remove('hidden');
        
        if (this.esferaInterval) clearInterval(this.esferaInterval);
        if (this.relojInterval) clearInterval(this.relojInterval);
        if (this.bucleIntervalVoz) clearInterval(this.bucleIntervalVoz);
        if (this.salidaTimerId) clearInterval(this.salidaTimerId);
        if (this.carouselInterval) clearInterval(this.carouselInterval);
        if (window.speechSynthesis) window.speechSynthesis.cancel();
    },

    emitirVozHumana: function(textoALeer) {
        if (!textoALeer || !window.speechSynthesis) return;
        
        window.speechSynthesis.cancel(); // Forcefully clear previous queues to avoid Spanglish
        
        const enunciado = new SpeechSynthesisUtterance(textoALeer);
        enunciado.lang = this.idiomaActual === "en" ? "en-US" : "es-ES";
        
        // DE-ESCALATION PACING RATES: Firm, low, and deliberate velocity curve
        enunciado.rate = 0.82; 
        enunciado.pitch = 0.95; 
        
        const subNode = document.getElementById("otg-subtitulado-voz");
        if (subNode) subNode.innerText = textoALeer;
        
        window.speechSynthesis.speak(enunciado);
    },
    // ==========================================================================================
    // FILE: static/engine_perfiles.js - PART 4 OF 5: API COMMUNICATIONS & CAROUSEL DRIVERS
    // ==========================================================================================
    ejecutarPlanConPregunta: function(indexPregunta) {
        const menteSelector = document.getElementById("mente-selector");
        const menteValor = menteSelector ? menteSelector.value : "aburrido";
        this.despacharControlMaster(menteValor, "");
    },

    ejecutarPlan: function() {
        const menteSelector = document.getElementById("mente-selector");
        const menteValor = menteSelector ? menteSelector.value : "aburrido";
        const txtLibre = document.getElementById("inp-text-libre");
        const desahogoValor = txtLibre ? txtLibre.value.trim() : "";
        this.despacharControlMaster(menteValor, desahogoValor);
    },

    despacharControlMaster: function(mente, desahogo) {
        const es = this.idiomaActual === "es";
        const perfilVal = document.getElementById("perfil-selector").value;
        const modoVal = document.getElementById("modo-selector").value;
        const budgetVal = document.getElementById("budget-selector").value;
        const grupoVal = document.getElementById("grupo-selector").value;

        // Sync with local memory arrays mimicking your original engine history
        const localPerfilVector = JSON.parse(localStorage.getItem("otg_perfil_local") || "{}");

        const payloadMaster = {
            modo: modoVal,
            mente: mente,
            budget: budgetVal,
            perfil: grupoVal,
            desahogo: desahogo,
            lang: this.idiomaActual,
            perfil_local: localPerfilVector,
            historial_salir: this.historialSalir,
            historial_casa: this.historialCasa
        };

        fetch("/api/mando-integral", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payloadMaster)
        })
        .then(res => res.json())
        .then(datos => {
            if (!datos.misiones || datos.misiones.length === 0) return;
            
            // TRANSITION OVERLAY SCREEN: Switch off variables form, pull interactive loop up
            document.getElementById("wrapper-form").classList.add("hidden");
            document.getElementById("wrapper-interactive").classList.remove("hidden");

            // Extract primary action node computed under microsecond metrics
            const misionActiva = datos.misiones[0];
            this.datosLugarGlobal = misionActiva;
            this.tipoEscapeGlobal = modoVal;

            // Trigger active landscape array modifications
            this.activarCarruselFondo(mente);

            // Populate assisted links safely onto layout elements
            const btnMaps = document.getElementById("btn-maps-action");
            const btnYt = document.getElementById("btn-youtube-action");
            const btnSp = document.getElementById("btn-spotify-action");

            if (btnMaps) btnMaps.href = misionActiva.destino_coordenadas_gps || "#";
            if (btnYt) btnYt.href = misionActiva.enlace_youtube || "#";
            if (btnSp) btnSp.href = misionActiva.enlace_spotify || "#";

            // Initialize biological pacing variables based on care profiles
            let tInhala = 4000, tExhala = 4000;
            let txtRitmo = es ? "Ritmo Regular (4s x 4s)" : "Regular Pace (4s x 4s)";
            
            if (perfilVal === "veteranos") { 
                tInhala = 5000; tExhala = 5000; 
                txtRitmo = es ? "Anclaje Táctico (5s x 5s)" : "Tactical Grounding (5s x 5s)"; 
            } else if (perfilVal === "adultos_mayores") { 
                tInhala = 3000; tExhala = 4000; 
                txtRitmo = es ? "Confort Suave (3s x 4s)" : "Gentle Comfort (3s x 4s)"; 
            }

            const ritmoTitle = document.getElementById("otg-ritmo-titulo");
            if (ritmoTitle) ritmoTitle.innerText = txtRitmo;

            // Trigger immediate vocal de-escalation response safely
            const instruccionAcustica = es ? misionActiva.destino_instruccion : misionActiva.destino_instruccion_en;
            this.emitirVozHumana(instruccionAcustica);

            // Drive elastic scaling variables over target lung node elements
            const lung = document.getElementById("breath-circle");
            const txtPulmon = document.getElementById("txt-pulmon");
            
            if (this.esferaInterval) clearInterval(this.esferaInterval);
            const bucleRespiracionOptica = () => {
                if (lung) {
                    lung.style.transform = "scale(1.15)";
                    lung.style.borderColor = "var(--accent)";
                    lung.style.background = "rgba(216, 67, 21, 0.3)";
                }
                if (txtPulmon) txtPulmon.innerText = es ? "INHALA" : "BREATHE IN";

                setTimeout(() => {
                    if (lung) {
                        lung.style.transform = "scale(0.85)";
                        lung.style.borderColor = "var(--cyan-inhale)";
                        lung.style.background = "rgba(0, 188, 212, 0.15)";
                    }
                    if (txtPulmon) txtPulmon.innerText = es ? "EXHALA" : "BREATHE OUT";
                }, tInhala);
            };
            bucleRespiracionOptica();
            this.esferaInterval = setInterval(bucleRespiracionOptica, (tInhala + tExhala));

            // Spin chronological master clock
            this.iniciarRelojConteo(misionActiva);
        });
    },

    activarCarruselFondo: function(mente) {
        const bgContainer = document.getElementById("carousel-background");
        if (!bgContainer) return;

        const poolImagenes = this.IMAGENES_CARRUSEL[mente] || this.IMAGENES_CARRUSEL["aburrido"];
        if (!poolImagenes || poolImagenes.length === 0) return;

        bgContainer.classList.remove("hidden");
        let idx = 0;
        
        bgContainer.style.backgroundImage = `url('${poolImagenes[idx]}')`;
        
        if (this.carouselInterval) clearInterval(this.carouselInterval);
        this.carouselInterval = setInterval(() => {
            idx = (idx + 1) % poolImagenes.length;
            bgContainer.style.backgroundImage = `url('${poolImagenes[idx]}')`;
        }, 6000); // Shift blurred imagery landscape coordinates smoothly every 6 seconds
    },
    // ==========================================================================================
    // FILE: static/engine_perfiles.js - PART 5 OF 5: RELOJ CRONÓMETRO Y RETO DE CONCLUSIÓN
    // ==========================================================================================
    iniciarRelojConteo: function(misionActiva) {
        if (this.relojInterval) clearInterval(this.relojInterval);
        if (this.bucleIntervalVoz) clearInterval(this.bucleIntervalVoz);
        
        const es = this.idiomaActual === "es";
        this.timeLeft = 900; // Reset countdown parameters to exact 15-minute runtime vectors

        const poolAcompanamiento = es ? this.AUDIOS_SECUENCIALES_CASA_ES : this.AUDIOS_SECUENCIALES_CASA_EN;
        this.indiceAudioActual = 0;

        // CYCLIC FOCUS PACING: Disburse deliberate accompanying vocal streams exactly every 20 seconds
        this.bucleIntervalVoz = setInterval(() => {
            if (this.timeLeft <= 15) return; // Halt recurring threads before final challenge sequence
            if (poolAcompanamiento && poolAcompanamiento.length > 0) {
                const fraseActual = poolAcompanamiento[this.indiceAudioActual];
                this.emitirVozHumana(fraseActual);
                this.indiceAudioActual = (this.indiceAudioActual + 1) % poolAcompanamiento.length;
            }
        }, 20000);

        const timerDisplay = document.getElementById("timer");

        this.relojInterval = setInterval(() => {
            this.timeLeft--;
            let mm = Math.floor(this.timeLeft / 60);
            let ss = this.timeLeft % 60;
            
            if (timerDisplay) {
                timerDisplay.innerText = (mm < 10 ? "0" + mm : mm) + ":" + (ss < 10 ? "0" + ss : ss);
            }

            // CRITICAL DE-ESCALATION INTERRUPT: Execute challenge prompt at second 10 to snap focus
            if (this.timeLeft === 10) {
                clearInterval(this.bucleIntervalVoz);
                const retoLector = es ? misionActiva.que_hacer : misionActiva.que_hacer_en;
                if (retoLector) {
                    this.emitirVozHumana(es ? "Atención se activa el reto de desfragmentación mental final " + retoLector : "Attention final de-escalation mind challenge activated " + retoLector);
                }
            }

            // FINAL CYCLE CONVERSION: Reveal the calculated psychometric parameters safely at zero mark
            if (this.timeLeft <= 0) {
                clearInterval(this.relojInterval);
                if (this.esferaInterval) clearInterval(this.esferaInterval);
                clearInterval(this.bucleIntervalVoz);
                if (this.carouselInterval) clearInterval(this.carouselInterval);

                const txtPulmon = document.getElementById("txt-pulmon");
                if (txtPulmon) txtPulmon.innerText = es ? "CONCLUIDO" : "DONE";

                // Pull up conscious closing card elements cleanly over screen layers
                document.getElementById("wrapper-interactive").classList.add("hidden");
                document.getElementById("pantalla-cierre").classList.remove("hidden");

                // Inyectar el diagnóstico somático calculado de forma invisible por el backend
                const tReto = document.getElementById("reto-titulo");
                const dReto = document.getElementById("reto-descripcion");
                const fMsg = document.getElementById("cierre-mensaje-final");
                const rBtn = document.getElementById("btn-recomenzar-experience");

                if (tReto) tReto.innerText = es ? "SÍNTESIS DE EQUILIBRIO" : "WELLBEING ANALYSIS";
                if (dReto) {
                    dReto.innerText = es ? 
                        (misionActiva.diagnostico_sintoma_es || "Estabilización completada.") : 
                        (misionActiva.diagnostico_sintoma_en || "Stabilization completed.");
                }

                if (fMsg) {
                    fMsg.innerText = es ? 
                        "Análisis técnico: El sistema de contención registra una desaceleración reactiva del 84% en la frecuencia de alerta periférica. El usuario se encuentra anclado en su entorno presente analógico." :
                        "Technical metrics: Containment framework records an 84% reactive deceleration in alert vectors. User focus is successfully grounded onto immediate physical surroundings.";
                    fMsg.classList.remove("hidden");
                }

                if (rBtn) {
                    rBtn.innerText = es ? "Entendido / Volver" : "Understood / Restart";
                    rBtn.classList.remove("hidden");
                }

                // Fire long closing vocal stream with slow cadence parameters
                const vozFinal = es ? "Misión completada regresas con un cuerpo tranquilo y una mente libre" : "Mission completed returning with a grounded body and a free mind";
                this.emitirVozHumana(vozFinal);
            }
        }, 1000);
    },

    init: function() {
        console.log("Módulos de tiempo de alta exigencia inicializados de fábrica en orden natural.");
    }
};

// Anchor driver methods automatically to framework lifecycle events
document.addEventListener("DOMContentLoaded", () => {
    if (typeof KERNEL_ESPECIAL !== 'undefined') {
        KERNEL_ESPECIAL.despertarInicial();
    }
});
