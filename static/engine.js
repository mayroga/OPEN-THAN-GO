// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.6.5.0
// Company: May Roga LLC
// File: static/engine.js

const KERNEL = {
    timerInaccion: null,
    timerClinico: null,
    temporizadorCascada: null,
    temporizadorTVid: null, // Nuevo temporizador para la intervención TVid
    timeLeft: 600,
    isLocked: false,
    idiomaActual: 'es',
    pasosMisiones: [],
    indiceMision: 0,
    datosLugarGlobal: null,
    tipoEscapeGlobal: "",
    tvidAsignadaGlobal: "", // Nueva variable para almacenar la TVid asignada

    // Variables de Control de Tiempo e Impaciencia SOLDADAS
    relojRealSegundos: 600,
    contadorToques: 0,
    secuenciaAdelantos: [5, 7, 9, 10, 14, 16, 17, 19, 21, 5],

    // ARQUITECTURA CONVERSACIONAL SECUENCIAL
    bloqueActual: 0,
    conteoInaccion: 0,
    indicePreguntaCascada: 0,
    
    // Almacena el estado actual de los selectores para enviarlos al backend
    estadoSeleccionado: {
        mente: '',
        budget: '',
        perfil: ''
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

    // MÁXIMA FIDELIDAD METODOLÓGICA: Objeto Javascript de datos con las 7 Técnicas de Vida (TVid®)
    TVID_DATA: {
        "Bien": {
            objetivo: "Entrenar al cerebro para identificar oportunidades, soluciones y aspectos positivos incluso en situaciones difíciles, sin negar la realidad.",
            principio: "Si encuentro algo bueno, mi mente tendrá una dirección para avanzar.",
            preguntas_choque: [
                "¿Qué puedo aprender?",
                "¿Qué oportunidad existe aquí?",
                "¿Qué sí puedo hacer hoy?"
            ],
            afirmacion: "Siempre existe un bien que puedo construir.",
            ejercicios: [
                "Observa cualquier situación que te preocupe. Pregúntate: ¿Qué puedo aprender? ¿Qué oportunidad existe aquí? ¿Qué sí puedo hacer hoy? Repite 3 veces: Siempre existe un bien que puedo construir.",
                "Al finalizar el día, escribe tres cosas buenas que ocurrieron. Por pequeñas que sean. Explica qué aprendiste de cada una.",
                "Frente a un problema específico, identifica al menos una oportunidad de crecimiento personal y una acción física concreta que puedas ejecutar inmediatamente."
            ]
        },
        "Mal": {
            objetivo: "Preparar la mente para reconocer riesgos, errores y consecuencias antes de actuar. No para vivir con miedo sino para prevenir.",
            principio: "Ver el peligro me permite evitarlo.",
            preguntas_choque: [
                "¿Qué podría salir mal?",
                "¿Cómo puedo prevenirlo?",
                "¿Tengo un plan B?"
            ],
            afirmacion: "Ver el riesgo me da el control y me permite actuar con tranquilidad.",
            ejercicios: [
                "Antes de tomar una decisión importante, pregúntate: ¿Qué podría salir mal? ¿Cómo puedo prevenirlo? ¿Tengo un plan B? Respira profundamente y responde con calma.",
                "Antes de tomar una decisión importante, haz una lista de los tres principales riesgos. Detalla cómo podrías prevenir cada uno de ellos.",
                "Imagina el peor escenario destructivo posible. Diseña un plan de contingencia alternativo que te dé control y tranquilidad emocional si ocurriera."
            ]
        },
        "Beso": {
            objetivo: "Activar emociones positivas mediante gestos de afecto, gratitud y conexión humana. No necesariamente implica un beso físico, sino una sonrisa, un abrazo, una palabra amable o cualquier gesto de cariño.",
            principio: "El afecto también cura.",
            preguntas_choque: [
                "¡Sonríe ahora mismo!",
                "Agradece mentalmente a alguien",
                "Coloca una mano sobre tu corazón"
            ],
            afirmacion: "El afecto cura, reduce la tensión y me reconecta con el mundo.",
            ejercicios: [
                "Durante un minuto entero, sonríe genuinamente. Expresa un agradecimiento verbal directo hacia otra persona por una acción específica que realizó en el pasado.",
                "Realiza un acto de afecto sincero: un abrazo físico, una palabra amable o, en aislamiento, coloca la mano derecha sobre el corazón mientras sonríes conscientemente.",
                "Realiza un acto de cariño interiorizado: manteniendo la mano en el pecho, exprésate un mensaje positivo de validación y afecto hacia ti mismo para reducir la tensión biológica."
            ]
        },
        "Niño": {
            objetivo: "Recuperar la creatividad, la curiosidad, el juego y la capacidad de sorprenderse, recordando que vivir también significa disfrutar.",
            principio: "Jugar también es sanar.",
            preguntas_choque: [
                "Imagina que eres un explorador",
                "Ríe exageradamente ahora",
                "Inventa una historia de un segundo"
            ],
            afirmacion: "Recupero mi curiosidad, mi creatividad y juego para despertar la alegría.",
            ejercicios: [
                "Dedica dos minutos a dibujar libremente, bailar, inventar una historia fantástica, reír de forma exagerada o caminar imaginando que eres un explorador en territorio desconocido.",
                "Destina cinco minutos ininterrumpidos a dibujar, colorear o modelar una creación abstracta con las manos, cancelando cualquier juicio crítico o racional sobre la calidad del producto.",
                "Reproduce tu canción favorita para bailarla intensamente o inventa una dinámica de juego manual simple durante unos minutos para reactivar los canales neuronales de la alegría y la curiosidad."
            ]
        },
        "Madre": {
            objetivo: "Desarrollar protección, cuidado, paciencia y compasión hacia uno mismo y hacia los demás.",
            principio: "Primero cuido para después poder ayudar.",
            preguntas_choque: [
                "Si fuera tu hijo quien viviera esto...",
                "¿Qué consejo tierno le darías?",
                "Date exactamente ese mismo consejo"
            ],
            afirmacion: "Me protejo con paciencia, comprensión y autocuidado.",
            ejercicios: [
                "Fuerza al individuo a distanciarse del problema. Pregúntate: 'Si fuera mi propio hijo quien estuviera viviendo este sufrimiento exacto, ¿qué consejo tierno le daría?'. Procede a aplicarte y obedecer exactamente ese mismo consejo.",
                "Redacta una carta de apoyo y compasión dirigida a ti mismo, utilizando términos de profundo cuidado, consuelo y comprensión amorosa, tratándote como a un ser querido en crisis.",
                "Reserva un bloque obligatorio de diez minutos en tu agenda para realizar una acción saludable de preservación biológica: descanso absoluto, hidratación consciente, meditación guiada o preparación de un alimento nutritivo."
            ]
        },
        "Padre": {
            objetivo: "Fortalecer la disciplina, la responsabilidad, los límites y la acción, convirtiendo las buenas intenciones en resultados.",
            principio: "El amor también exige compromiso.",
            preguntas_choque: [
                "Elige la tarea que has pospuesto",
                "Trabaja solo los primeros 5 minutos",
                "La meta es comenzar"
            ],
            afirmacion: "Acción, disciplina, límites y resultados tangibles.",
            ejercicios: [
                "Selecciona una responsabilidad o proyecto que has postergado crónicamente. Fúerzate a trabajar en ella únicamente los primeros cinco minutos, con el único objetivo de romper la inercia del reposo.",
                "Refina el enfoque instruyendo la selección de una tarea pendiente. Labora en ella durante cinco minutos bajo condiciones de cero distracciones y aislamiento tecnológico.",
                "Establece la regla conductual de fijar una meta diaria elemental y cumplirla de forma obligatoria antes de permitirte acceder a cualquier plataforma de entretenimiento o gratificación instantánea."
            ]
        },
        "Guerra": {
            objetivo: "Integrar las seis técnicas anteriores para responder con inteligencia, equilibrio y fortaleza cuando la vida presenta crisis, conflictos o momentos de alta presión. Combina Bien, Mal, Beso, Niño, Madre y Padre.",
            principio: "En la guerra de la vida no vence quien golpea más fuerte, sino quien mantiene el equilibrio.",
            preguntas_choque: [
                "Busca algo bueno que rescatar",
                "Identifica el mayor riesgo",
                "Respira, sonríe y baja el cortisol",
                "Piensa con creatividad de niño",
                "Trátate con compasión",
                "Decide tu primera acción"
            ],
            afirmacion: "Estoy preparado. Actúo con calma, inteligencia y determinación.",
            ejercicios: [
                "Ante crisis extremas, fuerza a la mente a rescatar un aspecto positivo (Bien), evaluar los riesgos (Mal), respirar y sonreír (Beso), procesar una salida creativa (Niño), tratarse con compasión (Madre) y ejecutar la primera acción táctica (Padre).",
                "Simula un combate: escribe un desafío complejo y detalla las acciones aplicando en orden inflexible las técnicas del Bien, Mal, Beso, Niño, Madre y Padre. Cierra con una determinación concreta para avanzar.",
                "Recopila de manera solemne la declaración de poseer los derechos civiles limpios, la estabilidad mental y la fortaleza del carácter, cerrando el ciclo con la afirmación imperativa: 'Estoy preparado. Actúo con calma, inteligencia y determinación'."
            ]
        }
    },
    
    // Almacena frases TVid ya mostradas para evitar repetición inmediata
    frasesTVidMostradas: [],
    
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
            // En caso de error de parseo, retorna un perfil base para evitar fallos.
            return {
                "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50,
                "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50,
                "juego": 50, "contemplacion": 50, "trabajo": 50, "descanso": 50, "organizacion": 50,
                "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50,
                "indicador_ansiedad": 0
            };
        }
    },

    init() {
        this.bloqueActual = parseInt(localStorage.getItem("otg_bloque_secuencial")) || 0;
        this.setupEventListeners();
        this.restaurarEstadoUI(); // Asegura que los botones de selección estén marcados
    },

    setupEventListeners() {
        // Event Listeners para los botones de estado (Mente, Gasto, Perfil)
        document.querySelectorAll('.btn-selector-mente').forEach(btn => {
            btn.onclick = () => this.seleccionarBoton('mente', btn.dataset.value);
        });
        document.querySelectorAll('.btn-selector-budget').forEach(btn => {
            btn.onclick = () => this.seleccionarBoton('budget', btn.dataset.value);
        });
        document.querySelectorAll('.btn-selector-perfil').forEach(btn => {
            btn.onclick = () => this.seleccionarBoton('perfil', btn.dataset.value);
        });
        document.getElementById('btn-activar-libre').onclick = () => this.ejecutarDesdeMandoLibre();

        // Monitorear cambios en el selector de modo
        document.getElementById('modo-selector').addEventListener('change', (event) => {
            const selectedMode = event.target.value;
            const selectorsContainer = document.getElementById('selectors-container');
            const oracleContainer = document.getElementById('oracle-container');
            const libreContainer = document.getElementById('bloque-escritura-libre');

            if (selectedMode === 'CASA') {
                selectorsContainer.classList.add('hidden');
                oracleContainer.classList.add('hidden');
                libreContainer.classList.add('hidden');
            } else { // SALIR
                selectorsContainer.classList.remove('hidden');
                oracleContainer.classList.remove('hidden');
                libreContainer.classList.remove('hidden');
            }
        });
    },

    seleccionarBoton(tipo, valor) {
        // Desmarcar todos los botones del mismo tipo
        document.querySelectorAll(`.btn-selector-${tipo}`).forEach(btn => {
            btn.classList.remove('selected');
        });
        // Marcar el botón clickeado
        const clickedBtn = document.querySelector(`.btn-selector-${tipo}[data-value="${valor}"]`);
        if (clickedBtn) {
            clickedBtn.classList.add('selected');
            this.estadoSeleccionado[tipo] = valor;
            // Guardar el estado en localStorage para persistencia
            localStorage.setItem(`otg_selected_${tipo}`, valor);
        }
        // console.log(`Selector ${tipo} establecido a: ${valor}`);
        clearInterval(this.timerInaccion); // Reiniciar el contador de inacción
        this.iniciarMonitoreoInaccion(); // O iniciar el monitoreo si no está activo
    },

    restaurarEstadoUI() {
        // Restaurar idioma
        const savedLang = localStorage.getItem('otg_lang') || 'es';
        this.cambiarIdioma(savedLang, false); // false para evitar hablar al inicio

        // Restaurar selecciones de mente, budget, perfil
        ['mente', 'budget', 'perfil'].forEach(tipo => {
            const savedValue = localStorage.getItem(`otg_selected_${tipo}`);
            if (savedValue) {
                this.seleccionarBoton(tipo, savedValue);
            }
        });

        // Asegurar que el modo selector se refleje en la UI inicial
        const modoSelector = document.getElementById('modo-selector');
        if (modoSelector) {
            const savedMode = localStorage.getItem('otg_mode') || 'SALIR';
            modoSelector.value = savedMode;
            // Disparar el evento change para actualizar la visibilidad de los contenedores
            modoSelector.dispatchEvent(new Event('change'));
        }
    },

    despertarInicial() {
        document.getElementById('pantalla-bienvenida').style.display = 'none';
        document.getElementById('wrapper-form').classList.remove('hidden');

        const modoSelector = document.getElementById('modo-selector');
        if (modoSelector) {
             // Asegurarse de que el modo por defecto (SALIR) muestre los selectores
            if (modoSelector.value === 'SALIR') {
                document.getElementById('selectors-container').classList.remove('hidden');
                document.getElementById('oracle-container').classList.remove('hidden');
                document.getElementById('bloque-escritura-libre').classList.remove('hidden');
            } else {
                 document.getElementById('selectors-container').classList.add('hidden');
                 document.getElementById('oracle-container').classList.add('hidden');
                 document.getElementById('bloque-escritura-libre').classList.add('hidden');
            }
        }
       
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

        this.liberarCajonEscrituraLibre(false); // Mantener el cajón de escritura activo
        this.iniciarEfectoCascada();
    },

    iniciarEfectoCascada() {
        this.indicePreguntaCascada = 0;
        const preguntasActuales = Array.from(document.querySelectorAll('.btn-pregunta-crisis'));
        
        if (preguntasActuales.length === 0) {
            this.liberarCajonEscrituraLibre(true); // Activa el botón de mando libre si no hay preguntas
            return;
        }

        this.temporizadorCascada = setInterval(() => {
            let botonParaDesvanecer = preguntasActuales[this.indicePreguntaCascada];
           
            if (botonParaDesvanecer) {
                // EFECTO DESVANECER REAL: Se desvanece uno por uno
                botonParaDesvanecer.classList.add('fade-out');
                
                let textoLimpio = botonParaDesvanecer.innerText.substring(3); // Obtener texto sin el número
                // Hablar la pregunta que se está desvaneciendo
                this.hablar(textoLimpio);

                this.indicePreguntaCascada++;
            }
           
            if (this.indicePreguntaCascada >= preguntasActuales.length) {
                clearInterval(this.temporizadorCascada);
                this.liberarCajonEscrituraLibre(true); // Activar el botón de mando libre al finalizar la cascada
            }
        }, 8000); // 8 segundos por pregunta exactos
    },

    liberarCajonEscrituraLibre(activarMando) {
        const textarea = document.getElementById('inp-text-libre');
        const btnLibre = document.getElementById('btn-activar-libre');
        const lblDesahogo = document.getElementById('lbl-desahogo');
        const instruccion = document.getElementById('lbl-oraculo-instruccion');

        if (instruccion) {
            instruccion.innerText = this.idiomaActual === 'es' ? "Mando libre listo. O elige arriba." : "Free control ready. Or choose above.";
        }
        if (lblDesahogo) lblDesahogo.style.color = "#fff";
        if (textarea) textarea.focus();

        if (btnLibre) {
            if (activarMando) {
                btnLibre.style.background = "var(--green-action)";
                btnLibre.style.color = "#fff";
                btnLibre.style.borderColor = "#4caf50";
                btnLibre.disabled = false;
            } else {
                btnLibre.style.background = "#111";
                btnLibre.style.color = "#555";
                btnLibre.style.borderColor = "#222";
                btnLibre.disabled = true; // Deshabilitar inicialmente
            }
        }
    },

    ejecutarDesdeMandoLibre() {
        const textarea = document.getElementById('inp-text-libre');
        let textoEscrito = textarea.value.trim();
        if (textoEscrito.length > 3) {
            this.reaccionarPreguntaSeleccionada(textoEscrito);
        } else {
            this.hablar(this.idiomaActual === 'es' ? "Escribe tu problema en el cuadro antes de activar el mando." : "Write your problem in the box before activating control.");
        }
    },

    iniciarMonitoreoInaccion() {
        clearInterval(this.timerInaccion);
        this.conteoInaccion = 0;
        this.timerInaccion = setInterval(() => {
            this.conteoInaccion++;
            if (this.conteoInaccion === 4 || this.conteoInaccion === 8) {
                clearInterval(this.temporizadorCascada);
                this.bloqueActual++;
                this.inyectarBloquePreguntas();
                this.hablar(this.idiomaActual === 'es' ? "Avanzamos de nivel. Mira estas otras opciones en pantalla." : "Moving up. Look at these other options on screen.");
            } else if (this.conteoInaccion >= 12) {
                clearInterval(this.timerInaccion);
                clearInterval(this.temporizadorCascada);
                this.hablar(this.idiomaActual === 'es' ? "Disculpa. Te daré tu tiempo. Sé que tu mente está cansada. Estaré aquí esperando." : "Apologies. I will give you time. I know your mind is tired. I will be waiting here.");
                const instruccion = document.getElementById('lbl-oraculo-instruccion');
                if (instruccion) {
                    instruccion.innerText = this.idiomaActual === 'es' ? "Tomando un respiro. Toca cuando estés listo..." : "Taking a breath. Tap when you are ready...";
                }
            }
        }, 12000); // 12 segundos por ciclo de inacción
    },

    reaccionarPreguntaSeleccionada(textoPregunta) {
        clearInterval(this.timerInaccion);
        clearInterval(this.temporizadorCascada);
        this.bloqueActual++;
        localStorage.setItem("otg_bloque_secuencial", this.bloqueActual);
       
        // Asigna el valor al input oculto antes de la petición Fetch
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

    cambiarIdioma(lang, speak = true) {
        this.idiomaActual = lang;
        localStorage.setItem('otg_lang', lang); // Persistir idioma
        document.getElementById('lang-es').classList.toggle('active', lang === 'es');
        document.getElementById('lang-en').classList.toggle('active', lang === 'en');
       
        const t = {
            es: { title: "OPEN THAN GO", zip: "Código Postal", mode: "Modo", mentalState: "Estado Mental", budget: "Presupuesto", socialContext: "Contexto Social", instruccion: "¿Qué te tiene atrapado hoy?", desahogo: "O escribe aquí tu propio agobio si no aparece arriba:", placeholder: "Cuéntale al mando libremente qué te pasa hoy...", btn: "Activar Mando Libre", alert: "Idioma cambiado a español.",
                    menteOptions: {aburrido: "Aburrido", agotado: "Agotado", estresado: "Estresado", cansado: "Cansado", ansioso: "Ansioso"},
                    budgetOptions: {zero: "Gratis", low: "Bajo Gasto", free: "Libre"},
                    perfilOptions: {solo: "Solo", familia: "Familia", hijos: "Hijos", adultos: "Adultos Mayores", veteranos: "Veteranos de Guerra", directivos: "Directivos/Empresarios", gobierno: "Trabajadores del Gobierno"}
                },
            en: { title: "OPEN THAN GO", zip: "ZIP Code", mode: "Mode", mentalState: "Mental State", budget: "Budget", socialContext: "Social Context", instruccion: "What has you trapped today?", desahogo: "Or write your own burden here if it does not appear above:", placeholder: "Tell the control freely what is happening to you today...", btn: "Activate Free Control", alert: "Language switched to English.",
                    menteOptions: {aburrido: "Bored", agotado: "Exhausted", estresado: "Stressed", cansado: "Tired", ansioso: "Anxious"},
                    budgetOptions: {zero: "Free", low: "Low Cost", free: "Any Cost"},
                    perfilOptions: {solo: "Alone", familia: "Family", hijos: "Children", adultos: "Seniors", veteranos: "Veterans", directivos: "Executives/Entrepreneurs", gobierno: "Government Workers"}
                }
        }[lang];
       
        document.getElementById('txt-app-title').innerText = t.title;
        document.getElementById('lbl-zip').innerText = t.zip;
        document.getElementById('lbl-mode').innerText = t.mode;
        document.getElementById('lbl-mente').innerText = t.mentalState;
        document.getElementById('lbl-budget').innerText = t.budget;
        document.getElementById('lbl-perfil').innerText = t.socialContext;
        document.getElementById('lbl-oraculo-instruccion').innerText = t.instruccion;
        document.getElementById('lbl-desahogo').innerText = t.desahogo;
        document.getElementById('inp-text-libre').placeholder = t.placeholder;
        document.getElementById('btn-activar-libre').innerText = t.btn;

        // Actualizar textos de los botones de selección
        document.querySelectorAll('.btn-selector-mente').forEach(btn => {
            btn.innerText = t.menteOptions[btn.dataset.value] || btn.dataset.value;
        });
        document.querySelectorAll('.btn-selector-budget').forEach(btn => {
            btn.innerText = t.budgetOptions[btn.dataset.key] || btn.dataset.value;
        });
        document.querySelectorAll('.btn-selector-perfil').forEach(btn => {
            btn.innerText = t.perfilOptions[btn.dataset.key] || btn.dataset.value;
        });

        if (speak) {
            this.hablar(t.alert);
        }
    },
    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;

        const modoSelector = document.getElementById('modo-selector');
        const currentMode = modoSelector ? modoSelector.value : "SALIR";
        localStorage.setItem('otg_mode', currentMode); // Persistir modo

        const payload = {
            zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
            modo: currentMode,
            desahogo: document.getElementById('inp-text-invisible') ? document.getElementById('inp-text-invisible').value : "",
            lang: this.idiomaActual,
            perfil_local: this.obtenerPerfilLocal(),
            mente: this.estadoSeleccionado.mente,
            budget: this.estadoSeleccionado.budget,
            perfil: this.estadoSeleccionado.perfil
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
            this.tvidAsignadaGlobal = data.tvid_asignada; // Captura la TVid asignada
            this.indiceMision = 0;

            if (this.tipoEscapeGlobal === "INTERVENCION_DOMESTICA") {
                // Para CASA mode, directamente iniciar el reloj clínico (ejercicio de respiración).
                // Las misiones individuales para CASA ya no se procesan secuencialmente aquí
                // ya que el usuario desea el círculo respiratorio inmediatamente.
                this.iniciarRelojClinicoCasa(container, t);
            } else { // ACCION_CAMPO - Incluye la intervención TVid
                this.iniciarIntervencionTVid();
            }
        } catch (error) {
            alert(this.idiomaActual === 'es' ? "Error de conexión." : "Connection error.");
            document.getElementById('wrapper-form').classList.remove('hidden');
            container.classList.add('hidden');
            this.isLocked = false;
        }
    },

    // La función procesarFlujoSecuencial ahora solo se usaría para misiones si se reintroducen,
    // pero para INTERVENCION_DOMESTICA (CASA) el flujo se ha modificado en ejecutar().
    // Por lo tanto, el contenido existente de esta función (que antes procesaba misiones) ya no se usa directamente para CASA.
    // Se mantiene por si hay lógica de ACCION_CAMPO que deba ir aquí, aunque el flujo actual la redirige a tvid.
    procesarFlujoSecuencial(container) {
        clearInterval(this.timerClinico);
        window.speechSynthesis.cancel();

        const t = {
            es: { inspira: "Inhala ahora", expira: "Exhala ahora", fin: "Protocolo completado. Borrando rastro.", listen: "ESCUCHA MI GUÍA", launch: "ABRIR CANAL BIG TECH YA" },
            en: { inspira: "Inhale now", expira: "Exhale now", fin: "Protocol completed. Clearing tracks.", listen: "LISTEN TO THE GUIDE", launch: "OPEN BIG TECH CHANNEL NOW" }
        }[this.idiomaActual];

        // Este bloque ya no se alcanzará para "INTERVENCION_DOMESTICA"
        // dado el cambio en la función `ejecutar`.
        // Si se desea reintroducir misiones para CASA, esta lógica debería ser revisada.
        if (this.tipoEscapeGlobal === "INTERVENCION_DOMESTICA") {
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
            return;
        }
    },

    iniciarIntervencionTVid() {
        const container = document.getElementById('wrapper-interactive');
        container.innerHTML = `
            <div id="tvid-intervention-screen">
                <div id="tvid-countdown">55</div> <!-- Aumentado a 55 segundos (35 + 20) -->
                <div id="tvid-phrase-container"></div>
            </div>`;
        
        const phraseContainer = document.getElementById('tvid-phrase-container');
        const countdownElement = document.getElementById('tvid-countdown');
        let tvidTimeLeft = 55; // Aumentado a 55 segundos (35 + 20)
        this.frasesTVidMostradas = []; // Reiniciar el registro de frases
        
        const tvid = this.TVID_DATA[this.tvidAsignadaGlobal] || this.TVID_DATA["Bien"];
        let allPhrases = [];
        allPhrases.push(tvid.principio);
        allPhrases.push(tvid.afirmacion);
        allPhrases = allPhrases.concat(tvid.preguntas_choque, tvid.ejercicios);
        
        const directions = [
            'corner-in', 'side-in', 'bottom-in', 'top-in', 'center-out', 'outside-in'
        ];
        let currentPhraseIndex = 0;

        // Función para mostrar la siguiente frase TVid
        const showNextPhrase = () => {
            if (tvidTimeLeft <= 0) return;

            // Selección de frase sin repetición en el ciclo de 55 segundos
            let availablePhrases = allPhrases.filter(p => !this.frasesTVidMostradas.includes(p));
            if (availablePhrases.length === 0) {
                this.frasesTVidMostradas = []; // Reiniciar si todas se han mostrado
                availablePhrases = allPhrases;
            }
            
            const phrase = availablePhrases[Math.floor(Math.random() * availablePhrases.length)];
            this.frasesTVidMostradas.push(phrase); // Marcar como mostrada

            // Eliminar frase anterior si existe
            const oldPhrase = phraseContainer.querySelector('.tvid-phrase');
            if (oldPhrase) {
                oldPhrase.classList.remove('show');
                oldPhrase.classList.add('hide'); // Iniciar animación de salida
                oldPhrase.addEventListener('animationend', () => oldPhrase.remove(), { once: true });
            }

            // Crear y mostrar nueva frase
            setTimeout(() => { // Pequeña pausa para evitar solapamiento visual/auditivo
                const newPhrase = document.createElement('div');
                newPhrase.className = 'tvid-phrase';
                newPhrase.textContent = phrase;
                
                // Asignar dirección de animación aleatoria
                const randomDirection = directions[Math.floor(Math.random() * directions.length)];
                newPhrase.classList.add(randomDirection);
                phraseContainer.appendChild(newPhrase);
                
                // Hablar la frase
                this.hablar(phrase);

                // Esperar un poco antes de mostrar la siguiente (ajustar para lectura y audio)
                // Usamos un tiempo basado en la longitud de la frase
                // Se mantiene el cálculo de readingTime, el pedido era por "ejercicios más cortos" (texto)
                // y "pantalla dinámica", lo cual se logra con las animaciones y el cambio de frase.
                const readingTime = Math.max(phrase.length * 80, 4000); // 80ms por caracter, mínimo 4 segundos
                
                if (tvidTimeLeft > 0) {
                    this.temporizadorTVid = setTimeout(showNextPhrase, readingTime);
                }
            }, 500); // Retraso de 0.5s para la entrada de la nueva frase
        };

        // Iniciar el ciclo de frases
        showNextPhrase();

        // Temporizador regresivo principal
        let countdownTimer = setInterval(() => {
            tvidTimeLeft--;
            if (countdownElement) countdownElement.textContent = tvidTimeLeft;

            if (tvidTimeLeft <= 0) {
                clearInterval(countdownTimer);
                clearTimeout(this.temporizadorTVid); // Detener el temporizador de frases
                window.speechSynthesis.cancel(); // Cancelar cualquier voz en curso
                
                // Mostrar el destino final de acción de campo
                this.mostrarDestinoAccionCampo();
            }
        }, 1000);
    },

    mostrarDestinoAccionCampo() {
        const container = document.getElementById('wrapper-interactive');
        const t = {
            es: { inspira: "Inhala ahora", expira: "Exhala ahora", fin: "Protocolo completado. Borrando rastro.", listen: "ESCUCHA MI GUÍA", launch: "ABRIR CANAL BIG TECH YA" },
            en: { inspira: "Inhale now", expira: "Exhale now", fin: "Protocol completed. Clearing tracks.", listen: "LISTEN TO THE GUIDE", launch: "OPEN BIG TECH CHANNEL NOW" }
        }[this.idiomaActual];

        if (this.datosLugarGlobal) {
            let textoFormateado = this.datosLugarGlobal.destino_instruccion.replace(/\n/g, '<br>');
            container.innerHTML = `
            <div class="mision-card">
                <small>${this.idiomaActual === 'es' ? 'Acción de Campo' : 'Field Action'}</small>
                <h2>${this.datosLugarGlobal.destino_titulo}</h2>
                <div class="instruccion-text">${textoFormateado}</div>
                <button id="btn-countdown-salida" style="width:100%; background:#222; color:#aaa; padding:17px; font-weight:bold; margin-top:15px; border:none; text-transform:uppercase; border-radius:4px; font-size:0.9rem;" disabled>0s ${t.listen}</button>
                <button id="btn-gps-action" style="width:100%; background:#0d47a1; color:#fff; padding:17px; font-weight:bold; margin-top:15px; border:none; text-transform:uppercase; border-radius:4px; cursor:pointer; font-size:0.95rem; letter-spacing:0.5px;">${t.launch}</button>
            </div>`;

            this.hablar(this.datosLugarGlobal.destino_instruccion);
           
            const btnGps = document.getElementById('btn-gps-action');
            if (btnGps) {
                btnGps.onclick = () => {
                    try {
                        let perfil = KERNEL.obtenerPerfilLocal();
                        let token = KERNEL.datosLugarGlobal.token_entorno || "general";
                        // Aquí se podrían añadir más lógicas para actualizar el perfil basado en el token_entorno
                        // Por ejemplo, si el token es "Parque Natural Silencioso", incrementar naturaleza y silencio
                        if (perfil) {
                            if (token.includes("Parque Natural") || token.includes("nature")) perfil["naturaleza"] = Math.min(perfil["naturaleza"] + 15, 100);
                            if (token.includes("Biblioteca") || token.includes("library")) perfil["aprendizaje"] = Math.min(perfil["aprendizaje"] + 15, 100);
                            if (token.includes("Sendero") || token.includes("trail")) perfil["movimiento"] = Math.min(perfil["movimiento"] + 15, 100);
                            if (token.includes("Centro Cultural") || token.includes("cultural")) perfil["creatividad"] = Math.min(perfil["creatividad"] + 15, 100);
                            if (token.includes("Contemplación") || token.includes("viewpoint")) perfil["contemplacion"] = Math.min(perfil["contemplacion"] + 15, 100);
                            localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
                        }
                    } catch (e) {
                        console.error("Error al actualizar perfil local:", e);
                    }
                    window.open(this.datosLugarGlobal.destino_coordenadas_gps, '_blank');
                    KERNEL.destruirYReiniciar();
                };
            }
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
                    } catch (e) {}
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
        clearInterval(this.temporizadorTVid); // Asegurar que el temporizador TVid también se detenga
        window.speechSynthesis.cancel();
        this.pasosMisiones = [];
        this.indiceMision = 0;
        this.isLocked = false;
        // sessionStorage.clear(); // Se mantiene comentado o se elimina si no es necesario para el reinicio
        location.reload();
    }
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());

// Asegurarse de que el botón de mando libre se habilite cuando hay texto
document.addEventListener('input', (event) => {
    if (event.target.id === 'inp-text-libre') {
        const btnLibre = document.getElementById('btn-activar-libre');
        if (btnLibre) {
            btnLibre.disabled = event.target.value.trim().length < 3;
            btnLibre.style.background = event.target.value.trim().length >= 3 ? "var(--green-action)" : "#111";
            btnLibre.style.color = event.target.value.trim().length >= 3 ? "#fff" : "#555";
            btnLibre.style.borderColor = event.target.value.trim().length >= 3 ? "#4caf50" : "#222";
        }
    }
});
