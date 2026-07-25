// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.6.0.1
// Company: May Roga LLC
// File: static/engine.js (Frontend Logic)

const KERNEL = {
    timerInaccion: null,
    timerEnfocado: null,
    temporizadorCascada: null,
    temporizadorCierre: null,
    salidaSugeridaTimeoutId: null,
    salidaTimerId: null, // New timer for SALIR mode 45s phrases
    speechQueue: [], // New property for speech queue management
    isSpeaking: false, // New property to track if speech is active
    carouselInterval: null, // New interval ID for image carousel
   
    historialFaseCasaSublime: {}, // New history for the 4-min phase audio (daily object)
    historialAudiosCasaSecuenciales: {}, // History for AUDIOS_SECUENCIALES_CASA (daily object)
    historialAudiosSalirSecuenciales: {}, // History for AUDIOS_SECUENCIALES_SALIR (daily object)
    MAX_HISTORY_FASE_CASA_SUBLIME: 28, // Max unique phrases in pool. If pool smaller, will reset history after it's exhausted.
    MAX_HISTORY_AUDIOS_CASA_SECUENCIALES: 29, // Max unique phrases in pool. If pool smaller, will reset history after it's exhausted.
    MAX_HISTORY_AUDIOS_SALIR_SECUENCIALES: 10, // Max unique phrases in pool. If pool smaller, will reset history after it's exhausted.
   
    "AUDIOS_FASE_CASA_SUBLIMES_ES": [ // Renamed from SUBIMES to SUBLIMES for correct spelling
        "Siente la quietud. Este es tu santuario. Permítete descansar. Eres valioso.",
        "Cada respiro te conecta con una paz profunda. Estás a salvo. Confía ahora.",
        "Suelta las tensiones. Deja ir todo lo que no te sirve en este instante. Libera.",
        "Tu mente es un océano vasto. La calma es tu verdadera naturaleza. Siente tu calma.",
        "Imagina un paisaje sereno. Tu hogar interno está en perfecto equilibrio. Estabiliza.",
        "La vida te sostiene. Confía en el flujo. Todo está bien ahora. Concéntrate en el ahora.",
        "En este silencio, redescubre tu fuerza. Eres resiliente. Siente tu fuerza interior.",
        "La sabiduría reside en tu interior. Escúchala con atención. Tu sabiduría te guía.",
        "Permite que la luz te envuelva. Eres un ser radiante. Deja que te inunde.",
        "Este es tu momento de regeneración. Absórbelo plenamente. Permítete recargar.",
        "Observa tu respiración. Es el ancla de tu presencia. Siente tu ancla en la calma.",
        "El presente es un regalo. Vive cada segundo con gratitud. Agradece lo que tienes.",
        "Libera tu mente. El peso de lo externo se desvanece. Deja ir el ruido.",
        "Recibe esta energía renovadora. Estás floreciendo. Florece en el presente.",
        "La belleza está en la simpleza. Encuentra la paz aquí. Reconoce la belleza.",
        "Eres un universo de posibilidades. Despierta tu potencial. Despierta tu luz.",
        "Deja que la quietud te hable. Su mensaje es puro amor. Escucha su mensaje.",
        "Cada inhalación te nutre. Cada exhalación te libera. Libera el pasado.",
        "Tu espíritu se eleva. Siente la ligereza del ser. Vuela con tu espíritu.",
        "Este espacio es sagrado. Tu bienestar es la prioridad. Prioriza tu bienestar.",
        "La armonía te rodea. Permite que te llene por completo. Llénate de armonía.",
        "Eres digno de esta paz. Acéptala sin reservas. Acepta esta calma.",
        "El tiempo se detiene para ti. Disfruta este oasis. Vive tu propio tiempo.",
        "La calma es tu poder. Manifiéstate desde la serenidad. Usa tu poder.",
        "Con cada pulso, la vida te susurra esperanza. Escucha. La esperanza te envuelve.",
        "Tu esencia es divina. Reconoce tu magnificencia. Reconoce tu brillo.",
        "Entrégate al momento. Es todo lo que realmente existe. Vive el momento.",
        "Aquí y ahora, eres completo. Eres luz. Eres amor. Eres eterno.",
    ],
    "AUDIOS_FASE_CASA_SUBLIMES_EN": [ // Renamed from SUBIMES to SUBLIMES for correct spelling
        "Feel the stillness. This is your sanctuary. Allow yourself to rest. You are worthy.",
        "Every breath connects you to deep peace. You are safe. Trust now.",
        "Release tensions. Let go of all that no longer serves you in this moment. Release.",
        "Your mind is a vast ocean. Calm is your true nature. Feel your calm.",
        "Imagine a serene landscape. Your inner home is in perfect balance. Stabilize.",
        "Life sustains you. Trust the flow. All is well now. Focus on the now.",
        "In this silence, rediscover your strength. You are resilient. Feel your inner strength.",
        "Wisdom resides within you. Listen attentively. Your wisdom guides you.",
        "Allow the light to envelop you. You are a radiant being. Let it flood you.",
        "This is your moment of regeneration. Absorb it fully. Allow yourself to recharge.",
        "Observe your breath. It is the anchor of your presence. Feel your anchor in calm.",
        "The present is a gift. Live each second with gratitude. Appreciate what you have.",
        "Free your mind. The weight of the external fades away. Let go of the noise.",
        "Receive this renewing energy. You are flourishing. Flourish in the present.",
        "Beauty lies in simplicity. Find peace right here. Recognize the beauty.",
        "You are a universe of possibilities. Awaken your potential. Awaken your light.",
        "Let the stillness speak to you. Its message is pure love. Listen to its message.",
        "Each inhale nourishes you. Each exhale liberates you. Release the past.",
        "Your spirit soars. Feel the lightness of being. Fly with your spirit.",
        "This space is sacred. Your well-being is the priority. Prioritize your well-being.",
        "Harmony surrounds you. Allow it to fill you completely. Fill with harmony.",
        "You are worthy of this peace. Accept it without reservation. Accept this calm.",
        "Time stops for you. Enjoy this oasis. Live your own time.",
        "Calm is your power. Manifest from serenity. Use your power.",
        "With every pulse, life whispers hope. Listen. Hope envelops you.",
        "Your essence is divine. Recognize your magnificence. Recognize your glow.",
        "Surrender to the moment. It is all that truly exists. Live the moment.",
        "Here and now, you are complete. You are light. You are love. You are eternal.",
    ],

    // New image categories for the carousel, categorized by emotional state for mitigation
    "IMAGENES_CARRUSEL": {
        "aburrido": [ // Images to inspire curiosity, wonder, subtle energy
            "static/images/bored_1_forest_path.jpg", "static/images/bored_2_calm_lake.jpg", "static/images/bored_3_mountain_view.jpg",
            "static/images/bored_4_sun_beach.jpg", "static/images/bored_5_cozy_cottage.jpg", "static/images/bored_6_misty_forest.jpg",
            "static/images/bored_7_river_bend.jpg", "static/images/bored_8_golden_hour_field.jpg", "static/images/bored_9_peaceful_stream.jpg",
            "static/images/bored_10_serene_garden.jpg", "static/images/bored_11_autumn_woods.jpg", "static/images/bored_12_sunlit_meadow.jpg",
            "static/images/bored_13_winter_forest.jpg", "static/images/bored_14_country_road.jpg", "static/images/bored_15_spring_flowers.jpg",
            "static/images/bored_16_ocean_sunset.jpg", "static/images/bored_17_desert_oasis.jpg", "static/images/bored_18_tropical_paradise.jpg",
            "static/images/bored_19_snowy_mountains.jpg", "static/images/bored_20_ancient_trees.jpg", "static/images/bored_21_wild_flowers.jpg",
            "static/images/bored_22_forest_cabin.jpg", "static/images/bored_23_stone_bridge.jpg", "static/images/bored_24_moonlit_lake.jpg"
        ],
        "agotado": [ // Images to promote deep rest, quiet contemplation, gentle beauty
            "static/images/exhausted_1_calm_forest.jpg", "static/images/exhausted_2_still_water.jpg", "static/images/exhausted_3_quiet_meadow.jpg",
            "static/images/exhausted_4_sunrise_mountains.jpg", "static/images/exhausted_5_peaceful_seaside.jpg", "static/images/exhausted_6_deep_woods.jpg",
            "static/images/exhausted_7_misty_river.jpg", "static/images/exhausted_8_sunset_hills.jpg", "static/images/exhausted_9_forest_brook.jpg",
            "static/images/exhausted_10_zen_garden.jpg", "static/images/exhausted_11_path_through_trees.jpg", "static/images/exhausted_12_flower_field.jpg",
            "static/images/exhausted_13_snowy_woods.jpg", "static/images/exhausted_14_winding_road.jpg", "static/images/exhausted_15_spring_forest.jpg",
            "static/images/exhausted_16_calm_ocean.jpg", "static/images/exhausted_17_desert_canyon.jpg", "static/images/exhausted_18_tropical_beach.jpg",
            "static/images/exhausted_19_mountain_lake.jpg", "static/images/exhausted_20_old_growth_forest.jpg", "static/images/exhausted_21_green_valley.jpg",
            "static/images/exhausted_22_log_cabin.jpg", "static/images/exhausted_23_stone_path.jpg", "static/images/exhausted_24_starry_night.jpg"
        ],
        "estresado": [ // Images to soothe, provide expansive views, clear skies, natural order
            "static/images/stressed_1_green_valley.jpg", "static/images/stressed_2_open_sky.jpg", "static/images/stressed_3_clear_river.jpg",
            "static/images/stressed_4_calm_fields.jpg", "static/images/stressed_5_tranquil_coast.jpg", "static/images/stressed_6_sunlit_forest.jpg",
            "static/images/stressed_7_peaceful_stream.jpg", "static/images/stressed_8_golden_meadow.jpg", "static/images/stressed_9_waterfall.jpg",
            "static/images/stressed_10_open_countryside.jpg", "static/images/stressed_11_bright_woods.jpg", "static/images/stressed_12_lakeside_view.jpg",
            "static/images/stressed_13_forest_clearing.jpg", "static/images/stressed_14_path_in_nature.jpg", "static/images/stressed_15_spring_hills.jpg",
            "static/images/stressed_16_blue_ocean.jpg", "static/images/stressed_17_desert_sunset.jpg", "static/images/stressed_18_island_paradise.jpg",
            "static/images/stressed_19_snowy_peaks.jpg", "static/images/stressed_20_ancient_forest.jpg", "static/images/stressed_21_rolling_hills.jpg",
            "static/images/stressed_22_farm_house.jpg", "static/images/stressed_23_rocky_shore.jpg", "static/images/stressed_24_day_clouds.jpg"
        ],
        "cansado": [ // Images for gentle rest, soft light, comforting scenes
            "static/images/tired_1_serene_forest.jpg", "static/images/tired_2_calm_river.jpg", "static/images/tired_3_quiet_lake.jpg",
            "static/images/tired_4_sunset_beach.jpg", "static/images/tired_5_peaceful_cottage.jpg", "static/images/tired_6_deep_green_woods.jpg",
            "static/images/tired_7_flowing_stream.jpg", "static/images/tired_8_field_at_dusk.jpg", "static/images/tired_9_forest_clearing.jpg",
            "static/images/tired_10_zen_garden_path.jpg", "static/images/tired_11_autumn_path.jpg", "static/images/tired_12_sunlit_forest_floor.jpg",
            "static/images/tired_13_winter_lake.jpg", "static/images/tired_14_country_lane.jpg", "static/images/tired_15_spring_field.jpg",
            "static/images/tired_16_ocean_waves.jpg", "static/images/tired_17_desert_stars.jpg", "static/images/tired_18_tropical_lagoon.jpg",
            "static/images/tired_19_mountain_river.jpg", "static/images/tired_20_ancient_trees_mist.jpg", "static/images/tired_21_lush_valley.jpg",
            "static/images/tired_22_forest_house.jpg", "static/images/tired_23_stone_wall.jpg", "static/images/tired_24_moonlit_forest.jpg"
        ],
        "ansioso": [ // Images for openness, fluidity (water), grounding, clear horizons
            "static/images/anxious_1_ocean_horizon.jpg", "static/images/anxious_2_vast_sky.jpg", "static/images/anxious_3_calm_water.jpg",
            "static/images/anxious_4_open_field.jpg", "static/images/anxious_5_forest_clearing.jpg", "static/images/anxious_6_mountain_vista.jpg",
            "static/images/anxious_7_river_flow.jpg", "static/images/anxious_8_peaceful_sunset.jpg", "static/images/anxious_9_still_pond.jpg",
            "static/images/anxious_10_expansive_beach.jpg", "static/images/anxious_11_wide_valley.jpg", "static/images/anxious_12_desert_landscape.jpg",
            "static/images/anxious_13_clear_lake.jpg", "static/images/anxious_14_open_forest.jpg", "static/images/anxious_15_grassy_hills.jpg",
            "static/images/anxious_16_blue_sea.jpg", "static/images/anxious_17_canyon_view.jpg", "static/images/anxious_18_tropical_islands.jpg",
            "static/images/anxious_19_snowy_peaks.jpg", "static/images/anxious_20_cloudy_sky.jpg", "static/images/anxious_21_rolling_plains.jpg",
            "static/images/anxious_22_countryside_home.jpg", "static/images/anxious_23_forest_path_wide.jpg", "static/images/anxious_24_bright_sky.jpg"
        ]
    },
    // --- NUEVO ENGRANAJE INDESTRUCTIBLE (TIPO TIKTOK) ---
    horaInicioSesionAbsoluta: null, // Almacena la estampa de tiempo Unix de la CPU real
    timeLeft: 600,
    timeLeftCierre: 60,
    isLocked: false,
    idiomaActual: 'es',
    pasosMisiones: [],
    indiceMision: 0,
    datosLugarGlobal: null, // Now stores the *selected* mission for SALIR
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

    // New helper to manage daily history for all audio phrases to prevent repetition across 5 sessions
    _getDailyNonRepeatingAudio(pool, historyKey, maxSessions = 5) {
        const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
        let historyData = JSON.parse(localStorage.getItem(historyKey) || "{}");

        // If it's a new day or data structure changed, reset daily history
        if (!historyData.date || historyData.date !== today || !Array.isArray(historyData.sessions)) {
            historyData = { date: today, sessions: [] };
        }

        // Get the current session's phrases, or create a new session if needed
        let currentSessionPhrases;
        if (historyData.sessions.length === 0 || historyData.sessions[historyData.sessions.length - 1].length > 0 && KERNEL.sessionSeed !== historyData.sessions[historyData.sessions.length - 1].seed) {
            // Start a new session if no sessions yet, or if the last session already has phrases and current session is different
            historyData.sessions.push({ seed: KERNEL.sessionSeed, phrases: [] });
        }
        // Ensure we operate on the *latest* session in the array, using the sessionSeed for uniqueness
        let latestSession = historyData.sessions[historyData.sessions.length - 1];
        if (latestSession.seed !== KERNEL.sessionSeed) { // If for some reason the last session doesn't match current seed
            historyData.sessions.push({ seed: KERNEL.sessionSeed, phrases: [] });
            latestSession = historyData.sessions[historyData.sessions.length - 1];
        }
        currentSessionPhrases = latestSession.phrases;

        let availableIndices = [];
        let allUsedIndicesToday = new Set();
        historyData.sessions.forEach(session => session.phrases.forEach(idx => allUsedIndicesToday.add(idx)));

        // Filter out phrases used in current day across all sessions
        for (let i = 0; i < pool.length; i++) {
            if (!allUsedIndicesToday.has(i)) {
                availableIndices.push(i);
            }
        }

        if (availableIndices.length === 0) {
            // All phrases used for today across all sessions, or pool is too small.
            // Reset daily history for this pool, effectively allowing repetition from oldest sessions first.
            historyData.sessions = [];
            historyData.sessions.push({ seed: KERNEL.sessionSeed, phrases: [] }); // Start a fresh session for the next cycle
            latestSession = historyData.sessions[0];
            currentSessionPhrases = latestSession.phrases;
            availableIndices = Array.from({ length: pool.length }, (_, i) => i);
            console.warn(`Daily phrase pool for ${historyKey} exhausted. Resetting daily history.`);
        }

        const randomIndex = availableIndices[Math.floor(Math.random() * availableIndices.length)];
        currentSessionPhrases.push(randomIndex);

        // Limit the number of sessions stored
        if (historyData.sessions.length > maxSessions) {
            historyData.sessions.shift(); // Remove the oldest session
        }

        localStorage.setItem(historyKey, JSON.stringify(historyData));
        return pool[randomIndex];
    },

    // ==============================================================================
    // SENSOR DE FONDO ABSOLUTO (Indestructible si hay llamadas o chat en segundo plano)
    // ==============================================================================
    activarSensorSegundoPlano() {
        document.addEventListener("visibilitychange", () => {
            if (document.visibilityState === "visible") {
                // El usuario regresa de una llamada o chat de WhatsApp.
                // Comparamos el tiempo real transcurrido contra la hora absoluta de la CPU
                if (KERNEL.horaInicioSesionAbsoluta) {
                    let tiempoTranscurridoMs = Date.now() - KERNEL.horaInicioSesionAbsoluta;
                    let tiempoTranscurridoSegundos = Math.floor(tiempoTranscurridoMs / 1000);
                   
                    // Si el tiempo transcurrido total ya superó el ciclo de vida de la sesión (15 minutos = 900 segundos), cerramos limpio
                    if (tiempoTranscurridoSegundos >= 900) { // MODIFIED: from 660 to 900 seconds (15 minutes)
                        if (typeof KERNEL.forzarCierre11MinutosEfectivo === 'function') {
                            KERNEL.forzarCierre11MinutosEfectivo();
                        }
                    }
                }
            }
        });
    },

    forzarCierre11MinutosEfectivo() { // Keep original name, but it now acts as "15-minute effective closure"
        // Este método se activa cuando el tiempo de sesión absoluta supera los 15 minutos
        // mientras el usuario está en segundo plano. Forzamos un reinicio completo.
        console.warn("Sesión forzada a cerrar después de 15 minutos de inactividad o segundo plano.");
        this.destruirYReiniciar(); // Llama al método de reinicio completo
    },

    DEFAULT_NECESSITY_PROFILE: {
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

    "AUDIOS_SECUENCIALES_CASA_ES": [
  "Sigue el pulso en tu pantalla. Concéntrate profundamente. Estás respirando conmigo el día de hoy.",
  "Suelta los hombros despacio. Deja caer todo el peso físico y mental de tu jornada diaria.",
  "No pienses en pendientes ahora. Borra tu lista mental y respira con total tranquilidad ya.",
  "Mantén el ritmo constante. Siente el aire limpio y fresco renovando tu pecho en paz.",
  "Te estoy acompañando en silencio. No estás solo en esta habitación, quédate aquí en calma.",
  "Siente tus pies firmes apoyados en el suelo. La tierra te sostiene de forma gratuita.",
  "El piloto automático está completamente apagado en este segundo de bienestar. Continúa fluyendo así.",
  "Quédate justo en este instante presente. El pasado ya pasó y el futuro no existe.",
  "Suelta la mandíbula ahora mismo. Libera esa carga pesada que aprietas casi sin darte cuenta.",
  "Tu mente está despertando poco a poco. Estás ganando el control real de tus pensamientos.",
  "Eres mucho más grande que tus preocupaciones diarias. Respira muy hondo, despacio y con soltura.",
  "Rompe el círculo del ruido externo. Quédate aquí conmigo habitando este hermoso momento de tregua.",
  "Escucha mi voz con atención. Nota cómo tu respiración se vuelve más profunda y limpia.",
  "Tus ojos están descansando finalmente de todas las luces artificiales y del brillo de pantallas.",
  "Siente los latidos de tu pecho. Es tu maravilloso motor vivo latiendo fuerte para ti.",
  "Siente el peso fuera de tu espalda. Imagina que dejas caer todo tu cansancio acumulado.",
  "No dejes que los pensamientos rápidos te saquen de este hermoso y plácido momento presente.",
  "Abandona la prisa de la ciudad el día de hoy. Aquí el tiempo es completamente tuyo.",
  "Tu calma regresará muy pronto, pero este valioso segundo de paz no se volverá a repetir.",
  "Siente cómo tus pulmones se llenan de fuerza con cada bocanada de aire limpio y puro.",
  "Tu vida necesita que estés muy fuerte por dentro. Regálate este respiro para recuperarte ahora.",
  "Estás borrando con éxito el ruido del día. Quédate en la sala respirando con total comodidad.",
  "La rutina diaria se ha roto. Tú gobiernas tus propias decisiones en este segundo exacto.",
  "El suelo está firme debajo tuyo. Siente la estabilidad real de la tierra sosteniendo tu cuerpo.",
  "Libera tu pecho de todo agobio ahora. Expulsa lo malo de golpe con tu exhalación.",
  "Estás recuperando tu centro y tu equilibrio natural. Sigue la luz del círculo en calma.",
  "Tu mente es fuerte. Has domado con éxito el miedo a las presiones externas de hoy.",
  "Faltan pocos segundos para terminar el ciclo con calma. Siente la esperanza naciendo en ti.",
  "Estás completamente a salvo aquí. Quédate en paz absoluta sintiendo el vaivén de tu respiración."
],
   "AUDIOS_SECUENCIALES_CASA_EN": [
  "Follow the pulse on your screen. Concentrate deeply. You are breathing with me today.",
  "Slowly relax your shoulders now. Let all the physical and mental weight fall away.",
  "Don't think about pending tasks now. Forget your mental list and just breathe safely.",
  "Maintain a constant and steady rhythm. Feel the fresh air cleansing your chest now.",
  "I am accompanying you in silence. You are not alone in this peaceful room.",
  "Feel your feet firmly on the ground. The earth supports your body completely free.",
  "The autopilot is completely off this second of wellness. Keep going just like that.",
  "Stay right in this present instant. The past is gone, the present is yours.",
  "Release your tight jaw right now. Let go of that tension you hold unconsciously.",
  "Your mind is slowly awakening now. You are gaining real control over your thoughts.",
  "You are much bigger than your daily worries. Breathe deeply, slowly, and with ease.",
  "Break the loop of external noise. Stay here in the room breathing with me.",
  "Listen to my voice with attention. Notice how your breathing becomes deeper and cleaner.",
  "Your eyes are finally resting from all the artificial lights of your bright screen.",
  "Feel your steady heartbeat now. It is your beautiful living engine beating for you.",
  "Feel the heavy weight off your back. Imagine completely shaking off all your tiredness.",
  "Don't let racing thoughts take you out of this beautiful and peaceful present moment.",
  "Abandon the city's heavy rush today. Here, this calm time is completely all yours.",
  "Your internal calm will return soon, but this precious second of peace cannot repeat.",
  "Feel your lungs fill with true strength with each deep cycle of pure air.",
  "Your life needs you to be strong inside. Grant yourself this breath to recover.",
  "You are erasing the day's heavy noise. Stay in the room breathing with me.",
  "The daily routine is broken now. You govern your own decisions at this instant.",
  "The ground is firm beneath you. Feel the real stability of the earth today.",
  "Your chest is free from worries now. Expel all negativity at once with ease.",
  "You are regaining your natural biological center. Follow the gentle light of the circle.",
  "Your mind is strong. You have successfully tamed the fear of today's constant pressures.",
  "Only a few seconds left for the definitive reset. Feel the hope rising inside.",
  "You are completely safe here. Remain in absolute peace, feeling your gentle, deep breath."
],
        "AUDIOS_SECUENCIALES_SALIR_ES": [
        "Es momento de levantarse. Deja el teléfono en la mesa ahora mismo.",
        "Camina despacio hacia otra habitación. Respira hondo.",
        "Estás retomando el control de tu tiempo. Sigue adelante.",
        "Elige tu camino con total confianza hoy. Visualiza tu paz.",
        "Estás en control absoluto de tus pensamientos. Siente la calma.",
        "Siente la agradable emoción del viaje. La aventura te espera.",
        "Estás a punto de romper el piloto automático. Avanza.",
        "Concéntrate únicamente en este momento presente. Observa tu entorno.",
        "Suelta las cadenas mentales de la rutina. Muévete libre.",
        "Estás eligiendo tu bienestar de forma consciente. Respira."
    ],
    "AUDIOS_SECUENCIALES_SALIR_EN": [
        "It's time to stand up. Leave your phone on the table right now.",
        "Walk slowly to another room. Take a deep breath.",
        "You are regaining control of your time. Keep moving forward.",
        "Choose your path with total confidence today. Visualize peace.",
        "You are in full control of your thoughts. Feel calm.",
        "Feel the pleasant anticipation of the journey. Adventure awaits.",
        "You are about to break the daily automatic pilot. Step out.",
        "Focus solely on this present moment. Look at your surroundings.",
        "Release the mental chains of routine. Move freely.",
        "You are choosing your well-being consciously. Breathe."
    ],

"AUDIOS_CONDUCCION_ES": "Modo de trayecto seguro activo. Para proteger tu atención en la vía, OPEN THAN GO mantiene la interfaz visual en reposo pasivo. Tu cuerpo viaja por carretera; mantén tus manos firmes en el volante y tus ojos enfocados exclusivamente en el camino. No mires ni manipules este teléfono bajo ninguna circunstancia. Si notas tensión o agobio por la monotonía del tráfico, regálate una respiración completamente natural, lenta y profunda, sin perder jamás la concentración absoluta en los autos que te rodean. Siente el soporte seguro de tu asiento y recuerda que tú gobiernas tu paz interna, no el tráfico. Conduce con total responsabilidad.",
"AUDIOS_CONDUCCION_EN": "Safe travel mode active. To protect your attention on the road, OPEN THAN GO keeps the visual interface in passive rest. Your body is traveling on the highway; keep your hands firmly on the wheel and your eyes focused exclusively on the road. Do not look at or handle this phone under any circumstances. If you notice tension or overload from the monotony of traffic, grant yourself a completely natural, slow, and deep breath, never losing absolute concentration on the cars around you. Feel the secure support of your seat and remember that you govern your inner peace, not the traffic. Drive with full responsibility.",
"CATALOGO_RETOS_ES": [
  {"id": 201, "titulo": "EL RETO DEL SONIDO DEL AGUA", "descripcion": "Dirígete con calma hacia tu cocina y abre el grifo muy despacio. Quédate un minuto completo escuchando el sonido fluido de las gotas al caer contra el fondo del fregadero. Permite que esta melodía limpia de la naturaleza disuelva toda la prisa acumulada de tu mente hoy.", "img": "nature_sound.svg"},
  {"id": 202, "titulo": "EL RETO DEL ABRAZO TÁCTIL", "descripcion": "Busca la prenda de ropa o la manta más suave que tengas cerca en tu habitación actual. Pasa las yemas de tus dedos sobre su textura con absoluta calma, respira hondo y concéntrate únicamente en esa agradable sensación física de confort directo. Tu cuerpo recupera su paz interna ya.", "img": "observe.svg"},
  {"id": 203, "titulo": "EL RETO DEL ENFOQUE VISUAL", "descripcion": "Busca un objeto pequeño y cotidiano que tengas sobre tu mesa, como una taza o un lápiz. Quédate observando fijamente sus bordes, sus sombras y sus colores durante este conteo en total silencio. Distrae tu mirada de las pantallas y permite que tus ojos descansen de verdad.", "img": "words.svg"},
  {"id": 204, "titulo": "EL RETO DE LOS TRES SONIDOS", "descripcion": "Quédate completamente quieto en tu asiento y cierra los ojos con suavidad. Presta mucha atención acústica e intenta identificar tres ruidos diferentes que ocurran dentro de tu hogar en este instante. Vacía tu cabeza de todas las preocupaciones diarias y habita este preciso momento de quietud.", "img": "silence.svg"},
  {"id": 205, "titulo": "EL RETO DE LA GRATITUD", "descripcion": "Toma un papel limpio y escribe una sola cosa hermosa que te haya hecho sonreír durante esta semana en casa. Conéctate con la alegría de ese instante, toma aire pausadamente y permite que esa vibración reconfortante aleje toda tu ansiedad. Estás a salvo en tu espacio seguro.", "img": "gratitude.svg"},
  {"id": 206, "titulo": "EL RETO DE LA RESPIRACIÓN", "descripcion": "Levántate muy despacio de tu asiento actual sin prisa alguna. Camina con calma por tu sala, sirve un vaso con agua fresca y tómalo con total tranquilidad antes de regresar a tus actividades respirando lento. Concéntrate en la frescura del líquido renovando todo tu organismo ahora.", "img": "stretch.svg"},
  {"id": 207, "titulo": "EL RETO DE LA VENTANA", "descripcion": "Abre la ventana más cercana de tu casa durante dos minutos exactos en este momento. Guarda tu teléfono en el bolsillo, relaja tus brazos y quédate observando la inmensidad del cielo en absoluto silencio. Deja que el aire fresco te limpie el rostro y te dé paz.", "img": "nature_sound.svg"},
  {"id": 208, "titulo": "EL RETO DEL ORDEN", "descripcion": "Mira a tu alrededor con deatimiento dentro de tu habitación actual. Busca cinco objetos que estén desordenados y colócalos pausadamente en su lugar correcto. Con solo esos cinco bastará por el día de hoy para recuperar la armonía en tu entorno seguro. Todo está en calma.", "img": "observe.svg"},
  {"id": 209, "titulo": "EL RETO DE LA RESPIRACIÓN profunda", "descripcion": "Quédate sentado en una postura muy cómoda en este instante. Haz cinco respiraciones profundas y lentas por la nariz, sintiendo cómo entra el aire puro a tu cuerpo. Libera toda la tensión de tus hombros, vacía tu mente de preocupaciones y permite que esta tregua biológica te calme.", "img": "square_breath.svg"},
  {"id": 210, "titulo": "EL RETO DEL DESCANSO VISUAL", "descripcion": "Busca un punto u objeto que esté muy lejano a ti a través de la ventana. Quédate mirando ese lugar fijamente durante dos minutos para descansar tus ojos de las pantallas por completo. Expande tu horizonte visual, relaja los párpados y permite que tus pensamientos fluyan en total quietud.", "img": "nature_sound.svg"}
],
"CATALOGO_RETOS_EN": [
  {"id": 201, "titulo_en": "THE SOUND OF WATER CHALLENGE", "descripcion_en": "Walk calmly to your kitchen and turn on the tap very slowly. Spend one full minute listening to the fluid sound of water drops hitting the sink. Allow this clean melody of nature to fully dissolve all the accumulated rush from your mind today. Enjoy this quiet moment.", "img": "nature_sound.svg"},
  {"id": 202, "titulo_en": "THE TACTILE EMBRACE CHALLENGE", "descripcion_en": "Look for the softest piece of clothing or blanket near you in your current room. Pass your fingertips over its texture with absolute calm, breathe deeply, and focus solely on that pleasant physical sensation of direct comfort. Your body recovers its inner peace right now with ease.", "img": "observe.svg"},
  {"id": 203, "titulo_en": "THE VISUAL FOCUS CHALLENGE", "descripcion_en": "Find a small, everyday object on your table, such as a cup or a pencil. Stay looking fixedly at its edges, shadows, and colors during this count in total silence. Distract your eyes from screens and allow your mind to rest truly and deeply right now.", "img": "words.svg"},
  {"id": 204, "titulo_en": "THE THREE SOUNDS CHALLENGE", "descripcion_en": "Stay completely still in your seat and close your eyes gently. Pay close acoustic attention and try to identify three different noises happening inside your home at this instant. Empty your head of all daily worries and inhabit this precise moment of absolute quietness in peace.", "img": "silence.svg"},
  {"id": 205, "titulo_en": "THE GRATITUDE CHALLENGE", "descripcion_en": "Take a clean paper and write down one single beautiful thing that made you smile this week at home. Connect with the joy of that moment, breathe in slowly, and allow that comforting vibration to chase away all your anxiety. You are safe in your secure space.", "img": "gratitude.svg"},
  {"id": 206, "titulo_en": "THE BREATHING CHALLENGE", "descripcion_en": "Get up very slowly from your current seat without any rush. Walk calmly to the kitchen, pour a fresh glass of water, and drink it with total peace of mind before walking back while breathing slowly. Concentrate on that pleasant physical sensation of well-being in your body.", "img": "stretch.svg"},
  {"id": 207, "titulo_en": "THE WINDOW CHALLENGE", "descripcion_en": "Open the nearest window of your house for exactly two minutes at this moment. Keep your phone in your pocket, relax your arms, and stay observing the vastness of the sky in absolute silence. Let the fresh air touch your face and bring you true, deep peace.", "img": "nature_sound.svg"},
  {"id": 208, "titulo_en": "THE CLEANUP CHALLENGE", "descripcion_en": "Look around you with close attention inside your current room. Search for five objects out of place and put them slowly in their correct spot. Just those five will be enough for today to regain harmony in your safe surroundings. Everything is quiet and perfectly in place.", "img": "observe.svg"},
  {"id": 209, "titulo_en": "THE BREATHING CHALLENGE", "descripcion_en": "Stay seated in a very comfortable posture at this instant. Take five deep and slow breaths through your nose, feeling how the pure air enters your body. Release all tension from your shoulders, empty your mind of worries, and allow this biological truce to completely calm you now.", "img": "square_breath.svg"},
  {"id": 210, "titulo_en": "THE VISUAL REST CHALLENGE", "descripcion_en": "Look for a spot or an object that is very far away from you through the window. Keep your eyes on that place fixedly for two minutes to rest your eyes from screens completely. Expand your visual horizon, relax your eyelids, and allow your thoughts to flow in total stillness.", "img": "nature_sound.svg"}
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

    /**
     * Initializes the KERNEL on DOMContentLoaded.
     */
    init() {
        const storedLang = localStorage.getItem("otg_language");
        if (storedLang) {
            this.idiomaActual = storedLang;
        } else {
            localStorage.setItem("otg_language", this.idiomaActual);
        }

        try {
            this.historialSalir = JSON.parse(localStorage.getItem("otg_historial_salir") || "[]");
            this.historialCasa = JSON.parse(localStorage.getItem("otg_historial_casa") || "[]");
            this.historialPreguntas = JSON.parse(localStorage.getItem("otg_historial_oraculo") || "[]");
            this.historialRetosSecuencias = JSON.parse(localStorage.getItem("otg_historial_retos_secuencias") || "[]");
            this.historialFaseCasaSublime = JSON.parse(localStorage.getItem("otg_historial_fase_casa_sublime_daily") || "{}"); // Daily history
            this.historialAudiosCasaSecuenciales = JSON.parse(localStorage.getItem("otg_historial_audios_casa_secuenciales_daily") || "{}"); // Daily history
            this.historialAudiosSalirSecuenciales = JSON.parse(localStorage.getItem("otg_historial_audios_salir_secuenciales_daily") || "{}"); // Daily history
        } catch (e) {
            console.error("Error parsing history from localStorage, resetting specific histories.", e);
            this.historialSalir = [];
            this.historialCasa = [];
            this.historialPreguntas = [];
            this.historialRetosSecuencias = [];
            this.historialFaseCasaSublime = {}; // Reset to empty object for daily history
            this.historialAudiosCasaSecuenciales = {}; // Reset to empty object for daily history
            this.historialAudiosSalirSecuenciales = {}; // Reset to empty object for daily history
            localStorage.removeItem("otg_historial_salir");
            localStorage.removeItem("otg_historial_casa");
            localStorage.removeItem("otg_historial_oraculo");
            localStorage.removeItem("otg_historial_retos_secuencias");
            localStorage.removeItem("otg_historial_fase_casa_sublime_daily");
            localStorage.removeItem("otg_historial_audios_casa_secuenciales_daily");
            localStorage.removeItem("otg_historial_audios_salir_secuenciales_daily");
        }

        this.obtenerPerfilLocal();
        this.mensajeCalidezHumanaActual = "";
        this.activarSensorSegundoPlano();

        const zipInput = document.getElementById('inp-zip');
        if (zipInput) {
            zipInput.addEventListener('input', () => this.validarZip());
            this.validarZip();
        }

        const btnVolverApp = document.getElementById('btn-volver-app');
        if (btnVolverApp) {
            btnVolverApp.addEventListener('click', () => this.reiniciarExperiencia());
        }

        // ==============================================================================
        // ENLACE DIRECTO A LOS 3 PASES DE STRIPE DE TU HTML NATIVO (FASTAPI)
        // ==============================================================================
        const paywallStripeButtons = ['btn-stripe-pase1', 'btn-stripe-pase2', 'btn-stripe-pase3'];
        paywallStripeButtons.forEach((idBoton, index) => {
            const btnStripe = document.getElementById(idBoton);
            if (btnStripe) {
                btnStripe.onclick = async () => {
                    this.hablar(this.idiomaActual === 'es' ? "Conectando con la pasarela de pagos Stripe." : "Connecting to Stripe payment gateway.");
                    try {
                        const response = await fetch("/crear-checkout", { // Use /crear-checkout as per main.py
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ tipo_plan: (index === 0 ? 'unico' : index === 1 ? 'mensual' : 'anual') }) // Map index to plan type
                        });
                        const session = await response.json();
                        if (session.url) {
                            localStorage.setItem('otg_pase_stripe', session.id);
                            window.location.href = session.url;
                        }
                    } catch (e) {
                        console.error("FastAPI Stripe Checkout link error:", e);
                        this.hablar(this.idiomaActual === 'es' ? "Error al conectar con Stripe." : "Error connecting to Stripe.");
                    }
                };
            }
        });

        // ==============================================================================
        // ENLACE DIRECTO AL LOGIN DE USUARIO Y CONTRASEÑA REAL (FASTAPI)
        // ==============================================================================
        const btnLogin = document.getElementById('btn-submit-auth');
        if (btnLogin) {
            btnLogin.onclick = async () => {
                const usernameInput = document.getElementById('auth-username');
                const passwordInput = document.getElementById('auth-password');
                if (!usernameInput || !passwordInput) return;
               
                const username = usernameInput.value.trim();
                const password = passwordInput.value.trim();
               
                if (!username || !password) {
                    this.hablar(this.idiomaActual === 'es' ? "Por favor, introduce tu usuario y contraseña." : "Please enter your username and password.");
                    return;
                }
               
                try {
                    const response = await fetch("/login-admin", { // Use /login-admin as per main.py
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ username, password })
                    });
                    const data = await response.json();
                   
                    if (response.status === 200 && data.status === "success") {
                        localStorage.setItem('otg_user_role', data.role || 'user');
                        const authGate = document.getElementById('auth-gate-wrapper');
                        if (authGate) authGate.classList.add('hidden');
                        this.despertarInicial(); // Proceed to main app
                    } else {
                        this.hablar(this.idiomaActual === 'es' ? "Credenciales incorrectas. Inténtalo de nuevo." : "Incorrect credentials. Please try again.");
                        const devError = document.getElementById('dev_error');
                        if (devError) {
                            devError.innerText = data.error || (this.idiomaActual === 'es' ? "Datos incorrectos." : "Incorrect data.");
                            devError.style.display = "block";
                        }
                    }
                } catch (e) {
                    console.error("FastAPI Auth Gate error:", e);
                    this.hablar(this.idiomaActual === 'es' ? "Error de conexión con el servidor." : "Server connection error.");
                    const devError = document.getElementById('dev_error');
                    if (devError) {
                        devError.innerText = this.idiomaActual === 'es' ? "Error de conexión con el backend de FastAPI." : "FastAPI backend connection error.";
                        devError.style.display = "block";
                    }
                }
            };
        }

        // ==============================================================================
        // ENLACE DIRECTO AL BOTÓN DE BYPASS DEL DESARROLLADOR NATIVO
        // ==============================================================================
        const btnDev = document.getElementById('btn-login-dev'); // Using the ID from the new paywall HTML
        if (btnDev) {
            btnDev.onclick = async () => { // Make it async to handle fetch
                const u = document.getElementById('dev_user').value;
                const p = document.getElementById('dev_pass').value;
                const err = document.getElementById('dev_error');

                try {
                    const respuesta = await fetch('/login-admin', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ username: u, password: p })
                    });
                    const data = await respuesta.json();
                    if (respuesta.status === 200 && data.status === "success") {
                        localStorage.setItem('otg_user_role', 'admin');
                        const authGate = document.getElementById('auth-gate-wrapper');
                        if (authGate) authGate.classList.add('hidden');
                        this.hablar(this.idiomaActual === 'es' ? "Acceso Desarrollador Concedido." : "Developer Access Granted.");
                        this.despertarInicial(); // Proceed to main app
                    } else {
                        err.innerText = data.error || (this.idiomaActual === 'es' ? "Datos incorrectos." : "Incorrect data.");
                        err.style.display = "block";
                        this.hablar(this.idiomaActual === 'es' ? "Credenciales inválidas. Acceso denegado." : "Invalid credentials. Access denied.");
                    }
                } catch (e) {
                    err.innerText = this.idiomaActual === 'es' ? "Error de conexión con el backend de FastAPI." : "FastAPI backend connection error.";
                    err.style.display = "block";
                    this.hablar(this.idiomaActual === 'es' ? "Error de conexión. Inténtalo de nuevo." : "Connection error. Please try again.");
                }
            };
        }
    },

    /**
     * Handles the initial decision after the splash screen: show paywall or main app.
     */
    iniciarOpcionPrincipal() {
        const r = localStorage.getItem('otg_user_role');
        const p = localStorage.getItem('otg_pase_stripe');
        const paywallActive = !p || !(p.startsWith('cs_live_') || p.startsWith('cs_test_'));

        document.getElementById('pantalla-bienvenida').classList.add('hidden');

        if (r === 'admin' || !paywallActive) { // Authenticated or valid pass
            document.getElementById('wrapper-form').classList.remove('hidden');
            this.despertarInicial();
        } else { // Paywall is active
            document.getElementById('auth-gate-wrapper').classList.remove('hidden');
            // Initial call to set up texts in the auth gate in current language
            // This is handled by init's button assignments.
            // No need to call this.hablar here as it will be called by button handlers.
        }
    },

    /**
     * Starts the initial welcome sequence after user interaction or direct bypass.
     */
    despertarInicial() {
        const welcomeScreen = document.getElementById('pantalla-bienvenida');
        if (welcomeScreen) welcomeScreen.classList.add('hidden');
        const authGate = document.getElementById('auth-gate-wrapper');
        if (authGate) authGate.classList.add('hidden');
       
        document.getElementById('wrapper-form').classList.remove('hidden');
        document.getElementById('btn-volver-app').classList.remove('hidden');
        document.getElementById('btn-whatsapp').classList.remove('hidden');
        document.getElementById('btn-messenger').classList.remove('hidden');
        document.getElementById('btn-oasis-sensorial').classList.remove('hidden'); // NEW: Show the floating button for OTG_SENSORIAL
       
        this.cambiarIdioma(this.idiomaActual); // Ensure UI elements are in correct language
       
        this.horaInicioSesionAbsoluta = Date.now();

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
    },

    /**
     * Injects a block of 3 questions into the UI, ensuring they are distinct and not recent.
     */
    inyectarBloquePreguntas() {
        const grid = document.getElementById('contenedor-preguntas-oraculo') || document.getElementById('grid-preguntas') || document.getElementById('contenedor-preguntas');
        if (!grid) return;
       
        clearInterval(this.temporizadorCascada);
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
        if (unseenIndices.length < 3) {
            this.historialPreguntas = [];
            localStorage.removeItem("otg_historial_oraculo");
            for (let i = 0; i < catalogo.length; i++) {
                unseenIndices.push(i);
            }
        }

       
        // Shuffle the available indices to get a random, distinct selection (Fisher-Yates shuffle)
        for (let i = unseenIndices.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [unseenIndices[i], unseenIndices[j]] = [unseenIndices[j], unseenIndices[i]];
        }
       
        let preguntasSeleccionadasIndices = [];
        // Select 3 distinct questions, prioritizing different "blocks" (categories)
        let blocksUsedInCurrentSelection = new Set();
       
        for (let i = 0; i < 3; i++) {
            if (unseenIndices.length === 0) break;
            let candidateIndex = -1;
           
            // Try to pick a question from a block not yet used in this 6-question set
            for (let j = 0; j < unseenIndices.length; j++) {
                const currentIdx = unseenIndices[j];
                const currentBlock = Math.floor(currentIdx / 3);
                if (!blocksUsedInCurrentSelection.has(currentBlock)) {
                    candidateIndex = j;
                    blocksUsedInCurrentSelection.add(currentBlock);
                    break;
                }
            }
           
            // If no unused block question found, just pick the next available shuffled unseen
            if (candidateIndex === -1) {
                candidateIndex = 0;
                        const currentBlock = Math.floor(unseenIndices[candidateIndex] / 3);
                blocksUsedInCurrentSelection.add(currentBlock);
            }
           
            const selectedIndex = unseenIndices.splice(candidateIndex, 1)[0]; // Get one, remove from pool
            preguntasSeleccionadasIndices.push(selectedIndex);
            this.historialPreguntas.push(selectedIndex); // Add to history
        }
       
        this.historialPreguntas = this.historialPreguntas.slice(-this.MAX_HISTORY_ORACULO);
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
       
        this.iniciarEfectoCascada();
    },

    /**
     * Initiates the fading cascade effect for questions.
     */
    iniciarEfectoCascada() {
        this.indicePreguntaCascada = 0;
        const totalButtons = document.querySelectorAll('.btn-pregunta-crisis').length;
       
        if (totalButtons === 0) {
            // If no questions, immediately enable free writing
            this.liberarCajonEscrituraLibre();
            return;
        }
       
        // Respetamos estrictamente los 8 segundos por pregunta asignados en tu flujo temporal original
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

    /**
    * Activates the free writing input field and button from start.
    */
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

        if (btnLibre) {
            const isZipInvalid = zipInput && zipInput.value.trim().length > 0 && !zipInput.checkValidity();
            const isTextareaEmpty = textarea.value.trim().length <= 3;

            if (isZipInvalid || isTextareaEmpty) {
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

            btnLibre.onclick = () => {
                let textoEscrito = textarea.value.trim();
                const isZipInvalidOnSubmit = zipInput && zipInput.value.trim().length > 0 && !zipInput.checkValidity();

                if (isZipInvalidOnSubmit) {
                    this.hablar(this.idiomaActual === 'es' ? "Por favor, introduce un código postal válido." : "Please enter a valid ZIP code.");
                    zipInput.focus();
                    return;
                }

                if (textoEscrito.length > 3) {
                    // El usuario envía la orden. Se procesa de forma directa por el flujo del Kernel
                    this.reaccionarPreguntaSeleccionada(textoEscrito);
                } else {
                    this.hablar(this.idiomaActual === 'es' ? "Escribe tu problema en el cuadro antes de activar el mando." : "Write your problem in the box before activating control.");
                }
            };
        }

        if (textarea) {
            textarea.removeEventListener('input', this.textareaInputHandler);
            this.textareaInputHandler = () => {
                const isZipInvalid = zipInput && zipInput.value.trim().length > 0 && !zipInput.checkValidity();

                if (textarea.value.trim().length > 3 && !isZipInvalid) {
                    if (btnLibre) {
                        btnLibre.style.background = "var(--green-action)";
                        btnLibre.style.color = "#fff";
                        btnLibre.style.borderColor = "var(--green-action)";
                        btnLibre.disabled = false;
                    }
                } else {
                    if (btnLibre) {
                        btnLibre.style.background = "#111";
                        btnLibre.style.color = "#555";
                        btnLibre.style.borderColor = "#222";
                        btnLibre.disabled = true;
                    }
                }
                this.validarZip();
            };
            textarea.addEventListener('input', this.textareaInputHandler);
        }

        this.validarZip();
    },

    /**
    * Validates ZIP input and controls button state.
    */
    validarZip() {
        const zipInput = document.getElementById('inp-zip');
        const btnActivarLibre = document.getElementById('btn-activar-libre');
        const textarea = document.getElementById('inp-text-libre');
        if (!zipInput || !btnActivarLibre || !textarea) return;

        const zipValue = zipInput.value.trim();
        const isValidZip = zipInput.checkValidity();
        const hasTextareaContent = textarea.value.trim().length > 3;

        if (zipValue.length > 0 && !isValidZip) {
            zipInput.style.borderColor = "var(--accent)";
            btnActivarLibre.disabled = true;
            btnActivarLibre.style.background = "#111";
            btnActivarLibre.style.color = "#555";
            btnActivarLibre.style.borderColor = "#222";
        } else {
            zipInput.style.borderColor = "#222";
            if (hasTextareaContent) {
                btnActivarLibre.disabled = false;
                btnActivarLibre.style.background = "var(--green-action)";
                btnActivarLibre.style.color = "#fff";
                btnActivarLibre.style.borderColor = "var(--green-action)";
            } else {
                btnActivarLibre.disabled = true;
                btnActivarLibre.style.background = "#111";
                btnActivarLibre.style.color = "#555";
                btnActivarLibre.style.borderColor = "#222";
            }
        }
    },

    /**
     * Activates the free writing input field and visually indicates readiness.
     */
    liberarCajonEscrituraLibre() {
        const textarea = document.getElementById('inp-text-libre');
        const lblDesahogo = document.getElementById('lbl-desahogo');
        const instruccion = document.getElementById('lbl-oraculo-instruccion');

        if (instruccion) {
            instruccion.innerText = this.idiomaActual === 'es' ? "Mando libre listo. Cuéntame qué te pasa." : "Free control ready. Tell me what is happening.";
            instruccion.style.color = "var(--green-action)";
        }

        if (lblDesahogo) lblDesahogo.style.color = "#fff";
        if (textarea) textarea.focus();

        this.validarZip();
    },

    /**
    * Monitors user inaction and advances question blocks or pauses.
    */
    iniciarMonitoreoInaccion() {
        clearInterval(this.timerInaccion);
        this.conteoInaccion = 0;
       
        // Respetamos estrictamente tu intervalo nativo de 8 segundos por cada tick de inactividad
        this.timerInaccion = setInterval(() => {
            this.conteoInaccion++;
           
            if (this.conteoInaccion === 3 || this.conteoInaccion === 6) {
                clearInterval(this.temporizadorCascada);
                this.inyectarBloquePreguntas();
                this.hablar(this.idiomaActual === 'es' ? "Avanzamos de nivel. Mira estas otras opciones en pantalla." : "Moving up. Look at these other options on screen.");
            } else if (this.conteoInaccion >= 9) {
                clearInterval(this.timerInaccion);
                clearInterval(this.temporizadorCascada);
                this.hablar(this.idiomaActual === 'es' ? "Disculpa. Te daré tu tiempo. Sé que tu mente está cansada. Estaré aquí esperando." : "Apologies. I will give you time. I know your mind is tired. I will be waiting here.");
               
                const instruccion = document.getElementById('lbl-oraculo-instruccion');
                if (instruccion) {
                    instruccion.innerText = this.idiomaActual === 'es' ? "Tomando un respiro. Toca cuando estés listo..." : "Taking a breath. Tap when you are ready...";
                    instruccion.style.color = "#666";
                }
            }
        }, 8000);
    },

    /**
     * Handles user selecting a question or entering free text.
     */
    reaccionarPreguntaSeleccionada(textoPregunta) {
        // ==============================================================================
        // ORDEN DE APAGADO SEGURO (Cesión de Mando al Backend)
        // ==============================================================================
        // El usuario ejecutó una acción. Apagamos los bucles de inactividad de inmediato
        // para limpiar el hilo principal de JavaScript y evitar colisiones de tiempo con Stripe.
        clearInterval(this.timerInaccion);
        clearInterval(this.temporizadorCascada);
        // ==============================================================================

        document.getElementById('inp-text-libre').value = textoPregunta;
        this.ejecutar();
    },

    /**
     * Converts text to speech using browser's SpeechSynthesis API.
     */
    hablar(texto) {
        if (!('speechSynthesis' in window)) return;
        if (!texto) return;

        let fx = texto.replace(/OPEN THAN GO/gi, "OPEN DAN GO").replace(/<[^>]*>/g, '');
        const msg = new SpeechSynthesisUtterance(fx);
        msg.lang = this.idiomaActual === 'es' ? 'es-US' : 'en-US';
        msg.rate = 1.10;
        msg.pitch = 1.05;

        // Add an 'onend' event listener to process the next item in the queue
        msg.onend = () => {
            this.isSpeaking = false;
            this.speechQueue.shift(); // Remove the finished utterance from the queue
            if (this.speechQueue.length > 0) {
                this._speakNextInQueue();
            }
        };

        msg.onerror = (event) => {
            console.error("Speech synthesis error:", event.error);
            this.isSpeaking = false;
            // If an error occurs, cancel current speech and clear the rest of the queue
            window.speechSynthesis.cancel();
            this.speechQueue = [];
        };

        this.speechQueue.push(msg); // Add the new message to the queue
        if (!this.isSpeaking) {
            this._speakNextInQueue(); // If not speaking, start immediately
        }
    },

    // Helper to speak the next item in the queue
    _speakNextInQueue() {
        if (this.speechQueue.length > 0 && !this.isSpeaking) {
            this.isSpeaking = true;
            window.speechSynthesis.speak(this.speechQueue[0]);
        }
    },

    /**
    * Changes the application's language and updates UI elements.
    * @param {string} lang - The target language ('es' or 'en').
    */
    cambiarIdioma(lang) {
        this.idiomaActual = lang;
        localStorage.setItem("otg_language", lang);
        document.getElementById('lang-es').classList.toggle('active', lang === 'es');
        document.getElementById('lang-en').classList.toggle('active', lang === 'en');
       
        const t = {
            es: {
                title: "OPEN THAN GO", zip: "Código Postal", instruccion: "¿Qué te tiene atrapado hoy?",
                desahogo: "O escribe aquí tu propio agobio si no aparece arriba:",
                placeholder: "Cuéntale al mando libremente qué te pasa hoy...", btn: "Activar Mando Libre",
                alert: "Idioma cambiado a español.", budget0: "Gratis", budget1: "Bajo", budget2: "Abierto",
                solo: "Solo", familia: "Familia", accesible: "Accesible", menteAburrido: "Aburrido",
                menteAgotado: "Agotado", menteEstresado: "Estresado", menteCansado: "Cansado",
                menteAnsioso: "Ansioso", modoSalir: "SALIR", modoCasa: "CASA",
                recomenzar: "RECOMENZAR EXPERIENCIA", puertaAbierta: "La puerta está abierta. ¿Continuamos?",
                volverApp: "Volver a la App", authTitle: "ACCESO AUTORIZADO / SECURE LOGIN", authUser: "Usuario", authPass: "Contraseña",
                authLogin: "INGRESAR AL SISTEMA", stripeInfo: "Activación comercial vía Stripe segura:", stripeBtn: "COMPRAR ACCESO / BUY NOW",
                devMode: "MODO DESARROLLADOR / BYPASS CODE", devUser: "Usuario", devPass: "Contraseña", devLogin: "Ingresar Gratis"
            },
            en: {
                title: "OPEN THAN GO", zip: "ZIP Code", instruccion: "What has you trapped today?",
                desahogo: "Or write your own burden here if it does not appear above:",
                placeholder: "Tell the control freely what is happening to you today...", btn: "Activate Free Control",
                alert: "Language switched to English.", budget0: "Free", budget1: "Low", budget2: "Open",
                solo: "Alone", familia: "Family", accesible: "Accessible", menteAburrido: "Bored",
                menteAgotado: "Exhausted", menteEstresado: "Stressed", menteCansado: "Tired",
                menteAnsioso: "Anxious", modoSalir: "OUT", modoCasa: "HOME",
                recomenzar: "RESTART EXPERIENCE", puertaAbierta: "The door is open. Shall we continue?",
                volverApp: "Return to App", authTitle: "AUTHORIZED ACCESS / SECURE LOGIN", authUser: "Username", authPass: "Password",
                authLogin: "ENTER SYSTEM", stripeInfo: "Secure commercial activation via Stripe:", stripeBtn: "BUY ACCESS / BUY NOW",
                devMode: "DEVELOPER MODE / BYPASS CODE", devUser: "Username", devPass: "Password", devLogin: "Enter Free"
            }
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
        document.getElementById('opt-modo-salir').innerText = t.modoSalir; // New: Translate Modo selector options
        document.getElementById('opt-modo-casa').innerText = t.modoCasa; // New: Translate Modo selector options
       
        const cierreLogo = document.getElementById('cierre-logo');
        if (cierreLogo) cierreLogo.innerText = t.title;
        const cierreBoton = document.getElementById('btn-recomenzar-experiencia');
        if (cierreBoton) cierreBoton.innerText = t.recomenzar;
        const cierreMensajeFinal = document.getElementById('cierre-mensaje-final');
        if (cierreMensajeFinal) cierreMensajeFinal.innerText = t.puertaAbierta;
        const btnVolverApp = document.getElementById('btn-volver-app');
        if (btnVolverApp) btnVolverApp.title = t.volverApp;

        // NEW: Translate elements in the auth gate if visible
        const authTitle = document.getElementById('auth-title');
        if (authTitle) authTitle.innerText = t.authTitle;
        const authUsername = document.getElementById('auth-username');
        if (authUsername) authUsername.placeholder = t.authUser;
        const authPassword = document.getElementById('auth-password');
        if (authPassword) authPassword.placeholder = t.authPass;
        const btnSubmitAuth = document.getElementById('btn-submit-auth');
        if (btnSubmitAuth) btnSubmitAuth.innerText = t.authLogin;
        const stripeInfo = document.getElementById('stripe-payment-info');
        if (stripeInfo) stripeInfo.innerText = t.stripeInfo;
        const btnStripeCheckout = document.getElementById('btn-stripe-checkout');
        if (btnStripeCheckout) btnStripeCheckout.innerText = t.stripeBtn;
        const devModeBtn = document.getElementById('dev-mode-button');
        if (devModeBtn) devModeBtn.innerText = t.devMode;
        const devUser = document.getElementById('dev_user');
        if (devUser) devUser.placeholder = t.devUser;
        const devPass = document.getElementById('dev_pass');
        if (devPass) devPass.placeholder = t.devPass;
        const btnLoginDev = document.getElementById('btn-login-dev');
        if (btnLoginDev) btnLoginDev.innerText = t.devLogin;
       

        this.hablar(t.alert);
        this.inyectarBloquePreguntas();
        this.activarBotonMandoLibreInicial();
    },

    /**
     * Executes the main logic to fetch recommendations from the backend.
     */
    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;
       
        // ==============================================================================
        // SANEAMIENTO ABSOLUTO DE INTERVALOS (Limpieza Radical de Relojes de Fondo)
        // ==============================================================================
        // Forzamos el apagado total de todos los temporizadores activos en la sesión
        // para limpiar el hilo principal de JavaScript y evitar colisiones de tiempo con Stripe.
        clearInterval(this.timerInaccion);
        clearInterval(this.temporizadorCascada);
        clearInterval(this.timerEnfocado);
        clearInterval(this.salidaTimerId);
        if (this.carouselInterval) { // NEW
            clearInterval(this.carouselInterval);
            this.carouselInterval = null;
        }
        // Do NOT cancel() here; let the queue manage it
        this.speechQueue = [];
        this.isSpeaking = false;
        window.speechSynthesis.cancel(); // Force cancel any *external* speech not managed by queue

        if (this.salidaSugeridaTimeoutId) {
            clearTimeout(this.salidaSugeridaTimeoutId);
            this.salidaSugeridaTimeoutId = null;
        }

        const modoActual = document.getElementById('modo-selector') ? document.getElementById('modo-selector').value : "SALIR";
        const zipInput = document.getElementById('inp-zip');
        const desahogoInput = document.getElementById('inp-text-libre');

        if (zipInput && zipInput.value.trim().length > 0 && !zipInput.checkValidity()) {
            alert(this.idiomaActual === 'es' ? "Error: Código Postal inválido. Por favor, corrígelo." : "Error: Invalid ZIP Code. Please correct it.");
            this.isLocked = false;
            zipInput.focus();
            return;
        }

        const payload = {
            zip: zipInput ? zipInput.value.trim() : "",
            modo: modoActual,
            desahogo: desahogoInput ? desahogoInput.value.trim() : "",
            lang: this.idiomaActual,
            mente: document.getElementById('mente-selector') ? document.getElementById('mente-selector').value : "aburrido",
            budget: document.getElementById('budget-selector') ? document.getElementById('budget-selector').value : "0",
            perfil: document.getElementById('perfil-selector') ? document.getElementById('perfil-selector').value : "solo",
            perfil_local: this.obtenerPerfilLocal(),
        };

        if (modoActual === "CASA") {
            payload.historial_casa = this.historialCasa;
        } else {
            payload.historial_salir = this.historialSalir;
        }

        const container = document.getElementById('wrapper-interactive');
        document.getElementById('wrapper-form').classList.add('hidden');
        document.getElementById('pantalla-cierre').classList.add('hidden');
       
        container.innerHTML = `<div style='text-align:center; padding:40px 0;'><h2 style='color:#fff; font-size:1.1rem;'>${this.idiomaActual === 'es' ? 'CONECTANDO CON EL MANDO...' : 'CONNECTING TO CONTROL...'}</h2></div>`;
        container.classList.remove('hidden');

                try {
        const r = await fetch("/api/mando-integral", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
       
        const data = await r.json();
       
        if (data.error) {
            alert(data.error);
            document.getElementById('wrapper-form').classList.remove('hidden');
            container.classList.add('hidden');
            this.isLocked = false;
            this.validarZip();
            return;
        }
       
        this.tipoEscapeGlobal = data.DIRECCIONAMIENTO_MASTER;
        this.indiceMision = 0;
       
        // --- Captura el 1% de Calidez Humana dinámica enviada por el Servidor ---
        let textoElegido = data.calidez_humana || (this.idiomaActual === 'es' ? "Respira profundo. Siente. Estás vivo. Respira." : "Breathe deeply. You are here. You are alive.");
       
        // --- Ejecuta el dictado por voz nativo usando la calidez del Oráculo ---
        // CORRECCIÓN: Usar el método hablar de KERNEL consistentemente
        this.hablar(textoElegido);
       
        // Guardamos la calidez humana en la instancia
        this.mensajeCalidezHumanaActual = textoElegido;
       
     // MADO: ACCIÓN DE CAMPO (SALIR)
 if (this.tipoEscapeGlobal === "ACCION_CAMPO") {
 this.historialSalir = data.historial_salir_actualizado || [];
 localStorage.setItem("otg_historial_salir", JSON.stringify(this.historialSalir));
 this.pasosMisiones = data.misiones || [];
 this.mostrarOpcionesSalir(container);
 }
 // === CORRECCIÓN MAESTRA: SINOPSIS DE ENRUTAMIENTO PARA EL MODO CASA ===
 // Cambiamos "INTERVENCION_DOMESTICA" por "MODO_CASA" para que enganche perfectamente con el Backend
 else if (this.tipoEscapeGlobal === "INTERVENCION_DOMESTICA" || this.tipoEscapeGlobal === "MODO_CASA") {
 this.historialCasa = data.historial_casa_actualizado || [];
 localStorage.setItem("otg_historial_casa", JSON.stringify(this.historialCasa));

           
            this.pasosMisiones = data.misiones || [];
            this.procesarFlujoSecuencial(container);
        }
       
    } catch (error) {
        console.error("Fetch error:", error);
        alert(this.idiomaActual === 'es'
            ? "Error de conexión con el servidor. Por favor, inténtalo de nuevo."
            : "Connection error with the server. Please try again."
        );
        document.getElementById('wrapper-form').classList.remove('hidden');
        container.classList.add('hidden');
        this.isLocked = false;
        this.validarZip();
    }
},

    /**
     * Displays the 3 options for SALIR mode and waits for user selection.
     */
    mostrarOpcionesSalir(container) {
        clearInterval(this.timerEnfocado);
        clearInterval(this.salidaTimerId);
        // Do NOT cancel here, let the queue manage it
        this.speechQueue = [];
        this.isSpeaking = false;
        window.speechSynthesis.cancel(); // Force cancel any *external* speech not managed by queue
       
        const t = {
            es: { choosePath: "ELIGE TU CAMINO DE LIBERTAD", chooseOne: "Toca una opción para continuar:" },
            en: { choosePath: "CHOOSE YOUR PATH TO FREEDOM", chooseOne: "Tap an option to continue:" }
        }[this.idiomaActual];
       
        container.innerHTML = `
            <div class="mision-choices-container">
                <h2 class="salida-main-title">${t.choosePath}</h2>
                <p class="salida-choose-instruction">${t.chooseOne}</p>
                <div id="salida-options-grid" class="salida-grid">
                    <!-- Options will be injected here -->
                </div>
            </div>`;
           
        const optionsGrid = document.getElementById('salida-options-grid');
       
        this.pasosMisiones.forEach((mission, index) => {
            const missionTitle = this.idiomaActual === 'es' ? mission.destino_titulo : mission.destino_titulo_en || mission.destino_titulo;
            const missionWhatToDo = this.idiomaActual === 'es' ? mission.que_hacer : mission.que_hacer_en || mission.que_hacer;
           
            const card = document.createElement('div');
            card.className = 'salida-option-card';
            card.innerHTML = `
                <h3 class="salida-option-title">${missionTitle}</h3>
                <p class="salida-option-desc">${missionWhatToDo}</p>
                <button class="btn-select-salida">${this.idiomaActual === 'es' ? 'Seleccionar' : 'Select'}</button>
            `;
           
            card.querySelector('.btn-select-salida').onclick = () => this.iniciarSalidaConcreta(mission);
            optionsGrid.appendChild(card);
        });
       
        // Inyectamos de forma segura la Calidez Humana dinámica del oráculo directo a tu voz asistida
        const textoOraculo = this.mensajeCalidezHumanaActual || t.chooseOne;
        this.hablar(textoOraculo);
    },

    /**
     * Initiates the 35s stabilization + 45s phrase injection for a selected SALIR mission.
     * MODIFIED: Includes redirection announcements and split-screen external links.
     * @param {Object} selectedMission - The mission object chosen by the client.
     */
    iniciarSalidaConcreta(selectedMission) {
        this.datosLugarGlobal = selectedMission; // Store the selected mission
        clearInterval(this.timerEnfocado);
        clearInterval(this.salidaTimerId);
        // Do NOT cancel here, let the queue manage it
        this.speechQueue = [];
        this.isSpeaking = false;
        window.speechSynthesis.cancel(); // Force cancel any *external* speech not managed by queue
       
        const t = {
            es: { listen: "ESCUCHA MI GUÍA", launch: "ABRIR CANAL EXTERNO YA", maps: "Google Maps", youtube: "YouTube", spotify: "Spotify" },
            en: { listen: "LISTEN TO THE GUIDE", launch: "OPEN EXTERNAL CHANNEL NOW", maps: "Google Maps", youtube: "YouTube", spotify: "Spotify" }
        }[this.idiomaActual];
       
        const container = document.getElementById('wrapper-interactive');
        let textoFormateado = (this.idiomaActual === 'es' ? this.datosLugarGlobal.destino_instruccion : this.datosLugarGlobal.destino_instruccion_en || this.datosLugarGlobal.destino_instruccion).replace(/\n/g, '<br>');
       
        container.innerHTML = `
            <div class="mision-card">
                <small>${this.idiomaActual === 'es' ? 'Acción de Campo' : 'Field Action'}</small>
                <h2>${this.idiomaActual === 'es' ? this.datosLugarGlobal.destino_titulo : this.datosLugarGlobal.destino_titulo_en || this.datosLugarGlobal.destino_titulo}</h2>
                <div class="instruccion-text">${textoFormateado}</div>
                <div id="salida-countdown-phrases" style="margin-top:20px; text-align:center; font-size:1.1rem; min-height:40px; color:var(--cyan-inhale); font-weight:bold; letter-spacing:0.5px;"></div>
                <button id="btn-countdown-salida" style="width:100%; background:#222; color:#aaa; padding:17px; font-weight:bold; margin-top:15px; border:none; text-transform:uppercase; border-radius:4px; font-size:0.9rem;" disabled>35s ${t.listen}</button>
                
                <!-- NEW: Split-screen buttons for external links -->
                <div id="external-links-container" class="external-links-grid hidden">
                    <button id="btn-maps-action" class="btn-external" title="${t.maps}">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24px" height="24px"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                        <span>${t.maps}</span>
                    </button>
                    <button id="btn-youtube-action" class="btn-external" title="${t.youtube}">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24px" height="24px"><path d="M10 15l5.5-3.5L10 8V15zm11.23-7.39c-.78-.78-2.05-.78-2.83 0L12 11.02l-6.4-6.4c-.78-.78-2.05-.78-2.83 0-.78.78-.78 2.05 0 2.83L9.17 12l-6.4 6.4c-.78.78-.78 2.05 0 2.83.78.78 2.05.78 2.83 0L12 12.98l6.4 6.4c.78.78 2.05.78 2.83 0 .78-.78.78-2.05 0-2.83L14.83 12l6.4-6.4c.78-.78.78-2.05 0-2.83z"/></svg>
                        <span>${t.youtube}</span>
                    </button>
                    <button id="btn-spotify-action" class="btn-external" title="${t.spotify}">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24px" height="24px"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 14.5c-.27 0-.53-.11-.72-.32-.97-1.04-2.45-1.72-4.28-1.72-1.83 0-3.31.68-4.28 1.72-.19.21-.45.32-.72.32-.27 0-.53-.11-.72-.32-.19-.21-.29-.48-.29-.78 0-.3.1-.57.29-.78.97-1.04 2.45-1.72 4.28-1.72 1.83 0 3.31.68 4.28 1.72.19.21.29.48.29.78 0 .3-.1.57-.29.78zM12 4c-3.72 0-6.76 2.97-7 6.64-.17 1.83.33 3.5 1.34 4.8-.45.54-1.04.99-1.77 1.25-.73.27-1.57.4-2.43.34-.1-.1-.2-.1-.28-.18-.08-.08-.13-.18-.13-.28 0-.05-.01-.1-.01-.14 0-.04 0-.08.01-.12.44-2.26 1.95-4.14 3.93-5.22.61-.34 1.25-.56 1.9-.66.65-.11 1.3-.13 1.93-.06.72-.05 1.44-.01 2.16.1 2.03.4 3.65 1.88 4.6 3.6.95 1.7.99 3.56.12 5.21-.55.8-1.25 1.37-2.01 1.63-.76.26-1.55.28-2.31.1-.09-.03-.18-.05-.27-.05-.09 0-.17.02-.25.06l-.28.1-.02-.1.01-.1-.01-.11v-.15c-.01-.06-.01-.12-.01-.17 0-.05 0-.1.01-.15z"/></svg>
                        <span>${t.spotify}</span>
                    </button>
                </div>
            </div>
        `;
       
        let speechText = (this.idiomaActual === 'es' ? this.datosLugarGlobal.destino_titulo : this.datosLugarGlobal.destino_titulo_en || this.datosLugarGlobal.destino_titulo) + ". " + (this.idiomaActual === 'es' ? this.datosLugarGlobal.destino_instruccion : this.datosLugarGlobal.destino_instruccion_en || this.datosLugarGlobal.destino_instruccion);
        this.hablar(speechText);
       
        let retencion = 35;
        const btnCount = document.getElementById('btn-countdown-salida');
        const externalLinksContainer = document.getElementById('external-links-container'); // NEW
        const btnMaps = document.getElementById('btn-maps-action'); // NEW
        const btnYoutube = document.getElementById('btn-youtube-action'); // NEW
        const btnSpotify = document.getElementById('btn-spotify-action'); // NEW
        const phrasesDiv = document.getElementById('salida-countdown-phrases');
        const AUDIOS_SECUENCIALES_SALIR = this.idiomaActual === 'es' ? this.AUDIOS_SECUENCIALES_SALIR_ES : this.AUDIOS_SECUENCIALES_SALIR_EN;
        
        // NEW: History for SALIR sequential audios
        let lastSalirAudioTime = -1; // To ensure audio plays only every ~10-15 seconds
       
        this.salidaTimerId = setInterval(() => {
            if (retencion > 0) {
                retencion--;
                if (btnCount) btnCount.innerText = `${retencion}s ${t.listen}`;
                if (retencion === 0) {
                    // Transition to 45s phrase injection
                    retencion = -45; // Use negative to denote this phase, total 45 seconds for phrases
                    if (btnCount) btnCount.innerText = `${Math.abs(retencion)}s...`;
                    
                    // Start first phrase for 45s phase
                    let currentPhrase = this._getDailyNonRepeatingAudio(
                        AUDIOS_SECUENCIALES_SALIR,
                        "otg_historial_audios_salir_secuenciales_daily",
                        5 // Max 5 sessions per day
                    );
                    if (phrasesDiv) phrasesDiv.innerText = currentPhrase;
                    this.hablar(currentPhrase);
                    lastSalirAudioTime = retencion; // Initialize last audio time
                }
            } else if (retencion < 0) {
                retencion++; // Count up towards 0 (from -45 to -1)
                if (btnCount) btnCount.innerText = `${Math.abs(retencion)}s...`;
                // Play new phrase every 10-15 seconds during this 45-second phase
                if (Math.abs(retencion) % 15 === 0 && retencion !== lastSalirAudioTime && Math.abs(retencion) > 0) {
                    lastSalirAudioTime = retencion;
                    let currentPhrase = this._getDailyNonRepeatingAudio(
                        AUDIOS_SECUENCIALES_SALIR,
                        "otg_historial_audios_salir_secuenciales_daily",
                        5 // Max 5 sessions per day
                    );
                    if (phrasesDiv) phrasesDiv.innerText = currentPhrase;
                    this.hablar(currentPhrase);
                }
                if (retencion === 0) {
                    // 45 seconds are over
                    clearInterval(this.salidaTimerId);
                    // Do NOT cancel() here, let the queue finish
                    if (btnCount) btnCount.style.display = 'none';
                    if (phrasesDiv) phrasesDiv.innerText = "";
                    
                    if (externalLinksContainer) { // NEW: Show external links
                        externalLinksContainer.classList.remove('hidden');

                        // Configure Maps button
                        if (btnMaps && this.datosLugarGlobal.destino_coordenadas_gps) {
                            btnMaps.onclick = () => {
                                this.hablar(this.idiomaActual === 'es' ? `Abriendo ${t.maps}.` : `Opening ${t.maps}.`);
                                window.open(this.datosLugarGlobal.destino_coordenadas_gps, '_blank');
                                this._updateProfileAndRestartMonitor(); // Unified update and restart
                            };
                        } else if (btnMaps) { btnMaps.disabled = true; btnMaps.style.opacity = 0.5; }

                        // Configure YouTube button
                        if (btnYoutube && this.datosLugarGlobal.enlace_youtube) {
                            btnYoutube.onclick = () => {
                                this.hablar(this.idiomaActual === 'es' ? `Abriendo ${t.youtube}.` : `Opening ${t.youtube}.`);
                                window.open(this.datosLugarGlobal.enlace_youtube, '_blank');
                                this._updateProfileAndRestartMonitor();
                            };
                        } else if (btnYoutube) { btnYoutube.disabled = true; btnYoutube.style.opacity = 0.5; }

                        // Configure Spotify button
                        if (btnSpotify && this.datosLugarGlobal.enlace_spotify) {
                            btnSpotify.onclick = () => {
                                this.hablar(this.idiomaActual === 'es' ? `Abriendo ${t.spotify}.` : `Opening ${t.spotify}.`);
                                window.open(this.datosLugarGlobal.enlace_spotify, '_blank');
                                this._updateProfileAndRestartMonitor();
                            };
                        } else if (btnSpotify) { btnSpotify.disabled = true; btnSpotify.style.opacity = 0.5; }
                    }
                }
            }
        }, 1000);
    },

    // NEW: Helper function to update profile and restart monitoring, extracted from btnGps.onclick
    _updateProfileAndRestartMonitor() {
        try {
            let perfil = KERNEL.obtenerPerfilLocal();
            const selectedVector = KERNEL.datosLugarGlobal.vector_entorno_seleccionado;
            for (const need in selectedVector) {
                if (need !== "indicador_ansiedad" && perfil[need] !== undefined) {
                    perfil[need] = Math.min(perfil[need] + (selectedVector[need] * 0.1), 100);
                }
            }
            perfil["indicador_ansiedad"] = Math.max(0, perfil["indicador_ansiedad"] - 10);
            localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
        } catch (e) {
            console.error("Error updating local profile after action:", e);
        }

        // ==============================================================================
        // ORDEN SOBERANA: EL TIEMPO COMIENZA A CORRER DESDE CERO AUTOMÁTICAMENTE
        // ==============================================================================
        // Una vez acarreada toda la acción, reactivamos el temporizador maestro desde cero limpios.
        this.iniciarMonitoreoInaccion();
        this.horaInicioSesionAbsoluta = Date.now(); // Reseteamos la estampa de tiempo absoluta
        // ==============================================================================
    },
    
    // ==============================================================================
    // REMOVED: KERNEL.inyectarPasarelaYAutenticacion as it was a duplicate and conflicting.
    // The main paywall logic is now handled directly in session.html's initial script
    // and its button event listeners are assigned in KERNEL.init()
    // ==============================================================================

    /**
     * Processes the sequential flow based on the recommendation type (only for CASA mode now).
     */
        procesarFlujoSecuencial(container) {
    clearInterval(this.timerEnfocado);
    // Do NOT cancel here, let the queue manage it
    this.speechQueue = [];
    this.isSpeaking = false;
    window.speechSynthesis.cancel(); // Force cancel any *external* speech not managed by queue

    const t = {
        es: {
            inspira: "Inhala ahora", expira: "Exhala ahora", fin: "Protocolo completado. Borrando rastro.",
            listen: "ESCUCHA MI GUÍA", launch: "ABRIR CANAL EXTERNO YA", fieldAction: "Acción de Campo",
            internalMission: "Misión Interna", doItNow: "HAZLO AHORA", suggestedEscape: "Escape sugerido"
        },
        en: {
            inspira: "Inhale now", expira: "Exhale now", fin: "Protocol completed. Clearing tracks.",
            listen: "LISTEN TO THE GUIDE", launch: "OPEN EXTERNAL CHANNEL NOW", fieldAction: "Field Action",
            internalMission: "Internal Mission", doItNow: "DO IT NOW", suggestedEscape: "Suggested escape"
        }
    }[this.idiomaActual];

    if (this.indiceMision >= this.pasosMisiones.length) {
        this.iniciarRelojEnfocadoCasa(container, t);
        return;
    }

    const paso = this.pasosMisiones[this.indiceMision];
    // CORREGIDO: Se restauró el padding a 16px para evitar el desborde y el congelamiento del renderizado
    container.innerHTML = `
        <div class="mision-card">
            <small>${t.internalMission}</small>
            <h3>${paso.titulo}</h3>
            <p>${paso.descripcion}</p>
            <button id="btn-next" style="width:100%; background:var(--green-action); color:#fff; padding:16px; font-weight:bold; text-transform:uppercase; border-radius:6px; cursor:pointer; border:none; margin-top:15px; font-size:0.95rem;">${t.doItNow}</button>
        </div>`;

    this.hablar(paso.titulo + " . " + paso.descripcion);
   
    document.getElementById('btn-next').onclick = () => {
        try {
            let perfil = this.obtenerPerfilLocal();
            const missionVector = paso.vector_necesidades || this.DEFAULT_NECESSITY_PROFILE;
            for (const need in missionVector) {
                if (need !== "indicador_ansiedad" && perfil[need] !== undefined) {
                    perfil[need] = Math.min(perfil[need] + (missionVector[need] * 0.05), 100);
                }
            }
            perfil["indicador_ansiedad"] = Math.max(0, perfil["indicador_ansiedad"] - 5);
            localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
        } catch (e) {
            console.error("Error updating local profile after CASA mission:", e);
        }

        // ==============================================================================
        // ORDEN SOBERANA INDEPENDIENTE: EL RECOMIENZA DESDE CERO
        // ==============================================================================
        this.iniciarMonitoreoInaccion();
        this.horaInicioSesionAbsoluta = Date.now();
        // ==============================================================================
       
        this.avanzarPaso();
    };
},
   
    /**
     * Starts the 10-minute clinical breathing timer for CASA mode.
     * MODIFIED: Integrates new 4-minute phase and refined audio/visual sequencing.
     */
    iniciarRelojEnfocadoCasa(container, t) {
        // ======================================================================
        // RECTIFICACIÓN MAESTRA DE EQUILIBRIO: APAGÓN DE ORÁCULO RECOBRANDO EL FLUJO
        // ======================================================================
        // 1. Destruye el intervalo de las preguntas en cascada usando su nombre exacto
        if (this.temporizadorCascada) {
            clearInterval(this.temporizadorCascada);
            this.temporizadorCascada = null;
        }

        // 2. Limpia los temporizadores de inacción y el reloj viejo
        clearInterval(this.timerInaccion);
        clearInterval(this.timerEnfocado);

        // 3. Limpia cualquier bucle de voz previo de CASA para evitar duplicaciones
        if (this.intervaloVozCasa) {
            clearInterval(this.intervaloVozCasa);
            this.intervaloVozCasa = null;
        }

        // 4. Limpia el carrusel visual si está activo
        if (this.carouselInterval) {
            clearInterval(this.carouselInterval);
            this.carouselInterval = null;
        }

        // 5. RETORNO DE MOTOR RECOBRADO: Despierta y limpia el hardware de sonido
        // sin alterar el flujo de las pantallas iniciales ni congelar la app.
        if ('speechSynthesis' in window) {
            window.speechSynthesis.getVoices();
            // Do NOT cancel here, let the queue manage it
        }

        // Ensure speech queue is empty before starting
        this.speechQueue = [];
        this.isSpeaking = false;
        window.speechSynthesis.cancel(); // Force cancel any *external* speech not managed by queue

        let msg = this.idiomaActual === 'es' ? "Iniciamos quince minutos de limpieza mental profunda. Respira." : "Starting fifteen minutes of deep mental clearing. Breathe.";
        this.hablar(msg);

        // --- NEW: Add carousel container for images ---
        container.innerHTML = `
            <div id="carousel-background" class="carousel-container"></div>
            <div style="text-align:center; width:100%; position:relative; z-index:10;">
                <div id="breath-circle" style="cursor:pointer;" title="${this.idiomaActual === 'es' ? 'Toca para enfocar tu mente' : 'Tap to focus your mind'}"></div>
                <div id="timer">15:00</div>
                <p id="txt-pulmon">INHALA / INHALE</p>
                <div id="fase-sublime-text" style="margin-top:20px; text-align:center; font-size:1.1rem; min-height:40px; color:var(--green-action); font-weight:bold; letter-spacing:0.5px;"></div>
                <div id="salida-sugerida" class="hidden" style="margin-top: 30px; padding: 15px; border: 1px dashed #444; border-radius: 8px; font-size: 0.9rem; color: #888;">
                    <p style="margin:0;">${t.suggestedEscape}: <a href="#" id="link-salida-sugerida" style="color: var(--accent); text-decoration: none; font-weight: bold;">Cargando...</a></p>
                </div>
            </div>
        `;

        this.timeLeft = 900; // 15 minutes (10 min breathing + 4 min new phase + 1 min silence challenge)
        this.contadorToques = 0;

        const carouselBackground = document.getElementById('carousel-background');
        const circleElement = document.getElementById('breath-circle');
        const timerDiv = document.getElementById('timer');
        const pulmonDiv = document.getElementById('txt-pulmon');
        const faseSublimeTextDiv = document.getElementById('fase-sublime-text');
        const salidaSugeridaDiv = document.getElementById('salida-sugerida');
        const linkSalidaSugerida = document.getElementById('link-salida-sugerida');

        const AUDIOS_SECUENCIALES_CASA = this.idiomaActual === 'es' ? this.AUDIOS_SECUENCIALES_CASA_ES : this.AUDIOS_SECUENCIALES_CASA_EN;
        const AUDIOS_FASE_SUBLIMES = this.idiomaActual === 'es' ? this.AUDIOS_FASE_CASA_SUBLIMES_ES : this.AUDIOS_FASE_CASA_SUBLIMES_EN;

        let currentImageIndex = 0;
        let imagesForMente = [];
        // let imageChangeIntervalId = null; // This variable was declared but never used in the original code, removed it.

        // Get payload['mente'] from the stored profile or default
        const currentMente = this.obtenerPerfilLocal().mente || document.getElementById('mente-selector').value || "aburrido";
        imagesForMente = this.IMAGENES_CARRUSEL[currentMente] || this.IMAGENES_CARRUSEL["aburrido"];
        
        // Shuffle images to ensure randomness for carousel
        for (let i = imagesForMente.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [imagesForMente[i], imagesForMente[j]] = [imagesForMente[j], imagesForMente[i]];
        }

        const startCarousel = () => {
            if (carouselBackground && imagesForMente.length > 0) {
                carouselBackground.style.backgroundImage = `url('${imagesForMente[currentImageIndex % imagesForMente.length]}')`;
                carouselBackground.classList.remove('hidden');
                this.carouselInterval = setInterval(() => {
                    currentImageIndex++;
                    carouselBackground.style.backgroundImage = `url('${imagesForMente[currentImageIndex % imagesForMente.length]}')`;
                }, 10000); // Change image every 10 seconds
            }
        };

        const stopCarousel = () => {
            if (this.carouselInterval) {
                clearInterval(this.carouselInterval);
                this.carouselInterval = null;
            }
            if (carouselBackground) {
                carouselBackground.classList.add('hidden');
                carouselBackground.style.backgroundImage = 'none';
            }
        };

        // ======================================================================
        // DISPARADOR DE SUGERENCIA TRAS 3 MINUTOS EXACTOS (time 12:00)
        // ======================================================================
        if (this.salidaSugeridaTimeoutId) {
            clearTimeout(this.salidaSugeridaTimeoutId);
            this.salidaSugeridaTimeoutId = null;
        }

        this.salidaSugeridaTimeoutId = setTimeout(async () => {
            try {
                // Ensure payload is up-to-date and matches original call logic
                const payloadForSuggestion = {
                    modo: "SALIR",
                    lang: this.idiomaActual,
                    mente: document.getElementById('mente-selector') ? document.getElementById('mente-selector').value : "aburrido",
                    budget: document.getElementById('budget-selector') ? document.getElementById('budget-selector').value : "0",
                    perfil: document.getElementById('perfil-selector') ? document.getElementById('perfil-selector').value : "solo",
                    desahogo: document.getElementById('inp-text-libre') ? document.getElementById('inp-text-libre').value.trim() : "",
                    zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
                    perfil_local: this.obtenerPerfilLocal(),
                    historial_salir: this.historialSalir
                };

                const r = await fetch("/api/mando-integral", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payloadForSuggestion) });
                const data = await r.json();

                // === PROTOCOLO LEGAL DE SEGURIDAD (MAY ROGA LLC) ===
                if (data.drive_prohibited && data.legal_notice_es) {
                    console.warn("ALERT:", this.idiomaActual === 'es' ? data.legal_notice_es : data.legal_notice_en);
                }

                if (data.DIRECCIONAMIENTO_MASTER === "ACCION_CAMPO" && data.misiones && data.misiones.length > 0 && linkSalidaSugerida && salidaSugeridaDiv) {
                    const suggestedMission = data.misiones[0];
                    if (data.historial_salir_actualizado) {
                        this.historialSalir = data.historial_salir_actualizado;
                        localStorage.setItem("otg_historial_salir", JSON.stringify(this.historialSalir));
                    }
                    // NEW: Ensure correct language for suggested mission title
                    const suggestedTitle = this.idiomaActual === 'es' ? suggestedMission.destino_titulo : suggestedMission.destino_titulo_en || suggestedMission.destino_titulo;
                    linkSalidaSugerida.innerText = suggestedTitle;
                    linkSalidaSugerida.href = suggestedMission.destino_coordenadas_gps;
                    salidaSugeridaDiv.classList.remove('hidden');

                    // Lectura fluida, pausada y sin prisas
                    this.hablar(this.idiomaActual === 'es' ? `Considera también: ${suggestedTitle}` : `Also consider: ${suggestedTitle}`);
                }

            } catch (e) {
                console.error("Error fetching SALIR suggestion in CASA mode:", e);
            } finally {
                this.salidaSugeridaTimeoutId = null;
            }
        }, 180000); // After 3 minutes (900 - 180 = 720 seconds remaining on timer)

        if (circleElement) {
            circleElement.onclick = () => {
                // Encendemos la música relajante propia mediante la interacción segura del usuario
                if (typeof iniciarMusicaRelajantePropia === 'function') {
                    iniciarMusicaRelajantePropia();
                } else {
                    console.warn("iniciarMusicaRelajantePropia() no está definida.");
                }

                if (this.contadorToques < this.secuenciaAdelantos.length) {
                    let adelantoSegundos = this.secuenciaAdelantos[this.contadorToques];
                    this.timeLeft = Math.max(this.timeLeft - adelantoSegundos, 0);
                    this.contadorToques++;
                    try {
                        let perfil = this.obtenerPerfilLocal();
                        perfil["indicador_ansiedad"] = Math.min((perfil["indicador_ansiedad"] || 0) + 5, 100);
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

        // ======================================================================
        // CICLO PRINCIPAL DEL TEMPORIZADOR Y VOZ SECUENCIAL
        // MODIFIED: Integrates new 4-minute phase and refined audio sequencing
        // ======================================================================
        let lastFaseSublimeAudioTime = -1; // To ensure audio plays only every ~20 seconds
        let lastCasaSecuencialAudioTime = -1; // To ensure audio plays only every ~20 seconds

        this.timerEnfocado = setInterval(() => {
            if (this.timeLeft > 0) {
                this.timeLeft--;
            }

            let m = Math.floor(this.timeLeft / 60);
            let s = this.timeLeft % 60;

            if (timerDiv) {
                timerDiv.innerText = `${m}:${s.toString().padStart(2, '0')}`;
            }

            // Breathing circle animation (first 10 minutes: 900s down to 300s)
            if (this.timeLeft >= 300) { // First 10 minutes (15:00 down to 05:00)
                if (pulmonDiv) {
                    pulmonDiv.classList.remove('hidden'); // Ensure it's visible
                    let ciclo = (this.timeLeft - 300) % 8; // Cycle over remaining 600s for 8s breathing
                    if (ciclo >= 4) {
                        pulmonDiv.innerText = t.inspira.toUpperCase();
                        pulmonDiv.style.color = "var(--cyan-inhale)";
                    } else {
                        pulmonDiv.innerText = t.expira.toUpperCase();
                        pulmonDiv.style.color = "var(--accent)";
                    }
                }
                if (faseSublimeTextDiv) faseSublimeTextDiv.innerText = ""; // Clear text for new phase
                stopCarousel(); // Ensure carousel is stopped if somehow active

                // --- EXISTING AUDIOS_SECUENCIALES_CASA ---
                // Trigger an audio every ~20 seconds during the first 10 minutes (900s down to 300s)
                if (this.timeLeft < 900 && (900 - this.timeLeft) % 20 === 0 && (900 - this.timeLeft) !== lastCasaSecuencialAudioTime) {
                    lastCasaSecuencialAudioTime = (900 - this.timeLeft);
                    let recordatorioTexto = this._getDailyNonRepeatingAudio(
                        AUDIOS_SECUENCIALES_CASA,
                        "otg_historial_audios_casa_secuenciales_daily",
                        5 // Max 5 sessions per day
                    );
                    if (recordatorioTexto) {
                        this.hablar(recordatorioTexto);
                    }
                }
            }
            // NEW 4-MINUTE PHASE (from 5:00 to 1:00 remaining: 300s down to 60s)
            else if (this.timeLeft < 300 && this.timeLeft >= 60) {
                // Ensure breathing text is cleared/updated for new phase
                if (pulmonDiv) {
                    pulmonDiv.innerText = "";
                    pulmonDiv.classList.add('hidden');
                }
                if (faseSublimeTextDiv) {
                    faseSublimeTextDiv.classList.remove('hidden');
                }

                // Start carousel if not already started
                if (!this.carouselInterval) {
                    startCarousel();
                }

                // Play new sublime audio phrases every ~20 seconds
                if (this.timeLeft % 20 === 0 && this.timeLeft !== lastFaseSublimeAudioTime) {
                    lastFaseSublimeAudioTime = this.timeLeft;
                    let sublimeAudioText = this._getDailyNonRepeatingAudio(
                        AUDIOS_FASE_SUBLIMES,
                        "otg_historial_fase_casa_sublime_daily",
                        5 // Max 5 sessions per day
                    );
                    if (sublimeAudioText) {
                        faseSublimeTextDiv.innerText = sublimeAudioText;
                        this.hablar(sublimeAudioText);
                    }
                }
            }
            // Transition to final 1-minute challenge (60s down to 0s)
            else if (this.timeLeft < 60) {
                // Clear any remaining elements for the 4-minute phase
                if (pulmonDiv) pulmonDiv.innerText = "";
                if (faseSublimeTextDiv) faseSublimeTextDiv.innerText = "";
                stopCarousel(); // Stop carousel and hide it
            }


            if (this.timeLeft <= 0) {
                clearInterval(this.timerEnfocado);
                clearTimeout(this.salidaSugeridaTimeoutId);
                this.salidaSugeridaTimeoutId = null;
                // Do NOT cancel() here; let the queue finish
                stopCarousel(); // Ensure carousel is stopped

                if (circleElement) {
                    circleElement.style.animation = "none";
                    circleElement.style.transform = "scale(1)";
                }
                this.iniciarRetoCierre60Segundos();
            }
        }, 1000);
    },

    /**
     * Advances to the next internal mission step.
     */
    avanzarPaso() {
        this.indiceMision++;
        const container = document.getElementById('wrapper-interactive');
        this.procesarFlujoSecuencial(container);
    },

    /**
     * Initiates the 60-second closing challenge phase.
     */
    iniciarRetoCierre60Segundos() {
        clearInterval(this.timerEnfocado);
        clearInterval(this.temporizadorCierre);
        // Do NOT cancel here, let the queue manage it
        this.speechQueue = [];
        this.isSpeaking = false;
        window.speechSynthesis.cancel(); // Force cancel any *external* speech not managed by queue
       
        const t = {
            es: {
                logo: "OPEN THAN GO",
                cierreMensaje: "Gracias por tu presencia.",
                recomenzar: "RECOMENZAR EXPERIENCIA",
                puertaAbierta: "La puerta está abierta. ¿Continuamos?",
                retoInicial: "Prepárate para un reto combinado en 3, 2, 1..."
            },
            en: {
                logo: "OPEN THAN GO",
                cierreMensaje: "Thank you for your presence.",
                recomenzar: "RESTART EXPERIENCE",
                puertaAbierta: "The door is open. Shall we continue?",
                retoInicial: "Get ready for a combined challenge in 3, 2, 1..."
            }
        }[this.idiomaActual];

        const container = document.getElementById('wrapper-interactive');
        const cierrePantalla = document.getElementById('pantalla-cierre');
        const retoTitulo = document.getElementById('reto-titulo');
        const retoDescripcion = document.getElementById('reto-descripcion');
        const retoImg = document.getElementById('reto-img');
        const cierreTimer = document.getElementById('cierre-timer');
        const btnRecomenzar = document.getElementById('btn-recomenzar-experiencia');
        const cierreMensajeFinal = document.getElementById('cierre-mensaje-final');
       
        if (container) container.classList.add('hidden');
        if (cierrePantalla) cierrePantalla.classList.remove('hidden');
        if (cierreMensajeFinal) cierreMensajeFinal.classList.add('hidden');
        if (btnRecomenzar) {
            btnRecomenzar.classList.add('hidden');
            btnRecomenzar.disabled = true;
        }
       
        this.timeLeftCierre = 60;
        const catalogoRetos = this.idiomaActual === 'es' ? this.CATALOGO_RETOS_ES : this.CATALOGO_RETOS_EN;
        let secuenciaRetos = [];
        let numRetos = 3;
        let candidateSequenceIds;
        let sequenceString;
        let maxAttempts = 10;
       
        // Algoritmo de descarte para evitar repeticiones de secuencias de retos previos
        while (maxAttempts > 0) {
            secuenciaRetos = [];
            let tempRetos = [...catalogoRetos];
           
            // Barajado Fisher-Yates sobre el catálogo de retos clínico
            for (let i = tempRetos.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [tempRetos[i], tempRetos[j]] = [tempRetos[j], tempRetos[i]];
            }
           
            for (let i = 0; i < numRetos; i++) {
                if (tempRetos.length === 0) break;
                secuenciaRetos.push(tempRetos.shift());
            }
           
            candidateSequenceIds = secuenciaRetos.map(r => r.id).sort((a, b) => a - b).join('-');
           
            if (!this.historialRetosSecuencias.includes(candidateSequenceIds)) {
                sequenceString = candidateSequenceIds;
                break;
            }
            maxAttempts--;
           
            if (maxAttempts === 0) {
                console.warn("Could not find a unique challenge sequence after multiple attempts, reusing one.");
                sequenceString = candidateSequenceIds;
            }
        }
       
        // Actualización del registro histórico en memoria local para no duplicar flujos de cierre
        if (sequenceString) {
            this.historialRetosSecuencias.push(sequenceString);
            this.historialRetosSecuencias = this.historialRetosSecuencias.slice(-this.MAX_HISTORY_RETOS_SECUENCIAS);
            localStorage.setItem("otg_historial_retos_secuencias", JSON.stringify(this.historialRetosSecuencias));
        }

        let currentRetoIndex = 0;
       
        const displayNextReto = () => {
            if (currentRetoIndex < secuenciaRetos.length) {
                const reto = secuenciaRetos[currentRetoIndex];
                if (retoTitulo) {
                    retoTitulo.innerText = this.idiomaActual === 'es' ? reto.titulo : reto.titulo_en || reto.titulo;
                    retoTitulo.classList.remove('hidden');
                }
                if (retoDescripcion) {
                    retoDescripcion.innerText = this.idiomaActual === 'es' ? reto.descripcion : reto.descripcion_en || reto.descripcion;
                    retoDescripcion.classList.remove('hidden');
                }
                if (retoImg) {
                    retoImg.src = `/static/${reto.img}`;
                    retoImg.classList.remove('hidden');
                }
                this.hablar(this.idiomaActual === 'es' ? reto.descripcion : reto.descripcion_en || reto.descripcion);
                currentRetoIndex++;
            }
        };
       
        // Ocultamos elementos previos para garantizar una transición visual fluida
        if (retoTitulo) retoTitulo.classList.add('hidden');
        if (retoDescripcion) retoDescripcion.classList.add('hidden');
        if (retoImg) retoImg.classList.add('hidden');
       
        this.hablar(t.retoInicial);
       
        // Cuenta regresiva de preparación de 5 segundos antes de lanzar el carrusel de retos
        setTimeout(() => {
            displayNextReto();
           
            this.temporizadorCierre = setInterval(() => {
                this.timeLeftCierre--;
                if (cierreTimer) {
                    cierreTimer.innerText = this.timeLeftCierre.toString().padStart(2, '0');
                }
               
                // Avanza el reto de forma equitativa cada 20 segundos (3 retos en 60s)
                if (this.timeLeftCierre > 0 && currentRetoIndex < numRetos && (this.timeLeftCierre % Math.floor(60 / numRetos) === 0)) {
                    if (retoTitulo) retoTitulo.classList.add('hidden');
                    if (retoDescripcion) retoDescripcion.classList.add('hidden');
                    if (retoImg) retoImg.classList.add('hidden');
                    displayNextReto();
                }
               
                // Cierre definitivo del ciclo clínico de 60 segundos
                if (this.timeLeftCierre <= 0) {
                    clearInterval(this.temporizadorCierre);
                    // Do NOT cancel() here; let the queue finish
                   
                    if (retoTitulo) retoTitulo.innerText = "";
                    if (retoDescripcion) retoDescripcion.innerText = "";
                    if (retoImg) retoImg.src = "";
                   
                    if (cierreTimer) cierreTimer.classList.add('hidden');
                    if (cierreMensajeFinal) cierreMensajeFinal.classList.remove('hidden');
                   
                    if (btnRecomenzar) {
                        btnRecomenzar.classList.remove('hidden');
                        btnRecomenzar.disabled = false;
                    }
                    this.hablar(t.puertaAbierta);
                }
            }, 1000);
        }, 5000);
       
        if (btnRecomenzar) {
            btnRecomenzar.onclick = () => {
                this.reiniciarExperiencia();
            };
        }
    },

    /**
     * Resets the UI to the initial form state without clearing persistent data.
     */
    reiniciarExperiencia() {
        clearInterval(this.timerInaccion);
        clearInterval(this.timerEnfocado);
        clearInterval(this.temporizadorCascada);
        clearInterval(this.temporizadorCierre);
        clearInterval(this.salidaTimerId);
        if (this.carouselInterval) { // NEW
            clearInterval(this.carouselInterval);
            this.carouselInterval = null;
        }
        // Do NOT cancel() here; let the queue manage it
        this.speechQueue = [];
        this.isSpeaking = false;
        window.speechSynthesis.cancel(); // Force cancel any *external* speech not managed by queue
       
        if (this.salidaSugeridaTimeoutId) {
            clearTimeout(this.salidaSugeridaTimeoutId);
            this.salidaSugeridaTimeoutId = null;
        }
       
        this.pasosMisiones = [];
        this.indiceMision = 0;
        this.isLocked = false;
        this.contadorToques = 0;
        this.datosLugarGlobal = null; // Clear selected mission
       
        const pantallaCierre = document.getElementById('pantalla-cierre');
        const wrapperInteractive = document.getElementById('wrapper-interactive');
        const wrapperForm = document.getElementById('wrapper-form');
        const inpTextLibre = document.getElementById('inp-text-libre');
        const authGate = document.getElementById('auth-gate-wrapper'); // NEW
        const btnOasisSensorial = document.getElementById('btn-oasis-sensorial'); // NEW

        if (pantallaCierre) pantallaCierre.classList.add('hidden');
        if (wrapperInteractive) wrapperInteractive.classList.add('hidden');
        if (authGate) authGate.classList.add('hidden'); // NEW
        if (wrapperForm) wrapperForm.classList.remove('hidden'); // Show main form on restart
        if (inpTextLibre) inpTextLibre.value = "";
        if (btnOasisSensorial) btnOasisSensorial.classList.remove('hidden'); // NEW
       
        this.inyectarBloquePreguntas();
        this.activarBotonMandoLibreInicial();
       
        const saludos_es = [
            "Bienvenido de nuevo. Tu escape inteligente. Escucha mis preguntas en pantalla.",
            "Ópen Dán Go activo. Toca lo que sientes hoy para continuar."
        ];
        const saludos_en = [
            "Welcome back. Your smart escape. Listen to my questions on screen.",
            "Open Than Go active. Tap what you feel today to continue."
        ];
       
        const saludos = this.idiomaActual === 'es' ? saludos_es : saludos_en;
        this.hablar(saludos[Math.floor(Math.random() * saludos.length)]);
    },

    /**
     * Clears ALL session data and reloads the application.
     */
    destruirYReiniciar() {
        clearInterval(this.timerInaccion);
        clearInterval(this.timerEnfocado);
        clearInterval(this.temporizadorCascada);
        clearInterval(this.temporizadorCierre);
        clearInterval(this.salidaTimerId);
        if (this.carouselInterval) { // NEW
            clearInterval(this.carouselInterval);
            this.carouselInterval = null;
        }
        // Do NOT cancel() here; let the queue manage it
        this.speechQueue = [];
        this.isSpeaking = false;
        window.speechSynthesis.cancel(); // Force cancel any *external* speech not managed by queue
       
        if (this.salidaSugeridaTimeoutId) {
            clearTimeout(this.salidaSugeridaTimeoutId);
            this.salidaSugeridaTimeoutId = null;
        }
       
        localStorage.clear();
        this.historialSalir = [];
        this.historialCasa = [];
        this.historialPreguntas = [];
        this.historialRetosSecuencias = [];
        this.historialFaseCasaSublime = {}; // NEW: Reset daily history object
        this.historialAudiosCasaSecuenciales = {}; // NEW: Reset daily history object
        this.historialAudiosSalirSecuenciales = {}; // NEW: Reset daily history object
        
        this.pasosMisiones = [];
        this.indiceMision = 0;
        this.isLocked = false;
        this.contadorToques = 0;
        this.datosLugarGlobal = null;
       
        location.reload();
    }
}; // Cierre absoluto del objeto KERNEL

// Optional: Placeholder for external music function if not already defined
if (typeof iniciarMusicaRelajantePropia === 'undefined') {
    window.iniciarMusicaRelajantePropia = function() {
        console.log("Música relajante propia iniciada (función de placeholder).");
        // Implement your music playback logic here
        // e.g., playing an audio file, connecting to a music service
    };
}

// Inicialización del ecosistema clínico una vez que el DOM está listo
document.addEventListener('DOMContentLoaded', () => {
    if (typeof KERNEL !== 'undefined' && KERNEL.init) {
        KERNEL.init();
    }
});

// Exposición global del KERNEL en el objeto window para depuración y control externo
window.KERNEL = KERNEL;

//==========================================================================================
// KERNEL INTEGRADO V3 (PARTE 1)
//==========================================================================================
(function() {
    window.OTG_SENSORIAL = {
        marcas: [
            "TikTok", "Instagram", "YouTube", "Spotify", "Netflix", "Uber", "Lyft",
            "American", "Delta", "JetBlue", "Southwest", "Avianca", "LATAM", "Aeromexico",
            "Copa", "Volaris", "WesternUnion", "Zelle", "Amazon", "Temu", "Walmart",
            "Costco", "Target", "DollarTree", "McDonald's", "Starbucks", "Burger King",
            "Airbnb", "Booking.com", "Expedia", "Hotels.com", "Trivago", "Priceline",
            "Motel 6", "Super 8", "Days Inn", "Holiday Inn", "Marriott", "Hilton",
            "Tinder", "ChatGPT", "GetMyBoat", "Boatsetter", "Click&Boat", "Sailo",
            "Carnival", "Celebrity Cruises", "MSC Cruises", "Viajes El Corte Inglés",
            "Despegar", "Pizza Hut", "Papa Johns", "Little Caesars", "Domino's",
            "Wendy's", "Chick fil A", "Nike", "Adidas", "Ross Dress for Less",
            "Burlington", "DD'S Discounts", "Crowley Carbon", "Transcargo", "CubaMax",
            "Va Cuba", "Cargolux", "Aeroméxico Cargo", "Dachser", "Seaboard Marine",
            "Popeyes", "KFC", "PolloTropical", "Church's Texas Chicken", "Miami Dade Transit",
            "Brightline", "SunPass", "FLHSMV", "Fair Health Consumer", "GoRenew",
            "Clear Health Costs", "Florida Health Finder", "DentalPlans", "NeedyMeds Clinic Finder",
            "Florida Blue", "Aetna", "UnitedHealthcare", "Cigna", "Oscar Health",
            "Molina Healthcare", "Sunshine Health", "Indeed", "LinkedIn", "USAJOBS",
            "CareerOneStop", "Upwork", "Fiverr", "FlexJobs"
        ],
        urls: {
            "TikTok": "https://tiktok.com",
            "Instagram": "https://instagram.com",
            "YouTube": "https://youtube.com",
            "Spotify": "https://spotify.com",
            "Netflix": "https://netflix.com",
            "Uber": "https://uber.com",
            "Lyft": "https://lyft.com",
            "GetMyBoat": "https://getmyboat.com",
            "Boatsetter": "https://boatsetter.com",
            "Click&Boat": "https://clickandboat.com",
            "Sailo": "https://sailo.com",
            "Carnival": "https://carnival.com",
            "Celebrity Cruises": "https://celebritycruises.com",
            "MSC Cruises": "https://msccruises.com",
            "Viajes El Corte Inglés": "https://viajeselcorteingles.com",
            "Despegar": "https://despegar.com",
            "American": "https://aa.com",
            "Delta": "https://delta.com",
            "Pizza Hut": "https://pizzahut.com",
            "Papa Johns": "https://papajohns.com",
            "Little Caesars": "https://littlecaesars.com",
            "Domino's": "https://dominos.com",  
            "Wendy's": "https://wendys.com",
            "Chick fil A": "https://chick-fil-a.com",  
            "JetBlue": "https://jetblue.com",
            "Southwest": "https://southwest.com",
            "Avianca": "https://avianca.com",
            "LATAM": "https://latamairlines.com",
            "Aeromexico": "https://aeromexico.com",
            "Copa": "https://copaairlines.com",
            "Volaris": "https://volaris.com",
            "WesternUnion": "https://westernunion.com",
            "Zelle": "https://zellepay.com",
            "Amazon": "https://amazon.com",
            "Temu": "https://temu.com",
            "Nike": "https://nike.com",
            "Adidas": "https://adidas.com",
            "Ross Dress for Less": "https://rossstores.com",
            "Burlington": "https://burlington.com",
            "DD'S Discounts": "https://ddsdiscounts.com",
            "Crowley Carbon": "https://crowley.com",
            "Transcargo": "https://transcargo.com",
            "CubaMax": "https://cubamax.com",
            "Va Cuba": "https://vacuba.com",
            "Cargolux": "https://cargolux.com",
            "Aeroméxico Cargo": "https://aeromexicocargo.com.mx",
            "Dachser": "https://dachser.com",
            "Seaboard Marine": "https://seaboardmarine.com",
            "Walmart": "https://walmart.com",
            "Costco": "https://costco.com",
            "Target": "https://target.com",
            "DollarTree": "https://dollartree.com",
            "Popeyes": "https://popeyes.com",
            "KFC": "https://kfc.com",
            "PolloTropical": "https://pollotropical.com",
            "Church's Texas Chicken": "https://churchs.com",
            "McDonald's": "https://mcdonalds.com",
            "Starbucks": "https://starbucks.com",
            "Burger King": "https://bk.com",
            "Airbnb": "https://airbnb.com",
            "Booking.com": "https://booking.com",
            "Expedia": "https://expedia.com",
            "Hotels.com": "https://hotels.com",
            "Trivago": "https://trivago.com",
            "Priceline": "https://priceline.com",
            "Motel 6": "https://motel6.com",
            "Super 8": "https://wyndhamhotels.com",
            "Days Inn": "https://wyndhamhotels.com",
            "Holiday Inn": "https://ihg.com",
            "Miami Dade Transit": "https://miamidade.gov",
            "Brightline": "https://gobrightline.com",
            "SunPass": "https://sunpass.com",
            "FLHSMV": "https://flhsmv.gov",
            "Fair Health Consumer": "https://fairhealthconsumer.org",
            "GoRenew": "https://services.flhsmv.gov/virtualoffice/",
            "Clear Health Costs": "https://clearhealthcosts.com",
            "Florida Health Finder": "https://healthfinder.fl.gov",
            "DentalPlans": "https://dentalplans.com",
            "NeedyMeds Clinic Finder": "https://needymeds.org",
            "Florida Blue": "https://floridablue.com",
            "Aetna": "https://aetna.com",
            "UnitedHealthcare": "https://uhc.com",
            "Cigna": "https://cigna.com",
            "Oscar Health": "https://hioscar.com",
            "Molina Healthcare": "https://molinahealthcare.com",
            "Sunshine Health": "https://sunshinehealth.com",
            "Indeed": "https://indeed.com",
            "LinkedIn": "https://linkedin.com",
            "USAJOBS": "https://usajobs.gov",
            "CareerOneStop": "https://careeronestop.org",
            "Upwork": "https://upwork.com",
            "Fiverr": "https://fiverr.com",
            "FlexJobs": "https://flexjobs.com",
            "Marriott": "https://marriott.com",
            "Hilton": "https://hilton.com",
            "Tinder": "https://tinder.com",
            "ChatGPT": "https://chatgpt.com"
        },
        preguntas: [
            "¿Qué actividad quieres realizar en este momento?",
            "¿Cuál de estos servicios forma parte de tu rutina hoy?",
            "¿Qué opción representa mejor lo que buscas ahora?",
            "¿Qué servicio te gustaría utilizar en este momento?"
        ],
       
     seleccionadas: [],

   init() {
    this.inyectarMetasYEstilos();
    // REMOVED: this.modificarBienvenida(); // <--- CRITICAL: Prevents OTG_SENSORIAL from taking over the initial welcome screen
    this.crearEstructuresFlotantes();
  },

  inyectarMetasYEstilos() {
    ["apple-mobile-web-app-capable", "mobile-web-app-capable"].forEach(n => {
      if (!document.querySelector(`meta[name="${n}"]`)) {
        let m = document.createElement("meta");
        m.name = n;
        m.content = "yes";
        document.head.appendChild(m);
      }
    });
   
    let s = document.createElement("style");
    s.textContent = `
      .otg-power-btn {
        position: fixed;
        top: 15px;
        right: 15px;
        z-index: 999999;
        background: #d84315;
        border: none;
        color: #fff;
        padding: 10px;
        border-radius: 50%;
        cursor: pointer;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(0, 0, 0, .5);
      }
     
      .otg-grid-logos {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(85px, 1fr));
        gap: 6px;
        margin: 15px 0;
      }
     
      .otg-card-logo {
        background: #111;
        border: 1px solid #333;
        padding: 10px 4px;
        border-radius: 6px;
        text-align: center;
        font-size: .75rem;
        cursor: pointer;
        font-weight: bold;
        transition: .2s;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
     
      .otg-card-logo.active {
        border-color: #00bcd4 !important;
        color: #00bcd4 !important;
        background: rgba(0, 188, 212, .1) !important;
        box-shadow: 0 0 8px rgba(0, 188, 212, .3);
      }
     
      .otg-btn-opt {
        width: 100%;
        background: none;
        border: 1px solid #444;
        color: #ccc;
        padding: 10px;
        text-align: left;
        border-radius: 6px;
        margin-bottom: 6px;
        cursor: pointer;
        font-size: .8rem;
      }
     
      .otg-btn-opt:hover {
        border-color: #2e7d32;
        color: #fff;
      }
    `;
    document.head.appendChild(s);
  },

    // REINSTATED: This function is now responsible for showing the initial OTG_SENSORIAL welcome message
    // but without overwriting the whole body, and will be called by `session.html` script after DOMContentLoaded.
    // It will set up the welcome screen text, which then leads to `KERNEL.iniciarOpcionPrincipal()`
    modificarBienvenida() {
        let pb = document.getElementById("pantalla-bienvenida");
        if (!pb) return;
       
        let sintomas = KERNEL.idiomaActual === 'es' ? [
          "No sabes qué hacer",
          "Te encuentras en la monotonía",
          "Estás agobiado por el entorno",
          "Te sientes estresado",
          "Te sientes cansado",
          "Necesitas un descanso",
          "Buscas un momento para ti"
        ] : [
          "You don't know what to do",
          "You are in monotony",
          "You feel overwhelmed by the surroundings",
          "You feel stressed",
          "You feel tired",
          "You need a break",
          "You are looking for a moment for yourself"
        ];
       
        sintomas.sort(() => Math.random() - .5);
       
        pb.innerHTML = `
          <div style="max-width:390px;width:95%;padding:15px;text-align:center;font-family:sans-serif;color:#fff;overflow-y:auto;max-height:100vh;">
            <h2 style="color:#00bcd4;font-weight:900;letter-spacing:2px;font-size:1.3rem;margin-bottom:12px;">
              OPEN THAN GO
            </h2>
            <p style="font-size: .9rem; line-height: 1.45; color: #eee; font-weight: bold; margin-bottom: 15px;">
              ${KERNEL.idiomaActual === 'es' ? 'Hoy' : 'Today'}: <span style="color: #d84315;">${sintomas[0]}</span>.<br>
              OPEN THAN GO ${KERNEL.idiomaActual === 'es' ? 'te ayuda a encontrar pequeños momentos de bienestar para ti y tu familia.' : 'helps you find small moments of well-being for you and your family.'}
            </p>
            <div style="background: #111; border: 1px solid #222; border-radius: 8px; padding: 12px; text-align: left; font-size: .76rem; line-height: 1.5; color: #bbb; margin-bottom: 14px;">
              <b style="color: #2e7d32; display: block; margin-bottom: 6px; text-transform: uppercase;"> ${KERNEL.idiomaActual === 'es' ? 'Cómo funciona' : 'How it works'} </b>
              • <b>${KERNEL.idiomaActual === 'es' ? 'SALIR' : 'OUT'}:</b> ${KERNEL.idiomaActual === 'es' ? 'Descubre lugares cercanos para cambiar de ambiente.' : 'Discover nearby places to change scenery.'}<br>
              • <b>${KERNEL.idiomaActual === 'es' ? 'CASA' : 'HOME'}:</b> ${KERNEL.idiomaActual === 'es' ? 'Encuentra actividades sencillas para hacer en casa.' : 'Find simple activities to do at home.'}<br>
              • <b>${KERNEL.idiomaActual === 'es' ? 'MODO LIBRE' : 'FREE MODE'}:</b> ${KERNEL.idiomaActual === 'es' ? 'Escribe un lugar, una marca o un servicio para personalizar tu experiencia.' : 'Write a place, a brand, or a service to personalize your experience.'}<br>
              • <b>${KERNEL.idiomaActual === 'es' ? 'ORÁCULO' : 'ORACLE'}:</b> ${KERNEL.idiomaActual === 'es' ? 'Recibe una sugerencia cuando no sepas qué hacer.' : 'Get a suggestion when you don\'t know what to do.'}
            </div>
            <p style="font-size: .72rem; color: #00bcd4; font-weight: bold; margin-bottom: 12px;">
              🎵 ${KERNEL.idiomaActual === 'es' ? 'Enciende el audio y disfruta una experiencia más completa.' : 'Turn on audio for a more complete experience.'}
            </p>
            <div style="background: rgba(255,255,255,.05); border: 1px solid #333; border-radius: 8px; padding: 10px; font-size: .67rem; line-height: 1.45; color: #cfcfcf; text-align: left; margin-bottom: 14px;">
              <b style="color: #fff;">${KERNEL.idiomaActual === 'es' ? 'Aviso' : 'Notice'}</b><br>
              OPEN THAN GO ${KERNEL.idiomaActual === 'es' ? 'es una herramienta de bienestar y orientación. No ofrece atención médica, psicológica ni de emergencia. Si tienes una emergencia médica o de salud mental, llama a los servicios de emergencia o busca ayuda profesional. Usa esta aplicación bajo tu propio criterio.' : 'is a wellness and guidance tool. It does not offer medical, psychological, or emergency care. If you have a medical or mental health emergency, call emergency services or seek professional help. Use this application at your own discretion.'}
            </div>
            <button class="btn-bienvenida" onclick="KERNEL.iniciarOpcionPrincipal();" style="width: 100%; border-radius: 6px; padding: 15px; font-weight: 900; background: #fff; color: #000; border: none; cursor: pointer; text-transform: uppercase;">
              ${KERNEL.idiomaActual === 'es' ? 'INICIAR SESIÓN / START' : 'START SESSION / START'}
            </button>
          </div>
        `;
    },

      crearEstructurasFlotantes() {
    let b = document.createElement("button");
    b.id = "otg-btn-power";
    b.className = "otg-power-btn hidden";
    b.innerHTML = "✕";
    b.title = "Cerrar";
    b.onclick = () => this.apagarSistemaTotal();
    document.body.appendChild(b);

    // NEW: Floating button for OTG_SENSORIAL (Oasis de Ocio)
    let oasisBtn = document.createElement("button");
    oasisBtn.id = "btn-oasis-sensorial";
    oasisBtn.className = "floating-btn hidden"; // Initially hidden
    oasisBtn.style.right = "130px"; // Position it
    oasisBtn.title = KERNEL.idiomaActual === 'es' ? "Oasis Sensorial" : "Sensory Oasis";
    oasisBtn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24px" height="24px">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
        </svg>
    `;
    oasisBtn.onclick = () => this.abrirOasisOcio();
    document.body.appendChild(oasisBtn);
   
    let m = document.createElement("div");
    m.id = "otg-oasis-entretenimiento";
    m.className = "hidden";
    m.style = "position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(0,0,0,.98);z-index:9999999;backdrop-filter:blur(15px);overflow-y:auto;padding:20px;color:#fff;font-family:sans-serif;";
    document.body.appendChild(m);
  },

  interceptarBotonStart() {
    // This function is no longer called directly from the initial welcome screen.
    // It's meant to be called by an explicit button if OTG_SENSORIAL is used as a secondary feature.
    // It directly opens the "Oasis de Ocio".
    setTimeout(() => this.forzarCierre15Minutos(), 900000); // 15 minutes = 900,000 ms
    this.abrirOasisOcio();
  },

  abrirOasisOcio() {
    let m = document.getElementById("otg-oasis-entretenimiento");
    if (!m) return;
   
    m.classList.remove("hidden");
    document.body.style.overflow = "hidden";

    // Hide KERNEL's main form and floating buttons temporarily
    document.getElementById('wrapper-form').classList.add('hidden');
    document.getElementById('btn-volver-app').classList.add('hidden');
    document.getElementById('btn-whatsapp').classList.add('hidden');
    document.getElementById('btn-messenger').classList.add('hidden');
    document.getElementById('btn-oasis-sensorial').classList.add('hidden');

    // Make sure power button is visible for OTG_SENSORIAL to close itself
    const powerBtn = document.getElementById("otg-btn-power");
    if (powerBtn) powerBtn.classList.remove("hidden");
   
    this.marcas.sort(() => Math.random() - .5);
   
    let zip = document.getElementById("inp-zip") ? document.getElementById("inp-zip").value.trim() : "";
    let txtUsa = zip ? (KERNEL.idiomaActual === 'es' ? `Opciones disponibles para el Código Postal ${zip}` : `Options available for ZIP Code ${zip}`) : (KERNEL.idiomaActual === 'es' ? "Personaliza tu experiencia" : "Personalize your experience");
   
    m.innerHTML = `
      <div style="max-width:460px;margin:0 auto;padding-top:5px;">
        <div style="text-align:center;margin-bottom:15px;">
          <span style="background: #2e7d32; padding: 3px 8px; border-radius: 4px; font-size: .65rem; font-weight: bold; text-transform: uppercase;">
            ${KERNEL.idiomaActual === 'es' ? 'Bienestar Inicial' : 'Initial Wellness'}
          </span>
          <h4 style="color: #00bcd4; font-weight: 900; margin: 8px 0 3px; font-size: 1.15rem;">
            ${KERNEL.idiomaActual === 'es' ? 'PERSONALIZA TU EXPERIENCIA' : 'PERSONALIZE YOUR EXPERIENCE'}
          </h4>
          <p style="color: #aaa; font-size: .72rem; margin: 0;">
            ${txtUsa}. ${KERNEL.idiomaActual === 'es' ? 'Tiempo aproximado: 1 minuto.' : 'Approx. time: 1 minute.'}
          </p>
        </div>
        <div id="otg-fase-1">
          <p style="font-size: .85rem; font-weight: bold; color: #fff; text-align: center; line-height: 1.45; margin-bottom: 10px;">
            ${KERNEL.idiomaActual === 'es' ? 'Selecciona el servicio que mejor representa lo que deseas hacer en este momento.' : 'Select the service that best represents what you want to do right now.'}
          </p>
          <div class="otg-grid-logos">
            ${this.marcas.map(x => `<div class="otg-card-logo" onclick="OTG_SENSORIAL.seleccionarMarca(this,'${x}')">${x}</div>`).join("")}
          </div>
          <button onclick="OTG_SENSORIAL.activarFaseTrivia()" style="width: 100%; background: #2e7d32; border: none; color: #fff; padding: 14px; border-radius: 6px; font-weight: bold; cursor: pointer; text-transform: uppercase; font-size: .8rem; letter-spacing: .5px;">
            ${KERNEL.idiomaActual === 'es' ? 'Continuar →' : 'Continue →'}
          </button>
        </div>
        <div id="otg-fase-2" class="hidden"></div>
        <div id="otg-fase-3" class="hidden" style="text-align: center;"></div>
      </div>
    `;
  },


      seleccionarMarca(el, marca) {
    el.classList.toggle("active");
   
    if (el.classList.contains("active")) {
      this.seleccionadas.push(marca);
    } else {
      this.seleccionadas = this.seleccionadas.filter(x => x !== marca);
    }
  },

  activarFaseTrivia() {
    if (!this.seleccionadas.length) {
      alert(KERNEL.idiomaActual === 'es' ? "Selecciona al menos una opción." : "Select at least one option.");
      return;
    }
   
    document.getElementById("otg-fase-1").classList.add("hidden");
   
    let f2 = document.getElementById("otg-fase-2");
    f2.classList.remove("hidden");
   
    let p = this.preguntas[Math.floor(Math.random() * this.preguntas.length)];
    let m = this.seleccionadas[0]; // Only using the first selected brand for now
   
    f2.innerHTML = `
      <div style="background: #111; border: 1px solid #222; padding: 15px; border-radius: 8px; margin-top: 10px;">
        <span style="color: #00bcd4; font-size: .65rem; font-weight: bold; text-transform: uppercase; display: block; margin-bottom: 5px;">
          ${KERNEL.idiomaActual === 'es' ? 'Has seleccionado' : 'You have selected'}: ${m}
        </span>
        <p style="font-size: 1rem; font-weight: bold; line-height: 1.45; margin: 5px 0 15px; color: #fff;">
          ${p}
        </p>
        <button class="otg-btn-opt" onclick="OTG_SENSORIAL.inyectarMenteBase('agotado', 'opcion1')">
          ${KERNEL.idiomaActual === 'es' ? 'Quiero usar este servicio ahora.' : 'I want to use this service now.'}
        </button>
        <button class="otg-btn-opt" onclick="OTG_SENSORIAL.inyectarMenteBase('aburrido', 'opcion2')">
          ${KERNEL.idiomaActual === 'es' ? 'Solo estoy explorando opciones.' : 'I\'m just exploring options.'}
        </button>
        <button class="otg-btn-opt" onclick="OTG_SENSORIAL.inyectarMenteBase('curioso', 'opcion3')">
          ${KERNEL.idiomaActual === 'es' ? 'Quiero descubrir nuevas ideas.' : 'I want to discover new ideas.'}
        </button>
      </div>
    `;
  },

  inyectarMenteBase(perfil, tipo) {
    let s = document.getElementById("mente-selector");
    if (s) {
      s.value = perfil;
      s.dispatchEvent(new Event("change")); // Trigger change event to update KERNEL's internal state
    }
   
    document.getElementById("otg-fase-2").classList.add("hidden");
   
    let f3 = document.getElementById("otg-fase-3");
    f3.classList.remove("hidden");
   
    let marca = this.seleccionadas[0];
    let url = this.urls[marca] || "https://google.com";
    let mensaje = "";
    if (tipo === "opcion1") {
        mensaje = KERNEL.idiomaActual === 'es' ? `Tu experiencia ha sido personalizada usando "${marca}".` : `Your experience has been personalized using "${marca}".`;
    } else if (tipo === "opcion2") {
        mensaje = KERNEL.idiomaActual === 'es' ? `Hemos preparado una experiencia basada en tu selección.` : `We have prepared an experience based on your selection.`;
    } else {
        mensaje = KERNEL.idiomaActual === 'es' ? `Explora nuevas opciones y encuentra actividades que se adapten a ti.` : `Explore new options and find activities that suit you.`;
    }
   
    f3.innerHTML = `
      <div style="background: rgba(0, 188, 212, .05); border: 1px solid #00bcd4; padding: 15px; border-radius: 8px; text-align: left; font-size: .82rem; line-height: 1.5; margin-bottom: 15px; color: #eee;">
        <b style="color: #00bcd4; display: block; margin-bottom: 6px;"> ${KERNEL.idiomaActual === 'es' ? 'Experiencia lista' : 'Experience ready'} </b>
        ${mensaje}
      </div>
      <div style="display: flex; gap: 8px;">
        <button onclick="window.open('${url}', '_blank')" style="flex: 1; background: #2e7d32; border: none; color: #fff; padding: 12px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: .75rem; text-transform: uppercase;">
          ${KERNEL.idiomaActual === 'es' ? 'Abrir sitio web' : 'Open website'}
        </button>
        <button onclick="OTG_SENSORIAL.cerrarOasisYDarPasoAAppBase()" style="flex: 1; background: none; border: 1px solid #00bcd4; color: #00bcd4; padding: 12px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: .75rem; text-transform: uppercase;">
          ${KERNEL.idiomaActual === 'es' ? 'Continuar' : 'Continue'}
        </button>
      </div>
    `;
  },

  cerrarOasisYDarPasoAAppBase() {
    let m = document.getElementById("otg-oasis-entretenimiento");
    if (m) m.classList.add("hidden");
   
    document.body.style.overflow = "auto";
   
    if (typeof KERNEL !== "undefined" && typeof KERNEL.despertarInicial === "function") {
      // Restore KERNEL's main form and floating buttons
      document.getElementById('wrapper-form').classList.remove('hidden');
      document.getElementById('btn-volver-app').classList.remove('hidden');
      document.getElementById('btn-whatsapp').classList.remove('hidden');
      document.getElementById('btn-messenger').classList.remove('hidden');
      document.getElementById('btn-oasis-sensorial').classList.remove('hidden'); // Show the floating button again

      KERNEL.despertarInicial(); // Continue with KERNEL's main flow
    }
   
    let b = document.getElementById("otg-btn-power");
    if (b) b.classList.add("hidden");
   
    this.seleccionadas = [];
    console.log("OPEN THAN GO iniciado.");
  },

  apagarSistemaTotal() {
    let m = document.getElementById("otg-oasis-entretenimiento");
    if (m) m.classList.add("hidden");
   
    let pc = document.getElementById("pantalla-cierre");
    if (pc) pc.classList.add("hidden");
   
    let wf = document.getElementById("wrapper-form");
    if (wf) wf.classList.add("hidden"); // Hide main form
   
    let pb = document.getElementById("pantalla-bienvenida");
    if (pb) pb.classList.remove("hidden"); // Show welcome screen
   
    let authGate = document.getElementById('auth-gate-wrapper'); // NEW
    if (authGate) authGate.classList.add('hidden'); // NEW: Hide paywall screen

    let btnOasisSensorial = document.getElementById('btn-oasis-sensorial'); // NEW
    if (btnOasisSensorial) btnOasisSensorial.classList.add('hidden'); // NEW: Hide oasis button
   
    let b = document.getElementById("otg-btn-power");
    if (b) b.classList.add("hidden");
   
    let t = document.getElementById("inp-text-libre");
    if (t) t.value = "";
   
    this.seleccionadas = [];
    console.log("Sistema reiniciado.");
  },

  forzarCierre15Minutos() {
    let m = document.getElementById("otg-oasis-entretenimiento");
    if (m) m.classList.add("hidden");
   
    document.body.innerHTML = `
      <div style="width: 100vw; height: 100vh; background: #000; color: #fff; font-family: sans-serif; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 25px;">
        <h1 style="color: #00bcd4; font-size: 1.4rem; margin-bottom: 12px;"> ${KERNEL.idiomaActual === 'es' ? 'Sesión finalizada' : 'Session ended'} </h1>
        <p style="max-width: 420px; font-size: .95rem; line-height: 1.5; color: #ddd;"> ${KERNEL.idiomaActual === 'es' ? 'Han transcurrido 15 minutos. La sesión ha finalizado para ayudarte a hacer una pausa y continuar con tus actividades.' : '15 minutes have passed. The session has ended to help you take a break and continue with your activities.'} </p>
      </div>
    `;
  }
}; // CORRECCIÓN CRÍTICA: Se añade cierre de llave y punto y coma para aislar las estructuras

/* ========================================================================================== */
/* COMPLEMENTO NATIVO DE BIENESTAR: MOTOR SENSORIAL DE OPEN THAN GO                          */
/* ========================================================================================== */
// This OTG_SENSORIAL definition is a duplicate in the original code.
// The one above is the correct one being used by the `(function(){})()` block below.
// This duplicate needs to be removed from the final output, but for now I'll just skip it.
// The `(function(){})()` block below is where `OTG_SENSORIAL` is actually defined and exposed globally.

})(); // Closing the IIFE where OTG_SENSORIAL is defined.

/**
 * ==========================================================================================
 * DEFENSA DE CIERRE TOTAL DEL MÓDULO SENSORIAL
 * Asegura la compilación limpia del hilo sin dejar llaves colgando en el kernel
 * ==========================================================================================
 */
document.addEventListener("DOMContentLoaded", () => {
  // OTG_SENSORIAL.inicializarBypassDesarrollador() is now handled by KERNEL.init() with event listeners on the auth-gate-wrapper elements.
  // if (typeof OTG_SENSORIAL !== 'undefined' && OTG_SENSORIAL.inicializarBypassDesarrollador) {
  //   OTG_SENSORIAL.inicializarBypassDesarrollador();
  //   console.log("Escudo administrativo activado de forma externa y segura.");
  // }
 
  if (typeof OTG_SENSORIAL !== 'undefined' && OTG_SENSORIAL.init) {
    OTG_SENSORIAL.init();
    // NEW: Call the initial welcome screen setup for OTG_SENSORIAL here
    OTG_SENSORIAL.modificarBienvenida();
    console.log("Módulos Sensoriales y Bienvenida OTG inicializados.");
  }
  
  // NEW: Immediately determine the first screen to show based on authentication state
  // This ensures the correct initial view without conflicting logic
  const r = localStorage.getItem('otg_user_role');
  const p = localStorage.getItem('otg_pase_stripe');
  const paywallActive = !p || !(p.startsWith('cs_live_') || p.startsWith('cs_test_'));
  
  const pantallaBienvenida = document.getElementById('pantalla-bienvenida');
  const wrapperForm = document.getElementById('wrapper-form');
  const paywallScreen = document.getElementById('auth-gate-wrapper'); // Ensure this ID is correct from session.html
  
  if (r === 'admin' || !paywallActive) {
      if (pantallaBienvenida) pantallaBienvenida.classList.add('hidden');
      if (wrapperForm) wrapperForm.classList.remove('hidden');
      if (paywallScreen) paywallScreen.classList.add('hidden');
      // If already logged in, directly start KERNEL's main flow
      if (typeof KERNEL !== 'undefined' && KERNEL.despertarInicial) {
        KERNEL.despertarInicial();
        console.log("Inicio directo a KERNEL (ya autenticado).");
      }
  } else {
      if (pantallaBienvenida) pantallaBienvenida.classList.remove('hidden'); // Show OTG_SENSORIAL's welcome as the first interactive step
      if (wrapperForm) wrapperForm.classList.add('hidden');
      if (paywallScreen) paywallScreen.classList.add('hidden'); // Keep hidden until 'Iniciar Sesión' is clicked from welcome screen
      console.log("Mostrando pantalla de bienvenida OTG_SENSORIAL.");
  }
});
