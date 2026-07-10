// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.6.5.0
// Company: May Roga LLC
// File: static/engine.js

const KERNEL = {
    timerInaccion: null,
    timerClinico: null,
    temporizadorCascada: null,
    tvidTimer: null, // Timer para el ejercicio TVid
    tvidContentInterval: null, // Intervalo para mostrar textos TVid
    tvidCountdown: 30, // Duración del ejercicio TVid
    tvidPhrasesShown: [], // Historial de frases TVid mostradas
    currentTvidKey: "", // Técnica TVid seleccionada
    lastDeepLinks: [], // Historial de Deep-Links para diversidad (últimos 5)

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
    secuenciaAdelantos: [5, 7, 9, 10, 14, 16, 17, 19, 21, 5],

    // ARQUITECTURA CONVERSACIONAL SECUENCIAL
    bloqueActual: 0,
    conteoInaccion: 0,
    indicePreguntaCascada: 0,
   
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

    TVID_METODOLOGIA: {
        "Bien": {
            "Principios": ["Si encuentro algo bueno, mi mente tendrá una dirección para avanzar."],
            "PreguntasChoque": ["¿Qué puedo aprender?", "¿Qué oportunidad existe aquí?", "¿Qué sí puedo hacer hoy?"],
            "Afirmaciones": ["Siempre existe un bien que puedo construir."],
            "Ejercicios": [
                "Observa cualquier situación que te preocupe y pregúntate: ¿Qué puedo aprender?, ¿Qué oportunidad existe aquí? y ¿Qué sí puedo hacer hoy?, para luego repetir tres veces: \"Siempre existe un bien que puedo construir.\"",
                "Al finalizar el día escribe tres cosas buenas que ocurrieron, por pequeñas que sean, y explica qué aprendiste de cada una.",
                "Cuando enfrentes un problema, identifica al menos una oportunidad de crecimiento y una acción concreta que puedas realizar en ese momento."
            ]
        },
        "Mal": {
            "Principios": ["Ver el peligro me permite evitarlo."],
            "PreguntasChoque": ["¿Qué podría salir mal?", "¿Cómo puedo prevenirlo?", "¿Tengo un plan B?"],
            "Afirmaciones": ["Ver el riesgo me da el control y me permite actuar con tranquilidad."],
            "Ejercicios": [
                "Antes de tomar una decisión importante pregúntate: ¿Qué podría salir mal?, ¿Cómo puedo prevenirlo? y ¿Tengo un plan B?, respirando profundamente y respondiendo con calma.",
                "Antes de tomar una decisión importante, haz una lista de los tres principales riesgos y cómo podrías prevenir cada uno.",
                "Imagina el peor escenario posible y diseña un plan alternativo que te permita actuar con tranquilidad si ese escenario llegara a ocurrir."
            ]
        },
        "Beso": {
            "Principios": ["El afecto también cura."],
            "PreguntasChoque": ["¡Sonríe ahora mismo!", "Agradece mentalmente a alguien", "Coloca una mano sobre tu corazón."],
            "Afirmaciones": ["El afecto cura, reduce la tensión y me reconecta con el mundo."],
            "Ejercicios": [
                "Durante un minuto sonríe, agradece a alguien, abraza a un familiar o amigo o, si estás solo, coloca una mano sobre tu corazón mientras sonríes.",
                "Dedica un minuto a sonreír mientras agradeces verbalmente a una persona por algo que haya hecho por ti.",
                "Realiza un acto de afecto sincero, como dar un abrazo, ofrecer una palabra amable o colocar una mano sobre tu corazón mientras expresas un mensaje positivo hacia ti mismo."
            ]
        },
        "Niño": {
            "Principios": ["Jugar también es sanar."],
            "PreguntasChoque": ["Imagina que eres un explorador", "Ríe exageradamente ahora", "Inventa una historia de un segundo."],
            "Afirmaciones": ["Recupero mi curiosidad, mi creatividad y juego para despertar la alegría."],
            "Ejercicios": [
                "Dedica dos minutos a dibujar, bailar, inventar una historia, reír exageradamente o caminar imaginando que eres un explorador; no importa el resultado, solo juega.",
                "Dedica cinco minutos a dibujar, colorear o crear algo sin preocuparte por el resultado.",
                "Baila tu canción favorita o inventa un juego sencillo durante unos minutos para despertar la creatividad y la alegría."
            ]
        },
        "Madre": {
            "Principios": ["Primero cuido para después poder ayudar."],
            "PreguntasChoque": ["Si fuera tu hijo quien estuviera viviendo esto...", "¿Qué consejo le darías?", "Date exactamente ese mismo consejo."],
            "Afirmaciones": ["Me protejo con paciencia, comprensión y autocuidado."],
            "Ejercicios": [
                "Pregúntate: \"Si fuera mi hijo quien estuviera viviendo esto, ¿qué consejo le daría?\" y luego date exactamente ese mismo consejo.",
                "Escribe una carta de apoyo dirigida a ti mismo utilizando palabras de comprensión y cariño, como si estuvieras consolando a un ser querido.",
                "Reserva diez minutos para cuidar de ti realizando una actividad saludable, como descansar, hidratarte, meditar o preparar una comida nutritiva."
            ]
        },
        "Padre": {
            "Principios": ["El amor también exige compromiso."],
            "PreguntasChoque": ["Elige la tarea que has estado posponiendo", "Trabaja únicamente los primeros cinco minutos", "La meta es comenzar."],
            "Afirmaciones": ["Acción, disciplina, límites y resultados tangibles."],
            "Ejercicios": [
                "Elige una tarea que has estado posponiendo y trabaja únicamente los primeros cinco minutos, pues la meta es comenzar.",
                "Selecciona una tarea pendiente y trabaja en ella durante cinco minutos sin interrupciones, enfocándote únicamente en comenzar.",
                "Establece una meta sencilla para el día y cúmplela antes de realizar actividades de entretenimiento, reforzando así la disciplina y el compromiso."
            ]
        },
        "Guerra": {
            "Principios": ["En la guerra de la vida no vence quien golpea más fuerte, sino quien mantiene el equilibrio."],
            "PreguntasChoque": ["Busca algo bueno que puedas rescatar", "Identifica el mayor riesgo", "Respira y sonríe para reducir la tensión", "Piensa con creatividad como un niño", "Trátate con compasión y decide tu primera acción."],
            "Afirmaciones": ["Estoy preparado. Actúo con calma, inteligencia y determinación."],
            "Ejercicios": [
                "Su ejercicio consiste en buscar algo bueno que puedas rescatar, identificar el mayor riesgo, respirar y sonreír para reducir la tensión, pensar con creatividad como un niño, tratarte con compasión y decidir la primera acción concreta; finalmente repite: \"Estoy preparado. Actúo con calma, inteligencia y determinación.\"",
                "Ante una situación difícil identifica un aspecto positivo, evalúa los riesgos, mantén la calma respirando profundamente, busca una solución creativa, trátate con compasión y ejecuta la primera acción necesaria.",
                "Simula un desafío importante escribiendo en una hoja qué harías aplicando, en orden, la Técnica del Bien, la Técnica del Mal, la Técnica del Beso, la Técnica del Niño, la Técnica de la Madre y la Técnica del Padre, terminando con una decisión concreta para avanzar."
            ]
        }
    },

    ANIMATION_CLASSES: [
        "cornerToCenter", "sideToCenter", "bottomToCenter",
        "topToCenter", "centerOut", "outIn"
    ],
    POSITION_CLASSES: [
        "pos-center", "pos-top-left", "pos-top-right", "pos-bottom-left",
        "pos-bottom-right", "pos-left-middle", "pos-right-middle",
        "pos-top-middle", "pos-bottom-middle"
    ],
    CRITICAL_WORDS: ["trabajo", "empleo", "compañia", "compañía", "job", "biles", "deudas", "bills", "miseria", "explotacion", "amazon", "walmart", "costco", "fresco", "tienda", "comprar", "dinero", "quincena", "salario"],

    obtenerPerfilLocal() {
        let perfilRaw = localStorage.getItem("otg_perfil_dinamico");
        if (!perfilRaw) {
            const perfilInicial = {
                "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50,
                "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50,
                "juego": 50, "contemplacion": 50, "trabajo": 50, "descanso": 50, "organizacion": 50,
                "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50,
                "indicador_ansiedad": 0
            };
            localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfilInicial));
            return perfilInicial;
        }
        try {
            return typeof perfilRaw === "string" ? JSON.parse(perfilRaw) : perfilRaw;
        } catch (e) {
            // Fallback a un perfil inicial si hay error de parseo
            console.error("Error al parsear perfil local:", e);
            const perfilInicial = {
                "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50,
                "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50,
                "juego": 50, "contemplacion": 50, "trabajo": 50, "descanso": 50, "organizacion": 50,
                "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50,
                "indicador_ansiedad": 0
            };
            localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfilInicial));
            return perfilInicial;
        }
    },

    obtenerLastDeepLinks() {
        try {
            const raw = localStorage.getItem("otg_last_deep_links");
            return raw ? JSON.parse(raw) : [];
        } catch (e) {
            console.error("Error al obtener Deep Links:", e);
            return [];
        }
    },

    guardarDeepLink(link) {
        let links = this.obtenerLastDeepLinks();
        links.unshift(link); // Añadir al principio
        if (links.length > 5) links = links.slice(0, 5); // Mantener solo los últimos 5
        localStorage.setItem("otg_last_deep_links", JSON.stringify(links));
    },

    init() {
        this.bloqueActual = parseInt(localStorage.getItem("otg_bloque_secuencial")) || 0;
        this.tvidPhrasesShown = JSON.parse(localStorage.getItem("otg_tvid_phrases_shown") || "{}");
        this.lastDeepLinks = this.obtenerLastDeepLinks();

        // Event Listeners para los botones de selección
        document.querySelectorAll('.selection-group .selection-btn').forEach(button => {
            button.addEventListener('click', () => this.toggleSelection(button));
        });
    },

    despertarInicial() {
        document.getElementById('pantalla-bienvenida').style.display = 'none';
        document.getElementById('wrapper-form').classList.remove('hidden');
       
        // VOZ DE BIENVENIDA RESTAURADA DE INMEDIATO
        const saludos = [
            "Bienvenido a ópen dán go. Tu escape inteligente. Escucha mis preguntas en pantalla.",
            "ópen dán go está activo. Olvida tus biles un momento. Mira las opciones en tu pantalla ya.",
            "Entraste a ópen dán go. Rompamos tu piloto automático ahora mismo. Toca lo que sientes hoy."
        ];
        this.hablar(saludos[Math.floor(Math.random() * saludos.length)]);
       
        this.inyectarBloquePreguntas();
        this.iniciarMonitoreoInaccion();
    },

    inyectarBloquePreguntas() {
        const grid = document.getElementById('contenedor-preguntas-oraculo');
        if (!grid) return;
       
        clearInterval(this.temporizadorCascada);
        grid.innerHTML = "";
        this.indicePreguntaCascada = 0;
       
        let inicioIdx = this.bloqueActual * 6;
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
            btnLibre.disabled = true; // Desactivar hasta que la cascada termine o haya inacción
        }
        if (lblDesahogo) lblDesahogo.style.color = "#666";

        this.iniciarEfectoCascada();
    },

    iniciarEfectoCascada() {
        this.indicePreguntaCascada = 0;
        const preguntaButtons = document.querySelectorAll('.btn-pregunta-crisis');
       
        this.temporizadorCascada = setInterval(() => {
            let botonParaEliminar = document.getElementById(`btn-pregunta-${this.indicePreguntaCascada}`);
           
            if (botonParaEliminar) {
                // EFECTO DESVANECER REAL: Se elimina uno por uno de arriba a abajo
                botonParaEliminar.classList.add('fade-out');
               
                let siguienteIdx = this.indicePreguntaCascada + 1;
                let siguienteBoton = document.getElementById(`btn-pregunta-${siguienteIdx}`);
                if (siguienteBoton) {
                    let textoLimpio = siguienteBoton.innerText.substring(3); // Eliminar "1. "
                    this.hablar(textoLimpio);
                }
                this.indicePreguntaCascada++;
            } else {
                clearInterval(this.temporizadorCascada);
                this.liberarCajonEscrituraLibre();
            }
        }, 8000); // 8 segundos por pregunta exactos
    },

    liberarCajonEscrituraLibre() {
        const textarea = document.getElementById('inp-text-libre');
        const btnLibre = document.getElementById('btn-activar-libre');
        const lblDesahogo = document.getElementById('lbl-desahogo');
        const instruccion = document.getElementById('lbl-oraculo-instruccion');

        if (instruccion) {
            instruccion.innerText = this.idiomaActual === 'es' ? "Mando libre listo. Cuéntame qué te pasa." : "Free control ready. Tell me what is happening.";
        }
        if (lblDesahogo) lblDesahogo.style.color = "#fff";
        if (textarea) textarea.focus();

        if (btnLibre) {
            btnLibre.style.background = "var(--green-action)";
            btnLibre.style.color = "#fff";
            btnLibre.style.borderColor = "#4caf50";
            btnLibre.disabled = false; // Habilitar el botón
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

    iniciarMonitoreoInaccion() {
        clearInterval(this.timerInaccion);
        this.conteoInaccion = 0;
        this.timerInaccion = setInterval(() => {
            this.conteoInaccion++;
            if (this.conteoInaccion === 4 || this.conteoInaccion === 8) { // 48s y 96s de inacción
                clearInterval(this.temporizadorCascada);
                this.bloqueActual++;
                this.inyectarBloquePreguntas();
                this.hablar(this.idiomaActual === 'es' ? "Avanzamos de nivel. Mira estas otras opciones en pantalla." : "Moving up. Look at these other options on screen.");
            } else if (this.conteoInaccion >= 12) { // 144s de inacción
                clearInterval(this.timerInaccion);
                clearInterval(this.temporizadorCascada);
                this.hablar(this.idiomaActual === 'es' ? "Disculpa. Te daré tu tiempo. Sé que tu mente está cansada. Estaré aquí esperando." : "Apologies. I will give you time. I know your mind is tired. I will be waiting here.");
                const instruccion = document.getElementById('lbl-oraculo-instruccion');
                if (instruccion) {
                    instruccion.innerText = this.idiomaActual === 'es' ? "Tomando un respiro. Toca cuando estés listo..." : "Taking a breath. Tap when you are ready...";
                }
                const btnLibre = document.getElementById('btn-activar-libre');
                if (btnLibre) btnLibre.disabled = false; // Asegurar que el botón esté activo para cuando decida continuar
            }
        }, 12000); // Cada 12 segundos
    },

    reaccionarPreguntaSeleccionada(textoPregunta) {
        clearInterval(this.timerInaccion);
        clearInterval(this.temporizadorCascada);
        this.bloqueActual++;
        localStorage.setItem("otg_bloque_secuencial", this.bloqueActual);
       
        // CORRECCIÓN DE CLIC: Asigna el valor al input oculto antes de la petición Fetch
        document.getElementById('inp-text-invisible').value = textoPregunta;
        this.ejecutar();
    },

    hablar(texto) {
        if (!texto) return;
        window.speechSynthesis.cancel();
        let fx = texto.replace(/OPEN THAN GO/gi, "OPEN DAN GO").replace(/<[^>]*>/g, '');
        const msg = new SpeechSynthesisUtterance(fx);
        msg.lang = 'es-US'; // Voz fija siempre en español por estabilidad nativa
        msg.rate = 1.20;
        window.speechSynthesis.speak(msg);
    },

    cambiarIdioma(lang) {
        this.idiomaActual = lang;
        document.getElementById('lang-es').classList.toggle('active', lang === 'es');
        document.getElementById('lang-en').classList.toggle('active', lang === 'en');
       
        // SINCRO DE BOTÓN DE INGLÉS REPARADO AL 100%
        const t = {
            es: { title: "OPEN THAN GO", zip: "Código Postal", instruccion: "¿Qué te tiene atrapado hoy?", desahogo: "O escribe aquí tu propio agobio si no aparece arriba:", placeholder: "Cuéntale al mando libremente qué te pasa hoy...", btn: "Activar Mando Libre", alert: "Idioma cambiado a español.",
                    mente: "Estado Mental (Vulnerabilidad Humana)", budget: "Presupuesto (Control de Consumo)", perfil: "Contexto Social e Identidad" },
            en: { title: "OPEN THAN GO", zip: "ZIP Code", instruccion: "What has you trapped today?", desahogo: "Or write your own burden here if it does not appear above:", placeholder: "Tell the control freely what is happening to you today...", btn: "Activate Free Control", alert: "Language switched to English.",
                    mente: "Mental State (Human Vulnerability)", budget: "Budget (Consumption Control)", perfil: "Social Context & Identity" }
        }[lang];
       
        document.getElementById('txt-app-title').innerText = t.title;
        document.getElementById('lbl-zip').innerText = t.zip;
        document.getElementById('lbl-oraculo-instruccion').innerText = t.instruccion;
        document.getElementById('lbl-desahogo').innerText = t.desahogo;
        document.getElementById('inp-text-libre').placeholder = t.placeholder;
        document.getElementById('btn-activar-libre').innerText = t.btn;

        // Actualizar labels de los nuevos grupos de selección
        document.querySelector('label[for="mente-group"]').innerText = t.mente;
        document.querySelector('label[for="budget-group"]').innerText = t.budget;
        document.querySelector('label[for="perfil-group"]').innerText = t.perfil;
        
        // No traducimos el texto dentro de los botones de selección, la app es nativa en español
        this.hablar(t.alert);
    },

    toggleSelection(button) {
        const group = button.closest('.selection-group');
        if (group) {
            group.querySelectorAll('.selection-btn').forEach(btn => {
                btn.classList.remove('active');
                btn.classList.remove('selected'); // Ambas clases por robustez
            });
            button.classList.add('active');
            button.classList.add('selected'); // Ambas clases por robustez
        }
    },

    getSelectedValue(groupId) {
        const group = document.getElementById(groupId);
        const selected = group ? group.querySelector('.selection-btn.active, .selection-btn.selected') : null;
        return selected ? selected.dataset.value : null;
    },

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;

        const selectedMente = this.getSelectedValue('mente-group') || "aburrido";
        const selectedBudget = this.getSelectedValue('budget-group') || "0";
        const selectedPerfil = this.getSelectedValue('perfil-group') || "solo";
        const desahogoText = document.getElementById('inp-text-invisible') ? document.getElementById('inp-text-invisible').value : "";

        const payload = {
            zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
            modo: document.getElementById('modo-selector') ? document.getElementById('modo-selector').value : "SALIR",
            mente: selectedMente,
            budget: selectedBudget,
            perfil: selectedPerfil,
            desahogo: desahogoText,
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
                this.procesarFlujoSecuencial(container);
            } else if (this.tipoEscapeGlobal === "ACCION_CAMPO") {
                const desahogoContieneCriticas = this.CRITICAL_WORDS.some(word => data.selected_desahogo.includes(word));
                
                // Si hay palabras críticas o si el Deep-Link es uno de los especiales (Spotify, Youtube, Staffing)
                // saltamos el ejercicio TVid y vamos directo a la "Activación Laboral" o "Reset Multimedia".
                const isSpecialLink = data.destino_coordenadas_gps.includes("spotify") ||
                                      data.destino_coordenadas_gps.includes("youtube") ||
                                      data.destino_coordenadas_gps.includes(this.CRITICAL_WORDS.find(w => data.destino_coordenadas_gps.includes(w)));
                
                if (desahogoContieneCriticas || isSpecialLink) {
                    this.procesarFlujoDeepLinkDirecto(container, data);
                } else {
                    // Si no hay palabras críticas, iniciamos el ejercicio TVid
                    this.currentTvidKey = this.determinarTvid(data.selected_mente, data.selected_perfil, data.selected_desahogo);
                    this.iniciarTvidEjercicio(container, data);
                }
            }
        } catch (error) {
            console.error("Error de conexión:", error);
            alert("Error de conexión. Inténtalo de nuevo.");
            document.getElementById('wrapper-form').classList.remove('hidden');
            container.classList.add('hidden');
            this.isLocked = false;
        }
    },

    // --- TVid® Metodología y Ejercicio de Choque Conductual ---
    determinarTvid(mente, perfil, desahogo) {
        let tvidKey = "Bien"; // Default

        // Regla 1: Técnica de Guerra (Veteranos, Crisis escritas, Textos largos)
        if (perfil.includes("veteranos_guerra") || desahogo.includes("crisis") || desahogo.length > 50) {
            return "Guerra";
        }
        // Regla 2: Técnica del Mal (Ansiedad o Miedos escritos)
        if (mente.includes("ansioso") || desahogo.includes("miedo") || desahogo.includes("preocupacion")) {
            return "Mal";
        }
        // Regla 3: Técnica del Beso (Cansancio, Estrés o Presión corporativa)
        if (mente.includes("cansado") || mente.includes("estresado") || desahogo.includes("corporativo") || desahogo.includes("presion")) {
            return "Beso";
        }
        // Regla 4: Técnica del Niño (Aburrimiento o Perfil de Familia/Hijos)
        if (mente.includes("aburrido") || perfil.includes("familia") || perfil.includes("hijos")) {
            return "Niño";
        }
        // Regla 5: Técnica de la Madre (Agotamiento severo o Perfil de Directivos)
        if (mente.includes("agotado") || perfil.includes("directivos")) {
            return "Madre";
        }
        // Regla 6: Técnica del Padre (Procrastinación escrita)
        if (desahogo.includes("posponer") || desahogo.includes("procrastinar") || desahogo.includes("pendiente")) {
            return "Padre";
        }

        return tvidKey; // Fallback a Bien si ninguna regla específica coincide
    },

    iniciarTvidEjercicio(container, data) {
        clearInterval(this.timerClinico); // Asegurarse de limpiar otros timers
        clearInterval(this.tvidTimer);
        clearInterval(this.tvidContentInterval);
        window.speechSynthesis.cancel();

        const tvidOverlay = document.getElementById('tvid-overlay');
        const tvidCountdownElement = document.getElementById('tvid-countdown');
        tvidOverlay.innerHTML = `<span id="tvid-countdown">30s</span>`; // Resetear overlay
        tvidOverlay.style.display = 'flex';
        this.tvidCountdown = 30;

        const tvidData = this.TVID_METODOLOGIA[this.currentTvidKey];
        if (!tvidData) {
            console.error("TVid no encontrado:", this.currentTvidKey);
            this.finalizarTvidEjercicio(container, data);
            return;
        }
        
        this.tvidPhrasesShown[this.currentTvidKey] = this.tvidPhrasesShown[this.currentTvidKey] || [];
        const currentTvidHistory = this.tvidPhrasesShown[this.currentTvidKey];

        const getUniqueContent = (type) => {
            const allContent = tvidData[type];
            if (!allContent || allContent.length === 0) return null;

            let availableContent = allContent.filter(c => !currentTvidHistory.includes(c));
            if (availableContent.length === 0) {
                // Si todo se ha mostrado, resetear historial para este TVid
                this.tvidPhrasesShown[this.currentTvidKey] = [];
                availableContent = allContent;
            }
            const selectedContent = availableContent[Math.floor(Math.random() * availableContent.length)];
            
            // Añadir al historial y limitar tamaño para evitar que crezca indefinidamente
            this.tvidPhrasesShown[this.currentTvidKey].push(selectedContent);
            if (this.tvidPhrasesShown[this.currentTvidKey].length > allContent.length * 2) { // Mantener un historial de doble del tamaño del contenido
                this.tvidPhrasesShown[this.currentTvidKey] = this.tvidPhrasesShown[this.currentTvidKey].slice(allContent.length);
            }
            localStorage.setItem("otg_tvid_phrases_shown", JSON.stringify(this.tvidPhrasesShown));
            return selectedContent;
        };

        const showNextTvidPhrase = () => {
            const types = ["Principios", "PreguntasChoque", "Afirmaciones", "Ejercicios"];
            const randomType = types[Math.floor(Math.random() * types.length)];
            let phrase = getUniqueContent(randomType);
            
            if (!phrase) return;

            const span = document.createElement('span');
            span.className = `tvid-text ${this.ANIMATION_CLASSES[Math.floor(Math.random() * this.ANIMATION_CLASSES.length)]} ${this.POSITION_CLASSES[Math.floor(Math.random() * this.POSITION_CLASSES.length)]}`;
            span.innerText = phrase;
            tvidOverlay.appendChild(span);
            this.hablar(phrase);

            span.addEventListener('animationend', () => {
                span.remove();
            });
        };

        this.tvidTimer = setInterval(() => {
            this.tvidCountdown--;
            const tvidCountdownElementInner = document.getElementById('tvid-countdown');
            if (tvidCountdownElementInner) tvidCountdownElementInner.innerText = `${this.tvidCountdown}s`;

            if (this.tvidCountdown <= 0) {
                this.finalizarTvidEjercicio(container, data);
            } else {
                showNextTvidPhrase(); // Mostrar una nueva frase cada ~4-5 segundos
            }
        }, 4500); // 4.5 segundos por frase para un total de ~6-7 frases en 30 segundos
        
        // Mostrar la primera frase inmediatamente
        showNextTvidPhrase();
    },

    finalizarTvidEjercicio(container, data) {
        clearInterval(this.tvidTimer);
        clearInterval(this.tvidContentInterval);
        window.speechSynthesis.cancel();
        
        const tvidOverlay = document.getElementById('tvid-overlay');
        tvidOverlay.style.display = 'none';
        tvidOverlay.innerHTML = ''; // Limpiar el overlay

        this.procesarFlujoDeepLinkDirecto(container, data); // Continuar con el Deep-Link
    },
    // --- Fin TVid® Metodología ---

    procesarFlujoSecuencial(container) {
        clearInterval(this.timerClinico);
        window.speechSynthesis.cancel();

        const t = {
            es: { inspira: "Inhala ahora", expira: "Exhala ahora", fin: "Protocolo completado. Borrando rastro.", listen: "ESCUCHA MI GUÍA", launch: "ABRIR CANAL BIG TECH YA", exit_now: "SALIR AHORA" },
            en: { inspira: "Inhale now", expira: "Exhale now", fin: "Protocol completed. Clearing tracks.", listen: "LISTEN TO THE GUIDE", launch: "OPEN BIG TECH CHANNEL NOW", exit_now: "EXIT NOW" }
        }[this.idiomaActual];

        // Esta función se llama para INTERVENCION_DOMESTICA
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

    // Nueva función para procesar Deep-Links directamente (saltándose TVid o después de TVid)
    procesarFlujoDeepLinkDirecto(container, data) {
        clearInterval(this.timerClinico);
        window.speechSynthesis.cancel();

        const t = {
            es: { inspira: "Inhala ahora", expira: "Exhala ahora", fin: "Protocolo completado. Borrando rastro.", listen: "ESCUCHA MI GUÍA", launch: "ABRIR CANAL BIG TECH YA", exit_now: "SALIR AHORA" },
            en: { inspira: "Inhale now", expira: "Exhale now", fin: "Protocol completed. Clearing tracks.", listen: "LISTEN TO THE GUIDE", launch: "OPEN BIG TECH CHANNEL NOW", exit_now: "EXIT NOW" }
        }[this.idiomaActual];

        if (data) {
            let textoFormateado = data.destino_instruccion.replace(/\n/g, '<br>');
            container.innerHTML = `
            <div class="mision-card">
                <small>${this.idiomaActual === 'es' ? 'Acción de Campo' : 'Field Action'}</small>
                <h2>${data.destino_titulo}</h2>
                <div class="instruccion-text">${textoFormateado}</div>
                <button id="btn-countdown-salida" style="width:100%; background:#222; color:#aaa; padding:17px; font-weight:bold; margin-top:15px; border:none; text-transform:uppercase; border-radius:4px; font-size:0.9rem;" disabled>35s ${t.listen}</button>
                <button id="btn-gps-action" class="hidden" style="width:100%; background:#0d47a1; color:#fff; padding:17px; font-weight:bold; margin-top:15px; border:none; text-transform:uppercase; border-radius:4px; cursor:pointer; font-size:0.95rem; letter-spacing:0.5px;">${t.launch}</button>
            </div>`;

            this.hablar(data.destino_instruccion);
           
            let retencion = 35;
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
                                let token = KERNEL.datosLugarGlobal.token_entorno || "general";
                                if (perfil) {
                                    if (token.includes("árbol") || token.includes("Sombra")) perfil["naturaleza"] = Math.min(perfil["naturaleza"] + 10, 100);
                                    else if (token.includes("Caminata") || token.includes("subida")) perfil["movimiento"] = Math.min(perfil["movimiento"] + 10, 100);
                                    else if (token.includes("Paseo") || token.includes("colores")) perfil["creatividad"] = Math.min(perfil["creatividad"] + 10, 100);
                                    localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
                                }
                                // Guardar Deep-Link para diversidad
                                this.guardarDeepLink(data.destino_coordenadas_gps);
                            } catch (e) {
                                console.error("Error al actualizar perfil local o guardar Deep-Link:", e);
                            }
                            window.open(data.destino_coordenadas_gps, '_blank');
                            KERNEL.destruirYReiniciar();
                        };
                    }
                }
            }, 1000);
            return;
        }
    },

    iniciarRelojClinicoCasa(container, t) {
        clearInterval(this.timerClinico);
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

        const circleElement = document.getElementById('breath-circle');
        const timerDiv = document.getElementById('timer');
        const pulmonDiv = document.getElementById('txt-pulmon');
        // CATÁLOGO COMPLETO DE LOS 30 AUDIOS BIOPREVENTIVOS SECUENCIALES FIJOS
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
                    } catch (e) {
                        console.error("Error al actualizar indicador_ansiedad:", e);
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
            this.relojRealSegundos--;
            if (this.timeLeft > 0) this.timeLeft--;
           
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

            if (this.relojRealSegundos < 600 && this.relojRealSegundos % 20 === 0) {
                let pasoAudioIdx = Math.floor((600 - this.relojRealSegundos) / 20) - 1;
                let recordatorioTexto = AUDIOS_SECUENCIALES_CASA[pasoAudioIdx];
                if (recordatorioTexto) {
                    window.speechSynthesis.cancel();
                    let msgFlotante = new SpeechSynthesisUtterance(recordatorioTexto);
                    msgFlotante.lang = 'es-US';
                    msgFlotante.rate = 1.20;
                    window.speechSynthesis.speak(msgFlotante);
                }
            }

            if (this.relojRealSegundos <= 0) {
                clearInterval(this.timerClinico);
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
        clearInterval(this.timerInaccion);
        clearInterval(this.timerClinico);
        clearInterval(this.temporizadorCascada);
        clearInterval(this.tvidTimer);
        clearInterval(this.tvidContentInterval);
        window.speechSynthesis.cancel();
        this.pasosMisiones = [];
        this.indiceMision = 0;
        this.isLocked = false;
        // No borrar todo el localStorage, solo session, y el historial de frases si es necesario
        // sessionStorage.clear(); // Eliminar solo si hay datos de sesión que no queremos persistir
        location.reload();
    }
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());

// Asigna las etiquetas label a los grupos de botones para la funcionalidad de traducción
document.addEventListener('DOMContentLoaded', () => {
    // Labels para los grupos de selección
    const menteGroup = document.getElementById('mente-group');
    if (menteGroup) {
        const labelMente = document.createElement('label');
        labelMente.setAttribute('for', 'mente-group');
        labelMente.id = 'lbl-mente-group'; // Añadir ID para fácil acceso en JS
        labelMente.innerText = 'Estado Mental (Vulnerabilidad Humana)';
        menteGroup.parentNode.insertBefore(labelMente, menteGroup);
    }

    const budgetGroup = document.getElementById('budget-group');
    if (budgetGroup) {
        const labelBudget = document.createElement('label');
        labelBudget.setAttribute('for', 'budget-group');
        labelBudget.id = 'lbl-budget-group'; // Añadir ID para fácil acceso en JS
        labelBudget.innerText = 'Presupuesto (Control de Consumo)';
        budgetGroup.parentNode.insertBefore(labelBudget, budgetGroup);
    }

    const perfilGroup = document.getElementById('perfil-group');
    if (perfilGroup) {
        const labelPerfil = document.createElement('label');
        labelPerfil.setAttribute('for', 'perfil-group');
        labelPerfil.id = 'lbl-perfil-group'; // Añadir ID para fácil acceso en JS
        labelPerfil.innerText = 'Contexto Social e Identidad';
        perfilGroup.parentNode.insertBefore(labelPerfil, perfilGroup);
    }
    
    // Asigna el ID 'lbl-zip' al label del zip code
    const labelZip = document.querySelector('label[for="inp-zip"]');
    if(labelZip) labelZip.id = 'lbl-zip';
    
    KERNEL.init(); // Inicializar KERNEL después de configurar los labels
});
