// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.3.3.0
// Company: May Roga LLC
// File: static/engine.js
// PARTE 1 DE 4: Inicialización, Sorpresa Inicial y Motor de Voz Activo

const KERNEL = {
    timer: null,
    timeLeft: 600,
    isLocked: false,
    idiomaActual: 'es',
    pasosMisiones: [],
    indiceMision: 0,
    datosLugarGlobal: null,
    tipoEscapeGlobal: "",

    init() {
        const btnMando = document.getElementById('btn-mando') || document.getElementById('btn-main-trigger');
        if (btnMando) {
            btnMando.onclick = () => this.ejecutar();
        }
    },

    despertarInicial() {
        // Quita la pantalla negra de golpe y revela el mando de control
        document.getElementById('pantalla-bienvenida').style.display = 'none';
        document.getElementById('wrapper-form').classList.remove('hidden');
        
        // Catálogo de 10 entradas con palabras cortas, sencillas y de acompañamiento inmediato
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

        // Selecciona al azar una de las 10 entradas humanas directas
        const saludoElegido = saludosSorpresa[Math.floor(Math.random() * saludosSorpresa.length)];
        
        // El teléfono ejecuta el audio veloz de inmediato
        this.hablar(saludoElegido);
    },

    hablar(texto) {
        if (!texto) return;
        window.speechSynthesis.cancel(); 
        
        // HACK DE MARCA: Sustituye el texto para obligar al teléfono a pronunciar "Open Dan Go" corrido
        let textoCorregido = texto.replace(/OPEN THAN GO/gi, "OPEN DAN GO");
        textoCorregido = textoCorregido.replace(/<[^>]*>/g, '');
        
        const msg = new SpeechSynthesisUtterance(textoCorregido);
        msg.lang = 'es-US';
        msg.rate = 1.15; // Velocidad de acción rápida y despierta, cero aburrida
        msg.pitch = 1.0;
        window.speechSynthesis.speak(msg);
    },
  
// PARTE 2 DE 4: Conmutador de Idiomas, Captura de Datos y Memoria Local Global de 50 Misiones

    cambiarIdioma(lang) {
        this.idiomaActual = lang;
        document.getElementById('lang-es').classList.toggle('active', lang === 'es');
        document.getElementById('lang-en').classList.toggle('active', lang === 'en');

        const contenidos = {
            es: { title: "OPEN THAN GO", zip: "Código Postal", mode: "Modo de Operación", mente: "Estado Mental", budget: "Presupuesto", perfil: "Perfil (Familia/Discapacidad)", desahogo: "Desahogo (Filtro Emocional)", placeholder: "Escribe libremente cómo te sientes hoy...", btn: "ACTIVAR MANDO" },
            en: { title: "OPEN THAN GO", zip: "ZIP Code", mode: "Operation Mode", mente: "Mental State", budget: "Budget Available", perfil: "Profile (Family/Disability)", desahogo: "Optional Venting (Filter)", placeholder: "Write freely about how you feel today...", btn: "ACTIVATE CONTROL" }
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
            
            // CONEXIÓN MASTER SIN SIMILITUDES: Sincronización perfecta con el nuevo backend
            this.datosLugarGlobal = data; 
            this.tipoEscapeGlobal = data.DIRECCIONAMIENTO_MASTER; 
            this.indiceMision = 0;

            if (this.tipoEscapeGlobal === "INTERVENCION_DOMESTICA") {
                let completadas = JSON.parse(localStorage.getItem('otg_completadas_50')) || [];
                let disponibles = data.misiones.filter(m => !completadas.includes(m.id));

                if (disponibles.length < 3) {
                    completadas = [];
                    localStorage.setItem('otg_completadas_50', JSON.stringify([]));
                    disponibles = data.misiones;
                }

                this.pasosMisiones = disponibles.slice(0, 3);
                this.pasosMisiones.forEach(m => completadas.push(m.id));
                localStorage.setItem('otg_completadas_50', JSON.stringify(completadas));
            } else {
                this.pasosMisiones = []; // Al salir, la lista va vacía porque se inyecta la tarjeta de Google Maps directa
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
 
// PARTE 3 DE 4: Discriminador Estricto de Rutas y Reloj de Retención de 35 Segundos (Corregido)

    procesarFlujoSecuencial(container) {
        clearInterval(this.timer);
        const traducciones = {
            es: { inspira: "Inhala ahora", expira: "Exhala ahora", fin_casa: "Protocolo completado. Borrando rastro de sesión por tu paz mental." },
            en: { inspira: "Inhale now", expira: "Exhale now", fin_casa: "Protocol completed. Clearing tracks for your mental peace." }
        };
        const traduccion = traducciones[this.idiomaActual];

        // EL BLOQUEO ABSOLUTO: Si es acción de campo, corta la casa e inyecta la tarjeta de Google Maps
        if (this.tipoEscapeGlobal === "ACCION_CAMPO") {
            if (this.datosLugarGlobal) {
                container.innerHTML = `
                    <div class="mision-card" style="border: 1px solid #333; padding: 20px; text-align: center; background: #0a0a0a; border-radius: 12px;">
                        <h2 style="color:#d84315; font-weight:900; font-size:1.3rem;">${this.datosLugarGlobal.destino_titulo}</h2>
                        <p style="font-size:13px; color:#aaa; margin:5px 0;">${this.datosLugarGlobal.destino_entorno}</p>
                        <hr style="border:0; border-top:1px dashed #333; margin:15px 0;">
                        <p style="text-align:left; font-size:14px; line-height:1.45; background:#111; padding:12px; border-radius:6px; border-left:4px solid #2e7d32; color:#fff;">
                            <strong>GUÍA ABSOLUTA DE ACCIÓN:</strong><br>${this.datosLugarGlobal.destino_instruccion}
                        </p>
                        <button id="btn-countdown-salida" style="width:100%; background:#222; color:#aaa; padding:16px; font-weight:bold; margin-top:15px;" disabled>35s ESCUCHA MI GUÍA</button>
                        <button id="btn-gps-action" class="hidden" style="width:100%; background:#4285f4; color:#fff; padding:16px; font-weight:bold; margin-top:15px;">ABRIR GOOGLE MAPS YA</button>
                    </div>`;

                // Lee de corrido la guía absoluta sin demoras pesadas
                this.hablar(this.datosLugarGlobal.destino_titulo + " . " + this.datosLugarGlobal.destino_instruccion);

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
                            // CORRECCIÓN DEFINITIVA: Llama a la variable exacta que envía Python
                            btnGps.onclick = () => { window.open(this.datosLugarGlobal.destino_coordenadas_gps, '_blank'); };
                        }
                    }
                }, 1000);
                return;
            }
        }

        // Si es Modo CASA, continúa con el flujo ordinario paso a paso de tus 50 misiones secuenciales
        if (this.indiceMision >= this.pasosMisiones.length) {
            this.iniciarRelojClinicoCasa(container, traduccion);
            return;
        }

        const paso = this.pasosMisiones[this.indiceMision];
        container.innerHTML = `
            <div class="mision-card">
                <small style="color:#666; font-weight:bold; display:block; margin-bottom:5px;">MISION INTERNA</small>
                <h3 style="color:#2e7d32; font-size:1.25rem; font-weight:800; text-transform:uppercase; margin-top:0;">${paso.titulo}</h3>
                <p style="font-size:1.1rem; line-height:1.55; color:#eee; margin:15px 0; text-align:left; border-left:3px solid #2e7d32; padding-left:12px;">${paso.descripcion}</p>
                <button id="btn-next" style="width:100%; background:#2e7d32; color:#fff; padding:15px; font-weight:bold; text-transform:uppercase; border-radius:6px; cursor:pointer; margin-top:15px;">HAZLO CONMIGO AHORA</button>
            </div>`;
        
        this.hablar(paso.titulo + " . " + paso.descripcion);
        document.getElementById('btn-next').onclick = () => this.avanzarPaso();
    },

// PARTE 4 DE 4: Reloj de Casa, Guía de Acompañamiento aleatoria expandida y Reset de Memoria

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

            // ACOMPAÑAMIENTO EN TIEMPO REAL EXPANDIDO CON 14 OPCIONES QUE NUNCA SE REPETIRÁN IGUAL
            if (this.timeLeft > 0 && this.timeLeft % 20 === 0) {
                let recordatorios = [
                    "Sigue el pulso azul ahora. Estás conmigo.",
                    "No mires tus biles. Respira ya.",
                    "Mantén el ritmo ahora. Estás ganando control.",
                    "Siente el peso fuera de tus hombros en este segundo.",
                    "Te estoy acompañando. No estás solo. Hazlo conmigo.",
                    "Siente el aire limpiando tu pecho ahora mismo.",
                    "El piloto automático está apagado. Continúa.",
                    "Quédate en este instante. El presente es tuyo.",
                    "Siente tus pies firmes. El suelo te sostiene gratis.",
                    "Suelta la mandíbula ahora. Libera esa carga ya.",
                    "Tu mente está despertando en este segundo. Sigue así.",
                    "Eres más grande que tus deudas. Respira hondo.",
                    "Rompe el zombi que llevas dentro en este instante.",
                    "Escucha mi voz. Quédate en la sala conmigo ahora."
                ];
                // Elige de forma aleatoria pura entre las 14 opciones dinámicas
                KERNEL.hablar(recordatorios[Math.floor(Math.random() * recordatorios.length)]);
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
        location.reload(); // Borrado instantáneo de rastro en el hardware
    }
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());
