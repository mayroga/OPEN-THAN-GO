
// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.6.5.0
// Company: May Roga LLC
// File: static/engine.js

const KERNEL = {
    timerInaccion: null,
    timerClinico: null,
    temporizadorCascada: null,
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
            return { "movimiento": 50, "naturaleza": 50, "silencio": 50 };
        }
    },

    init() {
        this.bloqueActual = parseInt(localStorage.getItem("otg_bloque_secuencial")) || 0;
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
        }, 12000);
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
            alert("Error de conexión.");
            document.getElementById('wrapper-form').classList.remove('hidden');
            container.classList.add('hidden');
            this.isLocked = false;
        }
    },

    procesarFlujoSecuencial(container) {
        clearInterval(this.timerClinico);
        window.speechSynthesis.cancel();

        const t = {
            es: { inspira: "Inhala ahora", expira: "Exhala ahora", fin: "Protocolo completado. Borrando rastro.", listen: "ESCUCHA MI GUÍA", launch: "ABRIR CANAL BIG TECH YA" },
            en: { inspira: "Inhale now", expira: "Exhale now", fin: "Protocol completed. Clearing tracks.", listen: "LISTEN TO THE GUIDE", launch: "OPEN BIG TECH CHANNEL NOW" }
        }[this.idiomaActual];

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
        window.speechSynthesis.cancel();
        this.pasosMisiones = [];
        this.indiceMision = 0;
        this.isLocked = false;
        sessionStorage.clear();
        location.reload();
    }
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());
