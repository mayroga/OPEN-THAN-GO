// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.6.5.0
// Company: May Roga LLC
// File: static/engine.js

const KERNEL = {
    timerInaccion: null,
    timerClinico: null, // Para el modo CASA
    timerChoqueSensorial: null, // Para el modo SALIR
    temporizadorCascada: null, // Para las preguntas del Oraculo
    tiempoRestanteChoque: 30, // Segundos para el choque sensorial
    tiempoRestanteCasa: 600, // Segundos para el modo CASA (10 minutos)
    isLocked: false,
    idiomaActual: 'es',
    pasosMisiones: [], // Para modo CASA
    indiceMision: 0, // Para modo CASA
    datosAccionCampo: null, // Datos recibidos de main.py para modo SALIR
   
    // Variables de Control de Tiempo e Impaciencia SOLDADAS
    relojRealSegundos: 600, // Para modo CASA
    contadorToques: 0, // Para modo CASA
    secuenciaAdelantos: [5, 7, 9, 10, 14, 16, 17, 19, 21, 5], // Para modo CASA

    // ARQUITECTURA CONVERSACIONAL SECUENCIAL (Oráculo)
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
    // METODOLOGÍA OFICIAL DE BIENESTAR INTEGRAL DE MAY ROGA LLC (TVid®)
    TVID_DATA: {
        "bien": {
            principio: "Si encuentro algo bueno, mi mente tendrá una dirección para avanzar.",
            preguntas: ["¿Qué puedo aprender?", "¿Qué oportunidad existe aquí?", "¿Qué sí puedo hacer hoy?"],
            afirmacion: "Siempre existe un bien que puedo construir.",
            ejercicios: [
                "Observa cualquier situación que te preocupe, hazte las tres preguntas y repite tres veces la afirmación.",
                "Escribe al final del día tres cosas buenas ocurridas (por pequeñas que sean) y su aprendizaje.",
                "Identifica una oportunidad de crecimiento y una acción concreta inmediata ante un problema."
            ]
        },
        "mal": {
            principio: "Ver el peligro me permite evitarlo.",
            preguntas: ["¿Qué podría salir mal?", "¿Cómo puedo prevenirlo?", "¿Tengo un plan B?"],
            afirmacion: "Ver el riesgo me da el control y me permite actuar con tranquilidad.",
            ejercicios: [
                "Antes de decidir, hazte las tres preguntas respirando profundamente y responde con calma.",
                "Haz una lista de los tres principales riesgos de una situación y cómo prevenir cada uno.",
                "Imagina el peor escenario posible y diseña un plan alternativo de tranquilidad."
            ]
        },
        "beso": {
            principio: "El afecto también cura.",
            preguntas: ["¡Sonríe ahora mismo!", "Agradece mentalmente a alguien", "Coloca una mano sobre tu corazón"],
            afirmacion: "El afecto cura, reduce la tensión y me reconecta con el mundo.",
            ejercicios: [
                "Sonríe durante un minuto, agradece a alguien, abraza a un amigo o pon la mano en el corazón si estás solo.",
                "Dedica un minuto a sonreír y agradecer verbalmente a una persona por algo realizado.",
                "Realiza un acto de afecto sincero: un abrazo, una palabra amable o un mensaje positivo propio con la mano al pecho."
            ]
        },
        "nino": {
            principio: "Jugar también es sanar.",
            preguntas: ["Imagina que eres un explorador", "Ríe exageradamente ahora", "Inventa una historia de un segundo"],
            afirmacion: "Recupero mi curiosidad, mi creatividad y juego para despertar la alegría.",
            ejercicios: [
                "Dedica dos minutos a dibujar, bailar, inventar una historia, reír exageradamente o caminar imaginando ser un explorador sin importar el resultado.",
                "Dedica cinco minutos a dibujar, colorear o crear algo sin preocuparse por el producto final.",
                "Baila tu canción favorita o inventa un juego sencillo para despertar la alegría."
            ]
        },
        "madre": {
            principio: "Primero cuido para después poder ayudar.",
            preguntas: ["Si fuera tu hijo quien estuviera viviendo esto...", "¿Qué consejo le darías?", "Date exactamente ese mismo consejo"],
            afirmacion: "Me protejo con paciencia, comprensión y autocuidado.",
            ejercicios: [
                "Pregúntate qué consejo le darías a un hijo en la misma situación y aplícatelo a ti mismo.",
                "Escribe una carta de apoyo dirigida a ti mismo con palabras de comprensión y cariño para consolarte como a un ser querido.",
                "Reserva diez minutos para el autocuidado mediante una actividad saludable como descansar, hidratarse, meditar o preparar comida nutritiva."
            ]
        },
        "padre": {
            principio: "El amor también exige compromiso.",
            preguntas: ["Elige la tarea que has estado posponiendo", "Trabaja únicamente los primeros cinco minutos", "La meta es comenzar"],
            afirmacion: "Acción, disciplina, límites y resultados tangibles.",
            ejercicios: [
                "Elige una tarea postergada y trabaja en ella únicamente los primeros cinco minutos con enfoque total en romper la inercia.",
                "Selecciona una tarea pendiente y labora en ella cinco minutos sin ningún tipo de interrupción.",
                "Establece una meta sencilla para el día y cúmplela estrictamente antes de realizar cualquier actividad de entretenimiento."
            ]
        },
        "guerra": {
            principio: "En la guerra de la vida no vence quien golpea más fuerte, sino quien mantiene el equilibrio.",
            preguntas: ["Identifica lo positivo", "Evalúa riesgos", "Respira profundo", "Busca solución creativa", "Actúa con compasión", "Ejecuta primera acción"], // Consolidado para el ejercicio
            afirmacion: "Estoy preparado. Actúo con calma, inteligencia y determinación.",
            ejercicios: [
                "Identifica un aspecto positivo ante la dificultad, evalúa los riesgos, mantén la calma respirando profundo, busca soluciones creativas, trátate con compasión y ejecuta la primera acción necesaria.",
                "Simula un desafío escribiendo y aplicando en orden estricto: Bien, Mal, Beso, Niño, Madre y Padre, terminando en una decisión concreta.",
                "Recopila las declaraciones de los derechos civiles limpios y la fuerza del carácter."
            ]
        }
    },

    obtenerPerfilLocal() {
        let perfilRaw = localStorage.getItem("otg_perfil_dinamico");
        if (!perfilRaw) {
            const perfilInicial = {
                "movimiento": 50, "naturaleza": 50, "silencio": 50, "agua": 50, "sol": 50,
                "sombra": 50, "aire_fresco": 50, "creatividad": 50, "comunidad": 50, "aprendizaje": 50,
                "juego": 50, "contemplacion": 50, "trabajo": 50, "descanso": 50, "organizacion": 50,
                "alimentacion": 50, "musica": 50, "risa": 50, "esperanza": 50,
                "indicador_ansiedad": 0 // Nuevo indicador para TVid del mal
            };
            localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfilInicial));
            return perfilInicial;
        }
        try {
            return typeof perfilRaw === "string" ? JSON.parse(perfilRaw) : perfilRaw;
        } catch (e) {
            console.error("Error al parsear perfil local, reiniciando:", e);
            localStorage.removeItem("otg_perfil_dinamico"); // Limpiar dato corrupto
            return this.obtenerPerfilLocal(); // Reintentar con un perfil inicial
        }
    },

    actualizarPerfilLocal(tokenEntorno) {
        let perfil = this.obtenerPerfilLocal();
        // Lógica de actualización de perfil basada en el "token_entorno"
        // Estos tokens vienen de main.py, representando la "intención" del lugar sugerido
        if (tokenEntorno.includes("árbol") || tokenEntorno.includes("Sombra") || tokenEntorno.includes("Jardín") || tokenEntorno.includes("Sendero")) perfil["naturaleza"] = Math.min(perfil["naturaleza"] + 15, 100);
        if (tokenEntorno.includes("Caminata") || tokenEntorno.includes("subida") || tokenEntorno.includes("Sendero")) perfil["movimiento"] = Math.min(perfil["movimiento"] + 15, 100);
        if (tokenEntorno.includes("Paseo") || tokenEntorno.includes("colores") || tokenEntorno.includes("Mercado")) perfil["creatividad"] = Math.min(perfil["creatividad"] + 15, 100);
        if (tokenEntorno.includes("Biblioteca") || tokenEntorno.includes("Fuente")) perfil["silencio"] = Math.min(perfil["silencio"] + 15, 100);
        if (tokenEntorno.includes("Banqueta") || tokenEntorno.includes("Mirador")) perfil["contemplacion"] = Math.min(perfil["contemplacion"] + 15, 100);
        if (tokenEntorno.includes("Mercado")) perfil["comunidad"] = Math.min(perfil["comunidad"] + 15, 100);
        if (tokenEntorno.includes("ACTIVACIÓN LABORAL") || tokenEntorno.includes("ECONOMIC ACTION")) perfil["trabajo"] = Math.min(perfil["trabajo"] + 20, 100); // Fuerte impacto si es laboral
        if (tokenEntorno.includes("RESET AUDITIVO") || tokenEntorno.includes("REINICIO VISUAL")) perfil["descanso"] = Math.min(perfil["descanso"] + 10, 100); // Descanso mental

        // Se guarda el perfil actualizado en localStorage
        localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
    },

    init() {
        this.bloqueActual = parseInt(localStorage.getItem("otg_bloque_secuencial")) || 0;
        // Restaurar idioma si estaba guardado
        const storedLang = localStorage.getItem("otg_lang") || 'es';
        this.cambiarIdioma(storedLang);
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                // El usuario ha cambiado de pestaña/app
                if (this.isLocked && this.timerChoqueSensorial) {
                    this.hablar(this.idiomaActual === 'es' ? "¡ATENCIÓN! El mando libre detectó que saliste de pantalla. Regresa ahora." : "ATTENTION! Free control detected you left the screen. Return now.");
                    // Implementar una penalización o pausa si se desea
                }
            }
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
            this.bloqueActual = 0; // Reinicia el ciclo de preguntas si se acaban
            inicioIdx = 0;
        }
        localStorage.setItem("otg_bloque_secuencial", this.bloqueActual);

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
            btnLibre.onclick = null; // Desactivar hasta que las preguntas desaparezcan o se escriba algo
        }
        if (lblDesahogo) lblDesahogo.style.color = "#666";

        this.iniciarEfectoCascada();
    },

    iniciarEfectoCascada() {
        this.indicePreguntaCascada = 0;
       
        this.temporizadorCascada = setInterval(() => {
            let botonParaEliminar = document.getElementById(`btn-pregunta-${this.indicePreguntaCascada}`);
           
            if (botonParaEliminar) {
                // EFECTO DESVANECER REAL: Se elimina uno por uno de arriba a abajo
                botonParaEliminar.classList.add('fade-out');
               
                let siguienteIdx = this.indicePreguntaCascada + 1;
                let siguienteBoton = document.getElementById(`btn-pregunta-${siguienteIdx}`);
                if (siguienteBoton) {
                    let textoLimpio = siguienteBoton.innerText.substring(3);
                    this.hablar(textoLimpio);
                }
                this.indicePreguntaCascada++;
            } else {
                clearInterval(this.temporizadorCascada);
                this.liberarCajonEscrituraLibre();
            }
        }, 6000); // 6 segundos por pregunta exactos, más rápido para interacción fluida
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
            btnLibre.onclick = () => {
                let textoEscrito = textarea.value.trim();
                // Si el usuario no escribió nada, o solo espacios, toma la última pregunta como "desahogo"
                if (textoEscrito.length < 3) {
                    const ultimaPreguntaActiva = this.CATALOGO_PREGUNTAS[this.bloqueActual * 6 + this.indicePreguntaCascada - 1] || "Estoy aburrido."; // Fallback si no hay preguntas activas
                    this.hablar(this.idiomaActual === 'es' ? "No te preocupes. Tomo tu última preocupación. Activando el mando." : "No worries. Taking your last concern. Activating control.");
                    this.reaccionarPreguntaSeleccionada(ultimaPreguntaActiva);
                } else {
                    this.reaccionarPreguntaSeleccionada(textoEscrito);
                }
            };
        }
    },

    iniciarMonitoreoInaccion() {
        clearInterval(this.timerInaccion);
        this.conteoInaccion = 0;
        this.timerInaccion = setInterval(() => {
            this.conteoInaccion++;
            if (this.conteoInaccion === 2 || this.conteoInaccion === 4) { // Más rápido para forzar interacción
                clearInterval(this.temporizadorCascada);
                this.bloqueActual = (this.bloqueActual + 1) % (this.CATALOGO_PREGUNTAS.length / 6); // Cicla los bloques
                this.inyectarBloquePreguntas();
                this.hablar(this.idiomaActual === 'es' ? "Avanzamos de nivel. Mira estas otras opciones en pantalla." : "Moving up. Look at these other options on screen.");
            } else if (this.conteoInaccion >= 6) { // Después de 6 ciclos de 12 segundos (72s)
                clearInterval(this.timerInaccion);
                clearInterval(this.temporizadorCascada);
                this.hablar(this.idiomaActual === 'es' ? "Disculpa. Te daré tu tiempo. Sé que tu mente está cansada. Estaré aquí esperando." : "Apologies. I will give you time. I know your mind is tired. I will be waiting here.");
                const instruccion = document.getElementById('lbl-oraculo-instruccion');
                if (instruccion) {
                    instruccion.innerText = this.idiomaActual === 'es' ? "Tomando un respiro. Toca cuando estés listo..." : "Taking a breath. Tap when you are ready...";
                }
            }
        }, 12000);
    },

    reaccionarPreguntaSeleccionada(textoPregunta) {
        clearInterval(this.timerInaccion);
        clearInterval(this.temporizadorCascada);
        // this.bloqueActual se actualiza en inyectarBloquePreguntas()
        // localStorage.setItem("otg_bloque_secuencial", this.bloqueActual); // Ya se hace en inyectarBloquePreguntas
       
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
        localStorage.setItem("otg_lang", lang); // Guardar idioma preferido
        document.getElementById('lang-es').classList.toggle('active', lang === 'es');
        document.getElementById('lang-en').classList.toggle('active', lang === 'en');
       
        // SINCRO DE BOTÓN DE INGLÉS REPARADO AL 100%
        const t = {
            es: { title: "OPEN THAN GO", zip: "Código Postal", instruccion: "¿Qué te tiene atrapado hoy?", desahogo: "O escribe aquí tu propio agobio si no aparece arriba:", placeholder: "Cuéntale al mando libremente qué te pasa hoy...", btn: "Activar Mando Libre", alert: "Idioma cambiado a español." },
            en: { title: "OPEN THAN GO", zip: "ZIP Code", instruccion: "What has you trapped today?", desahogo: "Or write your own burden here if it does not appear above:", placeholder: "Tell the control freely what is happening to you today...", btn: "Activate Free Control", alert: "Language switched to English." }
        }[lang];
       
        document.getElementById('txt-app-title').innerText = t.title;
        document.getElementById('lbl-zip').innerText = t.zip;
        document.getElementById('lbl-oraculo-instruccion').innerText = t.instruccion;
        document.getElementById('lbl-desahogo').innerText = t.desahogo;
        document.getElementById('inp-text-libre').placeholder = t.placeholder;
        document.getElementById('btn-activar-libre').innerText = t.btn;
        this.hablar(t.alert);
    },

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;

        const payload = {
            zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
            modo: document.getElementById('modo-selector') ? document.getElementById('modo-selector').value : "SALIR",
            mente: document.querySelector('.btn-mente.selected')?.dataset.mente || 'aburrido', // Captura estado mental seleccionado
            budget: document.querySelector('.btn-budget.selected')?.dataset.budget || '0', // Captura presupuesto
            perfil: document.querySelector('.btn-social.selected')?.dataset.perfil || 'solo', // Captura perfil social
            desahogo: document.getElementById('inp-text-invisible') ? document.getElementById('inp-text-invisible').value : "",
            lang: this.idiomaActual,
            perfil_local: this.obtenerPerfilLocal()
        };

        const containerForm = document.getElementById('wrapper-form');
        const containerInteractive = document.getElementById('wrapper-interactive');
        const pantallaChoque = document.getElementById('pantalla-choque');
       
        containerForm.classList.add('hidden');
        containerInteractive.classList.add('hidden'); // Asegura que la interactiva esté oculta por si acaso
        pantallaChoque.classList.add('hidden'); // Asegura que la pantalla de choque esté oculta

        // Muestra un mensaje de "Conectando..." mientras se carga
        containerInteractive.innerHTML = `<div style='text-align:center; padding:40px 0;'><h2 style='color:#fff; font-size:1.1rem;'>CONECTANDO...</h2></div>`;
        containerInteractive.classList.remove('hidden');


        try {
            const r = await fetch("/api/mando-integral", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await r.json();

            // KERNEL.datosLugarGlobal = data; // Renombrado a datosAccionCampo para claridad
            this.tipoEscapeGlobal = data.DIRECCIONAMIENTO_MASTER;

            if (this.tipoEscapeGlobal === "INTERVENCION_DOMESTICA") {
                this.pasosMisiones = data.misiones.slice(0, 3);
                this.indiceMision = 0;
                this.procesarFlujoSecuencialCasa(containerInteractive); // Llama a la lógica de Casa
            } else { // ACCION_CAMPO - Aquí es donde entra el choque sensorial
                this.datosAccionCampo = data; // Guarda todos los datos de main.py
                this.iniciarChoqueSensorial(); // Inicia el choque sensorial
            }
        } catch (error) {
            console.error("Error de conexión:", error);
            alert("Error de conexión. Intenta de nuevo.");
            containerForm.classList.remove('hidden');
            containerInteractive.classList.add('hidden');
            this.isLocked = false;
        }
    },

    // --- LÓGICA DEL CHOQUE SENSORIAL Y TVid® (MODO SALIR) ---
    selectTvid(mente, perfil, desahogo) {
        mente = mente.toLowerCase();
        perfil = perfil.toLowerCase();
        desahogo = desahogo.toLowerCase();

        // Orden de prioridad para la asignación de TVid®
        if (perfil === "veteranos de guerra" || desahogo.includes("crisis profundas") || desahogo.length > 100) return "guerra";
        if (mente === "ansioso" || desahogo.includes("miedo") || desahogo.includes("susto")) return "mal";
        if (mente === "cansado" || mente === "estresado" || desahogo.includes("presión corporativa") || desahogo.includes("trabajo")) return "beso";
        if (mente === "aburrido" || perfil === "familia" || perfil === "hijos") return "nino";
        if (mente === "agotado" || perfil === "directivos/empresarios") return "madre";
        if (desahogo.includes("procrastinacion") || desahogo.includes("vagancia") || desahogo.includes("retrasos") || desahogo.includes("posponer")) return "padre";
        
        return "bien"; // Default si no coincide con los anteriores
    },

    iniciarChoqueSensorial() {
        clearInterval(this.timerClinico);
        clearInterval(this.temporizadorCascada);
        window.speechSynthesis.cancel();
        
        document.getElementById('wrapper-form').classList.add('hidden');
        document.getElementById('wrapper-interactive').classList.add('hidden'); // Oculta la de "Conectando..."
        const pantallaChoque = document.getElementById('pantalla-choque');
        pantallaChoque.classList.remove('hidden');
        pantallaChoque.innerHTML = `
            <div id="choque-countdown">${this.tiempoRestanteChoque}</div>
            <div id="choque-content"></div>
        `;

        const t = {
            es: { fin: "¡MANDO CUMPLIDO! ¡LIBERTAD AHORA!", final_voz: "Mando cumplido. Te expulso de la pantalla. Busca tu libertad en los mapas. Es tu momento. ¡Ahora!" },
            en: { fin: "COMMAND FULFILLED! FREEDOM NOW!", final_voz: "Command fulfilled. Expelling you from the screen. Find your freedom on the maps. It's your moment. Now!" }
        }[this.idiomaActual];

        const tvidKey = this.selectTvid(
            this.datosAccionCampo.selected_mente,
            this.datosAccionCampo.selected_perfil,
            this.datosAccionCampo.user_desahogo
        );
        const tvid = this.TVID_DATA[tvidKey];
        const frasesTvid = [
            tvid.principio,
            ...tvid.preguntas,
            tvid.afirmacion,
            ...tvid.ejercicios
        ].filter(Boolean); // Eliminar cualquier elemento nulo o indefinido

        let fraseIndex = 0;
        const totalFrases = frasesTvid.length;
        const intervalTime = 3000; // 3 segundos por frase
        let maxTextDisplayTime = 4000; // Cuánto tiempo dura cada ráfaga de texto en pantalla

        if (tvidKey === "guerra") { // Guerra puede tener frases más largas, dale más tiempo
            maxTextDisplayTime = 5000;
        }

        const injectPhrase = () => {
            if (this.tiempoRestanteChoque <= 0) {
                clearInterval(this.timerChoqueSensorial);
                pantallaChoque.innerHTML = `<h2 style="color:var(--green-action); font-size:1.8rem;">${t.fin}</h2>`;
                this.hablar(t.final_voz);
                setTimeout(() => this.ejecutarEdgeHijacking(), 2000); // Ejecuta el hijack después de un breve mensaje
                return;
            }

            const frase = frasesTvid[fraseIndex % totalFrases];
            fraseIndex++;

            const phraseDiv = document.createElement('div');
            phraseDiv.className = 'shock-text';
            phraseDiv.innerText = frase;

            const animations = [
                'anim-corner-tl', 'anim-corner-tr', 'anim-corner-bl', 'anim-corner-br',
                'anim-side-l', 'anim-side-r', 'anim-bottom', 'anim-top',
                'anim-center-out', 'anim-out-in' // Añadidas las de concentración
            ];
            phraseDiv.classList.add(animations[Math.floor(Math.random() * animations.length)]);
            phraseDiv.style.color = `hsl(${Math.random() * 360}, 100%, 70%)`; // Colores vibrantes aleatorios

            document.getElementById('choque-content').appendChild(phraseDiv);
            this.hablar(frase); // Lee la frase
           
            // Eliminar la frase después de unos segundos
            setTimeout(() => {
                phraseDiv.remove();
            }, maxTextDisplayTime);
        };

        this.tiempoRestanteChoque = 30; // Reset
        document.getElementById('choque-countdown').innerText = this.tiempoRestanteChoque;

        this.timerChoqueSensorial = setInterval(() => {
            this.tiempoRestanteChoque--;
            if (document.getElementById('choque-countdown')) {
                document.getElementById('choque-countdown').innerText = this.tiempoRestanteChoque;
            }
            if (this.tiempoRestanteChoque <= 0) {
                clearInterval(this.timerChoqueSensorial);
                pantallaChoque.innerHTML = `<h2 style="color:var(--green-action); font-size:1.8rem;">${t.fin}</h2>`;
                this.hablar(t.final_voz);
                setTimeout(() => this.ejecutarEdgeHijacking(), 2000);
            } else {
                injectPhrase();
            }
        }, intervalTime); // Inyecta una frase cada X segundos

        injectPhrase(); // Inyecta la primera frase inmediatamente
    },

    generarEdgeHijackingUrl() {
        const data = this.datosAccionCampo;
        let gpsQuery = data.destino_gps_keywords_sugeridas || "places+of+interest+";
        const zip = data.user_zip;
        const mente = data.selected_mente.toLowerCase();
        const perfil = data.selected_perfil.toLowerCase();
        const desahogo = data.user_desahogo.toLowerCase();
        const budget = data.user_budget; // '0' para gratis, '1' para bajo gasto

        let finalKeywords = [];

        // Lógica de Edge-Hijacking basada en cruce psicológico y rol de USA
        // PRIORIDAD: Interceptor Financiero si está activo
        if (data.financial_interceptor_active) {
            if (data.financial_interceptor_channel === "SPOTIFY") return "https://open.spotify.com/genre/mood"; // Playlist de ánimo
            if (data.financial_interceptor_channel === "YOUTUBE") return "https://www.youtube.com/results?search_query=nature+sounds+relaxing"; // Sonidos de naturaleza
            if (data.financial_interceptor_channel === "MAPS") { // Agencias de empleo
                finalKeywords.push("staffing+agencies");
            }
        } else {
            // Sino, genera keywords basadas en TVid, mente, perfil
            // Puedes refinar gpsQuery original de main.py o usarlo como base

            // Refinamiento por mente
            if (mente === "aburrido") finalKeywords.push("creative+outlets", "local+events+free");
            else if (mente === "agotado") finalKeywords.push("quiet+retreats", "peaceful+places+relax");
            else if (mente === "estresado") finalKeywords.push("stress+relief+activities", "calming+environments");
            else if (mente === "cansado") finalKeywords.push("restorative+places", "slow+paced+activities");
            else if (mente === "ansioso") finalKeywords.push("mindfulness+spots", "breathing+spaces");
            
            // Refinamiento por perfil
            if (perfil === "solo") finalKeywords.push("solitary+nature+walks", "meditation+spots");
            else if (perfil === "familia" || perfil === "hijos") finalKeywords.push("family+parks+free", "kid+friendly+activities");
            else if (perfil === "adultos mayores") finalKeywords.push("accessible+gentle+walks", "senior+friendly+parks");
            else if (perfil === "veteranos de guerra") finalKeywords.push("veterans+memorial+parks", "healing+gardens");
            else if (perfil === "directivos/empresarios") finalKeywords.push("isolated+nature+retreats+no+wifi", "executive+wellness+destinations");
            else if (perfil === "trabajadores del gobierno") finalKeywords.push("public+parks+government+employees+relax", "quiet+public+spaces");

            // Refinamiento por presupuesto
            if (budget === '0') finalKeywords.push("free+activities", "no+cost+places");
            else if (budget === '1') finalKeywords.push("low+cost+experiences", "affordable+outings");

            // Si ya hay keywords sugeridas por main.py, las añadimos
            if (gpsQuery && !gpsQuery.includes("places+of+interest+")) {
                finalKeywords.unshift(gpsQuery.replace(/\+/g, ' ')); // Añade la sugerencia de main.py al principio
            }

            // Elimina duplicados y concatena
            finalKeywords = [...new Set(finalKeywords)].map(k => k.replace(/ /g, '+'));
            gpsQuery = finalKeywords.join("+") || "wellness+escape+"; // Fallback
        }


        // FÓRMULA GEOGRÁFICA UNIVERSAL FIJA ORIGINAL RESTAURADA SIN RECORTE NI ALTERACIONES
        const anclaje_geografico = zip ? zip : "USA"; // Si no hay ZIP, busca en todo USA por defecto
       
        let finalUrl = "";
        if (data.financial_interceptor_active && (data.financial_interceptor_channel === "SPOTIFY" || data.financial_interceptor_channel === "YOUTUBE")) {
             finalUrl = gpsQuery; // Ya es una URL completa
        } else {
             finalUrl = `${data.destino_base_url}${gpsQuery}+in+${anclaje_geografico}`.replace(" ", "+");
        }
       
        return finalUrl;
    },

    ejecutarEdgeHijacking() {
        const finalUrl = this.generarEdgeHijackingUrl();
        this.actualizarPerfilLocal(this.datosAccionCampo.token_entorno); // Actualiza el perfil basado en la sugerencia inicial de main.py
        window.open(finalUrl, "_self");
        this.destruirYReiniciar(); // Recarga la aplicación después de la expulsión
    },

    // --- LÓGICA MODO CASA (INTERVENCION_DOMESTICA) ---
    procesarFlujoSecuencialCasa(container) {
        clearInterval(this.timerClinico);
        window.speechSynthesis.cancel();

        const t = {
            es: { inspira: "Inhala ahora", expira: "Exhala ahora", fin: "Protocolo completado. Borrando rastro.", listen: "ESCUCHA MI GUÍA", launch: "ABRIR CANAL BIG TECH YA" },
            en: { inspira: "Inhale now", expira: "Exhale now", fin: "Protocol completed. Clearing tracks.", listen: "LISTEN TO THE GUIDE", launch: "OPEN BIG TECH CHANNEL NOW" }
        }[this.idiomaActual];

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

        this.tiempoRestanteCasa = 600; // 10 minutos
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
                if (this.contadorToques < this.secuenciaAdelantos.length) {
                    let adelantoSegundos = this.secuenciaAdelantos[this.contadorToques];
                    this.tiempoRestanteCasa = Math.max(this.tiempoRestanteCasa - adelantoSegundos, 0);
                    this.contadorToques++;
                    try {
                        let perfil = this.obtenerPerfilLocal();
                        perfil["indicador_ansiedad"] = Math.min((perfil["indicador_ansiedad"] || 0) + 10, 100);
                        localStorage.setItem("otg_perfil_dinamico", JSON.stringify(perfil));
                    } catch (e) { console.error("Error al actualizar indicador_ansiedad", e); }
                    let m = Math.floor(this.tiempoRestanteCasa / 60);
                    let s = this.tiempoRestanteCasa % 60;
                    if (timerDiv) {
                        timerDiv.innerText = `${m}:${s.toString().padStart(2, '0')}`;
                    }
                }
            };
        }

        this.timerClinico = setInterval(() => {
            this.relojRealSegundos--;
            if (this.tiempoRestanteCasa > 0) this.tiempoRestanteCasa--;
           
            let m = Math.floor(this.tiempoRestanteCasa / 60);
            let s = this.tiempoRestanteCasa % 60;
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
        this.procesarFlujoSecuencialCasa(container);
    },

    destruirYReiniciar() {
        clearInterval(this.timerInaccion);
        clearInterval(this.timerClinico);
        clearInterval(this.temporizadorCascada);
        clearInterval(this.timerChoqueSensorial);
        window.speechSynthesis.cancel();
        this.pasosMisiones = [];
        this.indiceMision = 0;
        this.isLocked = false;
        // sessionStorage.clear(); // No es necesario borrar toda la sesión, solo recargar
        location.reload();
    },

    // Funciones para manejar la selección de filtros (mente, budget, social)
    seleccionarFiltro(tipo, valor, element) {
        const parent = element.parentElement;
        parent.querySelectorAll(`.btn-${tipo}`).forEach(btn => btn.classList.remove('selected'));
        element.classList.add('selected');
       
        // Opcional: Hablar el nombre del filtro
        if (this.idiomaActual === 'es') {
            const nombreMente = {
                'aburrido': 'Aburrido', 'agotado': 'Agotado', 'estresado': 'Estresado', 'cansado': 'Cansado', 'ansioso': 'Ansioso',
                '0': 'Gratis', '1': 'Bajo Gasto',
                'solo': 'Solo', 'familia': 'Familia', 'hijos': 'Hijos', 'adultos mayores': 'Adultos Mayores', 'veteranos de guerra': 'Veteranos de Guerra',
                'directivos/empresarios': 'Directivos y Empresarios', 'trabajadores del gobierno': 'Trabajadores del Gobierno'
            }[valor] || valor;
            this.hablar(`${nombreMente} seleccionado.`);
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    KERNEL.init();
    // Inicializar listeners para los botones de filtro
    document.querySelectorAll('.btn-mente').forEach(btn => {
        btn.onclick = () => KERNEL.seleccionarFiltro('mente', btn.dataset.mente, btn);
    });
    document.querySelectorAll('.btn-budget').forEach(btn => {
        btn.onclick = () => KERNEL.seleccionarFiltro('budget', btn.dataset.budget, btn);
    });
    document.querySelectorAll('.btn-social').forEach(btn => {
        btn.onclick = () => KERNEL.seleccionarFiltro('social', btn.dataset.perfil, btn);
    });
});
