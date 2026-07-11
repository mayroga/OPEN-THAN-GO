// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.6.0.1
// Company: May Roga LLC
// File: static/engine.js (Frontend Logic)

const KERNEL = {
    timerInaccion: null,
    timerClinico: null,
    temporizadorCascada: null,
    timeLeft: 600, // 10 minutes for clinical timer (unified with relojRealSegundos)
    isLocked: false,
    idiomaActual: 'es',
    pasosMisiones: [],
    indiceMision: 0,
    datosLugarGlobal: null, // Stores the full response from backend for current recommendation
    tipoEscapeGlobal: "",
   
    // Time and Impatience Control Variables
    contadorToques: 0,
    secuenciaAdelantos: [5, 7, 9, 10, 14, 16, 17, 19, 21, 5], // Seconds to advance clinical timer per tap
    
    // ACTUALIZAR: seenIds, Debe convertirse en historialMisiones, historialCasa, historialSalir, historialPreguntas
    historialSalir: [], // Stores IDs of SALIR recommendations
    historialCasa: [],  // Stores IDs of CASA recommendations
    historialPreguntas: [], // Stores indices of Oracle questions shown recently
    lastDecayTimestamp: null, // For otg_last_decay in localStorage
    sessionSeed: null, // For otg_session_seed in localStorage

    // Constants for history limits (from main.py)
    MAX_HISTORY_SALIR: 5,
    MAX_HISTORY_CASA: 8,
    MAX_HISTORY_ORACULO: 12, // For Oracle questions
    DECAY_PER_DAY: 0.985, // From main.py

    // Sequential Conversational Architecture
    // ELIMINAR: bloqueActual
    conteoInaccion: 0, // Inaction counter for advancing question blocks
    indicePreguntaCascada: 0, // Index for fading out questions

    // Default template for the 19 human needs profile (must align with backend)
    DEFAULT_NECESSITY_PROFILE: {
        "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50,
        "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50,
        "juego": 50, "contemplacion": 50, "trabajo": 50, "descanso": 50, "organizacion": 50,
        "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50,
        "indicador_ansiedad": 0 // Special internal indicator, not a "need" for location matching
    },
   
    // Corrected: Separate question catalogs for each language
    CATALOGO_PREGUNTAS_ES: [
        // Bloque 1: El Bucle Digital Urbano (Redes, Contenido y Consumo)
        "¿Abres redes sociales por inercia, comparando tu día con imágenes idealizadas?",
        "¿Te pierdes en contenido de video que olvidas en pocos segundos, buscando llenar un vacío?",
        "¿Usas música para ahogar el ruido mental y la inquietud de tu día a día?",
        "¿Buscas novedades en tiendas online solo por la expectativa de recibir algo?",
        "¿Paseas por grandes superficies gastando sin rumbo fijo, solo por inercia?",
        "¿Sientes que lo digital te desconectó de la capacidad de observar el mundo real en calma?",

        // Bloque 2: Evasión y Rutina Física (Comida, Descanso y Movimiento)
        "¿Inviertes mucho en experiencias pasajeras buscando una satisfacción que se desvanece rápido?",
        "¿Te refugias en espacios ajenos huyendo de situaciones que te acompañan a todas partes?",
        "¿Conduces sin destino solo para escapar del encierro en tu propio entorno?",
        "¿Mantienes hábitos por costumbre, sintiendo que te anestesian de tu realidad?",
        "¿Te cuesta romper tu rutina por miedo a la incomodidad o el esfuerzo físico?",
        "¿Tu cuerpo te pide actividad, pero eliges la comodidad estática del sofá?",

        // Bloque 3: Distracción Nocturna y Aislamiento Social
        "¿Buscas ambientes ruidosos para silenciar los pensamientos que te inquietan?",
        "¿Bailas rodeado de gente, sintiendo a la vez una profunda soledad interior?",
        "¿Asistes a eventos sociales por compromiso, anhelando volver a tu propio espacio?",
        "¿Necesitas estímulos externos para sobrellevar conversaciones monótonas?",
        "¿Aceptas la compañía, pero te escudas detrás de tu dispositivo móvil?",
        "¿Proyectas una imagen de perfección social para ocultar tu verdadero sentir?",

        // Bloque 4: Entorno Familiar y Distancia Emocional
        "¿Existen roces constantes con tus seres queridos que impiden la armonía en casa?",
        "¿Sientes desinterés o apatía ante reuniones familiares inevitables?",
        "¿Compartes techo, pero la distancia emocional te hace sentir como extraños?",
        "¿La visita de un familiar te genera tensión en vez de verdadera paz y conexión?",
        "¿La añoranza por los que están lejos te paraliza y te impide vivir tu presente?",
        "¿Sientes que las presiones compartidas están creando silencios en tus relaciones?",

        // Bloque 5: Evasión por Viajes y Fugas de la Realidad
        "¿Subestimas lo que tienes cerca, soñando con escapes lejanos que te son inalcanzables?",
        "¿Deseas una huida total para que el cambio de escenario resuelva tus crisis internas?",
        "¿Crees que la solución a tu insatisfacción es un cambio radical de ubicación?",
        "¿Planeas grandes gastos en ocio que podrían comprometer tu estabilidad futura?",
        "¿Buscas imágenes de paisajes distantes porque perdiste la capacidad de asombrarte con tu propio cielo?",
        "¿Te sientes atado a tu lugar y asumes que la libertad requiere de un boleto a otro sitio?",

        // Bloque 6: Vulnerabilidad Corporal y Sensaciones
        "¿Aplazas tu bienestar físico por miedo a los costos o las complicaciones?",
        "¿Sientes molestias en el cuerpo causadas por la acumulación de estrés diario?",
        "¿Te preocupa cómo el sistema impactaría tu salud y la estabilidad de los tuyos?",
        "¿Sientes opresión en el pecho por la prisa del entorno y la incertidumbre del futuro?",
        "¿Tu bienestar se desgasta en una actividad que te exige demasiado a cambio de recompensas?",
        "¿Has olvidado el consuelo de una respiración profunda, libre de cualquier preocupación?",

        // Bloque 7: El Espejismo Material y Vacío Existencial
        "¿Buscas la tranquilidad en un entorno natural, pero tu mente sigue en el bucle de las responsabilidades?",
        "¿Tienes estabilidad y comodidades, pero una insatisfacción crónica te consume por dentro?",
        "¿Crees que la adquisición de propiedades te dará un sentido de pertenencia o identidad?",
        "¿Te paraliza la idea de dejar la seguridad de lo conocido, por miedo a un paso incierto?",
        "¿Te comparas con las posesiones y el estilo de vida de los demás?",
        "¿Sientes que la vida se te escapa dedicando todo a acumular cosas sin sentido?",

        // Bloque 8: El Despertar Maestro (Quiebre y Mando Absoluto)
        "¿Tu mente se convirtió en tu mayor prisión en este momento?",
        "¿Quieres ayudar a tu familia a estar mejor pero te paraliza no saber cómo empezar?",
        "¿Estás cansado de repetir patrones que consumen tu libertad y energía?",
        "¿Sientes que estás perdiendo tus mejores años esperando un milagro que no va a llegar?",
        "¿Te cuesta creer que exista un espacio gratis en tu zona capaz de devolverte la esperanza?",
        "¿Estás listo para obedecer al mando, soltar tus indecisiones y salir de tu encierro mental hoy?"
    ],
    CATALOGO_PREGUNTAS_EN: [
        // Block 1: The Urban Digital Loop (Social Media, Content, and Consumption)
        "Do you open social media out of inertia, comparing your day to idealized images?",
        "Do you get lost in video content that you forget in a few seconds, trying to fill a void?",
        "Do you use music to drown out mental noise and daily restlessness?",
        "Do you look for new items in online stores just for the anticipation of receiving something?",
        "Do you wander through big stores spending aimlessly, just out of inertia?",
        "Do you feel like technology disconnected you from the ability to calmly observe the real world?",

        // Block 2: Escape Consumption and Physical Routine (Food, Rest, and Movement)
        "Do you overspend on fleeting experiences looking for satisfaction that quickly fades?",
        "Do you take refuge in external spaces fleeing situations that accompany you everywhere?",
        "Do you drive aimlessly just to escape being cooped up in your own environment?",
        "Do you maintain habits out of custom, feeling that they numb you to your reality?",
        "Are you afraid to break your routine for fear of discomfort or physical effort?",
        "Does your body crave activity, but you choose the static comfort of the couch?",

        // Block 3: Nightly Distraction and Social Isolation
        "Do you seek noisy environments to silence the thoughts that trouble you?",
        "Do you dance surrounded by people, while feeling a deep inner loneliness?",
        "Do you attend social events out of obligation, wishing to return to your own space?",
        "Do you need external stimuli to endure monotonous conversations?",
        "Do you accept company but shield yourself behind your mobile device?",
        "Do you project an image of social perfection to hide your true feelings?",

        // Block 4: Family Environment and Emotional Distance
        "Do you constantly argue with your loved ones over differences that prevent harmony at home?",
        "Do you live under the same roof with your family but emotional distance makes you feel like strangers?",
        "Does a family visit generate tension instead of true peace and connection?",
        "Does longing for those far away paralyze you and prevent you from living your present?",
        "Do you feel that shared pressures are creating silences in your relationships?",

        // Block 5: Travel Evasion and Escapes from Reality
        "Do you underestimate what's near you, dreaming of distant escapes that are unattainable?",
        "Do you wish for a total escape so that a change of scenery resolves your internal crises?",
        "Do you believe that the solution to your dissatisfaction is a radical change of location?",
        "Do you plan large expenses on leisure that could compromise your future stability?",
        "Do you search for images of distant landscapes because you've lost the ability to be amazed by your own sky?",
        "Do you feel tied to your place and assume that freedom requires a ticket to another location?",

        // Block 6: Bodily Vulnerability and Sensations
        "Do you postpone your physical well-being for fear of costs or complications?",
        "Do you feel physical discomfort caused by the accumulation of daily stress?",
        "Are you concerned about how the system would impact your health and your family's stability?",
        "Do you feel tightness in your chest from the rush of your environment and the uncertainty of the future?",
        "Is your well-being wearing out in an activity that demands too much in exchange for rewards?",
        "Have you forgotten the comfort of a deep breath, free from any worry?",

        // Block 7: The Material Mirage and Existential Void
        "Do you seek tranquility in a natural environment, but your mind remains in the loop of responsibilities?",
        "Do you have stability and comforts but a chronic dissatisfaction consumes you within?",
        "Do you believe that acquiring property will give you a sense of belonging or identity?",
        "Does the idea of leaving the security of the known paralyze you, for fear of an uncertain step?",
        "Do you secretly compare yourself to the status and possessions of others?",
        "Do you feel time slipping through your fingers, dedicating everything to accumulating meaningless things?",

        // Block 8: The Master Awakening (Breakthrough and Absolute Command)
        "Has your mind become your biggest prison right now?",
        "Do you want to help your family be better but are paralyzed by not knowing how to start?",
        "Are you tired of repeating patterns that consume your freedom and energy?",
        "Do you feel like you are losing your best years waiting for a miracle that won't come?",
        "Is it hard for you to believe there's a free space in your area capable of restoring your hope?",
        "Are you ready to obey the command, let go of your indecisions, and break free from your mental imprisonment today?"
    ],

    // Corrected: Separate audio catalogs for each language
    AUDIOS_SECUENCIALES_CASA_ES: [
        "Sigue el pulso en tu pantalla. Concéntrate. Estás conmigo hoy.",
        "Suelta los hombros despacio. Deja caer todo el peso físico y mental de la semana.",
        "No pienses en responsabilidades ahora. No mires tu lista de tareas. Respira ya.",
        "Mantén el ritmo constante. Siente el aire fresco limpiando tu pecho.",
        "Te estoy acompañando en silencio. No estás solo en esta habitación.",
        "Siente tus pies firmes apoyados en el suelo. La tierra te sostiene gratis.",
        "El piloto automático corporativo está apagado en este segundo. Continúa así.",
        "Quédate justo en este instante. El pasado ya pasó, el presente es tuyo.",
        "Suelta la mandíbula ahora. Libera esa carga que aprietas sin darte cuenta.",
        "Tu mente está despertando poco a poco. Estás ganando control real.",
        "Eres mucho más grande que tus preocupaciones. Respira hondo y despacio.",
        "Rompe el zombi que el sistema quiere que seas. Quédate en la sala conmigo.",
        "Escucha mi voz. Nota cómo tu respiración se vuelve más profunda y limpia.",
        "Tus ojos están descansando finalmente de las luces artificiales de la pantalla.",
        "Siente los latidos de tu pecho. Es tu motor vivo latiendo para ti.",
        "Siente el peso fuera de tu espalda. Imagina que dejas caer tu mochila.",
        "No dejes que los pensamientos rápidos te saquen de este momento de paz.",
        "Abandona la prisa de la ciudad hoy. Aquí el tiempo es tuyo.",
        "Las oportunidades regresarán, pero este segundo de calma no se repite.",
        "Siente cómo tus pulmones se llenan de fuerza con cada ciclo de aire azul.",
        "Tu familia necesita que estés fuerte por dentro. Recupérate ahora.",
        "Olvídate de las aplicaciones de compras. Tu mente está por encima del consumo.",
        "Estás borrando el ruido del día. Quédate en la sala respirando conmigo.",
        "La rutina diaria se ha roto. Tú gobiernas tus decisiones en este instante.",
        "El suelo está firme debajo tuyo. Siente la estabilidad de la tierra.",
        "Tu pecho está libre de agobios ahora. Expulsa todo lo malo de golpe.",
        "Estás recuperando tu centro biopsicosocial. Sigue la luz del círculo.",
        "Tu mente es fuerte. Has domado el miedo a las presiones de hoy.",
        "Faltan pocos segundos para el reinicio definitivo. Siente la esperanza.",
        "Estás completamente a salvo aquí. Quédate en paz absoluta en este segundo."
    ],
    AUDIOS_SECUENCIALES_CASA_EN: [
        "Follow the pulse on your screen. Concentrate. You are with me today.",
        "Slowly relax your shoulders. Let all the physical and mental weight of the week fall away.",
        "Don't think about responsibilities now. Don't look at your to-do list. Breathe now.",
        "Maintain a constant rhythm. Feel the fresh air cleansing your chest.",
        "I am accompanying you in silence. You are not alone in this room.",
        "Feel your feet firmly on the ground. The earth supports you for free.",
        "The corporate autopilot is off this second. Keep going.",
        "Stay right in this instant. The past is gone, the present is yours.",
        "Release your jaw now. Let go of that tension you hold without realizing.",
        "Your mind is slowly awakening. You are gaining real control.",
        "You are much bigger than your worries. Breathe deeply and slowly.",
        "Break the zombie the system wants you to be. Stay in the room with me.",
        "Listen to my voice. Notice how your breathing becomes deeper and cleaner.",
        "Your eyes are finally resting from the artificial lights of the screen.",
        "Feel your heartbeat. It's your living engine beating for you.",
        "Feel the weight off your back. Imagine dropping your backpack.",
        "Don't let racing thoughts take you out of this peaceful moment.",
        "Abandon the city's rush today. Here, time is yours.",
        "Opportunities will return, but this second of calm will not repeat.",
        "Feel your lungs fill with strength with each cycle of blue air.",
        "Your family needs you to be strong inside. Recover now.",
        "Forget shopping apps. Your mind is above consumption.",
        "You are erasing the day's noise. Stay in the room breathing with me.",
        "The daily routine is broken. You govern your decisions at this instant.",
        "The ground is firm beneath you. Feel the stability of the earth.",
        "Your chest is free from worries now. Expel all negativity at once.",
        "You are regaining your biopsychosocial center. Follow the light of the circle.",
        "Your mind is strong. You have tamed the fear of today's pressures.",
        "Only a few seconds left for the definitive reset. Feel the hope.",
        "You are completely safe here. Remain in absolute peace this second."
    ],

    /**
     * Retrieves or initializes the user's dynamic profile from localStorage.
     * Ensures all 19 needs are present with default values if missing.
     * ACTUALIZAR: Agregar fecha, timestamp, decaimiento automático.
     * @returns {Object} The user's dynamic profile.
     */
    obtenerPerfilLocal() {
        let perfilRaw = localStorage.getItem("otg_perfil_dinamico");
        let perfil = {};

        if (!perfilRaw) {
            perfil = { ...this.DEFAULT_NECESSITY_PROFILE };
        } else {
            try {
                perfil = JSON.parse(perfilRaw);
                // Ensure all default needs are present in the loaded profile
                for (const need in this.DEFAULT_NECESSITY_PROFILE) {
                    if (!(need in perfil)) {
                        perfil[need] = this.DEFAULT_NECESSITY_PROFILE[need];
                    }
                }
            } catch (e) {
                console.error("Error parsing otg_perfil_dinamico from localStorage, resetting.", e);
                perfil = { ...this.DEFAULT_NECESSITY_PROFILE };
            }
        }

        // AGREGAR: fecha, timestamp, decaimiento automático, y otg_session_seed
        const now = Date.now();
        let lastDecayTimestamp = parseInt(localStorage.getItem("otg_last_decay") || now);
        this.sessionSeed = localStorage.getItem("otg_session_seed") || Math.random().toString(36).substring(2, 15);

        const daysPassed = (now - lastDecayTimestamp) / (1000 * 60 * 60 * 24);

        if (daysPassed >= 1) { // Apply decay if at least one full day has passed
            const newPerfil = {};
            const base = 50; // The default value for needs
            for (const necesidad in perfil) {
                if (necesidad === "indicador_ansiedad") {
                    newPerfil[necesidad] = perfil[necesidad];
                    continue;
                }
                const valor = perfil[necesidad];
                let diferencia = valor - base;
                diferencia *= (this.DECAY_PER_DAY ** daysPassed);
                newPerfil[necesidad] = Math.round((base + diferencia) * 100) / 100; // Round to 2 decimal places
            }
            perfil = newPerfil;
            lastDecayTimestamp = now; // Update last decay timestamp after decay applied
        }

        perfil.fecha = new Date(now).toISOString().split('T')[0]; // YYYY-MM-DD
        perfil.timestamp = now;

        localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
        localStorage.setItem("otg_last_decay", lastDecayTimestamp.toString());
        localStorage.setItem("otg_session_seed", this.sessionSeed);

        return perfil;
    },

    /** Initializes the KERNEL on DOMContentLoaded. */
    init() {
        // ELIMINAR la lógica de bloqueActual
        // this.bloqueActual = parseInt(localStorage.getItem("otg_bloque_secuencial")) || 0;

        // Set initial language if not already set (e.g., from a prior session)
        const storedLang = localStorage.getItem("otg_language");
        if (storedLang) {
            this.idiomaActual = storedLang;
        } else {
            localStorage.setItem("otg_language", this.idiomaActual);
        }
        // Load new history keys from localStorage
        try {
            this.historialSalir = JSON.parse(localStorage.getItem("otg_historial_salir") || "[]");
            this.historialCasa = JSON.parse(localStorage.getItem("otg_historial_casa") || "[]");
            this.historialPreguntas = JSON.parse(localStorage.getItem("otg_historial_oraculo") || "[]");
        } catch (e) {
            console.error("Error parsing history from localStorage, resetting.", e);
            this.historialSalir = [];
            this.historialCasa = [];
            this.historialPreguntas = [];
            localStorage.removeItem("otg_historial_salir");
            localStorage.removeItem("otg_historial_casa");
            localStorage.removeItem("otg_historial_oraculo");
        }
        // Ensure profile is loaded and decay is applied on app start
        this.obtenerPerfilLocal();
    },

    /** Starts the initial welcome sequence after user interaction. */
    despertarInicial() {
        document.getElementById('pantalla-bienvenida').style.display = 'none';
        document.getElementById('wrapper-form').classList.remove('hidden');
       
        // Apply language settings to UI elements *before* initial speech
        this.cambiarIdioma(this.idiomaActual);
       
        // Translate initial greetings based on selected language
        const saludos_es = [
            "Bienvenido a ópen dán go. Tu escape inteligente. Escucha mis preguntas en pantalla.",
            "ópen dán go está activo. Concéntrate un momento. Mira las opciones en tu pantalla ya.",
            "Entraste a ópen dán go. Rompamos tu piloto automático ahora mismo. Toca lo que sientes hoy."
        ];
        const saludos_en = [
            "Welcome to open than go. Your smart escape. Listen to my questions on screen.",
            "open than go is active. Focus for a moment. Look at the options on your screen now.",
            "You entered open than go. Let's break your autopilot right now. Tap what you feel today."
        ];
        const saludos = this.idiomaActual === 'es' ? saludos_es : saludos_en;
        this.hablar(saludos[Math.floor(Math.random() * saludos.length)]);
       
        // ACTUALIZAR: inyectarBloquePreguntas() debe reconstruirse
        this.inyectarBloquePreguntas();
        this.iniciarMonitoreoInaccion();
       
        // Ensure free writing button is always active, but only triggers if text is present
        this.activarBotonMandoLibreInicial();
    },

    /**
     * Injects a block of 6 questions into the UI, ensuring they are distinct and not recent.
     * ACTUALIZAR: Debe reconstruirse. 6 distintas, 6 de temas diferentes, 6 no recientes.
     */
    inyectarBloquePreguntas() {
        const grid = document.getElementById('contenedor-preguntas-oraculo');
        if (!grid) return;
       
        clearInterval(this.temporizadorCascada); // Stop any existing cascade
        grid.innerHTML = ""; // Clear previous questions
        this.indicePreguntaCascada = 0;
       
        const catalogo = this.idiomaActual === 'es' ? this.CATALOGO_PREGUNTAS_ES : this.CATALOGO_PREGUNTAS_EN;
        let preguntasDisponiblesIndices = [];
        let preguntasYaVistasRecientemente = new Set(this.historialPreguntas);

        // Prioritize questions not seen recently
        let unseenIndices = [];
        for (let i = 0; i < catalogo.length; i++) {
            if (!preguntasYaVistasRecientemente.has(i)) {
                unseenIndices.push(i);
            }
        }

        // If not enough unseen questions, reset history and use all available questions
        if (unseenIndices.length < 6) {
            this.historialPreguntas = []; // Reset history
            localStorage.removeItem("otg_historial_oraculo");
            for (let i = 0; i < catalogo.length; i++) {
                unseenIndices.push(i); // Add all indices again for selection
            }
        }
        
        // Shuffle the available indices to get a random, distinct selection
        // Fisher-Yates shuffle
        for (let i = unseenIndices.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [unseenIndices[i], unseenIndices[j]] = [unseenIndices[j], unseenIndices[i]];
        }

        let preguntasSeleccionadasIndices = [];
        for (let i = 0; i < 6; i++) { // Select 6 distinct questions
            if (unseenIndices.length === 0) break; // Safety break if no more questions
            const selectedIndex = unseenIndices.shift(); // Get one, remove from pool
            preguntasSeleccionadasIndices.push(selectedIndex);
            // Add to history and keep it limited
            this.historialPreguntas = [...this.historialPreguntas, selectedIndex].slice(-this.MAX_HISTORY_ORACULO);
        }
        localStorage.setItem("otg_historial_oraculo", JSON.stringify(this.historialPreguntas));

        // Create buttons for selected questions
        preguntasSeleccionadasIndices.forEach((questionIdx, i) => {
            let preguntaTexto = catalogo[questionIdx];
            if (!preguntaTexto) return; // Should not happen with robust selection

            let btn = document.createElement('button');
            btn.className = 'btn-pregunta-crisis';
            btn.id = `btn-pregunta-${i}`;
            btn.innerText = `${i + 1}. ${preguntaTexto}`;
            btn.onclick = () => this.reaccionarPreguntaSeleccionada(preguntaTexto);
            grid.appendChild(btn);
        });

        // ACTUALIZAR: iniciarEfectoCascada() - no cambiar la animación. Solo cambiar la forma en que recibe las preguntas.
        this.iniciarEfectoCascada();
    },

    /** Initiates the fading cascade effect for questions. */
    iniciarEfectoCascada() {
        this.indicePreguntaCascada = 0;
       
        const totalButtons = document.querySelectorAll('.btn-pregunta-crisis').length;
        if (totalButtons === 0) { // If no questions, immediately enable free writing
            this.liberarCajonEscrituraLibre();
            return;
        }

        this.temporizadorCascada = setInterval(() => {
            let botonParaEliminar = document.getElementById(`btn-pregunta-${this.indicePreguntaCascada}`);
           
            if (botonParaEliminar) {
                botonParaEliminar.classList.add('fade-out');
               
                let siguienteIdx = this.indicePreguntaCascada + 1;
                let siguienteBoton = document.getElementById(`btn-pregunta-${siguienteIdx}`);
                if (siguienteBoton) {
                    let textoLimpio = siguienteBoton.innerText.substring(3); // Remove the number prefix
                    this.hablar(textoLimpio);
                }
                this.indicePreguntaCascada++;
            } else {
                clearInterval(this.temporizadorCascada);
                this.liberarCajonEscrituraLibre(); // Once all questions are faded, activate free writing
            }
        }, 8000); // 8 seconds per question exactly
    },

    /** Activates the free writing input field and button from start. */
    activarBotonMandoLibreInicial() {
        const textarea = document.getElementById('inp-text-libre');
        const btnLibre = document.getElementById('btn-activar-libre');
        const lblDesahogo = document.getElementById('lbl-desahogo');
        const instruccion = document.getElementById('lbl-oraculo-instruccion');

        // Reset instruction to its initial state for questions
        if (instruccion) {
            instruccion.innerText = this.idiomaActual === 'es' ? "¿Qué te tiene atrapado hoy?" : "What has you trapped today?";
            instruccion.style.color = "var(--accent)";
        }
        if (lblDesahogo) lblDesahogo.style.color = "#666";

        if (btnLibre) {
            // Initial styling for the free command button (not yet "active")
            btnLibre.style.background = "#111";
            btnLibre.style.color = "#555";
            btnLibre.style.borderColor = "#222";
            btnLibre.onclick = () => {
                let textoEscrito = textarea.value.trim();
                if (textoEscrito.length > 3) {
                    this.reaccionarPreguntaSeleccionada(textoEscrito);
                } else {
                    this.hablar(this.idiomaActual === 'es' ? "Escribe tu problema en el cuadro antes de activar el mando." : "Write your problem in the box before activating control.");
                }
            };
        }
        // Add input event listener to textarea for immediate visual feedback and button activation
        if (textarea) {
            // Remove previous listener to prevent duplicates after language change or re-init
            textarea.removeEventListener('input', this.textareaInputHandler);
            // Store the handler reference for removal
            this.textareaInputHandler = () => {
                if (textarea.value.trim().length > 3) {
                    if (btnLibre) {
                        btnLibre.style.background = "var(--green-action)";
                        btnLibre.style.color = "#fff";
                        btnLibre.style.borderColor = "var(--green-action)";
                    }
                } else {
                    if (btnLibre) {
                        btnLibre.style.background = "#111";
                        btnLibre.style.color = "#555";
                        btnLibre.style.borderColor = "#222";
                    }
                }
            };
            textarea.addEventListener('input', this.textareaInputHandler);
        }
    },

    /** Activates the free writing input field and visually indicates readiness. */
    liberarCajonEscrituraLibre() {
        const textarea = document.getElementById('inp-text-libre');
        const btnLibre = document.getElementById('btn-activar-libre');
        const lblDesahogo = document.getElementById('lbl-desahogo');
        const instruccion = document.getElementById('lbl-oraculo-instruccion');

        if (instruccion) {
            instruccion.innerText = this.idiomaActual === 'es' ? "Mando libre listo. Cuéntame qué te pasa." : "Free control ready. Tell me what is happening.";
            instruccion.style.color = "var(--green-action)"; // Make instruction stand out
        }
        if (lblDesahogo) lblDesahogo.style.color = "#fff";
        if (textarea) textarea.focus();

        // Button styling is now handled by the input listener.
        // This ensures it becomes green as soon as text is typed, and can be clicked.
    },

    /**
     * Monitors user inaction and advances question blocks or pauses.
     * Reconstruido para no depender de bloqueActual.
     */
    iniciarMonitoreoInaccion() {
        clearInterval(this.timerInaccion);
        this.conteoInaccion = 0;
        this.timerInaccion = setInterval(() => {
            this.conteoInaccion++;
            if (this.conteoInaccion === 4 || this.conteoInaccion === 8) { // After 48s and 96s of inaction (4 or 8 * 12s)
                clearInterval(this.temporizadorCascada);
                // Ya no se usa bloqueActual, simplemente se recargan nuevas preguntas
                this.inyectarBloquePreguntas();
                this.hablar(this.idiomaActual === 'es' ? "Avanzamos de nivel. Mira estas otras opciones en pantalla." : "Moving up. Look at these other options on screen.");
            } else if (this.conteoInaccion >= 12) { // After 144s of inaction (12 * 12s)
                clearInterval(this.timerInaccion);
                clearInterval(this.temporizadorCascada);
                this.hablar(this.idiomaActual === 'es' ? "Disculpa. Te daré tu tiempo. Sé que tu mente está cansada. Estaré aquí esperando." : "Apologies. I will give you time. I know your mind is tired. I will be waiting here.");
                const instruccion = document.getElementById('lbl-oraculo-instruccion');
                if (instruccion) {
                    instruccion.innerText = this.idiomaActual === 'es' ? "Tomando un respiro. Toca cuando estés listo..." : "Taking a breath. Tap when you are ready...";
                    instruccion.style.color = "#666"; // Dim instruction
                }
            }
        }, 12000); // Check every 12 seconds
    },

    /**
     * Handles user selecting a question or entering free text.
     * Reconstruido para no depender de bloqueActual.
     */
    reaccionarPreguntaSeleccionada(textoPregunta) {
        clearInterval(this.timerInaccion);
        clearInterval(this.temporizadorCascada);
        // Eliminado: this.bloqueActual++;
        // Eliminado: localStorage.setItem("otg_bloque_secuencial", this.bloqueActual);
       
        // Use inp-text-libre value directly
        document.getElementById('inp-text-libre').value = textoPregunta;
        this.ejecutar();
    },

    /**
     * Converts text to speech using browser's SpeechSynthesis API.
     * Checks for API support and uses a fixed Spanish voice for consistency as per instructions.
     * @param {string} texto - The text to speak.
     */
    hablar(texto) {
        if (!('speechSynthesis' in window)) {
            console.warn("Speech Synthesis API not supported in this browser.");
            return;
        }
        if (!texto) return;
        window.speechSynthesis.cancel(); // Stop any ongoing speech
        let fx = texto.replace(/OPEN THAN GO/gi, "OPEN DAN GO").replace(/<[^>]*>/g, '');
        const msg = new SpeechSynthesisUtterance(fx);
        // Dynamically set language for speech synthesis
        msg.lang = this.idiomaActual === 'es' ? 'es-US' : 'en-US';
        msg.rate = 1.20; // Slightly faster for efficiency
        window.speechSynthesis.speak(msg);
    },

    /**
     * Changes the application's language and updates UI elements.
     * @param {string} lang - The target language ('es' or 'en').
     */
    cambiarIdioma(lang) {
        this.idiomaActual = lang;
        localStorage.setItem("otg_language", lang); // Persist language choice
        document.getElementById('lang-es').classList.toggle('active', lang === 'es');
        document.getElementById('lang-en').classList.toggle('active', lang === 'en');
       
        // SYNC ENGLISH BUTTON FIXED 100%
        const t = {
            es: { title: "OPEN THAN GO", zip: "Código Postal", instruccion: "¿Qué te tiene atrapado hoy?", desahogo: "O escribe aquí tu propio agobio si no aparece arriba:", placeholder: "Cuéntale al mando libremente qué te pasa hoy...", btn: "Activar Mando Libre", alert: "Idioma cambiado a español.", budget0: "Gratis", budget1: "Bajo", budget2: "Abierto", solo: "Solo", familia: "Familia", accesible: "Accesible", menteAburrido: "Aburrido", menteAgotado: "Agotado", menteEstresado: "Estresado", menteCansado: "Cansado", menteAnsioso: "Ansioso", modoSalir: "SALIR", modoCasa: "CASA" },
            en: { title: "OPEN THAN GO", zip: "ZIP Code", instruccion: "What has you trapped today?", desahogo: "Or write your own burden here if it does not appear above:", placeholder: "Tell the control freely what is happening to you today...", btn: "Activate Free Control", alert: "Language switched to English.", budget0: "Free", budget1: "Low", budget2: "Open", solo: "Alone", familia: "Family", accesible: "Accessible", menteAburrido: "Bored", menteAgotado: "Exhausted", menteEstresado: "Stressed", menteCansado: "Tired", menteAnsioso: "Anxious", modoSalir: "OUT", modoCasa: "HOME" }
        }[lang];
       
        document.getElementById('html-title').innerText = t.title;
        document.getElementById('txt-app-title').innerText = t.title;
        document.getElementById('lbl-zip').innerText = t.zip;
        document.getElementById('lbl-oraculo-instruccion').innerText = t.instruccion;
        document.getElementById('lbl-desahogo').innerText = t.desahogo;
        document.getElementById('inp-text-libre').placeholder = t.placeholder;
        document.getElementById('btn-activar-libre').innerText = t.btn;
        document.getElementById('opt-budget-0').innerText = t.budget0;
        document.getElementById('opt-budget-1').innerText = t.budget1;
        document.getElementById('opt-budget-2').innerText = t.budget2;
        document.getElementById('opt-perfil-solo').innerText = t.solo;
        document.getElementById('opt-perfil-familia').innerText = t.familia;
        document.getElementById('opt-perfil-accesible').innerText = t.accesible;
        document.getElementById('opt-mente-aburrido').innerText = t.menteAburrido;
        document.getElementById('opt-mente-agotado').innerText = t.menteAgotado;
        document.getElementById('opt-mente-estresado').innerText = t.menteEstresado;
        document.getElementById('opt-mente-cansado').innerText = t.menteCansado;
        document.getElementById('opt-mente-ansioso').innerText = t.menteAnsioso;
        document.querySelector('#modo-selector option[value="SALIR"]').innerText = t.modoSalir;
        document.querySelector('#modo-selector option[value="CASA"]').innerText = t.modoCasa;


        this.hablar(t.alert);
        this.inyectarBloquePreguntas(); // Re-inject questions in new language
        this.activarBotonMandoLibreInicial(); // Re-initialize free writing button in new language
    },

    /**
     * Executes the main logic to fetch recommendations from the backend.
     * Modificado para enviar historial_salir y historial_casa según el modo.
     */
    async ejecutar() {
        if (this.isLocked) return; // Prevent multiple submissions
        this.isLocked = true;

        const modoActual = document.getElementById('modo-selector') ? document.getElementById('modo-selector').value : "SALIR";

        const payload = {
            zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
            modo: modoActual,
            desahogo: document.getElementById('inp-text-libre') ? document.getElementById('inp-text-libre').value.trim() : "",
            lang: this.idiomaActual,
            mente: document.getElementById('mente-selector') ? document.getElementById('mente-selector').value : "aburrido",
            budget: document.getElementById('budget-selector') ? document.getElementById('budget-selector').value : "0",
            perfil: document.getElementById('perfil-selector') ? document.getElementById('perfil-selector').value : "solo",
            perfil_local: this.obtenerPerfilLocal(), // Send the user's dynamic profile
        };

        // Enviar historial específico según el modo, compatible con las claves que espera main.py
        if (modoActual === "CASA") {
            payload.seen_ids_casa = this.historialCasa; // Usar historialCasa para modo CASA
        } else { // Default to SALIR
            payload.seen_ids = this.historialSalir; // Usar historialSalir para modo SALIR
        }

        const container = document.getElementById('wrapper-interactive');
        document.getElementById('wrapper-form').classList.add('hidden');
        container.innerHTML = `<div style='text-align:center; padding:40px 0;'><h2 style='color:#fff; font-size:1.1rem;'>${this.idiomaActual === 'es' ? 'CONECTANDO...' : 'CONNECTING...'}</h2></div>`;
        container.classList.remove('hidden');

        try {
            const r = await fetch("/api/mando-integral", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await r.json();

            if (data.error) { // Handle backend validation errors
                alert(data.error);
                document.getElementById('wrapper-form').classList.remove('hidden');
                container.classList.add('hidden');
                this.isLocked = false;
                return;
            }

            this.datosLugarGlobal = data; // Store full backend response
            this.tipoEscapeGlobal = data.DIRECCIONAMIENTO_MASTER;
            this.indiceMision = 0;
           
            // Si el backend devuelve un historial actualizado, usarlo.
            // Para SALIR, el backend ahora devuelve 'historial_salir_actualizado'
            if (this.tipoEscapeGlobal === "ACCION_CAMPO" && data.historial_salir_actualizado) {
                this.historialSalir = data.historial_salir_actualizado;
                localStorage.setItem("otg_historial_salir", JSON.stringify(this.historialSalir));
            }
            // Para CASA, el backend ahora devuelve 'historial_casa_actualizado'
            else if (this.tipoEscapeGlobal === "INTERVENCION_DOMESTICA" && data.historial_casa_actualizado) {
                this.historialCasa = data.historial_casa_actualizado;
                localStorage.setItem("otg_historial_casa", JSON.stringify(this.historialCasa));
            }


            if (this.tipoEscapeGlobal === "INTERVENCION_DOMESTICA") {
                this.pasosMisiones = data.misiones.slice(0, 3); // Take first 3 for sequential display
            } else {
                this.pasosMisiones = []; // No internal missions for field action
            }
            this.procesarFlujoSecuencial(container);
        } catch (error) {
            console.error("Fetch error:", error);
            alert(this.idiomaActual === 'es' ? "Error de conexión con el servidor. Por favor, inténtalo de nuevo." : "Connection error with the server. Please try again.");
            document.getElementById('wrapper-form').classList.remove('hidden');
            container.classList.add('hidden');
            this.isLocked = false;
        }
    },

    /**
     * Processes the sequential flow based on the recommendation type.
     * Modificado para actualizar los historiales específicos.
     */
    procesarFlujoSecuencial(container) {
        clearInterval(this.timerClinico);
        window.speechSynthesis.cancel();

        const t = {
            es: { inspira: "Inhala ahora", expira: "Exhala ahora", fin: "Protocolo completado. Borrando rastro.", listen: "ESCUCHA MI GUÍA", launch: "ABRIR CANAL EXTERNO YA", fieldAction: "Acción de Campo", internalMission: "Misión Interna", doItNow: "HAZLO AHORA", suggestedEscape: "Escape sugerido" },
            en: { inspira: "Inhale now", expira: "Exhale now", fin: "Protocol completed. Clearing tracks.", listen: "LISTEN TO THE GUIDE", launch: "OPEN EXTERNAL CHANNEL NOW", fieldAction: "Field Action", internalMission: "Internal Mission", doItNow: "DO IT NOW", suggestedEscape: "Suggested escape" }
        }[this.idiomaActual];

        // Handles external "Field Action" recommendations
        if (this.tipoEscapeGlobal === "ACCION_CAMPO") {
            if (this.datosLugarGlobal) {
                // historialSalir ya se actualiza en ejecutar() si el backend lo devuelve.
                // Si no, el frontend podría replicar la lógica aquí para seguridad.
                // Sin embargo, ahora el backend lo devuelve explícitamente.

                let textoFormateado = this.datosLugarGlobal.destino_instruccion.replace(/\n/g, '<br>');
                container.innerHTML = `
                <div class="mision-card">
                    <small>${t.fieldAction}</small>
                    <h2>${this.datosLugarGlobal.destino_titulo}</h2>
                    <div class="instruccion-text">${textoFormateado}</div>
                    <button id="btn-countdown-salida" style="width:100%; background:#222; color:#aaa; padding:17px; font-weight:bold; margin-top:15px; border:none; text-transform:uppercase; border-radius:4px; font-size:0.9rem;" disabled>35s ${t.listen}</button>
                    <button id="btn-gps-action" class="hidden" style="width:100%; background:var(--secondary); color:#fff; padding:17px; font-weight:bold; margin-top:15px; border:none; text-transform:uppercase; border-radius:4px; cursor:pointer; font-size:0.95rem; letter-spacing:0.5px;">${t.launch}</button>
                </div>`;

                this.hablar(this.datosLugarGlobal.destino_instruccion);
               
                let retencion = 35; // Countdown for listening to the guide
                const btnCount = document.getElementById('btn-countdown-salida');
                const btnGps = document.getElementById('btn-gps-action');
               
                this.timerClinico = setInterval(() => {
                    retencion--;
                    if (btnCount) btnCount.innerText = `${retencion}s ${t.listen}`;
                    if (retencion <= 0) {
                        clearInterval(this.timerClinico);
                        if (btnCount) btnCount.style.display = 'none';
                        if (btnGps) {
                            btnGps.classList.remove('hidden');
                            btnGps.onclick = () => {
                                try {
                                    let perfil = KERNEL.obtenerPerfilLocal();
                                    const selectedVector = KERNEL.datosLugarGlobal.vector_entorno_seleccionado;
                                   
                                    // Dynamically update local profile based on the selected environment's needs vector
                                    for (const need in selectedVector) {
                                        // Only update actual needs, not the internal anxiety indicator
                                        if (need !== "indicador_ansiedad" && perfil[need] !== undefined) {
                                            // Increase the preference for the activated need, capping at 100
                                            perfil[need] = Math.min(perfil[need] + (selectedVector[need] * 0.1), 100); // 10% of the place's score is added
                                        }
                                    }
                                    localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
                                } catch (e) {
                                    console.error("Error updating local profile after action:", e);
                                }
                                window.open(this.datosLugarGlobal.destino_coordenadas_gps, '_blank');
                                KERNEL.destruirYReiniciar(); // Reset and restart app after external navigation
                            };
                        }
                    }
                }, 1000);
                return;
            }
        }

        // Handles internal "Domestic Intervention" missions
        if (this.indiceMision >= this.pasosMisiones.length) {
            this.iniciarRelojClinicoCasa(container, t); // All internal missions completed, start clinical timer
            return;
        }

        const paso = this.pasosMisiones[this.indiceMision];
        // historialCasa ya se actualiza en ejecutar() si el backend lo devuelve.
        // Si no, el frontend podría replicar la lógica aquí para seguridad.
        // Sin embargo, ahora el backend lo devuelve explícitamente.
       

        container.innerHTML = `
        <div class="mision-card">
            <small>${t.internalMission}</small>
            <h3>${paso.titulo}</h3>
            <p>${paso.descripcion}</p>
            <button id="btn-next" style="width:100%; background:var(--green-action); color:#fff; padding:16px; font-weight:bold; text-transform:uppercase; border-radius:6px; cursor:pointer; border:none; margin-top:15px; font-size:0.95rem;">${t.doItNow}</button>
        </div>`;

        this.hablar(paso.titulo + " . " + paso.descripcion);
        document.getElementById('btn-next').onclick = () => this.avanzarPaso();
    },

    /** Starts the 10-minute clinical breathing timer for CASA mode. */
    iniciarRelojClinicoCasa(container, t) {
        clearInterval(this.timerClinico);
        window.speechSynthesis.cancel();
       
        let msg = this.idiomaActual === 'es' ? "Iniciamos diez minutos de limpieza mental profunda. Respira." : "Starting ten minutes of deep mental clearing. Breathe.";
        this.hablar(msg);
       
        container.innerHTML = `
        <div style="text-align:center; width:100%;">
            <div id="breath-circle" style="cursor:pointer;" title="${this.idiomaActual === 'es' ? 'Toca para enfocar tu mente' : 'Tap to focus your mind'}"></div>
            <div id="timer">10:00</div>
            <p id="txt-pulmon">INHALA / INHALE</p>
            <!-- Corrected: Dynamic suggestion for SALIR mode during CASA mode -->
            <div id="salida-sugerida" class="hidden" style="margin-top: 30px; padding: 15px; border: 1px dashed #444; border-radius: 8px; font-size: 0.9rem; color: #888;">
                <p style="margin:0;">${t.suggestedEscape}: <a href="#" id="link-salida-sugerida" style="color: var(--accent); text-decoration: none; font-weight: bold;">Cargando...</a></p>
            </div>
        </div>`;

        this.timeLeft = 600; // Unified timer variable
        this.contadorToques = 0;

        const circleElement = document.getElementById('breath-circle');
        const timerDiv = document.getElementById('timer');
        const pulmonDiv = document.getElementById('txt-pulmon');
        const salidaSugeridaDiv = document.getElementById('salida-sugerida');
        const linkSalidaSugerida = document.getElementById('link-salida-sugerida');

        // Corrected: Use language-specific audio catalog
        const AUDIOS_SECUENCIALES_CASA = this.idiomaActual === 'es' ? this.AUDIOS_SECUENCIALES_CASA_ES : this.AUDIOS_SECUENCIALES_CASA_EN;

        if (circleElement) {
            circleElement.onclick = () => {
                if (this.contadorToques < this.secuenciaAdelantos.length) {
                    let adelantoSegundos = this.secuenciaAdelantos[this.contadorToques];
                    this.timeLeft = Math.max(this.timeLeft - adelantoSegundos, 0); // Decrement actual timer
                    this.contadorToques++;
                    try {
                        let perfil = this.obtenerPerfilLocal();
                        // Increase anxiety indicator when user taps, as it suggests impatience/seeking relief
                        perfil["indicador_ansiedad"] = Math.min((perfil["indicador_ansiedad"] || 0) + 5, 100); // Slight increase, capped at 100
                        localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
                    } catch (e) {
                        console.error("Error updating anxiety indicator:", e);
                    }
                    let m = Math.floor(this.timeLeft / 60);
                    let s = this.timeLeft % 60;
                    if (timerDiv) {
                        timerDiv.innerText = `${m}:${s.toString().padStart(2, '0')}`;
                    }
                }
            };
        }

        // Fetch SALIR suggestion for CASA mode after some time
        let salidaSugeridaTimeout = setTimeout(async () => {
            try {
                const r = await fetch("/api/mando-integral", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        modo: "SALIR",
                        lang: this.idiomaActual,
                        mente: "aburrido", // Default mood for initial suggestion, can be dynamic
                        budget: "0",
                        perfil: "solo",
                        desahogo: "",
                        zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
                        perfil_local: this.obtenerPerfilLocal(),
                        seen_ids: this.historialSalir // Send the correct history for SALIR suggestion
                    })
                });
                const data = await r.json();
               
                if (data.DIRECCIONAMIENTO_MASTER === "ACCION_CAMPO" && linkSalidaSugerida && salidaSugeridaDiv) {
                    // Update historialSalir if backend returned it (for consistency)
                    if (data.historial_salir_actualizado) {
                        this.historialSalir = data.historial_salir_actualizado;
                        localStorage.setItem("otg_historial_salir", JSON.stringify(this.historialSalir));
                    }

                    linkSalidaSugerida.innerText = data.destino_titulo;
                    linkSalidaSugerida.href = data.destino_coordenadas_gps;
                    salidaSugeridaDiv.classList.remove('hidden');
                    this.hablar(this.idiomaActual === 'es' ? `Considera también: ${data.destino_titulo}` : `Also consider: ${data.destino_titulo_en || data.destino_titulo}`);
                }
            } catch (e) {
                console.error("Error fetching SALIR suggestion in CASA mode:", e);
            }
        }, 180000); // Fetch after 3 minutes (180 seconds)

        this.timerClinico = setInterval(() => {
            if (this.timeLeft > 0) this.timeLeft--; // Decrement user-facing countdown

            let m = Math.floor(this.timeLeft / 60);
            let s = this.timeLeft % 60;
            if (timerDiv) timerDiv.innerText = `${m}:${s.toString().padStart(2, '0')}`;
           
            // Breathing animation text update
            if (pulmonDiv) {
                let ciclo = this.timeLeft % 8; // Use unified timeLeft
                if (ciclo >= 4) {
                    pulmonDiv.innerText = t.inspira.toUpperCase();
                    pulmonDiv.style.color = "var(--cyan-inhale)"; // Cyan for inhale
                } else {
                    pulmonDiv.innerText = t.expira.toUpperCase();
                    pulmonDiv.style.color = "var(--accent)"; // Orange for exhale
                }
            }

            // Play sequential audio messages every 20 seconds, based on elapsed time from 600s
            if (this.timeLeft < 600 && (600 - this.timeLeft) % 20 === 0 && (600 - this.timeLeft) !== 0) {
                let pasoAudioIdx = Math.floor((600 - this.timeLeft) / 20) - 1; // Calculate index
                if (pasoAudioIdx >= 0 && pasoAudioIdx < AUDIOS_SECUENCIALES_CASA.length) { // Ensure index is valid
                    let recordatorioTexto = AUDIOS_SECUENCIALES_CASA[pasoAudioIdx];
                    if (recordatorioTexto) {
                        this.hablar(recordatorioTexto);
                    }
                }
            }

            // End condition for the clinical timer
            if (this.timeLeft <= 0) {
                clearInterval(this.timerClinico);
                clearTimeout(salidaSugeridaTimeout); // Clear the timeout as well
                window.speechSynthesis.cancel();
                if (circleElement) {
                    circleElement.style.animation = "none";
                    circleElement.style.transform = "scale(1)";
                }
                this.hablar(t.fin);
                this.destruirYReiniciar();
            }
        }, 1000); // Update every second
    },

    /** Advances to the next internal mission step. */
    avanzarPaso() {
        this.indiceMision++;
        const container = document.getElementById('wrapper-interactive');
        this.procesarFlujoSecuencial(container);
    },

    /**
     * Clears session data and restarts the application.
     * Modificado para limpiar las nuevas claves de historial de localStorage.
     */
    destruirYReiniciar() {
        clearInterval(this.timerInaccion);
        clearInterval(this.timerClinico);
        clearInterval(this.temporizadorCascada);
        window.speechSynthesis.cancel();
        this.pasosMisiones = [];
        this.indiceMision = 0;
        this.isLocked = false;
        // Clear all specific history keys from localStorage upon restart
        localStorage.removeItem("otg_historial_salir");
        localStorage.removeItem("otg_historial_casa");
        localStorage.removeItem("otg_historial_oraculo");
        localStorage.removeItem("otg_last_decay");
        localStorage.removeItem("otg_session_seed");
        // Clear old, unused keys for good measure
        localStorage.removeItem("otg_bloque_secuencial");
        // And the old seen_ids key if it somehow persists
        localStorage.removeItem("otg_seen_ids");


        // Reset in-memory lists
        this.historialSalir = [];
        this.historialCasa = [];
        this.historialPreguntas = [];

        location.reload(); // Reload the page to reset the UI
    }
};

// Initialize KERNEL when DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => KERNEL.init());

// Expose KERNEL to global scope for HTML onclick events (e.g., KERNEL.despertarInicial())
window.KERNEL = KERNEL;
