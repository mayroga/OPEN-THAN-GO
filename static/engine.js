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
        // Disparador de urgencia inicial
        this.iniciarMonitoreoAtencion();
    },

    // NUEVO: Motor de urgencia para evitar abandono (Estilo Amazon/FB)
    iniciarMonitoreoAtencion() {
        setInterval(() => {
            if (!this.isLocked && document.getElementById('wrapper-form') && !document.getElementById('wrapper-form').classList.contains('hidden')) {
                // Si el usuario lleva más de 30 segundos sin hacer clic en el mando
                this.hablar("El tiempo de tu despertar corre. No te detengas. Toca el mando ahora.");
            }
        }, 30000); 
    },

    despertarInicial() {
        document.getElementById('pantalla-bienvenida').style.display = 'none';
        document.getElementById('wrapper-form').classList.remove('hidden');
        
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

        const saludoElegido = saludosSorpresa[Math.floor(Math.random() * saludosSorpresa.length)];
        this.hablar(saludoElegido);
    },

    hablar(texto) {
        if (!texto) return;
        window.speechSynthesis.cancel();
        
        let textoCorregido = texto.replace(/OPEN THAN GO/gi, "OPEN DAN GO");
        textoCorregido = textoCorregido.replace(/<[^>]*>/g, '');
        
        const msg = new SpeechSynthesisUtterance(textoCorregido);
        msg.lang = 'es-US';
        msg.rate = 1.15; 
        msg.pitch = 1.0;
        window.speechSynthesis.speak(msg);
    },

    // NUEVO: Refuerzo de dopamina tras interacción
    reforzarLogro() {
        this.hablar("Bien. Tu sistema interno ha procesado la instrucción. El siguiente paso ya está listo.");
    }
    // PARTE 2 DE 4: Conmutador de Idiomas, Captura de Datos y Memoria Local Global de 50 Misiones

    cambiarIdioma(lang) {
        this.idiomaActual = lang;
        document.getElementById('lang-es').classList.toggle('active', lang === 'es');
        document.getElementById('lang-en').classList.toggle('active', lang === 'en');

        const contenidos = {
            es: { title: "OPEN DAN GO", zip: "Código Postal", mode: "Modo de Operación", mente: "Estado Mental", budget: "Presupuesto", perfil: "Perfil (Familia/Discapacidad)", desahogo: "Desahogo (Filtro Emocional)", placeholder: "Escribe libremente cómo te sientes hoy...", btn: "ACTIVAR MANDO" },
            en: { title: "OPEN DAN GO", zip: "ZIP Code", mode: "Operation Mode", mente: "Mental State", budget: "Budget Available", perfil: "Profile (Family/Disability)", desahogo: "Optional Venting (Filter)", placeholder: "Write freely about how you feel today...", btn: "ACTIVATE CONTROL" }
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
        
        this.hablar(lang === 'es' ? "Idioma cambiado." : "Language switched.");
    },

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;

        // Captura directa y reforzada
        const payload = {
            zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
            mente: document.getElementById('inp-mente') ? document.getElementById('inp-mente').value : "agotado",
            modo: document.getElementById('modo-selector') ? document.getElementById('modo-selector').value : "SALIR",
            budget: document.getElementById('inp-budget') ? document.getElementById('inp-budget').value : "0",
            perfil: document.getElementById('inp-perfil') ? document.getElementById('inp-perfil').value : "solo",
            desahogo: document.getElementById('inp-text') ? document.getElementById('inp-text').value.trim() : "",
            estado: document.getElementById('inp-state') ? document.getElementById('inp-state').value : "FL"
        };

        // Feedback inmediato: El sistema confirma la captura y toma control
        this.reforzarLogro(); 
        
        const container = document.getElementById('wrapper-interactive');
        document.getElementById('wrapper-form').classList.add('hidden');
        container.innerHTML = `<div style='text-align:center; padding:40px 0;'><h2 style='color:#fff; font-size:1.1rem; letter-spacing:1px;'>PROCESANDO TU DESPERTAR...</h2></div>`;
        container.classList.remove('hidden');

        try {
            const respuesta = await fetch("/api/mando-integral", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await respuesta.json();
            
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
                this.pasosMisiones = []; 
            }

            this.procesarFlujoSecuencial(container);
        } catch (error) {
            this.hablar("Error de conexión. Reintenta tu despertar.");
            document.getElementById('wrapper-form').classList.remove('hidden');
            container.classList.add('hidden');
            this.isLocked = false;
        }
    },

    procesarRespuesta(res) {
        this.isLocked = false;
    },
// PARTE 3 DE 4: Discriminador Estricto de Rutas y Reloj de Retención de 35 Segundos

    procesarFlujoSecuencial(container) {
        clearInterval(this.timer);
        const traducciones = {
            es: { inspira: "Inhala ahora", expira: "Exhala ahora", fin_casa: "Protocolo completado. Sesión cerrada para tu paz mental." },
            en: { inspira: "Inhale now", expira: "Exhale now", fin_casa: "Protocol completed. Session closed for your mental peace." }
        };
        const traduccion = traducciones[this.idiomaActual];

        // EL BLOQUEO ABSOLUTO: El sistema decide, el usuario ejecuta.
        if (this.tipoEscapeGlobal === "ACCION_CAMPO") {
            if (this.datosLugarGlobal) {
                let textoMostrar = this.datosLugarGlobal.destino_instruccion.replace(/\n/g, '<br>');

                container.innerHTML = `
                    <div class="mision-card" style="border: 1px solid #333; padding: 20px; text-align: center; background: #0a0a0a; border-radius: 12px;">
                        <h2 style="color:#d84315; font-weight:900; font-size:1.3rem;">${this.datosLugarGlobal.destino_titulo}</h2>
                        <p style="font-size:13px; color:#aaa; margin:5px 0;">${this.datosLugarGlobal.destino_entorno}</p>
                        <hr style="border:0; border-top:1px dashed #333; margin:15px 0;">
                        <div style="text-align:left; font-size:13.5px; line-height:1.5; background:#111; padding:15px; border-radius:6px; border-left:4px solid #2e7d32; color:#fff; font-weight:500;">
                            ${textoMostrar}
                        </div>
                        <button id="btn-countdown-salida" style="width:100%; background:#222; color:#aaa; padding:16px; font-weight:bold; margin-top:15px;" disabled>35s ESCUCHA MI GUÍA</button>
                        <button id="btn-gps-action" class="hidden" style="width:100%; background:#4285f4; color:#fff; padding:16px; font-weight:bold; margin-top:15px;">ABRIR GOOGLE MAPS YA</button>
                    </div>`;

                this.hablar("Veredicto listo. " + this.datosLugarGlobal.destino_instruccion);

                let retencion = 35;
                const btnCount = document.getElementById('btn-countdown-salida');
                const btnGps = document.getElementById('btn-gps-action');

                let relojSalida = setInterval(() => {
                    retencion--;
                    if (btnCount) btnCount.innerText = `${retencion}s ESCUCHA MI GUÍA`;
                    
                    // Refuerzo constante: recordatorio cada 10 segundos para evitar abandono
                    if (retencion === 25 || retencion === 10) {
                        this.hablar("Mantente enfocado en la instrucción. Estoy contigo.");
                    }

                    if (retencion <= 0) {
                        clearInterval(relojSalida);
                        if (btnCount) btnCount.style.display = 'none';
                        if (btnGps) {
                            btnGps.classList.remove('hidden');
                            this.hablar("La ruta está desbloqueada. Muévete ahora.");
                            btnGps.onclick = () => { window.open(this.datosLugarGlobal.destino_coordenadas_gps, '_blank'); };
                        }
                    }
                }, 1000);
                return;
            }
        }

        // Si es Modo CASA, continúa con el flujo ordinario
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
import random
import time

# --- Parte 4: Reloj, Aleatoriedad y Reset ---

def system_clock():
    """Retorna el tiempo actual del sistema."""
    return time.strftime("%H:%M:%S")

def get_random_accompaniment():
    """Selección aleatoria para interacción dinámica."""
    options = [
        "¿Requiere asistencia adicional con la carga?",
        "Estoy aquí para revisar los parámetros actuales.",
        "¿Desea ajustar algún detalle de la estiba?"
    ]
    return random.choice(options)

def reset_memory(session_data):
    """Limpieza de memoria para mantener la privacidad."""
    session_data.clear()
    return "Memoria del sistema restablecida correctamente."

# --- Ejemplo de uso ---
# print(f"Hora: {system_clock()}")
# print(get_random_accompaniment())
# reset_memory(my_data_dict)
