// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.6.0.1
// Company: May Roga LLC
// File: static/engine.js (Frontend Logic)

const KERNEL = {
    timerInaccion: null,
    timerEnfocado: null,
    temporizadorCascada: null,
    temporizadorCierre: null,
    salidaSugeridaTimeoutId: null, // Timer for CASA mode audio phrases
    salidaTimerId: null, // Timer for SALIR mode 45s phrases
    timeLeft: 600, // Initial value for interaction timer (e.g., 10 minutes)
    timeLeftCierre: 60, // Initial value for closure timer (e.g., 60 seconds)
    isLocked: false, // Flag for specific UI lock states
    idiomaActual: 'es',
    pasosMisiones: [], // For CASA mode, holds the sequence of micro-missions
    indiceMision: 0, // Current index in pasosMisiones
    datosLugarGlobal: null, // Stores the *selected* SALIR mission details for eventual display
    tipoEscapeGlobal: "", // "CASA" or "SALIR"

    contadorToques: 0, // Not explicitly used yet, but kept for future expansion.
    secuenciaAdelantos: [5, 7, 9, 10, 14, 16, 17, 19, 21, 5], // For CASA mode audio timing

    historialSalir: [],
    historialCasa: [],
    historialPreguntas: [],
    historialRetosSecuencias: [], // Tracks sequence of closure challenges

    lastDecayTimestamp: null, // For tracking dynamic profile decay
    sessionSeed: null, // Unique seed for the session

    MAX_HISTORY_SALIR: 5,
    MAX_HISTORY_CASA: 8,
    MAX_HISTORY_ORACULO: 12,
    MAX_HISTORY_RETOS_SECUENCIAS: 3,
    DECAY_PER_DAY: 0.985, // Daily decay rate for necessity profile values

    conteoInaccion: 0, // Tracks inactivity for prompt
    indicePreguntaCascada: 0, // For the cascading question effect

    DEFAULT_NECESSITY_PROFILE: { // Matches main.py for client-side scoring logic (when applicable)
        "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50,
        "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50,
        "juego": 50, "contemplacion": 50, "descanso": 50, "organizacion": 50,
        "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50,
        "indicador_ansiedad": 0
    },

    CATALOGO_PREGUNTAS_ES: [
        // Bloque 1: El Bucle Digital Urbano (Redes, Contenido y Consumo)
        "¿Abres redes sociales por inercia, comparando tu día con imágenes idealizadas?",
        "¿Te pierdes en contenido de video que olvidas en pocos segundos, buscando llenar un vacío?",
        "¿Usas música para ahogar el ruido mental y la inquietud de tu día a día?",
        "¿Sientes que lo digital te desconectó de la capacidad de observar el mundo real en calma?",

        // Bloque 2: Evasión y Rutina Física (Comida, Descanso y Movimiento)
        "¿Invierdes mucho en experiencias pasajeras buscando una satisfacción que se desvanece rápido?",
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
        "¿Sientes que las interacciones diarias están creando silencios en tus relaciones?",

        // Bloque 5: Evasión por Viajes y Fugas de la Realidad
        "¿Subestimas lo que tienes cerca, soñando con escapes lejanos que te son inalcanzables?",
        "¿Deseas una huida total para que el cambio de escenario resuelva tus crisis internas?",
        "¿Crees que la solución a tu insatisfacción es un cambio radical de ubicación?",
        "¿Planeas grandes gastos en ocio que podrían comprometer tu calma futura?",
        "¿Buscas imágenes de paisajes distantes porque perdiste la capacidad de asombrarte con tu propio cielo?",
        "¿Te sientes atado a tu lugar y asumes que la libertad requiere de un boleto a otro sitio?",

        // Bloque 6: Vulnerabilidad Corporal y Sensaciones
        "¿Aplazas tu bienestar físico por miedo a los costos o las complicaciones?",
        "¿Sientes molestias en el cuerpo causadas por la acumulación de tensión diaria?",
        "¿Sientes opresión en el pecho por la prisa del entorno y la incertidumbre del futuro?",
        "¿Has olvidado el consuelo de una respiración profunda, libre de cualquier preocupación?",

        // Bloque 7: El Espejismo Material y Vacío Existencial
        "¿Buscas la tranquilidad en un entorno natural, pero tu mente sigue en el bucle de las preocupaciones?",
        "¿Tienes comodidades, pero una insatisfacción crónica te consume por dentro?",
        "¿Crees que la adquisición de bienes te dará un sentido de pertenencia o identidad?",
        "¿Te paraliza la idea de dejar la seguridad de lo conocido, por miedo a un paso incierto?",
        "¿Te comparas con las posesiones y el estilo de vida de los demás?",

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
        "Does longing for those far away paralyze you and prevent you to live your present?",
        "Do you feel that daily interactions are creating silences in your relationships?",

        // Block 5: Travel Evasion and Escapes from Reality
        "Do you underestimate what's near you, dreaming of distant escapes that are unattainable?",
        "Do you wish for a total escape so that a change of scenery resolves your internal crises?",
        "Do you believe that the solution to your dissatisfaction is a radical change of location?",
        "Do you plan large expenses on leisure that could compromise your future calm?",
        "Do you search for images of distant landscapes because you've lost the ability to be amazed by your own sky?",
        "Do you feel tied to your place and assume that freedom requires a ticket to another location?",

        // Block 6: Bodily Vulnerability and Sensations
        "Do you postpone your physical well-being for fear of costs or complications?",
        "Do you feel physical discomfort caused by the accumulation of daily tension?",
        "Do you feel tightness in your chest from the rush of your environment and the uncertainty of the future?",
        "Have you forgotten the comfort of a deep breath, free from any worry?",

        // Block 7: The Material Mirage and Existential Void
        "Do you seek tranquility in a natural environment, but your mind remains in the loop of worries?",
        "Do you have comforts but a chronic dissatisfaction consumes you within?",
        "Do you believe that acquiring property will give you a sense of belonging or identity?",
        "Does the idea of leaving the security of the known paralyze you, for fear of an uncertain step?",
        "Do you secretly compare yourself to the status and possessions of others?",

        // Block 8: The Master Awakening (Breakthrough and Absolute Command)
        "Has your mind become your biggest prison right now?",
        "Do you want to help your family be better but are paralyzed by not knowing how to start?",
        "Are you tired of repeating patterns that consume your freedom and energy?",
        "Do you feel like you are losing your best years waiting for a miracle that won't come?",
        "Is it hard for you to believe there's a free space in your area capable of restoring your hope?",
        "Are you ready to obey the command, let go of your indecisions, and break free from your mental imprisonment today?"
    ],

    AUDIOS_SECUENCIALES_CASA_ES: [
        "Sigue el pulso en tu pantalla. Concéntrate. Estás conmigo hoy.",
        "Suelta los hombros despacio. Deja caer todo el peso físico y mental de tu día.",
        "No pienses en pendientes ahora. No mires tu lista mental. Respira ya.",
        "Mantén el ritmo constante. Siente el aire fresco limpiando tu pecho.",
        "Te estoy acompañando en silencio. No estás solo en esta habitación.",
        "Siente tus pies firmes apoyados en el suelo. La tierra te sostiene gratis.",
        "El piloto automático está apagado en este segundo. Continúa así.",
        "Quédate justo en este instante. El pasado ya pasó, el presente es tuyo.",
        "Suelta la mandíbula ahora. Libera esa carga que aprietas sin darte cuenta.",
        "Tu mente está despertando poco a poco. Estás ganando control real.",
        "Eres mucho más grande que tus preocupaciones. Respira hondo y despacio.",
        "Rompe el bucle que el ruido externo quiere que seas. Quédate en la sala conmigo.",
        "Escucha mi voz. Nota cómo tu respiración se vuelve más profunda y limpia.",
        "Tus ojos están descansando finalmente de las luces artificiales de la pantalla.",
        "Siente los latidos de tu pecho. Es tu motor vivo latiendo para ti.",
        "Siente el peso fuera de tu espalda. Imagina que dejas caer el cansancio.",
        "No dejes que los pensamientos rápidos te saquen de este momento de paz.",
        "Abandona la prisa de la ciudad hoy. Aquí el tiempo es tuyo.",
        "Tu calma regresará, pero este segundo de paz no se repite.",
        "Siente cómo tus pulmones se llenan de fuerza con cada ciclo de aire azul.",
        "Tu familia necesita que estés fuerte por dentro. Recupérate ahora.",
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
        "Slowly relax your shoulders. Let all the physical and mental weight of your day fall away.",
        "Don't think about pending tasks now. Don't look at your mental list. Breathe now.",
        "Maintain a constant rhythm. Feel the fresh air cleansing your chest.",
        "I am accompanying you in silence. You are not alone in this room.",
        "Feel your feet firmly on the ground. The earth supports you for free.",
        "The autopilot is off this second. Keep going.",
        "Stay right in this instant. The past is gone, the present is yours.",
        "Release your jaw now. Let go of that tension you hold without realizing.",
        "Your mind is slowly awakening. You are gaining real control.",
        "You are much bigger than your worries. Breathe deeply and slowly.",
        "Break the loop the external noise wants you to be. Stay in the room with me.",
        "Listen to my voice. Notice how your breathing becomes deeper and cleaner.",
        "Your eyes are finally resting from the artificial lights of the screen.",
        "Feel your heartbeat. It's your living engine beating for you.",
        "Feel the weight off your back. Imagine shaking off tiredness.",
        "Don't let racing thoughts take you out of this peaceful moment.",
        "Abandon the city's rush today. Here, time is yours.",
        "Your calm will return, but this second of peace will not repeat.",
        "Feel your lungs fill with strength with each cycle of blue air.",
        "Your family needs you to be strong inside. Recover now.",
        "You are erasing the day's noise. Stay in the room breathing with me.",
        "The daily routine is broken. You govern your decisions at this instant.",
        "The ground is firm beneath you. Feel the stability of the earth.",
        "Your chest is free from worries now. Expel all negativity at once.",
        "You are regaining your biopsychosocial center. Follow the light of the circle.",
        "Your mind is strong. You have tamed the fear of today's pressures.",
        "Only a few seconds left for the definitive reset. Feel the hope.",
        "You are completely safe here. Remain in absolute peace this second."
    ],

    // NEW AUDIOS_SECUENCIALES for SALIR mode (45-second phrase injection)
    AUDIOS_SECUENCIALES_SALIR_ES: [
        "Respira hondo. El mundo exterior espera, pero tú controlas tu paz.",
        "Cada segundo es una oportunidad para soltar lo que no te sirve.",
        "Visualiza tu destino. Siente la libertad de ir hacia él con propósito.",
        "Elige tu camino. No hay errores, solo nuevas rutas de bienestar.",
        "Estás en control. Tu decisión te guía a un nuevo espacio de calma.",
        "Siente la expectativa. La aventura te espera, sin agobios ni prisa.",
        "Estás a punto de romper el patrón. Un nuevo aire te revitaliza.",
        "Concéntrate en el momento. Tu mente es libre para explorar y disfrutar.",
        "Suelta las cadenas mentales. Tu cuerpo te pide movimiento y libertad.",
        "Estás eligiendo tu bienestar. Cada paso es un acto de amor propio."
    ],
    AUDIOS_SECUENCIALES_SALIR_EN: [
        "Breathe deeply. The outside world waits, but you control your peace.",
        "Every second is an opportunity to release what doesn't serve you.",
        "Visualize your destination. Feel the freedom of moving towards it with purpose.",
        "Choose your path. There are no mistakes, only new routes to well-being.",
        "You are in control. Your decision guides you to a new space of calm.",
        "Feel the anticipation. Adventure awaits you, without worries or rush.",
        "You are about to break the pattern. A fresh air revitalizes you.",
        "Focus on the moment. Your mind is free to explore and enjoy.",
        "Release mental chains. Your body craves movement and freedom.",
        "You are choosing your well-being. Every step is an act of self-love."
    ],

    // Audio script for the conceptual driving contingency mode
    AUDIOS_CONDUCCION_ES: "Atención. OPEN THAN GO ha bloqueado tu pantalla por tu seguridad física. Estás manejando en una de las carreteras interestatales de los Estados Unidos, una infraestructura de asfalto diseñada para mover cuerpos de forma mecánica. Tu cuerpo viaja a alta velocidad, pero tu mente está atrapada en una prisión mental de monotonía o estrés. No mires este teléfono. Mantén tus ojos fijos en el camino. Hackea este trayecto mediante el Módulo de Ventilación Pasiva en este mismo instante: inhala profundamente por la nariz expandiendo tu caja torácica, retén el aire sintiendo los latidos de tu corazón, y exhala de forma lenta y prolongada por la boca vaciando el dióxido de carbono acumulado en tu torrente sanguíneo. Utiliza el volante y el asiento como anclas táctiles de presencia. Observa la inmensidad de las nubes, el cielo o la luna sobre el horizonte sin perder la concentración en la vía. Estás en control de tu vida, no del tráfico. Has transformado esta autopista en tu pista de descompresión cerebral a costo cero. Ejecución pasiva activada.",
    AUDIOS_CONDUCCION_EN: "Attention. OPEN THAN GO has locked your screen for your physical safety. You are driving on one of the interstate highways of the United States, an asphalt infrastructure designed to move bodies mechanically. Your body travels at high speed, but your mind is trapped in a mental prison of monotony or stress. Do not look at this phone. Keep your eyes fixed on the road. Hack this journey through the Passive Ventilation Module right now: inhale deeply through your nose expanding your rib cage, hold your breath feeling your heart beat, and exhale slowly and prolonged through your mouth emptying the accumulated carbon dioxide in your bloodstream. Use the steering wheel and seat as tactile anchors of presence. Observe the vastness of the clouds, the sky, or the moon over the horizon without losing concentration on the road. You are in control of your life, not the traffic. You have transformed this highway into your brain decompression track at zero cost. Passive execution activated.",


    // NUEVO CATÁLOGO DE RETOS DE CIERRE (Microacciones de Recuperación Mental)
    CATALOGO_RETOS_ES: [
        {"id": 201, "titulo": "EL RETO DE LA SUSCRIPCIÓN OLVIDADA", "descripcion": "Abre tu correo o tu aplicación bancaria. Busca 'Subscription', 'Invoice' o 'Payment' y cancela una sola suscripción que ya no utilices. Recuperar el control también es ahorrar.", "img": "gratitude.svg"},
        {"id": 202, "titulo": "EL RETO DE LOS TRES GASTOS", "descripcion": "Abre una nota en tu teléfono y escribe únicamente los tres gastos inevitables de esta semana. No pienses en todo el mes. Solo en esta semana.", "img": "words.svg"},
        {"id": 203, "titulo": "EL RETO DEL ORDEN DIGITAL", "descripcion": "Borra veinte capturas de pantalla, archivos o documentos que ya no necesites. El orden digital también reduce la carga mental.", "img": "observe.svg"},
        {"id": 204, "titulo": "EL RETO DEL SILENCIO", "descripcion": "Silencia durante una hora las aplicaciones que más ansiedad te generan. Tu atención también necesita descansar.", "img": "silence.svg"},
        {"id": 205, "titulo": "EL RETO DE LA GRATITUD", "descripcion": "Escribe tres cosas que hoy tienes y que hace algunos años deseabas. Tu mente necesita recordar que también has avanzado.", "img": "gratitude.svg"},
        {"id": 206, "titulo": "EL RETO DEL AGUA", "descripcion": "Levántate despacio, bebe un vaso completo de agua y vuelve respirando con calma.", "img": "stretch.svg"},
        {"id": 207, "titulo": "EL RETO DE LA VENTANA", "descripcion": "Abre una ventana durante dos minutos y observa el cielo sin mirar el teléfono.", "img": "nature_sound.svg"},
        {"id": 208, "titulo": "EL RETO DEL ORDEN", "descripcion": "Guarda únicamente cinco objetos que estén fuera de lugar. Cinco son suficientes por hoy.", "img": "observe.svg"},
        {"id": 209, "titulo": "EL RETO DE LA RESPIRACIÓN", "descripcion": "Realiza cinco respiraciones profundas siguiendo un ritmo lento. No tienes que hacer nada más.", "img": "square_breath.svg"},
        {"id": 210, "titulo": "EL RETO DEL DESCANSO VISUAL", "descripcion": "Durante dos minutos mira un punto lejano para permitir que tus ojos descansen de la pantalla.", "img": "nature_sound.svg"},
    ],
    CATALOGO_RETOS_EN: [
        {"id": 201, "titulo": "THE FORGOTTEN SUBSCRIPTION CHALLENGE", "descripcion": "Open your email or banking app. Search for 'Subscription', 'Invoice', or 'Payment' and cancel a single subscription you no longer use. Regaining control is also saving.", "img": "gratitude.svg"},
        {"id": 202, "titulo": "THE THREE EXPENSES CHALLENGE", "descripcion": "Open a note on your phone and write down only the three unavoidable expenses for this week. Don't think about the whole month. Just this week.", "img": "words.svg"},
        {"id": 203, "titulo": "THE DIGITAL ORDER CHALLENGE", "descripcion": "Delete twenty screenshots, files, or documents you no longer need. Digital order also reduces mental load.", "img": "observe.svg"},
        {"id": 204, "titulo": "THE SILENCE CHALLENGE", "descripcion": "Silence the apps that generate the most anxiety for an hour. Your attention also needs rest.", "img": "silence.svg"},
        {"id": 205, "titulo": "THE GRATITUDE CHALLENGE", "descripcion": "Write down three things you have today that you wished for a few years ago. Your mind needs to remember that you have also made progress.", "img": "gratitude.svg"},
        {"id": 206, "titulo": "THE WATER CHALLENGE", "descripcion": "Slowly stand up, drink a full glass of water, and return, breathing calmly.", "img": "stretch.svg"},
        {"id": 207, "titulo": "THE WINDOW CHALLENGE", "descripcion": "Open a window for two minutes and observe the sky without looking at your phone.", "img": "nature_sound.svg"},
        {"id": 208, "titulo": "THE ORDER CHALLENGE", "descripcion": "Put away only five objects that are out of place. Five are enough for today.", "img": "observe.svg"},
        {"id": 209, "titulo": "THE BREATHING CHALLENGE", "descripcion": "Take five deep breaths following a slow rhythm. You don't have to do anything else.", "img": "square_breath.svg"},
        {"id": 210, "titulo": "THE VISUAL REST CHALLENGE", "descripcion": "For two minutes, look at a distant point to allow your eyes to rest from the screen.", "img": "nature_sound.svg"},
    ],

    /**
     * Retrieves or initializes the user's dynamic profile from localStorage.
     * Ensures all 19 needs are present with default values if missing.
     * Applies gradual daily reduction (decay) towards base values.
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

        const now = Date.now();
        let lastDecayTimestamp = parseInt(localStorage.getItem("otg_last_decay") || now);
        this.sessionSeed = localStorage.getItem("otg_session_seed") || Math.random().toString(36).substring(2, 15);

        const daysPassed = (now - lastDecayTimestamp) / (1000 * 60 * 60 * 24);

        if (daysPassed >= 1) {
            const newPerfil = {};
            const base = 50;
            for (const necesidad in perfil) {
                if (necesidad === "indicador_ansiedad") {
                    newPerfil[necesidad] = Math.max(0, perfil[necesidad] - (daysPassed * 2));
                    continue;
                }
                const valor = perfil[necesidad];
                let diferencia = valor - base;
                diferencia *= (this.DECAY_PER_DAY ** daysPassed);
                newPerfil[necesidad] = Math.round((base + diferencia) * 100) / 100;
            }
            perfil = newPerfil;
            lastDecayTimestamp = now;
        }

        perfil.fecha = new Date(now).toISOString().split('T')[0];
        perfil.timestamp = now;

        localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
        localStorage.setItem("otg_last_decay", lastDecayTimestamp.toString());
        localStorage.setItem("otg_session_seed", this.sessionSeed);

        return perfil;
    },

    /** Initializes the KERNEL on DOMContentLoaded. */
    init() {
        const storedLang = localStorage.getItem("otg_language");
        if (storedLang) {
            this.idiomaActual = storedLang;
            this.cambiarIdioma(storedLang); // Apply stored language immediately
        } else {
            localStorage.setItem("otg_language", this.idiomaActual);
        }
        try {
            this.historialSalir = JSON.parse(localStorage.getItem("otg_historial_salir") || "[]");
            this.historialCasa = JSON.parse(localStorage.getItem("otg_historial_casa") || "[]");
            this.historialPreguntas = JSON.parse(localStorage.getItem("otg_historial_oraculo") || "[]");
            this.historialRetosSecuencias = JSON.parse(localStorage.getItem("otg_historial_retos_secuencias") || "[]");
        } catch (e) {
            console.error("Error parsing history from localStorage, resetting specific histories.", e);
            this.historialSalir = [];
            this.historialCasa = [];
            this.historialPreguntas = [];
            this.historialRetosSecuencias = [];
            localStorage.removeItem("otg_historial_salir");
            localStorage.removeItem("otg_historial_casa");
            localStorage.removeItem("otg_historial_oraculo");
            localStorage.removeItem("otg_historial_retos_secuencias");
        }
        this.obtenerPerfilLocal();

        const zipInput = document.getElementById('inp-zip');
        if (zipInput) {
            zipInput.addEventListener('input', () => this.validarZip());
        }
        document.getElementById('modo-selector').addEventListener('change', () => this.activarBotonMandoLibreInicial());
        document.getElementById('mente-selector').addEventListener('change', () => this.reiniciarExperiencia());
        document.getElementById('budget-selector').addEventListener('change', () => this.reiniciarExperiencia());
        document.getElementById('perfil-selector').addEventListener('change', () => this.reiniciarExperiencia());

        document.getElementById('btn-volver-app').addEventListener('click', () => this.reiniciarExperiencia());
        
        // Initial setup for floating buttons after KERNEL.init
        this.toggleFloatingButtons(true);
    },

    /** Starts the initial welcome sequence after user interaction. */
    despertarInicial() {
        document.getElementById('pantalla-bienvenida').classList.add('hidden');
        document.getElementById('wrapper-form').classList.remove('hidden');
        this.toggleFloatingButtons(true); // Show floating buttons
       
        this.cambiarIdioma(this.idiomaActual); // Ensure all UI text is updated
       
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
       
        this.inyectarBloquePreguntas();
        this.iniciarMonitoreoInaccion();
       
        this.activarBotonMandoLibreInicial();
        window.OTG_SENSORIAL.resetAutodestruccion(); // Reset autodestrucción timer on initial interaction
    },

    /**
     * Toggles visibility of floating action buttons.
     * @param {boolean} show - True to show, false to hide.
     */
    toggleFloatingButtons(show) {
        document.getElementById('btn-volver-app').classList.toggle('hidden', !show);
        document.getElementById('btn-whatsapp').classList.toggle('hidden', !show);
        document.getElementById('btn-messenger').classList.toggle('hidden', !show);
        document.getElementById('otg-power-button').classList.toggle('otg-hidden', !show);
    },

    /**
     * Injects a block of 6 questions into the UI, ensuring they are distinct and not recent.
     */
    inyectarBloquePreguntas() {
        const grid = document.getElementById('contenedor-preguntas-oraculo');
        if (!grid) return;
       
        clearInterval(this.temporizadorCascada); // Clear previous cascade timer if any
        grid.innerHTML = "";
        this.indicePreguntaCascada = 0;
       
        const catalogo = this.idiomaActual === 'es' ? this.CATALOGO_PREGUNTAS_ES : this.CATALOGO_PREGUNTAS_EN;
        let preguntasYaVistasRecientemente = new Set(this.historialPreguntas);

        let unseenIndices = [];
        for (let i = 0; i < catalogo.length; i++) {
            if (!preguntasYaVistasRecientemente.has(i)) {
                unseenIndices.push(i);
            }
        }

        if (unseenIndices.length < 6) {
            console.warn("Not enough unseen questions. Resetting Oracle history.");
            this.historialPreguntas = []; // Reset history for more questions
            localStorage.removeItem("otg_historial_oraculo");
            unseenIndices = Array.from({length: catalogo.length}, (_, i) => i);
        }
       
        // Shuffle unseen indices
        for (let i = unseenIndices.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [unseenIndices[i], unseenIndices[j]] = [unseenIndices[j], unseenIndices[i]];
        }

        let preguntasSeleccionadasIndices = [];
        let blocksUsedInCurrentSelection = new Set(); // To ensure block diversity

        // Try to pick 6 questions, prioritizing block diversity
        for (let i = 0; i < 6; i++) {
            if (unseenIndices.length === 0) break;

            let candidateIndexInUnseen = -1;
            for (let j = 0; j < unseenIndices.length; j++) {
                const currentIdx = unseenIndices[j];
                const currentBlock = Math.floor(currentIdx / 6); // Each block has 6 questions
                if (!blocksUsedInCurrentSelection.has(currentBlock)) {
                    candidateIndexInUnseen = j;
                    blocksUsedInCurrentSelection.add(currentBlock);
                    break;
                }
            }

            if (candidateIndexInUnseen === -1) {
                // If no diverse block found, just take the first available
                candidateIndexInUnseen = 0;
                const currentBlock = Math.floor(unseenIndices[candidateIndexInUnseen] / 6);
                blocksUsedInCurrentSelection.add(currentBlock);
            }
           
            const selectedIndex = unseenIndices.splice(candidateIndexInUnseen, 1)[0];
            preguntasSeleccionadasIndices.push(selectedIndex);
           
            this.historialPreguntas.push(selectedIndex);
        }
        this.historialPreguntas = this.historialPreguntas.slice(-this.MAX_HISTORY_ORACULO);
        localStorage.setItem("otg_historial_oraculo", JSON.stringify(this.historialPreguntas));

        preguntasSeleccionadasIndices.forEach((questionIdx, i) => {
            let preguntaTexto = catalogo[questionIdx];
            if (!preguntaTexto) return;

            let btn = document.createElement('button');
            btn.className = 'btn-pregunta-crisis';
            btn.id = `btn-pregunta-${i}`;
            btn.innerText = `${i + 1}. ${preguntaTexto}`;
            btn.onclick = () => this.reaccionarPreguntaSeleccionada(preguntaTexto);
            grid.appendChild(btn);
        });

        this.iniciarEfectoCascada();
    },

    /** Initiates the fading cascade effect for questions. */
    iniciarEfectoCascada() {
        this.indicePreguntaCascada = 0;
       
        const totalButtons = document.querySelectorAll('.btn-pregunta-crisis').length;
        if (totalButtons === 0) {
            this.activarBotonMandoLibreInicial(); // If no questions, ensure free writing is active
            return;
        }

        const firstButton = document.getElementById(`btn-pregunta-0`);
        if (firstButton) {
            let textoLimpio = firstButton.innerText.substring(3); // Remove the "1. " prefix
            this.hablar(textoLimpio);
        }

        // Use a shorter interval for the cascade if there are many questions, or just start it
        // The current 8s interval is good for user to read and listen.
        this.temporizadorCascada = setInterval(() => {
            let botonParaEliminar = document.getElementById(`btn-pregunta-${this.indicePreguntaCascada}`);
           
            if (botonParaEliminar) {
                botonParaEliminar.classList.add('fade-out');
               
                this.indicePreguntaCascada++;
                let siguienteBoton = document.getElementById(`btn-pregunta-${this.indicePreguntaCascada}`);
                if (siguienteBoton) {
                    let textoLimpio = siguienteBoton.innerText.substring(3); // Remove the index prefix
                    this.hablar(textoLimpio);
                } else {
                    clearInterval(this.temporizadorCascada);
                    this.temporizadorCascada = null; // Clear reference for RAM
                    this.activarBotonMandoLibreInicial();
                }
            } else {
                clearInterval(this.temporizadorCascada);
                this.temporizadorCascada = null; // Clear reference for RAM
                this.activarBotonMandoLibreInicial();
            }
        }, 8000); // 8 seconds per question
    },

    /** Activates the free writing input field and button, manages its state. */
    activarBotonMandoLibreInicial() {
        const textarea = document.getElementById('inp-text-libre');
        const btnLibre = document.getElementById('btn-activar-libre');
        const lblDesahogo = document.getElementById('lbl-desahogo');
        const instruccion = document.getElementById('lbl-oraculo-instruccion');
        const zipInput = document.getElementById('inp-zip');

        if (instruccion) {
            instruccion.innerText = this.idiomaActual === 'es' ? "¿Qué te tiene atrapado hoy?" : "What has you trapped today?";
            instruccion.style.color = "var(--accent)";
        }
        if (lblDesahogo) lblDesahogo.style.color = "#666";

        const updateButtonState = () => {
            const isZipInvalid = zipInput && zipInput.value.trim().length > 0 && !zipInput.checkValidity();
            const isTextareaEmpty = textarea.value.trim().length <= 3;
            const modo = document.getElementById('modo-selector').value;

            // Mando Libre always requires a zip code if modo is SALIR
            const requiresZip = modo === 'SALIR';

            if (isZipInvalid || (requiresZip && zipInput.value.trim().length === 0) || isTextareaEmpty) {
                btnLibre.style.background = "#111";
                btnLibre.style.color = "#555";
                btnLibre.style.borderColor = "#222";
                btnLibre.disabled = true;
            } else {
                btnLibre.style.background = "var(--green-action)";
                btnLibre.style.color = "#fff";
                btnLibre.style.borderColor = "var(--green-action)";
                btnLibre.disabled = false;
            }
        };

        if (btnLibre) {
            btnLibre.onclick = () => {
                let textoEscrito = textarea.value.trim();
                const isZipInvalidOnSubmit = zipInput && zipInput.value.trim().length > 0 && !zipInput.checkValidity();
                const modo = document.getElementById('modo-selector').value;
                const requiresZip = modo === 'SALIR';

                if (requiresZip && zipInput.value.trim().length === 0) {
                    this.hablar(this.idiomaActual === 'es' ? "Por favor, introduce tu código postal para el modo SALIR." : "Please enter your ZIP code for SALIR mode.");
                    zipInput.focus();
                    return;
                }
                if (isZipInvalidOnSubmit) {
                    this.hablar(this.idiomaActual === 'es' ? "Por favor, introduce un código postal válido." : "Please enter a valid ZIP code.");
                    zipInput.focus();
                    return;
                }
                if (textoEscrito.length > 3) {
                    this.reaccionarPreguntaSeleccionada(textoEscrito);
                } else {
                    this.hablar(this.idiomaActual === 'es' ? "Escribe tu problema en el cuadro antes de activar el mando." : "Write your problem in the box before activating control.");
                }
            };
        }
        if (textarea) {
            // Remove previous listener to prevent duplicates
            textarea.removeEventListener('input', this.textareaInputHandler);
            this.textareaInputHandler = () => {
                updateButtonState();
                this.validarZip(); // Also call zip validation on text input
                window.OTG_SENSORIAL.resetAutodestruccion(); // User activity
            };
            textarea.addEventListener('input', this.textareaInputHandler);
        }
        if (zipInput) {
            zipInput.removeEventListener('input', this.zipInputHandler);
            this.zipInputHandler = () => {
                this.validarZip(); // Visual feedback for zip
                updateButtonState(); // Update button state
                window.OTG_SENSORIAL.resetAutodestruccion(); // User activity
            };
            zipInput.addEventListener('input', this.zipInputHandler);
        }
        // Initial state update
        updateButtonState();
        this.validarZip(); // Initial visual feedback for zip
    },

    /** Validates ZIP input and controls button state visually */
    validarZip() {
        const zipInput = document.getElementById('inp-zip');
        if (!zipInput) return;

        const zipValue = zipInput.value.trim();
        const isValidZip = zipInput.checkValidity();

        if (zipValue.length > 0 && !isValidZip) {
            zipInput.style.borderColor = "var(--accent)";
        } else {
            zipInput.style.borderColor = "#222";
        }
    },

    /** Responds to a user selecting an oracle question or typing in free text. */
    reaccionarPreguntaSeleccionada(preguntaTexto) {
        window.OTG_SENSORIAL.resetAutodestruccion(); // User activity
        clearInterval(this.temporizadorCascada); // Stop the cascade effect
        this.temporizadorCascada = null; // Clear reference for RAM

        this.isLocked = true; // Lock UI for processing
        document.getElementById('wrapper-form').classList.add('hidden'); // Hide input form
        document.getElementById('wrapper-interactive').classList.remove('hidden'); // Show interactive output area
        document.getElementById('wrapper-interactive').innerHTML = ''; // Clear previous content

        this.hablar(this.idiomaActual === 'es' ? "Pensando una solución..." : "Thinking of a solution...");
        
        const modo = document.getElementById('modo-selector').value;
        const zip = document.getElementById('inp-zip').value;
        const mente = document.getElementById('mente-selector').value;
        const budget = document.getElementById('budget-selector').value;
        const perfilTipo = document.getElementById('perfil-selector').value;

        // Update anxiety indicator based on interaction (simple example)
        let perfilLocal = this.obtenerPerfilLocal();
        perfilLocal.indicador_ansiedad = Math.min(100, perfilLocal.indicador_ansiedad + 10); // Increase anxiety on interaction
        localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfilLocal));

        this.llamarBackend({
            modo: modo,
            zip: zip,
            estado: "FL", // Placeholder, not used in main.py currently for direct query
            region: "",  // Placeholder
            mente: mente,
            budget: budget,
            perfil: perfilTipo,
            desahogo: preguntaTexto,
            lang: this.idiomaActual,
            perfil_local: perfilLocal,
            historial_salir: this.historialSalir,
            historial_casa: this.historialCasa
        });
    },

    /** Makes an API call to the backend. */
    async llamarBackend(payload) {
        try {
            const response = await fetch('/api/mando-integral', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Backend error:', errorData);
                this.hablar(this.idiomaActual === 'es' ? "Error del sistema. Intenta de nuevo." : "System error. Please try again.");
                this.reiniciarExperiencia();
                return;
            }

            const data = await response.json();
            this.procesarRespuestaBackend(data);

        } catch (error) {
            console.error('Network or API call error:', error);
            this.hablar(this.idiomaActual === 'es' ? "Error de conexión. Revisa tu internet." : "Connection error. Check your internet.");
            this.reiniciarExperiencia();
        }
    },

    /** Processes the response received from the backend. */
    procesarRespuestaBackend(data) {
        window.OTG_SENSORIAL.resetAutodestruccion(); // User activity

        // Update local histories
        if (data.historial_salir_actualizado) {
            this.historialSalir = data.historial_salir_actualizado;
            localStorage.setItem("otg_historial_salir", JSON.stringify(this.historialSalir));
        }
        if (data.historial_casa_actualizado) {
            this.historialCasa = data.historial_casa_actualizado;
            localStorage.setItem("otg_historial_casa", JSON.stringify(this.historialCasa));
        }

        const wrapperInteractive = document.getElementById('wrapper-interactive');
        wrapperInteractive.innerHTML = ''; // Clear previous content

        if (data.DIRECCIONAMIENTO_MASTER === "ACCION_CAMPO") {
            if (data.forced_recovery) {
                // This is a special "HACKEO" mission for detected brands
                this.iniciarMisionHackeo(data.misiones[0]);
            } else {
                // Regular SALIR mode with multiple mission options
                this.iniciarSalidaMisiones(data.misiones);
            }
        } else if (data.DIRECCIONAMIENTO_MASTER === "INTERVENCION_DOMESTICA") {
            // CASA mode missions
            this.pasosMisiones = data.misiones; // Backend sends an array of missions
            this.indiceMision = 0;
            this.iniciarMisionCasa();
        } else {
            console.error("Tipo de direccionamiento desconocido:", data.DIRECCIONAMIENTO_MASTER);
            this.hablar(this.idiomaActual === 'es' ? "No sé qué hacer. Reiniciando." : "Unknown directive. Restarting.");
            this.reiniciarExperiencia();
        }
    },

    /** Initiates CASA mode micro-missions sequence. */
    iniciarMisionCasa() {
        window.OTG_SENSORIAL.resetAutodestruccion(); // User activity
        this.limpiarTimersActivos(); // Clear any existing timers
        document.getElementById('wrapper-form').classList.add('hidden');
        document.getElementById('wrapper-interactive').classList.remove('hidden');

        // Reset timer and lung animation for each CASA mission
        document.getElementById('wrapper-interactive').innerHTML = `
            <div class="mision-card">
                <small id="txt-card-small"></small>
                <h2 id="txt-mision-titulo"></h2>
                <div id="breath-circle"></div>
                <div id="timer">00</div>
                <p id="txt-pulmon"></p>
                <p class="instruccion-text" id="txt-mision-instruccion"></p>
            </div>
        `;
        this.mostrarMisionCasaActual();
    },

    /** Displays the current CASA mission. */
    mostrarMisionCasaActual() {
        if (this.indiceMision >= this.pasosMisiones.length) {
            this.iniciarCierreConsciente();
            return;
        }

        const misionActual = this.pasosMisiones[this.indiceMision];
        if (!misionActual) {
            console.error("Misión actual no definida:", this.indiceMision, this.pasosMisiones);
            this.iniciarCierreConsciente();
            return;
        }

        document.getElementById('txt-card-small').innerText = this.idiomaActual === 'es' ? "Misión Doméstica" : "Home Mission";
        document.getElementById('txt-mision-titulo').innerText = misionActual.titulo;
        document.getElementById('txt-mision-instruccion').innerText = misionActual.descripcion;

        this.timeLeft = 600; // 10 minutes for focused mission
        this.hablar(misionActual.descripcion);
        this.iniciarContadorMisionCasa();
        this.iniciarAudioSecuencialCasa();
    },

    /** Starts the countdown for CASA mission. */
    iniciarContadorMisionCasa() {
        const timerDisplay = document.getElementById('timer');
        if (!timerDisplay) return;

        clearInterval(this.timerEnfocado);
        timerDisplay.style.color = '#fff';
        document.getElementById('breath-circle').style.animationPlayState = 'running';

        this.timerEnfocado = setInterval(() => {
            window.OTG_SENSORIAL.resetAutodestruccion(); // User activity every second
            const minutes = Math.floor(this.timeLeft / 60);
            const seconds = this.timeLeft % 60;
            timerDisplay.innerText = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

            if (this.timeLeft <= 0) {
                clearInterval(this.timerEnfocado);
                this.timerEnfocado = null;
                this.avanzarMisionCasa();
            }
            this.timeLeft--;
        }, 1000);
    },

    /** Manages the sequential audio prompts for CASA mode. */
    iniciarAudioSecuencialCasa() {
        clearInterval(this.salidaSugeridaTimeoutId);
        let audioIndex = 0;
        const audios = this.idiomaActual === 'es' ? this.AUDIOS_SECUENCIALES_CASA_ES : this.AUDIOS_SECUENCIALES_CASA_EN;
        const txtPulmon = document.getElementById('txt-pulmon');
        if (!txtPulmon) return;

        txtPulmon.innerText = audios[audioIndex];
        this.hablar(audios[audioIndex]);
        audioIndex++;

        this.salidaSugeridaTimeoutId = setInterval(() => {
            window.OTG_SENSORIAL.resetAutodestruccion(); // User activity
            if (audioIndex < audios.length) {
                txtPulmon.innerText = audios[audioIndex];
                this.hablar(audios[audioIndex]);
                audioIndex++;
            } else {
                audioIndex = 0; // Loop audio suggestions
            }
        }, 8000); // New audio every 8 seconds for CASA
    },

    /** Moves to the next CASA mission or ends the session. */
    avanzarMisionCasa() {
        window.OTG_SENSORIAL.resetAutodestruccion(); // User activity
        this.indiceMision++;
        if (this.indiceMision < this.pasosMisiones.length) {
            this.mostrarMisionCasaActual();
        } else {
            this.iniciarCierreConsciente();
        }
    },

    /** Initiates the special "HACKEO" mission display (for forced recovery). */
    iniciarMisionHackeo(mision) {
        window.OTG_SENSORIAL.resetAutodestruccion(); // User activity
        this.limpiarTimersActivos(); // Clear all existing timers
        document.getElementById('wrapper-form').classList.add('hidden');
        document.getElementById('wrapper-interactive').classList.remove('hidden');

        const interactiveWrapper = document.getElementById('wrapper-interactive');
        interactiveWrapper.innerHTML = `
            <div class="mision-card" style="text-align: center;">
                <h3 style="color: var(--accent); font-size: 1.6rem;">${this.idiomaActual === 'es' ? mision.destino_titulo : mision.destino_titulo_en}</h3>
                <p class="otg-cyberpunk-text" style="font-size: 1.1rem; color: #00bcd4;">${this.idiomaActual === 'es' ? mision.diagnostico_sintoma_es : mision.diagnostico_sintoma_en}</p>
                <p class="instruccion-text" style="font-size: 1.2rem; color: #eee; border-left-color: var(--cyan-inhale);">
                    ${this.idiomaActual === 'es' ? mision.destino_instruccion : mision.destino_instruccion_en}
                </p>
                <button id="btn-abrir-mapa-hackeo" class="otg-oasis-cta-btn" style="margin-top: 25px; background: var(--secondary);">
                    ${this.idiomaActual === 'es' ? 'ABRIR MAPA' : 'OPEN MAP'}
                </button>
            </div>
        `;
        
        // Voice message for the hackeo mission
        const fullInstruction = this.idiomaActual === 'es' ? mision.destino_instruccion : mision.destino_instruccion_en;
        if (fullInstruction.includes("Atención. OPEN THAN GO ha bloqueado tu pantalla")) { // Driving contingency
            this.isLocked = true;
            document.body.style.pointerEvents = 'none'; // Lock all interaction
            interactiveWrapper.style.filter = 'blur(2px)'; // Visual cue for locked state
            this.hablar(fullInstruction);
            // Hide the open map button temporarily if it's a driving lock.
            document.getElementById('btn-abrir-mapa-hackeo').classList.add('hidden');

            setTimeout(() => { // After 20 seconds, unlock and show map button
                this.isLocked = false;
                document.body.style.pointerEvents = 'auto';
                interactiveWrapper.style.filter = 'none';
                document.getElementById('btn-abrir-mapa-hackeo').classList.remove('hidden');
                this.hablar(this.idiomaActual === 'es' ? "Ahora puedes abrir el mapa y activar tu contraataque." : "You can now open the map and activate your counterattack.");
                window.OTG_SENSORIAL.resetAutodestruccion(); // User activity after lock release
            }, 20000); // Give user 20 seconds to listen/focus while driving

        } else {
            this.hablar(this.idiomaActual === 'es' ? mision.diagnostico_sintoma_es : mision.diagnostico_sintoma_en);
            // After a short delay, read the instruction
            setTimeout(() => {
                this.hablar(this.idiomaActual === 'es' ? mision.destino_instruccion : mision.destino_instruccion_en);
            }, 5000); // 5-second delay before reading instruction
        }
        
        document.getElementById('btn-abrir-mapa-hackeo').addEventListener('click', () => {
            window.OTG_SENSORIAL.resetAutodestruccion(); // User activity
            window.open(mision.destino_coordenadas_gps, '_blank');
            this.hablar(this.idiomaActual === 'es' ? "Mapa abierto. ¡Activa tu contraataque!" : "Map opened. Activate your counterattack!");
            // After opening the map, offer to return to the app or auto-return after a delay
            setTimeout(() => {
                this.reiniciarExperiencia();
            }, 10000); // Auto-return to app after 10 seconds if user doesn't interact further
        });
    },

    /** Initiates display of multiple SALIR missions (3 options). */
    iniciarSalidaMisiones(misiones) {
        window.OTG_SENSORIAL.resetAutodestruccion(); // User activity
        this.limpiarTimersActivos(); // Clear all existing timers
        document.getElementById('wrapper-form').classList.add('hidden');
        document.getElementById('wrapper-interactive').classList.remove('hidden');

        const wrapperInteractive = document.getElementById('wrapper-interactive');
        wrapperInteractive.innerHTML = `
            <div class="cierre-content"> <!-- Reusing cierre-content for styling consistency -->
                <h2 class="salida-main-title">${this.idiomaActual === 'es' ? "3 CAMINOS VARIADOS" : "3 VARIED PATHS"}</h2>
                <p class="salida-choose-instruction">${this.idiomaActual === 'es' ? "Elige el que resuene contigo. O quédate a reflexionar con la APP." : "Choose the one that resonates. Or stay to reflect with the APP."}</p>
                <div class="salida-grid" id="salida-misiones-grid">
                    <!-- Missions will be injected here -->
                </div>
            </div>
        `;

        const grid = document.getElementById('salida-misiones-grid');
        misiones.forEach(mision => {
            const card = document.createElement('div');
            card.className = 'salida-option-card';
            card.innerHTML = `
                <h3 class="salida-option-title">${this.idiomaActual === 'es' ? mision.destino_titulo : mision.destino_titulo_en}</h3>
                <p class="salida-option-desc">${this.idiomaActual === 'es' ? mision.destino_instruccion : mision.destino_instruccion_en}</p>
                <button class="btn-select-salida">${this.idiomaActual === 'es' ? 'VER EN MAPA' : 'SEE ON MAP'}</button>
            `;
            card.querySelector('.btn-select-salida').addEventListener('click', () => {
                window.OTG_SENSORIAL.resetAutodestruccion(); // User activity
                window.open(mision.destino_coordenadas_gps, '_blank');
                this.hablar(this.idiomaActual === 'es' ? `Abriendo mapa para ${mision.destino_titulo}.` : `Opening map for ${mision.destino_titulo_en}.`);
                // After opening the map, offer to return to the app or auto-return after a delay
                setTimeout(() => {
                    this.reiniciarExperiencia();
                }, 10000);
            });
            grid.appendChild(card);
        });

        this.iniciarAudioSecuencialSalir(); // Start audio prompts for SALIR mode
    },

    /** Manages sequential audio prompts for SALIR mode. */
    iniciarAudioSecuencialSalir() {
        clearInterval(this.salidaTimerId);
        let audioIndex = 0;
        const audios = this.idiomaActual === 'es' ? this.AUDIOS_SECUENCIALES_SALIR_ES : this.AUDIOS_SECUENCIALES_SALIR_EN;

        // Immediately speak the first audio if available
        if (audios.length > 0) {
            this.hablar(audios[audioIndex]);
            audioIndex++;
        }

        this.salidaTimerId = setInterval(() => {
            window.OTG_SENSORIAL.resetAutodestruccion(); // User activity
            if (audioIndex < audios.length) {
                this.hablar(audios[audioIndex]);
                audioIndex++;
            } else {
                audioIndex = 0; // Loop audio suggestions
            }
        }, 45000); // New audio every 45 seconds for SALIR
    },

    /** Initiates the conscious closure sequence. */
    iniciarCierreConsciente() {
        window.OTG_SENSORIAL.resetAutodestruccion(); // User activity
        this.limpiarTimersActivos(); // Clear all timers
        document.getElementById('wrapper-interactive').classList.add('hidden');
        document.getElementById('pantalla-cierre').classList.remove('hidden');

        this.timeLeftCierre = 60; // Reset closure timer to 60 seconds

        const retoActual = this.seleccionarRetoCierre();

        document.getElementById('cierre-logo').innerText = "OPEN THAN GO"; // Ensure logo is correct
        document.getElementById('reto-img').src = `/static/logos/${retoActual.img}`;
        document.getElementById('reto-img').classList.remove('hidden');
        document.getElementById('reto-titulo').innerText = retoActual.titulo;
        document.getElementById('reto-titulo').dataset.retoId = retoActual.id; // Store ID for language change
        document.getElementById('reto-descripcion').innerText = retoActual.descripcion;
        document.getElementById('cierre-mensaje-final').classList.add('hidden');
        document.getElementById('btn-recomenzar-experiencia').classList.add('hidden');
        document.getElementById('btn-recomenzar-experiencia').disabled = true;

        this.hablar(this.idiomaActual === 'es' ? `Tu reto es: ${retoActual.titulo}. ${retoActual.descripcion}.` : `Your challenge is: ${retoActual.titulo}. ${retoActual.descripcion}.`);
        this.iniciarContadorCierre();
    },

    /** Selects a closure challenge, ensuring it's not recently repeated. */
    seleccionarRetoCierre() {
        const catalogo = this.idiomaActual === 'es' ? this.CATALOGO_RETOS_ES : this.CATALOGO_RETOS_EN;
        let retosDisponibles = catalogo.filter(reto => !this.historialRetosSecuencias.includes(reto.id));

        if (retosDisponibles.length === 0) {
            this.historialRetosSecuencias = []; // Reset history if all have been shown
            retosDisponibles = catalogo;
        }

        const retoSeleccionado = retosDisponibles[Math.floor(Math.random() * retosDisponibles.length)];
        this.historialRetosSecuencias.push(retoSeleccionado.id);
        this.historialRetosSecuencias = this.historialRetosSecuencias.slice(-this.MAX_HISTORY_RETOS_SECUENCIAS); // Keep only recent history
        localStorage.setItem("otg_historial_retos_secuencias", JSON.stringify(this.historialRetosSecuencias));
        return retoSeleccionado;
    },

    /** Starts the countdown for the closure screen. */
    iniciarContadorCierre() {
        const cierreTimerDisplay = document.getElementById('cierre-timer');
        if (!cierreTimerDisplay) return;

        clearInterval(this.temporizadorCierre);
        cierreTimerDisplay.style.color = 'var(--accent)';

        this.temporizadorCierre = setInterval(() => {
            window.OTG_SENSORIAL.resetAutodestruccion(); // User activity every second
            cierreTimerDisplay.innerText = this.timeLeftCierre.toString().padStart(2, '0');
            if (this.timeLeftCierre <= 0) {
                clearInterval(this.temporizadorCierre);
                this.temporizadorCierre = null;
                document.getElementById('cierre-mensaje-final').innerText = this.idiomaActual === 'es' ? "¡Éxito! Has completado tu pausa consciente." : "Success! You have completed your conscious pause.";
                document.getElementById('cierre-mensaje-final').classList.remove('hidden');
                
                const btnRecomenzar = document.getElementById('btn-recomenzar-experiencia');
                btnRecomenzar.innerText = this.idiomaActual === 'es' ? "REINICIAR EXPERIENCIA" : "RESTART EXPERIENCE";
                btnRecomenzar.classList.remove('hidden');
                btnRecomenzar.disabled = false;
                btnRecomenzar.onclick = () => this.reiniciarExperiencia();
                
                this.hablar(this.idiomaActual === 'es' ? "Éxito. Puedes reiniciar la experiencia." : "Success. You can restart the experience.");
            }
            this.timeLeftCierre--;
        }, 1000);
    },

    /** Resets the application to its initial form state. */
    reiniciarExperiencia() {
        window.OTG_SENSORIAL.hideAllOverlays(); // Hide any OTG_SENSORIAL overlays
        window.OTG_SENSORIAL.resetOasisState(); // Reset Oasis game state
        window.OTG_SENSORIAL.resetAutodestruccion(); // Reset autodestrucción timer

        this.limpiarTimersActivos(); // Clear all KERNEL timers

        this.isLocked = false;
        this.pasosMisiones = [];
        this.indiceMision = 0;
        this.datosLugarGlobal = null;
        this.tipoEscapeGlobal = "";
        this.contadorToques = 0;
        this.conteoInaccion = 0;
        this.indicePreguntaCascada = 0;
        
        document.getElementById('wrapper-form').classList.remove('hidden');
        document.getElementById('wrapper-interactive').classList.add('hidden');
        document.getElementById('pantalla-cierre').classList.add('hidden');
        document.body.style.pointerEvents = 'auto'; // Ensure interaction is re-enabled

        // Clear input fields
        document.getElementById('inp-zip').value = '';
        document.getElementById('inp-text-libre').value = '';

        // Reset selectors to default
        document.getElementById('modo-selector').value = 'SALIR';
        document.getElementById('mente-selector').value = 'aburrido';
        document.getElementById('budget-selector').value = '0';
        document.getElementById('perfil-selector').value = 'solo';

        this.inyectarBloquePreguntas(); // Re-inject new questions
        this.iniciarMonitoreoInaccion(); // Restart inactivity monitor
        this.activarBotonMandoLibreInicial(); // Re-activate free writing button logic
        this.toggleFloatingButtons(true); // Ensure floating buttons are visible
        this.cambiarIdioma(this.idiomaActual); // Reapply language to new elements
    },

    /** Clears all active KERNEL-managed timers and intervals. */
    limpiarTimersActivos() {
        clearInterval(this.timerInaccion);
        clearInterval(this.timerEnfocado);
        clearInterval(this.temporizadorCascada);
        clearInterval(this.temporizadorCierre);
        clearInterval(this.salidaSugeridaTimeoutId);
        clearInterval(this.salidaTimerId);

        this.timerInaccion = null;
        this.timerEnfocado = null;
        this.temporizadorCascada = null;
        this.temporizadorCierre = null;
        this.salidaSugeridaTimeoutId = null;
        this.salidaTimerId = null;
    },

    /** Starts monitoring user inactivity to prompt interaction. */
    iniciarMonitoreoInaccion() {
        clearInterval(this.timerInaccion); // Clear any existing timer
        this.conteoInaccion = 0; // Reset counter

        this.timerInaccion = setInterval(() => {
            if (document.getElementById('wrapper-form').classList.contains('hidden')) {
                // Only monitor inactivity on the main form
                this.conteoInaccion = 0;
                return;
            }

            this.conteoInaccion++;
            if (this.conteoInaccion === 30) { // After 30 seconds of inactivity
                this.hablar(this.idiomaActual === 'es' ? "¿Hay alguien en la sala?" : "Is anyone still here?");
            } else if (this.conteoInaccion === 60) { // After 60 seconds
                this.hablar(this.idiomaActual === 'es' ? "Si te sientes perdido, toca una tarjeta o usa el mando libre." : "If you feel lost, tap a card or use free command.");
            } else if (this.conteoInaccion >= 90) { // After 90 seconds, reset and re-prompt
                this.conteoInaccion = 0;
                this.hablar(this.idiomaActual === 'es' ? "Tu atención es valiosa. ¿Qué te agobia hoy?" : "Your attention is valuable. What troubles you today?");
            }
        }, 1000);
    },

    /** Changes the UI language (Spanish/English). */
    cambiarIdioma(lang) {
        this.idiomaActual = lang;
        localStorage.setItem("otg_language", lang);

        document.getElementById('lang-es').classList.toggle('active', lang === 'es');
        document.getElementById('lang-en').classList.toggle('active', lang === 'en');

        document.getElementById('html-title').innerText = lang === 'es' ? "OPEN THAN GO" : "OPEN THAN GO"; // Title remains the same
        document.getElementById('txt-app-title').innerText = lang === 'es' ? "OPEN THAN GO" : "OPEN THAN GO";

        // Update form labels
        document.getElementById('lbl-zip').innerText = lang === 'es' ? "Código Postal" : "ZIP Code";
        document.querySelector('#modo-selector option[value="SALIR"]').innerText = lang === 'es' ? "SALIR" : "GO OUT";
        document.querySelector('#modo-selector option[value="CASA"]').innerText = lang === 'es' ? "CASA" : "HOME";
       
        document.querySelector('#opt-mente-aburrido').innerText = lang === 'es' ? "Aburrido" : "Bored";
        document.querySelector('#opt-mente-agotado').innerText = lang === 'es' ? "Agotado" : "Exhausted";
        document.querySelector('#opt-mente-estresado').innerText = lang === 'es' ? "Estresado" : "Stressed";
        document.querySelector('#opt-mente-cansado').innerText = lang === 'es' ? "Cansado" : "Tired";
        document.querySelector('#opt-mente-ansioso').innerText = lang === 'es' ? "Ansioso" : "Anxious";

        document.querySelector('#opt-budget-0').innerText = lang === 'es' ? "Gratis" : "Free";
        document.querySelector('#opt-budget-1').innerText = lang === 'es' ? "Bajo" : "Low";
        document.querySelector('#opt-budget-2').innerText = lang === 'es' ? "Abierto" : "Open";

        document.querySelector('#opt-perfil-solo').innerText = lang === 'es' ? "Solo" : "Solo";
        document.querySelector('#opt-perfil-familia').innerText = lang === 'es' ? "Familia" : "Family";
        document.querySelector('#opt-perfil-accesible').innerText = lang === 'es' ? "Accesible" : "Accessible";

        document.getElementById('lbl-oraculo-instruccion').innerText = lang === 'es' ? "¿Qué te tiene atrapado hoy?" : "What has you trapped today?";
        document.getElementById('lbl-desahogo').innerText = lang === 'es' ? "O escribe aquí tu propio agobio si no aparece arriba:" : "Or write your own problem here if it's not above:";
        document.getElementById('inp-text-libre').placeholder = lang === 'es' ? "Cuéntale al mando libremente qué te pasa hoy..." : "Tell the command freely what's bothering you today...";
        document.getElementById('btn-activar-libre').innerText = lang === 'es' ? "Activar Mando Libre" : "Activate Free Command";

        // Re-inject questions to update their text
        if (!document.getElementById('wrapper-form').classList.contains('hidden')) {
            this.inyectarBloquePreguntas();
            this.activarBotonMandoLibreInicial(); // Ensure mando libre button state is updated
        }
        
        // Update content on closure screen if visible
        if (!document.getElementById('pantalla-cierre').classList.contains('hidden')) {
            const currentRetoId = document.getElementById('reto-titulo').dataset.retoId;
            const catalogo = lang === 'es' ? this.CATALOGO_RETOS_ES : this.CATALOGO_RETOS_EN;
            const currentReto = catalogo.find(r => r.id == currentRetoId); // Find by ID
            if (currentReto) {
                document.getElementById('reto-titulo').innerText = currentReto.titulo;
                document.getElementById('reto-descripcion').innerText = currentReto.descripcion;
            }
            document.getElementById('cierre-mensaje-final').innerText = lang === 'es' ? "¡Éxito! Has completado tu pausa consciente." : "Success! You have completed your conscious pause.";
            document.getElementById('btn-recomenzar-experiencia').innerText = lang === 'es' ? "REINICIAR EXPERIENCIA" : "RESTART EXPERIENCE";
        }

        // Update OTG_SENSORIAL elements if they are active
        if (!document.getElementById('otg-oasis-entretenimiento').classList.contains('otg-hidden')) {
             document.getElementById('otg-game-instruction').innerText = lang === 'es' ? "Si tu mente está sorda y no sabes qué hacer, no pienses: simplemente APRIETA la imagen o el nombre de la plataforma que tengas justo enfrente por pura distracción." : "If your mind is deaf and you don't know what to do, don't think: simply PRESS the image or name of the platform right in front of you purely for distraction.";
             document.getElementById('otg-trivia-submit-btn').innerText = lang === 'es' ? "Continuar" : "Continue";
             document.getElementById('otg-open-link-btn').innerText = lang === 'es' ? "ABRIR ENLACE EXTERNO" : "OPEN EXTERNAL LINK";
             document.getElementById('otg-return-to-app-btn').innerText = lang === 'es' ? "REGRESAR A LA APP" : "RETURN TO APP";
        }
    },

    /**
     * Text-to-speech function using SpeechSynthesis.
     * @param {string} text - The text to be spoken.
     */
    hablar(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = this.idiomaActual === 'es' ? 'es-ES' : 'en-US';
            window.speechSynthesis.cancel(); // Stop any current speech
            window.speechSynthesis.speak(utterance);
        } else {
            console.warn("Speech Synthesis not supported in this browser.");
        }
    }
};

// The KERNEL.init() call is now managed by the OTG_SENSORIAL script in session.html.
// It will be called if the app is not in a forced shutdown or sleep state.
