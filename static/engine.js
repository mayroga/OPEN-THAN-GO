// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.6.0.0
// Company: May Roga LLC
// File: static/engine.js (Frontend Logic)

const KERNEL = {
    timerInaccion: null,
    timerClinico: null,
    temporizadorCascada: null,
    timerTVid: null, // New timer for TVid exercise
    timeLeft: 600, // 10 minutes for clinical timer
    tvidTimeLeft: 30, // 30 seconds for TVid exercise
    isLocked: false,
    idiomaActual: 'es',
    pasosMisiones: [],
    indiceMision: 0,
    datosLugarGlobal: null, // Stores the full response from backend for current recommendation
    tipoEscapeGlobal: "",
   
    // Time and Impatience Control Variables
    relojRealSegundos: 600,
    contadorToques: 0,
    secuenciaAdelantos: [5, 7, 9, 10, 14, 16, 17, 19, 21, 5], // Seconds to advance clinical timer per tap

    // Sequential Conversational Architecture
    bloqueActual: 0, // Current block of questions being displayed
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
   
    CATALOGO_PREGUNTAS: [
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

    // NEW: TVid® Methodological Content - MÁXIMA FIDELIDAD METODOLÓGICA
    TVid_DATA: {
        "Bien": {
            principios: ["Si encuentro algo bueno, mi mente tendrá una dirección para avanzar."],
            preguntas_choque: ["¿Qué puedo aprender?", "¿Qué oportunidad existe aquí?", "¿Qué sí puedo hacer hoy?"],
            afirmaciones: ["Siempre existe un bien que puedo construir."],
            ejercicios: [
                "Observa cualquier situación que te preocupe y pregúntate: ¿Qué puedo aprender?, ¿Qué oportunidad existe aquí? y ¿Qué sí puedo hacer hoy?, para luego repetir tres veces: \"Siempre existe un bien que puedo construir.\"",
                "Al finalizar el día escribe tres cosas buenas que ocurrieron, por pequeñas que sean, y explica qué aprendiste de cada una.",
                "Cuando enfrentes un problema, identifica al menos una oportunidad de crecimiento y una acción concreta que puedas realizar en ese momento."
            ]
        },
        "Mal": {
            principios: ["Ver el peligro me permite evitarlo."],
            preguntas_choque: ["¿Qué podría salir mal?", "¿Cómo puedo prevenirlo?", "¿Tengo un plan B?"],
            afirmaciones: ["Ver el riesgo me da el control y me permite actuar con tranquilidad."],
            ejercicios: [
                "Antes de tomar una decisión importante pregúntate: ¿Qué podría salir mal?, ¿Cómo puedo prevenirlo? y ¿Tengo un plan B?, respirando profundamente y respondiendo con calma.",
                "Antes de tomar una decisión importante, haz una lista de los tres principales riesgos y cómo podrías prevenir cada uno.",
                "Imagina el peor escenario posible y diseña un plan alternativo que te permita actuar con tranquilidad si ese escenario llegara a ocurrir."
            ]
        },
        "Beso": {
            principios: ["El afecto también cura."],
            preguntas_choque: ["¡Sonríe ahora mismo!", "Agradece mentalmente a alguien", "Coloca una mano sobre tu corazón."],
            afirmaciones: ["El afecto cura, reduce la tensión y me reconecta con el mundo."],
            ejercicios: [
                "Durante un minuto sonríe, agradece a alguien, abraza a un familiar o amigo o, si estás solo, coloca una mano sobre tu corazón mientras sonríes.",
                "Dedica un minuto a sonreír mientras agradeces verbalmente a una persona por algo que haya hecho por ti.",
                "Realiza un acto de afecto sincero, como dar un abrazo, ofrecer una palabra amable o colocar una mano sobre tu corazón mientras expresas un mensaje positivo hacia ti mismo."
            ]
        },
        "Niño": {
            principios: ["Jugar también es sanar."],
            preguntas_choque: ["Imagina que eres un explorador", "Ríe exageradamente ahora", "Inventa una historia de un segundo."],
            afirmaciones: ["Recupero mi curiosidad, mi creatividad y juego para despertar la alegría."],
            ejercicios: [
                "Dedica dos minutos a dibujar, bailar, inventar una historia, reír exageradamente o caminar imaginando que eres un explorador; no importa el resultado, solo juega.",
                "Dedica cinco minutos a dibujar, colorear o crear algo sin preocuparte por el resultado.",
                "Baila tu canción favorita o inventa un juego sencillo durante unos minutos para despertar la creatividad y la alegría."
            ]
        },
        "Madre": {
            principios: ["Primero cuido para después poder ayudar."],
            preguntas_choque: ["Si fuera tu hijo quien estuviera viviendo esto...", "¿Qué consejo le darías?", "Date exactamente ese mismo consejo."],
            afirmaciones: ["Me protejo con paciencia, comprensión y autocuidado."],
            ejercicios: [
                "Pregúntate: \"Si fuera mi hijo quien estuviera viviendo esto, ¿qué consejo le daría?\" y luego date exactamente ese mismo consejo.",
                "Escribe una carta de apoyo dirigida a ti mismo utilizando palabras de comprensión y cariño, como si estuvieras consolando a un ser querido.",
                "Reserva diez minutos para cuidar de ti realizando una actividad saludable, como descansar, hidratarte, meditar o preparar una comida nutritiva."
            ]
        },
        "Padre": {
            principios: ["El amor también exige compromiso."],
            preguntas_choque: ["Elige la tarea que has estado posponiendo", "Trabaja únicamente los primeros cinco minutos", "La meta es comenzar."],
            afirmaciones: ["Acción, disciplina, límites y resultados tangibles."],
            ejercicios: [
                "Elige una tarea que has estado posponiendo y trabaja únicamente los primeros cinco minutos, pues la meta es comenzar.",
                "Selecciona una tarea pendiente y trabaja en ella durante cinco minutos sin interrupciones, enfocándote únicamente en comenzar.",
                "Establece una meta sencilla para el día y cúmplela antes de realizar actividades de entretenimiento, reforzando así la disciplina y el compromiso."
            ]
        },
        "Guerra": {
            principios: ["En la guerra de la vida no vence quien golpea más fuerte, sino quien mantiene el equilibrio."],
            preguntas_choque: ["Busca algo bueno que puedas rescatar", "Identifica el mayor riesgo", "Respira y sonríe para reducir la tensión", "Piensa con creatividad como un niño", "Trátate con compasión y decide tu primera acción."],
            afirmaciones: ["Estoy preparado. Actúo con calma, inteligencia y determinación."],
            ejercicios: [
                "Su ejercicio consiste en buscar algo bueno que puedas rescatar, identificar el mayor riesgo, respirar y sonreír para reducir la tensión, pensar con creatividad como un niño, tratarte con compasión y decidir la primera acción concreta; finalmente repite: \"Estoy preparado. Actúo con calma, inteligencia y determinación.\"",
                "Ante una situación difícil identifica un aspecto positivo, evalúa los riesgos, mantén la calma respirando profundamente, busca una solución creativa, trátate con compasión y ejecuta la primera acción necesaria.",
                "Simula un desafío importante escribiendo en una hoja qué harías aplicando, en orden, la Técnica del Bien, la Técnica del Mal, la Técnica del Beso, la Técnica del Niño, la Técnica de la Madre y la Técnica del Padre, terminando con una decisión concreta para avanzar."
            ]
        }
    },

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
    },

    /** Starts the initial welcome sequence after user interaction. */
    despertarInicial() {
        document.getElementById('pantalla-bienvenida').style.display = 'none';
        document.getElementById('wrapper-form').classList.remove('hidden');
        this.cambiarIdioma(this.idiomaActual); // Apply language settings to UI elements
       
        // RESTORED INITIAL WELCOME VOICE IMMEDIATELY
        const saludos = [
            "Bienvenido a ópen dán go. Tu escape inteligente. Escucha mis preguntas en pantalla.",
            "ópen dán go está activo. Olvida tus biles un momento. Mira las opciones en tu pantalla ya.",
            "Entraste a ópen dán go. Rompamos tu piloto automático ahora mismo. Toca lo que sientes hoy."
        ];
        this.hablar(saludos[Math.floor(Math.random() * saludos.length)]);
       
        this.inyectarBloquePreguntas();
        this.iniciarMonitoreoInaccion();
    },

    /** Injects a block of 6 questions into the UI. */
    inyectarBloquePreguntas() {
        const grid = document.getElementById('contenedor-preguntas-oraculo');
        if (!grid) return;
       
        clearInterval(this.temporizadorCascada); // Stop any existing cascade
        grid.innerHTML = ""; // Clear previous questions
        this.indicePreguntaCascada = 0;
       
        let inicioIdx = this.bloqueActual * 6;
        // Loop back to the start if all questions have been shown
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
            btn.id = `btn-pregunta-${i}`;
            btn.innerText = `${i + 1}. ${preguntaTexto}`;
            btn.onclick = () => this.reaccionarPreguntaSeleccionada(preguntaTexto);
            grid.appendChild(btn);
        }

        const btnLibre = document.getElementById('btn-activar-libre');
        const lblDesahogo = document.getElementById('lbl-desahogo');
        if (btnLibre) {
            btnLibre.style.background = "#111";
            btnLibre.style.color = "#555";
            btnLibre.style.borderColor = "#222";
        }
        if (lblDesahogo) lblDesahogo.style.color = "#666";

        this.iniciarEfectoCascada();
    },

    /** Initiates the fading cascade effect for questions. */
    iniciarEfectoCascada() {
        this.indicePreguntaCascada = 0;
       
        this.temporizadorCascada = setInterval(() => {
            let botonParaEliminar = document.getElementById(`btn-pregunta-${this.indicePreguntaCascada}`);
           
            if (botonParaEliminar) {
                // REAL FADE EFFECT: Each button is removed one by one from top to bottom
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

    /** Activates the free writing input field. */
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

        if (btnLibre) {
            btnLibre.style.background = "var(--green-action)";
            btnLibre.style.color = "#fff";
            btnLibre.style.borderColor = "#4caf50";
            btnLibre.onclick = () => {
                let textoEscrito = textarea.value.trim();
                if (textoEscrito.length > 3) {
                    this.reaccionarPreguntaSeleccionada(textoEscrito);
                } else {
                    this.hablar(this.idiomaActual === 'es' ? "Escribe tu problema en el cuadro antes de activar el mando." : "Write your problem in the box before activating control.");
                }
            };
        }
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
       
        // Assign the value to the hidden input before the Fetch request
        document.getElementById('inp-text-invisible').value = textoPregunta;
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
        msg.lang = 'es-US'; // Fixed Spanish voice for native stability as per instructions
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
       
        // SYNC ENGLISH BUTTON FIXED 100% and new profile options
        const t = {
            es: { title: "OPEN THAN GO", zip: "Código Postal", instruccion: "¿Qué te tiene atrapado hoy?", desahogo: "O escribe aquí tu propio agobio si no aparece arriba:", placeholder: "Cuéntale al mando libremente qué te pasa hoy...", btn: "Activar Mando Libre", alert: "Idioma cambiado a español.", budget0: "Gratis", budget1: "Bajo", budget2: "Abierto", solo: "Solo", familia: "Familia", hijos: "Hijos", adultosMayores: "Adultos Mayores", veteranosGuerra: "Veteranos de Guerra", directivosEmpresarios: "Directivos/Empresarios", trabajadoresGobierno: "Trabajadores del Gobierno", menteAburrido: "Aburrido", menteAgotado: "Agotado", menteEstresado: "Estresado", menteCansado: "Cansado", menteAnsioso: "Ansioso" },
            en: { title: "OPEN THAN GO", zip: "ZIP Code", instruccion: "What has you trapped today?", desahogo: "Or write your own burden here if it does not appear above:", placeholder: "Tell the control freely what is happening to you today...", btn: "Activate Free Control", alert: "Language switched to English.", budget0: "Free", budget1: "Low", budget2: "Open", solo: "Alone", familia: "Family", hijos: "Children", adultosMayores: "Seniors", veteranosGuerra: "War Veterans", directivosEmpresarios: "Executives/Entrepreneurs", trabajadoresGobierno: "Government Workers", menteAburrido: "Bored", menteAgotado: "Exhausted", menteEstresado: "Stressed", menteCansado: "Tired", menteAnsioso: "Anxious" }
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
        document.getElementById('opt-perfil-hijos').innerText = t.hijos;
        document.getElementById('opt-perfil-adultos-mayores').innerText = t.adultosMayores;
        document.getElementById('opt-perfil-veteranos-guerra').innerText = t.veteranosGuerra;
        document.getElementById('opt-perfil-directivos-empresarios').innerText = t.directivosEmpresarios;
        document.getElementById('opt-perfil-trabajadores-gobierno').innerText = t.trabajadoresGobierno;
        document.getElementById('opt-mente-aburrido').innerText = t.menteAburrido;
        document.getElementById('opt-mente-agotado').innerText = t.menteAgotado;
        document.getElementById('opt-mente-estresado').innerText = t.menteEstresado;
        document.getElementById('opt-mente-cansado').innerText = t.menteCansado;
        document.getElementById('opt-mente-ansioso').innerText = t.menteAnsioso;

        this.hablar(t.alert);
    },

    /** NEW: Selects a TVid® based on user input for client-side routing. */
    seleccionarTVid(mente, perfil, desahogo) {
        // Prioritize desahogo keywords
        if (desahogo.includes("miedo") || desahogo.includes("ansiedad") || desahogo.includes("inseguridad") || desahogo.includes("preocupacion")) {
            return "Mal";
        }
        if (desahogo.includes("procrastinar") || desahogo.includes("posponer") || desahogo.includes("tarea pendiente") || desahogo.includes("disciplina")) {
            return "Padre";
        }
        if (desahogo.includes("crisis") || desahogo.length > 50 || desahogo.includes("conflicto") || desahogo.includes("presion") || desahogo.includes("guerra") || perfil === "veteranos_guerra") {
            return "Guerra";
        }

        // Then based on Estado Mental (mente)
        if (mente === "ansioso") return "Mal";
        if (mente === "cansado" || mente === "estresado") return "Beso";
        if (mente === "aburrido") return "Niño";
        if (mente === "agotado" || perfil === "directivos_empresarios") return "Madre"; // Agotamiento severo or Directivos

        // Then based on Contexto Social (perfil)
        if (perfil === "familia" || perfil === "hijos") return "Niño";
        if (perfil === "adultos_mayores") return "Madre"; // Cuidado y paciencia
        if (perfil === "trabajadores_gobierno") return "Padre"; // Acción y disciplina

        return "Bien"; // Default
    },

    /** NEW: Initiates the 30-second TVid® exercise with chaotic text animations. */
    iniciarTVidEjercicio(tvidSeleccionada, finalActionCallback) {
        document.getElementById('wrapper-form').classList.add('hidden');
        document.getElementById('wrapper-interactive').classList.add('hidden'); // Ensure interactive is also hidden
        const tvidWrapper = document.getElementById('wrapper-tvid');
        const countdownElement = document.getElementById('tvid-countdown');
        const textContainer = document.getElementById('tvid-text-container');
        
        tvidWrapper.classList.remove('hidden');
        textContainer.innerHTML = ''; // Clear previous texts
        
        this.tvidTimeLeft = 30; // Reset countdown
        countdownElement.innerText = this.tvidTimeLeft;

        // Function to create and animate a single text element
        const displayAnimatedText = (text) => {
            const div = document.createElement('div');
            div.classList.add('tvid-text');
            div.innerText = text;

            // Randomly select one of the 6 animation types
            const animations = [
                'tvid-corner-to-center',
                'tvid-side-to-center-left',
                'tvid-side-to-center-right',
                'tvid-bottom-to-center',
                'tvid-top-to-center',
                'tvid-center-out',
                'tvid-out-in'
            ];
            const randomAnim = animations[Math.floor(Math.random() * animations.length)];
            div.style.animation = `${randomAnim} 5s ease-in-out forwards`; // Each text animates for 5 seconds

            textContainer.appendChild(div);

            // Remove the element after its animation finishes to free up RAM/GPU
            setTimeout(() => {
                div.remove();
            }, 5000); // Match animation duration
        };

        // Function to select a random piece of content from the TVid
        const getRandomTVidContent = (tvid) => {
            const tvidData = this.TVid_DATA[tvid];
            const contentTypes = ['principios', 'preguntas_choque', 'afirmaciones', 'ejercicios'];
            const randomType = contentTypes[Math.floor(Math.random() * contentTypes.length)];
            const contentArray = tvidData[randomType];
            return contentArray[Math.floor(Math.random() * contentArray.length)];
        };

        // Start TVid exercise timer
        this.timerTVid = setInterval(() => {
            this.tvidTimeLeft--;
            countdownElement.innerText = this.tvidTimeLeft;

            // Display a new text every 2-3 seconds for 30 seconds
            if (this.tvidTimeLeft > 0 && this.tvidTimeLeft % 2 === 0 && Math.random() < 0.7) { // Chaotic burst
                const content = getRandomTVidContent(tvidSeleccionada);
                displayAnimatedText(content);
                this.hablar(content); // Speak the text
            }

            if (this.tvidTimeLeft <= 0) {
                clearInterval(this.timerTVid);
                window.speechSynthesis.cancel();
                tvidWrapper.classList.add('hidden');
                finalActionCallback(); // Execute the callback after TVid exercise
            }
        }, 1000);
    },

    /** Executes the main logic to fetch recommendations from the backend. */
    async ejecutar() {
        if (this.isLocked) return; // Prevent multiple submissions
        this.isLocked = true;

        const zip = document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "";
        const modo = document.getElementById('modo-selector') ? document.getElementById('modo-selector').value : "SALIR";
        const desahogo = document.getElementById('inp-text-invisible') ? document.getElementById('inp-text-invisible').value : "";
        const mente = document.getElementById('mente-selector') ? document.getElementById('mente-selector').value : "aburrido";
        const budget = document.getElementById('budget-selector') ? document.getElementById('budget-selector').value : "0";
        const perfil = document.getElementById('perfil-selector') ? document.getElementById('perfil-selector').value : "solo";

        // NEW: Select TVid and start exercise BEFORE backend call returns
        const tvidSeleccionada = this.seleccionarTVid(mente, perfil, desahogo);
        
        let backendResponsePromise;
        if (modo === "SALIR") {
            // For SALIR mode, send backend request in parallel with TVid exercise
            const payload = {
                zip: zip,
                modo: modo,
                desahogo: desahogo,
                lang: this.idiomaActual,
                mente: mente,
                budget: budget,
                perfil: perfil,
                perfil_local: this.obtenerPerfilLocal()
            };
            backendResponsePromise = fetch("/api/mando-integral", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            }).then(r => r.json());
        } else {
            // For CASA mode, a simplified immediate "backend" response for the frontend flow
            backendResponsePromise = Promise.resolve({
                DIRECCIONAMIENTO_MASTER: "INTERVENCION_DOMESTICA",
                misiones: this.pasosMisiones.length > 0 ? this.pasosMisiones : (this.TVid_DATA["Bien"].ejercicios.map(e => ({ titulo: tvidSeleccionada, descripcion: e }))), // Placeholder
                vector_entorno_seleccionado: this.DEFAULT_NECESSITY_PROFILE
            });
        }
        
        this.iniciarTVidEjercicio(tvidSeleccionada, async () => {
            try {
                const data = await backendResponsePromise;
                this.datosLugarGlobal = data;
                this.tipoEscapeGlobal = data.DIRECCIONAMIENTO_MASTER;
                this.indiceMision = 0;

                const container = document.getElementById('wrapper-interactive');

                if (this.tipoEscapeGlobal === "INTERVENCION_DOMESTICA") {
                    this.pasosMisiones = data.misiones.slice(0, 3); // Take first 3 for sequential display for CASA
                    // Proceed with CASA flow
                    container.classList.remove('hidden');
                    this.procesarFlujoSecuencial(container);
                } else { // ACCION_CAMPO (SALIR mode)
                    // Directly activate Deep-Link after TVid exercise
                    this.activarDeepLink();
                }
            } catch (error) {
                console.error("Fetch error or TVid callback error:", error);
                alert(this.idiomaActual === 'es' ? "Error de conexión o en la intervención. Por favor, inténtalo de nuevo." : "Connection or intervention error. Please try again.");
                this.destruirYReiniciar(); // Ensure reset
            } finally {
                this.isLocked = false;
            }
        });
    },

    /** NEW: Activates the Deep-Link for external navigation (SALIR mode). */
    activarDeepLink() {
        if (this.datosLugarGlobal && this.datosLugarGlobal.destino_coordenadas_gps) {
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
            this.destruirYReiniciar(); // Reset and restart app after external navigation
        } else {
            alert(this.idiomaActual === 'es' ? "No se pudo generar el destino de escape." : "Could not generate escape destination.");
            this.destruirYReiniciar();
        }
    },


    /** Processes the sequential flow based on the recommendation type. */
    procesarFlujoSecuencial(container) {
        clearInterval(this.timerClinico);
        window.speechSynthesis.cancel();

        const t = {
            es: { inspira: "Inhala ahora", expira: "Exhala ahora", fin: "Protocolo completado. Borrando rastro.", listen: "ESCUCHA MI GUÍA", launch: "ABRIR CANAL BIG TECH YA", fieldAction: "Acción de Campo", internalMission: "Misión Interna", doItNow: "HAZLO AHORA" },
            en: { inspira: "Inhale now", expira: "Exhale now", fin: "Protocol completed. Clearing tracks.", listen: "LISTEN TO THE GUIDE", launch: "OPEN BIG TECH CHANNEL NOW", fieldAction: "Field Action", internalMission: "Internal Mission", doItNow: "DO IT NOW" }
        }[this.idiomaActual];

        // This block for SALIR mode is now unreachable because `activarDeepLink` handles it directly.
        // The original `procesarFlujoSecuencial` was for both modes, now it's mainly for CASA.
        if (this.tipoEscapeGlobal === "ACCION_CAMPO") {
            // This case should ideally not be hit directly anymore.
            // If it is, something went wrong, and we should just go to the link directly.
            console.warn("procesarFlujoSecuencial called for ACCION_CAMPO, should have been handled by activarDeepLink.");
            this.activarDeepLink();
            return;
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
        </div>`;

        this.timeLeft = 600;
        this.relojRealSegundos = 600;
        this.contadorToques = 0;

        const circleElement = document.getElementById('breath-circle');
        const timerDiv = document.getElementById('timer');
        const pulmonDiv = document.getElementById('txt-pulmon');

        // COMPLETE CATALOG OF 30 FIXED SEQUENTIAL BIOPREVENTIVE AUDIOS
        const AUDIOS_SECUENCIALES_CASA = [
            (this.idiomaActual === 'es' ? "Sigue el pulso en tu pantalla. Concéntrate. Estás conmigo hoy." : "Follow the pulse on your screen. Concentrate. You are with me today."),
            (this.idiomaActual === 'es' ? "Suelta los hombros despacio. Deja caer todo el peso físico de la semana." : "Slowly relax your shoulders. Let all the physical weight of the week fall away."),
            (this.idiomaActual === 'es' ? "No mires tus biles ahora. No mires tu cartera. Respira ya." : "Don't look at your bills now. Don't look at your wallet. Breathe now."),
            (this.idiomaActual === 'es' ? "Mantén el ritmo constante. Siente el aire fresco limpiando tu pecho." : "Maintain a constant rhythm. Feel the fresh air cleansing your chest."),
            (this.idiomaActual === 'es' ? "Te estoy acompañando en silencio. No estás solo en esta habitación." : "I am accompanying you in silence. You are not alone in this room."),
            (this.idiomaActual === 'es' ? "Siente tus pies firmes apoyados en el suelo. La tierra te sostiene gratis." : "Feel your feet firmly on the ground. The earth supports you for free."),
            (this.idiomaActual === 'es' ? "El piloto automático corporativo está apagado en este segundo. Continúa así." : "The corporate autopilot is off this second. Keep going."),
            (this.idiomaActual === 'es' ? "Quédate justo en este instante. El pasado ya pasó, el presente es tuyo." : "Stay right in this instant. The past is gone, the present is yours."),
            (this.idiomaActual === 'es' ? "Suelta la mandíbula ahora. Libera esa carga que aprietas sin darte cuenta." : "Release your jaw now. Let go of that tension you hold without realizing."),
            (this.idiomaActual === 'es' ? "Tu mente está despertando poco a poco. Estás ganando control real." : "Your mind is slowly awakening. You are gaining real control."),
            (this.idiomaActual === 'es' ? "Eres mucho más grande que tus deudas. Respira hondo y despacio." : "You are much bigger than your debts. Breathe deeply and slowly."),
            (this.idiomaActual === 'es' ? "Rompe el zombi que el sistema quiere que seas. Quédate en la sala conmigo." : "Break the zombie the system wants you to be. Stay in the room with me."),
            (this.idiomaActual === 'es' ? "Escucha mi voz. Nota cómo tu respiración se vuelve más profunda y limpia." : "Listen to my voice. Notice how your breathing becomes deeper and cleaner."),
            (this.idiomaActual === 'es' ? "Tus ojos están descansando finalmente de las luces artificiales de la pantalla." : "Your eyes are finally resting from the artificial lights of the screen."),
            (this.idiomaActual === 'es' ? "Siente los latidos de tu pecho. Es tu motor vivo latiendo para ti." : "Feel your heartbeat. It's your living engine beating for you."),
            (this.idiomaActual === 'es' ? "Siente el peso fuera de tu espalda. Imagina que dejas caer tu mochila." : "Feel the weight off your back. Imagine dropping your backpack."),
            (this.idiomaActual === 'es' ? "No dejes que los pensamientos rápidos te saquen de este momento de paz." : "Don't let racing thoughts take you out of this peaceful moment."),
            (this.idiomaActual === 'es' ? "Abandona la prisa de la ciudad hoy. Aquí el tiempo es tuyo." : "Abandon the city's rush today. Here, time is yours."),
            (this.idiomaActual === 'es' ? "El dinero regresará a tus bolsillos, pero este segundo de calma no se repite." : "Money will return to your pockets, but this second of calm will not repeat."),
            (this.idiomaActual === 'es' ? "Siente cómo tus pulmones se llenan de fuerza con cada ciclo de aire azul." : "Feel your lungs fill with strength with each cycle of blue air."),
            (this.idiomaActual === 'es' ? "Tu familia necesita que estés fuerte por dentro. Recupérate ahora." : "Your family needs you to be strong inside. Recover now."),
            (this.idiomaActual === 'es' ? "Olvídate de las aplicaciones de compras. Tu mente está por encima del consumo." : "Forget shopping apps. Your mind is above consumption."),
            (this.idiomaActual === 'es' ? "Estás borrando el ruido del día. Quédate en la sala respirando conmigo." : "You are erasing the day's noise. Stay in the room breathing with me."),
            (this.idiomaActual === 'es' ? "La rutina diaria se ha roto. Tú gobiernas tus decisiones en este instante." : "The daily routine is broken. You govern your decisions at this instant."),
            (this.idiomaActual === 'es' ? "El suelo está firme debajo tuyo. Siente la estabilidad de la tierra." : "The ground is firm beneath you. Feel the stability of the earth."),
            (this.idiomaActual === 'es' ? "Tu pecho está libre de agobios ahora. Expulsa todo lo malo de golpe." : "Your chest is free from worries now. Expel all negativity at once."),
            (this.idiomaActual === 'es' ? "Estás recuperando tu centro biopsicosocial. Sigue la luz del círculo." : "You are regaining your biopsychosocial center. Follow the light of the circle."),
            (this.idiomaActual === 'es' ? "Tu mente es fuerte. Has domado el miedo a perder el trabajo hoy." : "Your mind is strong. You have tamed the fear of losing your job today."),
            (this.idiomaActual === 'es' ? "Faltan pocos segundos para el reinicio definitivo. Siente la esperanza." : "Only a few seconds left for the definitive reset. Feel the hope."),
            (this.idiomaActual === 'es' ? "Estás completamente a salvo aquí. Quédate en paz absoluta en este segundo." : "You are completely safe here. Remain in absolute peace this second.")
        ];

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

        this.timerClinico = setInterval(() => {
            this.relojRealSegundos--; // This timer runs independently for audio triggers
            if (this.timeLeft > 0) this.timeLeft--; // This is the user-facing countdown

            let m = Math.floor(this.timeLeft / 60);
            let s = this.timeLeft % 60;
            if (timerDiv) timerDiv.innerText = `${m}:${s.toString().padStart(2, '0')}`;
           
            // Breathing animation text update
            if (pulmonDiv) {
                let ciclo = this.relojRealSegundos % 8;
                if (ciclo >= 4) {
                    pulmonDiv.innerText = t.inspira.toUpperCase();
                    pulmonDiv.style.color = "var(--cyan-inhale)"; // Cyan for inhale
                } else {
                    pulmonDiv.innerText = t.expira.toUpperCase();
                    pulmonDiv.style.color = "var(--accent)"; // Orange for exhale
                }
            }

            // Play sequential audio messages every 20 seconds
            if (this.relojRealSegundos < 600 && this.relojRealSegundos % 20 === 0) {
                // Calculate index based on how many 20-second intervals have passed
                let pasoAudioIdx = Math.floor((600 - this.relojRealSegundos) / 20) - 1;
                let recordatorioTexto = AUDIOS_SECUENCIALES_CASA[pasoAudioIdx];
                if (recordatorioTexto) {
                    this.hablar(recordatorioTexto); // Use the common hablar function
                }
            }

            // End condition for the clinical timer
            if (this.relojRealSegundos <= 0) {
                clearInterval(this.timerClinico);
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
        clearInterval(this.timerTVid); // Clear TVid timer
        window.speechSynthesis.cancel();
        this.pasosMisiones = [];
        this.indiceMision = 0;
        this.isLocked = false;
        // localStorage for otg_perfil_dinamico and otg_bloque_secuencial, otg_language remains
        location.reload(); // Reload the page to reset the UI
    }
};

// Initialize KERNEL when DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => KERNEL.init());

// Expose KERNEL to global scope for HTML onclick events (e.g., KERNEL.despertarInicial())
window.KERNEL = KERNEL;
