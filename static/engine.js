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
        lastRecommendationId: null, // Corrected: Store the ID of the last recommendation
        
        // Sequential Conversational Architecture
        bloqueActual: 0, // Current block of questions being displayed
        conteoInaccion: 0, // Inaction counter for advancing question blocks
        indicePreguntaCascada: 0, // Index for fading out questions

        // Default template for the 19 human needs profile (must align with backend)
        // NOTE: This is duplicated in backend for quick access. For larger projects,
        // consider a shared configuration file or API endpoint to ensure canonical definition.
        DEFAULT_NECESSITY_PROFILE: {
            "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50,
            "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50,
            "juego": 50, "contemplacion": 50, "trabajo": 50, "descanso": 50, "organizacion": 50,
            "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50,
            "indicador_ansiedad": 0 // Special internal indicator, not a "need" for location matching
        },
    
        // Corrected: Separate question catalogs for each language
        CATALOGO_PREGUNTAS_ES: [
            // Bloque 1: El Bucle Digital Urbano (Facebook, YouTube, Spotify y Amazon)
            "¿Abres Facebook por inercia para ver vidas falsas y compararlas con tu rutina gris?",
            "¿Te quedas dormido viendo videos en YouTube que olvidas a los cinco segundos?",
            "¿Te pones audífonos en Spotify para tapar con música el ruido y la ansiedad de tu mente?",
            "¿Buscas ofertas innecesarias en Amazon solo por la dopamina de esperar un paquete?",
            "¿Caminas por los pasillos de Walmart o Costco gastando dinero por puro aburrimiento?",
            "¿Sientes que la tecnología te robó la capacidad de contemplar el mundo real en silencio?",

            // Bloque 2: Consumo de Escape y Rutina Física (Restaurantes, Hoteles y Autos)
            "¿Gastas de más en restaurantes lujosos buscando una felicidad que dura solo una cena?",
            "¿Te encierras en el cuarto de un hotel huyendo de problemas que viajan en tu maleta?",
            "¿Manejas tu auto sin rumbo fijo solo para no estar encerrado en tu propia casa?",
            "¿Pagas biles de servicios que usas mecánicamente para mantenerte anestesiado?",
            "¿Te da terror romper tu salida de rutina habitual por miedo a cansarte físicamente?",
            "¿Tu cuerpo te pide a gritos mover los músculos pero eliges la comodidad del sofá?",

            // Bloque 3: Distracción Nocturna y Evasión (Discotecas, Clubes y Fiestas de Amigos)
            "¿Vas a clubes nocturnos buscando ruido para ensordecer las deudas que te preocupan?",
            "¿Bailas en una discoteca rodeado de extraños sintiendo una soledad profunda por dentro?",
            "¿Asistes a la fiesta de un amigo solo por compromiso, deseando regresar a tu aislamiento?",
            "¿Bebes alcohol en reuniones sociales para poder aguantar conversaciones monótonas?",
            "¿Aceptas la visita de un amigo pero te escondes detrás de la pantalla de tu celular?",
            "¿Finges que todo está perfecto en tu vida social para no mostrar tu encarcelamiento mental?",

            // Bloque 4: Entorno Familiar y Distancia (Fiestas Familiares y Visitas)
            "¿Discutes constantemente con tus hijos por diferencias que bloquean la armonía en casa?",
            "¿Sientes flojera o apatía antes de asistir a una fiesta familiar obligatoria de fin de semana?",
            "¿Vives bajo el mismo techo con tu familia pero se sienten como perfectos extraños aislados?",
            "¿La visita de un familiar te genera tensión en lugar de darte paz y alegría real?",
            "¿Extrañas tanto a tus familiares lejanos que te paralizas y dejas de vivir tu presente?",
            "¿Sientes el peso de biles compartidos abriendo grietas de silencio en tus relaciones?",

            // Bloque 5: Viajes Largos y Fugas de la Realidad (Aviones y Cruceros)
            "¿Suestimas el valor de tu entorno local y sueñas con un viaje en avión que no puedes pagar?",
            "¿Deseas meterte en un crucero de lujo para que el mar se lleve tus crisis existenciales?",
            "¿Crees que la solución a tu infelicidad es mudarte de ciudad o cambiar de estado en USA?",
            "¿Planificas vacaciones costosas con dinero que deberías usar para proteger tu economía?",
            "¿Buscas paisajes lejanos en internet porque has perdido la capacidad de asombrarte con tu cielo?",
            "¿Te sientes atrapado en el territorio y asumes que la libertad depende de un boleto de viaje?",

            // Bloque 6: Vulnerabilidad Corporal y Dolor (Hospitales, Clínicas e Impotencia)
            "¿Postergas tu visita a la clínica de dientes o al hospital por miedo a gastar tu presupuesto?",
            "¿Sientes dolores físicos en la espalda o el cuello causados por el estrés de tus biles?",
            "¿Te aterra enfermarte en este sistema y perder la estabilidad laboral de tu familia?",
            "¿Sientes el pecho apretado por la prisa de la ciudad y el miedo constante al futuro?",
            "¿Ganas buen dinero pero tu salud se está desgastando en un trabajo que te explota?",
            "¿Has olvidado el alivio de respirar aire puro con los ojos cerrados libres de preocupación?",

            // Bloque 7: El Espejismo Material y Vacío (Playas y Propiedades)
            "¿Vas a la playa a tomar el sol pero tu mente sigue contando deudas y obligaciones?",
            "¿Tienes estabilidad material y comodidades pero sientes un inconformismo crónico devorándote?",
            "¿Quieres comprarte una casa o un terreno pensando que las paredes te darán identidad?",
            "¿Te da pánico equivocarte si dejas la rutina cómoda y segura que ya conoces?",
            "¿Te comparas secretamente con el estatus y las posesiones de tus vecinos en Estados Unidos?",
            "¿Sientes que el tiempo se te escapa de las manos trabajando solo para acumular botes vacíos?",

            // Bloque 8: El Despertar Maestro (Quiebre y Mando Absoluto)
            "¿Tu mente se convirtió en tu mayor prisión en este momento?",
            "¿Quieres ayudar a tu familia a estar mejor pero te paraliza no saber cómo empezar?",
            "¿Estás cansado de caer siempre en los mismos lugares innecesarios devorando tu libertad?",
            "¿Sientes que estás perdiendo tus mejores años esperando un milagro que no va a llegar?",
            "¿Te cuesta creer que exista un espacio gratis en tu zona capaz de devolverte la esperanza?",
            "¿Estás listo para obedecer al mando, soltar tus indecisiones y salir de tu encierro mental hoy?"
        ],
        CATALOGO_PREGUNTAS_EN: [
            // Block 1: The Urban Digital Loop (Facebook, YouTube, Spotify and Amazon)
            "Do you open Facebook out of inertia to see fake lives and compare them to your gray routine?",
            "Do you fall asleep watching YouTube videos that you forget five seconds later?",
            "Do you put on headphones on Spotify to cover up the noise and anxiety in your mind with music?",
            "Do you look for unnecessary deals on Amazon just for the dopamine rush of waiting for a package?",
            "Do you walk the aisles of Walmart or Costco spending money purely out of boredom?",
            "Do you feel like technology stole your ability to contemplate the real world in silence?",

            // Block 2: Escape Consumption and Physical Routine (Restaurants, Hotels and Cars)
            "Do you overspend in luxury restaurants looking for happiness that only lasts one dinner?",
            "Do you lock yourself in a hotel room fleeing problems that travel in your suitcase?",
            "Do you drive your car aimlessly just to avoid being cooped up in your own home?",
            "Do you pay for services you use mechanically to keep yourself anesthetized?",
            "Are you terrified of breaking your usual routine out of fear of physical exhaustion?",
            "Does your body scream at you to move your muscles, but you choose the comfort of the couch?",

            // Block 3: Nightly Distraction and Evasion (Nightclubs, Clubs and Friends' Parties)
            "Do you go to nightclubs looking for noise to deafen the debts that worry you?",
            "Do you dance in a discotheque surrounded by strangers feeling deep loneliness inside?",
            "Do you attend a friend's party just out of obligation, wishing to return to your isolation?",
            "Do you drink alcohol at social gatherings to endure monotonous conversations?",
            "Do you accept a friend's visit but hide behind your cell phone screen?",
            "Do you pretend that everything is perfect in your social life to hide your mental imprisonment?",

            // Block 4: Family Environment and Distance (Family Parties and Visits)
            "Do you constantly argue with your children over differences that block harmony at home?",
            "Do you feel laziness or apathy before attending a mandatory weekend family party?",
            "Do you live under the same roof with your family but feel like perfect isolated strangers?",
            "Does a family visit generate tension instead of giving you real peace and joy?",
            "Do you miss your distant relatives so much that you become paralyzed and stop living your present?",
            "Do you feel the weight of shared bills opening cracks of silence in your relationships?",

            // Block 5: Long Journeys and Escapes from Reality (Planes and Cruises)
            "Do you underestimate the value of your local environment and dream of a plane trip you cannot afford?",
            "Do you wish to go on a luxury cruise for the sea to carry away your existential crises?",
            "Do you believe that the solution to your unhappiness is to move cities or change states in the USA?",
            "Do you plan expensive vacations with money you should use to protect your economy?",
            "Do you look for distant landscapes online because you have lost the ability to be amazed by your sky?",
            "Do you feel trapped in the territory and assume that freedom depends on a travel ticket?",

            // Block 6: Bodily Vulnerability and Pain (Hospitals, Clinics and Impotence)
            "Do you postpone your visit to the dental clinic or hospital for fear of spending your budget?",
            "Do you feel physical pain in your back or neck caused by the stress of your bills?",
            "Are you afraid of getting sick in this system and losing your family's job stability?",
            "Do you feel tightness in your chest from the city's rush and the constant fear of the future?",
            "Do you earn good money but your health is wearing out in an exploitative job?",
            "Have you forgotten the relief of breathing fresh air with your eyes closed, free from worry?",

            // Block 7: The Material Mirage and Emptiness (Beaches and Properties)
            "Do you go to the beach to sunbathe but your mind keeps counting debts and obligations?",
            "Do you have material stability and comforts but feel a chronic dissatisfaction devouring you?",
            "Do you want to buy a house or land thinking that walls will give you identity?",
            "Are you terrified of making a mistake if you leave the comfortable and secure routine you already know?",
            "Do you secretly compare yourself to the status and possessions of your neighbors in the United States?",
            "Do you feel time slipping through your fingers working only to accumulate empty containers?",

            // Block 8: The Master Awakening (Breakthrough and Absolute Command)
            "Has your mind become your biggest prison right now?",
            "Do you want to help your family be better but are paralyzed by not knowing how to start?",
            "Are you tired of always falling into the same unnecessary places devouring your freedom?",
            "Do you feel like you are losing your best years waiting for a miracle that won't come?",
            "Is it hard for you to believe there's a free space in your area capable of restoring your hope?",
            "Are you ready to obey the command, let go of your indecisions, and break free from your mental imprisonment today?"
        ],

        // Corrected: Separate audio catalogs for each language
        AUDIOS_SECUENCIALES_CASA_ES: [
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
        ],
        AUDIOS_SECUENCIALES_CASA_EN: [
            "Follow the pulse on your screen. Concentrate. You are with me today.",
            "Slowly relax your shoulders. Let all the physical weight of the week fall away.",
            "Don't look at your bills now. Don't look at your wallet. Breathe now.",
            "Maintain a constant rhythm. Feel the fresh air cleansing your chest.",
            "I am accompanying you in silence. You are not alone in this room.",
            "Feel your feet firmly on the ground. The earth supports you for free.",
            "The corporate autopilot is off this second. Keep going.",
            "Stay right in this instant. The past is gone, the present is yours.",
            "Release your jaw now. Let go of that tension you hold without realizing.",
            "Your mind is slowly awakening. You are gaining real control.",
            "You are much bigger than your debts. Breathe deeply and slowly.",
            "Break the zombie the system wants you to be. Stay in the room with me.",
            "Listen to my voice. Notice how your breathing becomes deeper and cleaner.",
            "Your eyes are finally resting from the artificial lights of the screen.",
            "Feel your heartbeat. It's your living engine beating for you.",
            "Feel the weight off your back. Imagine dropping your backpack.",
            "Don't let racing thoughts take you out of this peaceful moment.",
            "Abandon the city's rush today. Here, time is yours.",
            "Money will return to your pockets, but this second of calm will not repeat.",
            "Feel your lungs fill with strength with each cycle of blue air.",
            "Your family needs you to be strong inside. Recover now.",
            "Forget shopping apps. Your mind is above consumption.",
            "You are erasing the day's noise. Stay in the room breathing with me.",
            "The daily routine is broken. You govern your decisions at this instant.",
            "The ground is firm beneath you. Feel the stability of the earth.",
            "Your chest is free from worries now. Expel all negativity at once.",
            "You are regaining your biopsychosocial center. Follow the light of the circle.",
            "Your mind is strong. You have tamed the fear of losing your job today.",
            "Only a few seconds left for the definitive reset. Feel the hope.",
            "You are completely safe here. Remain in absolute peace this second."
        ],

        /**
         * Retrieves or initializes the user's dynamic profile from localStorage.
         * Ensures all 19 needs are present with default values if missing.
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
            localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
            return perfil;
        },

        /** Initializes the KERNEL on DOMContentLoaded. */
        init() {
            this.bloqueActual = parseInt(localStorage.getItem("otg_bloque_secuencial")) || 0;
            // Set initial language if not already set (e.g., from a prior session)
            const storedLang = localStorage.getItem("otg_language");
            if (storedLang) {
                this.idiomaActual = storedLang;
            } else {
                localStorage.setItem("otg_language", this.idiomaActual);
            }
            // Corrected: Load last recommendation ID
            this.lastRecommendationId = localStorage.getItem("otg_last_rec_id");
        },

        /** Starts the initial welcome sequence after user interaction. */
        despertarInicial() {
            document.getElementById('pantalla-bienvenida').style.display = 'none';
            document.getElementById('wrapper-form').classList.remove('hidden');
            
            // Corrected: Apply language settings to UI elements *before* initial speech
            this.cambiarIdioma(this.idiomaActual); 
           
            // Corrected: Translate initial greetings based on selected language
            const saludos_es = [
                "Bienvenido a ópen dán go. Tu escape inteligente. Escucha mis preguntas en pantalla.",
                "ópen dán go está activo. Olvida tus biles un momento. Mira las opciones en tu pantalla ya.",
                "Entraste a ópen dán go. Rompamos tu piloto automático ahora mismo. Toca lo que sientes hoy."
            ];
            const saludos_en = [
                "Welcome to open than go. Your smart escape. Listen to my questions on screen.",
                "open than go is active. Forget your bills for a moment. Look at the options on your screen now.",
                "You entered open than go. Let's break your autopilot right now. Tap what you feel today."
            ];
            const saludos = this.idiomaActual === 'es' ? saludos_es : saludos_en;
            this.hablar(saludos[Math.floor(Math.random() * saludos.length)]);
           
            this.inyectarBloquePreguntas();
            this.iniciarMonitoreoInaccion();
            
            // Corrected: Ensure free writing button is always active, but only triggers if text is present
            this.activarBotonMandoLibreInicial();
        },

        /** Injects a block of 6 questions into the UI. */
        inyectarBloquePreguntas() {
            const grid = document.getElementById('contenedor-preguntas-oraculo');
            if (!grid) return;
           
            clearInterval(this.temporizadorCascada); // Stop any existing cascade
            grid.innerHTML = ""; // Clear previous questions
            this.indicePreguntaCascada = 0;
           
            const catalogo = this.idiomaActual === 'es' ? this.CATALOGO_PREGUNTAS_ES : this.CATALOGO_PREGUNTAS_EN;
            let inicioIdx = this.bloqueActual * 6;
            
            // Corrected: Loop back to the start if all questions have been shown
            if (inicioIdx >= catalogo.length) {
                this.bloqueActual = 0;
                inicioIdx = 0;
                localStorage.setItem("otg_bloque_secuencial", 0);
            }

            for (let i = 0; i < 6; i++) {
                let preguntaTexto = catalogo[inicioIdx + i];
                if (!preguntaTexto) break;

                let btn = document.createElement('button');
                btn.className = 'btn-pregunta-crisis';
                btn.id = `btn-pregunta-${i}`;
                btn.innerText = `${i + 1}. ${preguntaTexto}`;
                btn.onclick = () => this.reaccionarPreguntaSeleccionada(preguntaTexto);
                grid.appendChild(btn);
            }
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

        /** Corrected: Activates the free writing input field and button from start. */
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
                textarea.addEventListener('input', () => {
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
                });
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

        /** Monitors user inaction and advances question blocks or pauses. */
        iniciarMonitoreoInaccion() {
            clearInterval(this.timerInaccion);
            this.conteoInaccion = 0;
            this.timerInaccion = setInterval(() => {
                this.conteoInaccion++;
                if (this.conteoInaccion === 4 || this.conteoInaccion === 8) { // After 48s and 96s of inaction
                    clearInterval(this.temporizadorCascada);
                    this.bloqueActual++;
                    this.inyectarBloquePreguntas();
                    this.hablar(this.idiomaActual === 'es' ? "Avanzamos de nivel. Mira estas otras opciones en pantalla." : "Moving up. Look at these other options on screen.");
                } else if (this.conteoInaccion >= 12) { // After 144s of inaction
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

        /** Handles user selecting a question or entering free text. */
        reaccionarPreguntaSeleccionada(textoPregunta) {
            clearInterval(this.timerInaccion);
            clearInterval(this.temporizadorCascada);
            this.bloqueActual++;
            localStorage.setItem("otg_bloque_secuencial", this.bloqueActual);
           
            // Corrected: Use inp-text-libre value directly
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
            // Corrected: Dynamically set language for speech synthesis
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
                es: { title: "OPEN THAN GO", zip: "Código Postal", instruccion: "¿Qué te tiene atrapado hoy?", desahogo: "O escribe aquí tu propio agobio si no aparece arriba:", placeholder: "Cuéntale al mando libremente qué te pasa hoy...", btn: "Activar Mando Libre", alert: "Idioma cambiado a español.", budget0: "Gratis", budget1: "Bajo", budget2: "Abierto", solo: "Solo", familia: "Familia", accesible: "Accesible", menteAburrido: "Aburrido", menteAgotado: "Agotado", menteEstresado: "Estresado", menteCansado: "Cansado", menteAnsioso: "Ansioso" },
                en: { title: "OPEN THAN GO", zip: "ZIP Code", instruccion: "What has you trapped today?", desahogo: "Or write your own burden here if it does not appear above:", placeholder: "Tell the control freely what is happening to you today...", btn: "Activate Free Control", alert: "Language switched to English.", budget0: "Free", budget1: "Low", budget2: "Open", solo: "Alone", familia: "Family", accesible: "Accessible", menteAburrido: "Bored", menteAgotado: "Exhausted", menteEstresado: "Stressed", menteCansado: "Tired", menteAnsioso: "Anxious" }
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

            this.hablar(t.alert);
            this.inyectarBloquePreguntas(); // Corrected: Re-inject questions in new language
            this.activarBotonMandoLibreInicial(); // Corrected: Re-initialize free writing button in new language
        },

        /** Executes the main logic to fetch recommendations from the backend. */
        async ejecutar() {
            if (this.isLocked) return; // Prevent multiple submissions
            this.isLocked = true;

            const payload = {
                zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
                modo: document.getElementById('modo-selector') ? document.getElementById('modo-selector').value : "SALIR",
                desahogo: document.getElementById('inp-text-libre') ? document.getElementById('inp-text-libre').value.trim() : "", // Corrected: Use inp-text-libre
                lang: this.idiomaActual,
                mente: document.getElementById('mente-selector') ? document.getElementById('mente-selector').value : "aburrido",
                budget: document.getElementById('budget-selector') ? document.getElementById('budget-selector').value : "0",
                perfil: document.getElementById('perfil-selector') ? document.getElementById('perfil-selector').value : "solo",
                perfil_local: this.obtenerPerfilLocal(), // Send the user's dynamic profile
                last_recommendation_id: this.lastRecommendationId // Corrected: Send last recommendation ID
            };

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
                // Corrected: Store the ID of the current recommendation for next request
                if (data.destino_id) {
                    this.lastRecommendationId = data.destino_id;
                    localStorage.setItem("otg_last_rec_id", data.destino_id);
                } else {
                    this.lastRecommendationId = null;
                    localStorage.removeItem("otg_last_rec_id");
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

        /** Processes the sequential flow based on the recommendation type. */
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
                            perfil["indicador_ansiedad"] = Math.min((perfil["indicador_ansiedad"] || 0) + 10, 100);
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

            // Corrected: Fetch SALIR suggestion for CASA mode after some time
            let salidaSugeridaTimeout = setTimeout(async () => {
                try {
                    const r = await fetch("/api/mando-integral", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            modo: "SALIR",
                            lang: this.idiomaActual,
                            mente: "aburrido", // Default mood for initial suggestion
                            budget: "0",
                            perfil: "solo",
                            desahogo: "",
                            zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
                            perfil_local: this.obtenerPerfilLocal(),
                            last_recommendation_id: this.lastRecommendationId
                        })
                    });
                    const data = await r.json();
                    if (data.DIRECCIONAMIENTO_MASTER === "ACCION_CAMPO" && linkSalidaSugerida && salidaSugeridaDiv) {
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
                    let recordatorioTexto = AUDIOS_SECUENCIALES_CASA[pasoAudioIdx];
                    if (recordatorioTexto) {
                        this.hablar(recordatorioTexto);
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

        /** Clears session data and restarts the application. */
        destruirYReiniciar() {
            clearInterval(this.timerInaccion);
            clearInterval(this.timerClinico);
            clearInterval(this.temporizadorCascada);
            window.speechSynthesis.cancel();
            this.pasosMisiones = [];
            this.indiceMision = 0;
            this.isLocked = false;
            // Corrected: Clear lastRecommendationId from localStorage upon restart
            localStorage.removeItem("otg_last_rec_id"); 
            location.reload(); // Reload the page to reset the UI
        }
    };

    // Initialize KERNEL when DOM is fully loaded
    document.addEventListener('DOMContentLoaded', () => KERNEL.init());

    // Expose KERNEL to global scope for HTML onclick events (e.g., KERNEL.despertarInicial())
    window.KERNEL = KERNEL;
                
