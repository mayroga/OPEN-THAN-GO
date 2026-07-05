// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.5.5.0
// Company: May Roga LLC
// File: static/engine.js
// PARTE 1 DE 4: Inicialización, Saludos de Choque Aleatorios y Motor de Voz Veloz

const KERNEL = {
    timer: null,
    timeLeft: 600,
    isLocked: false,
    idiomaActual: 'es',
    pasosMisiones: [],
    indiceMision: 0,
    datosLugarGlobal: null,
    tipoEscapeGlobal: "",
    listaAudiosChoqueGlobal: [],

    init() {
        const btnMando = document.getElementById('btn-mando') || document.getElementById('btn-main-trigger');
        if (btnMando) {
            btnMando.onclick = () => this.ejecutar();
        }
    },

    despertarInicial() {
        // Quita la pantalla negra de golpe y revela el mando de control interactivo
        document.getElementById('pantalla-bienvenida').style.display = 'none';
        document.getElementById('wrapper-form').classList.remove('hidden');
        
        // Catálogo máster de 10 entradas con palabras cortas, sencillas y de acompañamiento inmediato
        const saludosSorpresa = [
            "Bienvenido a ópen dán go. Tu escape inteligente. Estoy contigo ahora. Pon tus datos en el mando y hazlo conmigo ya.",
            "ópen dán go está activo en este segundo. Olvida tus biles por un momento. Escucha mi voz. Activa el mando ahora mismo.",
            "Entraste a ópen dán go. El despertador está encendido. Vamos a sacarte de la rutina gris en este instante. Hazlo conmigo.",
            "ópen dán go tomó el control. Deja de dar vueltas en círculos. Mira el mando. Pon tu zona y comencemos ya.",
            "Ya estás dentro de ópen dán go. No mires los colores de la pantalla. Siente tu respiración. Activa el mando ahora.",
            "ópen dán go te saluda hoy. El sistema te quiere dormido, pero yo te voy a despertar. Usa el mando en este segundo.",
            "Frecuencias alineadas en ópen dán go. Estoy al lado tuyo ahora. Rompamos el piloto automático juntos. Activa el mando ya.",
            "ópen dán go inició ahora. La vida está afuera, no en tus preocupaciones. Pon tus datos en la pantalla en este instante.",
            "Bienvenido al despierto de ópen dán go. Una acción corta puede cambiar tu día entero hoy. Haz clic en activar ya.",
            "Mando listo en ópen dán go. Tu mente necesita un escape real ahora mismo. No lo pienses más. Pon tu zona y camina conmigo."
        ];

        // Selecciona de forma aleatoria pura uno de los 10 impactos auditivos sorpresa
        const saludoElegido = saludosSorpresa[Math.floor(Math.random() * saludosSorpresa.length)];
        this.hablar(saludoElegido);
    },

    hablar(texto) {
        if (!texto) return;
        // Corta de raíz audios viejos al avanzar de fase, evitando que se sature el hardware del teléfono
        window.speechSynthesis.cancel(); 
        
        // HACK FONÉTICO UNIVERSAL: Reemplaza las siglas para obligar al teléfono a pronunciar ópen dán go de corrido
        let textoCorregido = texto.replace(/OPEN THAN GO/gi, "ópen dán go");
        textoCorregido = textoCorregido.replace(/OPEN DAN GO/gi, "ópen dán go");
        textoCorregido = textoCorregido.replace(/<[^>]*>/g, '');
        
        const msg = new SpeechSynthesisUtterance(textoCorregido);
        msg.lang = this.idiomaActual === 'es' ? 'es-US' : 'en-US';
        msg.rate = 1.15; // Velocidad de acción despierta acelerada, cero robótica, muy clara y asertiva
        msg.pitch = 1.0;
        window.speechSynthesis.speak(msg);
    },
// PARTE 2 DE 4: Conmutador de Idiomas, Captura Elástica de 4 Preguntas y Memoria Local

    cambiarIdioma(lang) {
        this.idiomaActual = lang;
        document.getElementById('lang-es').classList.toggle('active', lang === 'es');
        document.getElementById('lang-en').classList.toggle('active', lang === 'en');

        const contenidos = {
            es: { title: "OPEN THAN GO", zip: "Código Postal / Zona / Estado", mode: "Modo de Operación", mente: "Pregunta 1: ¿Dónde está atrapado tu agobio hoy?", budget: "Pregunta 2: ¿Cómo se siente tu motor físico ahora?", perfil: "Pregunta 3: ¿A quién tienes la obligación de arrastrar hoy?", desahogo: "Pregunta 4: Desahogo Emocional Corto (Filtro Mental)", placeholder: "Ej: trabajo, deudas, biles, veterano, dolor, alquiler...", btn: "ACTIVAR MANDO" },
            en: { title: "OPEN THAN GO", zip: "ZIP Code / Zone / State", mode: "Operation Mode", mente: "Question 1: Where is your burden trapped today?", budget: "Question 2: How does your physical engine feel right now?", perfil: "Question 3: Who do you have the obligation to drag today?", desahogo: "Question 4: Short Emotional Venting (Mental Filter)", placeholder: "Ex: job, bills, debts, veteran, pain, rent...", btn: "ACTIVATE CONTROL" }
        };

        const traduccion = contenidos[lang];
        document.getElementById('txt-app-title').innerText = traduccion.title;
        document.getElementById('lbl-zip').innerText = traduccion.zip;
        document.getElementById('lbl-mode').innerText = traduccion.mode;
        document.getElementById('lbl-mente').innerText = traduccion.mente;
        document.getElementById('lbl-budget').innerText = traduccion.budget;
        document.getElementById('lbl-perfil').innerText = traduccion.perfil;
        document.getElementById('lbl-desahogo').innerText = traduccion.desahogo;
        document.getElementById('inp-text').placeholder = traduccion.placeholder;
        document.getElementById('btn-mando').innerText = traduccion.btn;
        
        this.hablar(lang === 'es' ? "Idioma cambiado a español" : "Language switched to English");
    },

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;

        const payload = {
            zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
            mente: document.getElementById('inp-mente') ? document.getElementById('inp-mente').value : "agotado",
            modo: document.getElementById('modo-selector') ? document.getElementById('modo-selector').value : "SALIR",
            budget: document.getElementById('inp-budget') ? document.getElementById('inp-budget').value : "0",
            perfil: document.getElementById('inp-perfil') ? document.getElementById('inp-perfil').value : "solo",
            desahogo: document.getElementById('inp-text') ? document.getElementById('inp-text').value.trim() : "",
            estado: document.getElementById('inp-state') ? document.getElementById('inp-state').value : "FL"
        };

        const container = document.getElementById('wrapper-interactive');
        document.getElementById('wrapper-form').classList.add('hidden');
        container.innerHTML = `<div style='text-align:center; padding:40px 0;'><h2 style='color:#fff; font-size:1.1rem; letter-spacing:1px;'>CONECTANDO CON TU ENTORNO REAL...</h2></div>`;
        container.classList.remove('hidden');

        try {
            const respuesta = await fetch("/api/mando-integral", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await respuesta.json();
            
            // CONEXIÓN MASTER SIN SIMILITUDES: Sincronización exacta con las claves únicas de Python
            this.datosLugarGlobal = data; 
            this.tipoEscapeGlobal = data.DIRECCIONAMIENTO_MASTER; 
            this.indiceMision = 0;

            if (this.tipoEscapeGlobal === "INTERVENCION_DOMESTICA") {
                // Guardamos el lote de recordatorios específicos despachado de forma inteligente por el servidor
                this.listaAudiosChoqueGlobal = data.recordatorios_voz_choque || [];

                // Carga la lista de misiones completa (ya sean 30 o 50) si el protocolo incluye un número en su nombre
                if (/\d+/.test(data.tipo_protocolo)) {
                    this.pasosMisiones = data.misiones || [];
                } else {
                    // Flujo común de 3 pasos rotativos usando la memoria física local del dispositivo
                    let completadas = JSON.parse(localStorage.getItem('otg_completadas_50')) || [];
                    let disponibles = (data.misiones || []).filter(m => !completadas.includes(m.id));

                    if (disponibles.length < 3) {
                        completadas = [];
                        localStorage.setItem('otg_completadas_50', JSON.stringify([]));
                        disponibles = data.misiones || [];
                    }

                    this.pasosMisiones = disponibles.slice(0, 3);
                    this.pasosMisiones.forEach(m => completadas.push(m.id));
                    localStorage.setItem('otg_completadas_50', JSON.stringify(completadas));
                }
            } else {
                this.pasosMisiones = []; // Al salir va vacía porque se inyecta la tarjeta de campo directa
            }

            this.procesarFlujoSecuencial(container);
        } catch (error) {
            alert("Error de enlace satelital con el servidor.");
            document.getElementById('wrapper-form').classList.remove('hidden');
            container.classList.add('hidden');
            this.isLocked = false;
        }
    },

    procesarRespuesta(res) {
        this.isLocked = false;
    },
// PARTE 3 DE 4: Intervención de Choque, Segundo Negro y Despliegue de Veredicto Único

    procesarFlujoSecuencial(container) {
        clearInterval(this.timer);
        const traducciones = {
            es: { inspira: "Inhala ahora mismo", expira: "Exhala ahora mismo", fin_casa: "Protocolo completado. Borrando rastro de sesión por tu paz mental." },
            en: { inspira: "Inhale right now", expira: "Exhale right now", fin_casa: "Protocol completed. Clearing tracks for your mental peace." }
        };
        const traduccion = traducciones[this.idiomaActual];

        // EL BLOQUEO ABSOLUTO: Si es acción de campo, corta la casa de inmediato e inyecta la tarjeta de escape
        if (this.tipoEscapeGlobal === "ACCION_CAMPO") {
            if (this.datosLugarGlobal) {
                // EL EFECTO SORPRESA DE CHOQUE: Pantalla totalmente negra un segundo para romper tu letargo visual
                container.innerHTML = `<div style="position:fixed; top:0; left:0; width:100%; height:100%; background:#000; z-index:99999; display:flex; justify-content:center; align-items:center;"><h2 style="color:#fff; letter-spacing:3px; font-size:1.1rem; font-weight:900;">OPEN THAN GO DIRIGIENDO TU VIDA...</h2></div>`;
                
                setTimeout(() => {
                    let textoMostrar = this.datosLugarGlobal.destino_instruccion.replace(/\n/g, '<br>');
                    
                    // Inyección de las 3 alternativas obligatorias de contingencia por si el destino principal está cerrado
                    let opcionesHtml = "";
                    this.datosLugarGlobal.alternativas_contingencia.forEach((alt) => {
                        opcionesHtml += `
                            <div style="background:#111; padding:10px; margin-top:8px; border-radius:6px; border:1px solid #222; text-align:left;">
                                <span style="font-size:11px; color:#aaa; font-weight:bold; display:block;">INFRAESTRUCTURA DISPONIBLE ABIERTA:</span>
                                <strong style="font-size:12px; color:#fff; display:block; margin:2px 0;">${alt.titulo}</strong>
                                <small style="color:#777; display:block; margin-bottom:5px;">${alt.entorno}</small>
                                <button onclick="window.open('${alt.gps}', '_blank')" style="background:#222; color:#fff; padding:6px 12px; font-size:11px; margin-top:0; width:100%; text-transform:uppercase; font-weight:bold; border-radius:4px; cursor:pointer;">ACTIVAR ESTA RUTA YA</button>
                            </div>`;
                    });

                    container.innerHTML = `
                        <div class="mision-card" style="border: 1px solid #333; padding: 20px; text-align: center; background: #0a0a0a; border-radius: 12px;">
                            <h2 style="color:#d84315; font-weight:900; font-size:1.3rem;">${this.datosLugarGlobal.destino_titulo}</h2>
                            <p style="font-size:13px; color:#aaa; margin:5px 0;">${this.datosLugarGlobal.destino_entorno}</p>
                            <p style="font-size:11px; color:#2e7d32; font-weight:bold; text-transform:uppercase; margin:5px 0; letter-spacing:1px;">✨ TU SENDERO LUMINOSO HA SIDO ENCONTRADO ✨</p>
                            <hr style="border:0; border-top:1px dashed #333; margin:15px 0;">
                            <div style="text-align:left; font-size:13.5px; line-height:1.5; background:#111; padding:15px; border-radius:6px; border-left:4px solid #2e7d32; color:#fff; font-weight:500;">
                                ${textoMostrar}
                            </div>
                            <button id="btn-countdown-salida" style="width:100%; background:#222; color:#aaa; padding:16px; font-weight:bold; margin-top:15px;" disabled>35s ESCUCHA MI GUÍA</button>
                            <button id="btn-gps-action" class="hidden" style="width:100%; background:#4285f4; color:#fff; padding:16px; font-weight:bold; margin-top:15px; text-transform:uppercase; border-radius:6px; cursor:pointer;">EJECUTAR MANDO AHORA</button>
                            
                            <div style="margin-top:20px; border-top:1px solid #222; padding-top:15px;">
                                <p style="font-size:11px; font-weight:bold; color:#555; text-transform:uppercase; letter-spacing:1px; text-align:left; margin:0 0 5px 0;">⚠️ ENTORNO COMPLEMENTARIO BAJO TU CONTROL DE ACCIÓN INTERACTIVA:</p>
                                ${opcionesHtml}
                            </div>
                        </div>`;

                    // La voz autoritaria te amarra y te convence con oraciones cortas de acción directa
                    this.hablar("He tomado el control de tus decisiones. Escucha tu sendero luminoso. " + this.datosLugarGlobal.destino_instruccion);

                    let retencion = 35;
                    const btnCount = document.getElementById('btn-countdown-salida');
                    const btnGps = document.getElementById('btn-gps-action');

                    let relojSalida = setInterval(() => {
                        retencion--;
                        if (btnCount) btnCount.innerText = `${retencion}s ESCUCHA MI GUÍA`;
                        if (retencion <= 0) {
                            clearInterval(relojSalida);
                            if (btnCount) btnCount.style.display = 'none';
                            if (btnGps) {
                                btnGps.classList.remove('hidden');
                                // Abre de forma limpia la app oficial nativa de Google Maps, Amazon, Zillow o Meta asignada
                                btnGps.onclick = () => { window.open(this.datosLugarGlobal.destino_coordenadas_gps, '_blank'); };
                            }
                        }
                    }, 1000);
                }, 1000); // Un segundo exacto de apagón visual de choque somático
                return;
            }
        }

        // Si es Modo CASA, continúa con el flujo ordinario paso a paso del catálogo de misiones
        if (this.indiceMision >= this.pasosMisiones.length) {
            this.iniciarRelojClinicoCasa(container, traduccion);
            return;
        }

        const paso = this.pasosMisiones[this.indiceMision];
        container.innerHTML = `
            <div class="mision-card" style="background:#0a0a0a; border:1px solid #333; padding:25px; border-radius:12px; text-align:center;">
                <small style="color:#666; font-weight:bold; display:block; margin-bottom:5px;">INTERVENCION INTERNA</small>
                <h3 style="color:#2e7d32; font-size:1.25rem; font-weight:800; text-transform:uppercase; margin-top:0;">${paso.titulo}</h3>
                <p style="font-size:1.1rem; line-height:1.55; color:#eee; margin:15px 0; text-align:left; border-left:3px solid #2e7d32; padding-left:12px;">${paso.descripcion}</p>
                <button id="btn-next" style="width:100%; background:#2e7d32; color:#fff; padding:15px; font-weight:bold; text-transform:uppercase; border-radius:6px; cursor:pointer; margin-top:15px;">HAZLO CONMIGO AHORA</button>
            </div>`;
        
        this.hablar(paso.titulo + " . " + paso.descripcion);
        document.getElementById('btn-next').onclick = () => this.avanzarPaso();
    },
// PARTE 4 DE 4: Reloj Clínico de Casa, Guía de Voz cada 20s y Reset de Memoria de Hardware

    iniciarRelojClinicoCasa(container, traduccion) {
        this.hablar("Fase de misiones terminada. Iniciamos la sesión de limpieza mental profunda de diez minutos. Hazlo conmigo ahora. Sincroniza tu respiración.");
        container.innerHTML = `
            <div id="breath-circle"></div>
            <div id="timer" style="font-weight:900; text-align:center; font-size:2.8rem; margin:15px 0;">10:00</div>
            <p id="txt-pulmon" style="font-size:14px; text-transform:uppercase; font-weight:bold; color:#00bcd4; text-align:center;">INHALA / INSPIRA AHORA</p>
        `;
        this.timeLeft = 600;
        this.timer = setInterval(() => {
            this.timeLeft--;
            let m = Math.floor(this.timeLeft / 60);
            let s = this.timeLeft % 60;
            const timerDiv = document.getElementById('timer');
            const pulmonDiv = document.getElementById('txt-pulmon');
            if (timerDiv) timerDiv.innerText = `${m}:${s.toString().padStart(2, '0')}`;
            
            if (pulmonDiv) {
                let ciclo = this.timeLeft % 8;
                if (ciclo >= 4) { pulmonDiv.innerText = traduccion.inspira; pulmonDiv.style.color = "#00bcd4"; }
                else { pulmonDiv.innerText = traduccion.expira; pulmonDiv.style.color = "#d84315"; }
            }

            // REGLA DE ACOMPAÑAMIENTO DINÁMICA CLÍNICA: Ejecuta órdenes cortas cada 20 segundos fijos en silencio
            if (this.timeLeft > 0 && this.timeLeft % 20 === 0) {
                // Carga el lote de audios inyectado en secreto (Comunes, Veteranos, Gobierno, Senior, Jefes, Lesionados, Discapacidad)
                let listaAudios = this.listaAudiosChoqueGlobal && this.listaAudiosChoqueGlobal.length > 0 ? this.listaAudiosChoqueGlobal : [
                    "Sigue el pulso azul ahora. Estás conmigo.",
                    "Mantén el ritmo ahora. Estás ganando control."
                ];
                // Lanza la frase al azar a velocidad enérgica y asertiva corrida
                let audioElegido = listaAudios[Math.floor(Math.random() * listaAudios.length)];
                KERNEL.hablar(audioElegido);
            }

            if (this.timeLeft <= 0) {
                clearInterval(this.timer);
                this.hablar(traduccion.fin_casa);
                alert(traduccion.fin_casa);
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
        clearInterval(this.timer);
        window.speechSynthesis.cancel();
        this.pasosMisiones = [];
        this.indiceMision = 0;
        this.isLocked = false;
        location.reload(); // Borrado instantáneo de rastro en el hardware del teléfono para riesgo cero de saturación
    }
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());
