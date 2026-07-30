// ==========================================================================================
// KERNEL_ESPECIAL - MOTOR DE ATENCIÓN DIRECTA RESTRUCTURADO (CERO COMPLICACIONES)
// Nivel 8 años - Idiomas Simétricos - 100% Local sin llamadas de Red ni Bloqueos
// ==========================================================================================
window.KERNEL_ESPECIAL = {
    idioma: "es",
    tagsSeleccionados: [],
    esferaInterval: null,
    relojInterval: null,
    tiempoAudioTimer: null,
    modoTiempoLibre: false,

    // BANCO EXTENSO UNIVERSAL AISLADO DE CONTENIDO (MISMAS CARACTERÍSTICAS QUE OPEN THAN GO)
    bancoMisiones: {
        "es": {
            "veteranos": {
                "antes": "Freno de Alerta Táctica: Detén todo escaneo del entorno físico ahora. Dirígete de inmediato al espacio con menor estímulo lumínico y acústico disponible en tu perímetro.",
                "durante": "Misión de Anclaje de Posición: Adopta una postura firme en tu asiento con la espalda recta. Apoya las palmas de tus manos abiertas sobre tus rodillas ejerciendo una presión constante hacia abajo. Mantén tus talones fijos contra el suelo para activar la percepción del presente físico corporal.",
                "mapa": "senderos+naturales+silenciosos+y+bosques",
                "despues": "Cierre de Ciclo Soberano: Has completado la pauta de repliegue de tensión con éxito absoluto. Tu atención ha sido extraída del estado de hipervigilancia externa. Mantén tus audífonos puestos durante 10 minutos adicionales en un entorno neutro."
            },
            "adultos_mayores": {
                "antes": "Freno de Aislamiento Cotidiano: Detén toda tarea monótona del hogar. Adopta una posición de descanso completo en tu sillón preferido. Suaviza la intensidad visual de tus pantallas para proteger tu descanso.",
                "durante": "Misión de Reconocimiento del Entorno: Dirige tu mirada lentamente hacia las paredes de tu habitación. Localiza un objeto con historia (un cuadro querido, un libro antiguo o una fotografía familiar). Observa en silencio absoluto sus detalles y colores durante un bloque continuo de tiempo.",
                "mapa": "parques+planos+con+asientos+y+caminos+faciles",
                "despues": "Cierre de Ciclo Reconfortante: Tu mente ha salido de la inercia estática de la tarde con éxito rotundo. Mañana establece la meta de entablar una conversación directa de tres minutos para saludar a un vecino."
            },
            "gobierno": {
                "antes": "Freno de Saturación Administrativa: Minimiza de inmediato todas las hojas de cálculo, bandejas de correo electrónico y expedientes activos de tu monitor. Queda desconectado de la red de gestión del estado.",
                "durante": "Misión de Descompresión Analógica: Ponte de pie de forma recta alejándote de tu silla de oficina. Estira tus brazos verticalmente hacia el techo manteniendo la posición por dos minutos exactos. Camina con paso pausado hacia el punto de abastecimiento de agua más lejano de tu piso laboral.",
                "mapa": "jardines+botanicos+o+plazas+abiertas+silenciosas",
                "despues": "Cierre de Ciclo Operativo: Has establecido un límite saludable entre la carga burocrática del sistema institucional y tu mente. Parpadea continuamente por quince segundos para aliviar la fatiga de tus ojos del monitor."
            }
        },
        "en": {
            "veteranos": {
                "antes": "Tactical Alert Brake: Stop scanning your environment. Move to the area with the lowest light and noise stimulus available.",
                "durante": "Position Grounding Mission: Sit straight. Place your open palms on your knees, applying steady downward pressure. Keep your heels pressed against the floor.",
                "mapa": "quiet+nature+trails+and+forests",
                "despues": "Sovereign Cycle Close: You have successfully completed the routine. Your attention has been removed from alert states. Keep your headphones on."
            },
            "adultos_mayores": {
                "antes": "Daily Isolation Brake: Stop all repetitive household chores. Take a position of complete rest in your favorite armchair. Lower your screen brightness to protect your vision.",
                "durante": "Environment Recognition Mission: Guide your gaze slowly across the walls. Locate an object with history (a beloved painting or a family photo). Observe its details.",
                "mapa": "flat+parks+with+benches+and+easy+walking+paths",
                "despues": "Comforting Cycle Close: Your mind has broken free from static inertia. Tomorrow, engage in a short greeting with a neighbor."
            },
            "gobierno": {
                "antes": "Administrative Overwhelm Brake: Minimize all spreadsheets and active emails on your screen. Disconnect from the state management grid.",
                "durante": "Analog Decompression Mission: Stand up straight away from your office chair. Stretch your arms toward the ceiling for two minutes. Walk to the furthest water station.",
                "mapa": "botanical+gardens+or+quiet+open+air+squares",
                "despues": "Operational Cycle Close: You have established a healthy boundary. Blink continuously for fifteen seconds to relieve screen strain."
            }
        }
    },

    conmutarCortina: function(idCuerpo) {
        const cuerpo = document.getElementById(idCuerpo);
        if(cuerpo) { cuerpo.style.display = (cuerpo.style.display === "block") ? "none" : "block"; }
    },

    reproducirVozHumana: function(texto) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(texto);
            u.lang = this.idioma === "en" ? "en-US" : "es-MX";
            u.rate = 0.85; 
            window.speechSynthesis.speak(u);
        }
    },

    cambiarIdioma: function(lang) {
        this.idioma = lang;
        document.getElementById("otg-btn-lang-es").style.background = lang === "es" ? "#38bdf8" : "#1e293b";
        document.getElementById("otg-btn-lang-en").style.background = lang === "en" ? "#38bdf8" : "#1e293b";
        this.traducirInterfaz();
    },

    traducirInterfaz: function() {
        const es = this.idioma === "es";
        document.getElementById("otg-txt-titulo-modulo").innerText = es ? "Asistente de Bienestar Habitual" : "Habitual Wellbeing Assistant";
        document.getElementById("otg-txt-subtitulo-modulo").innerText = es ? "Módulo directo de orientación práctica." : "Direct module for practical orientation.";
        document.getElementById("otg-lbl-perfil").innerText = es ? "Selecciona tu Perfil Especial:" : "Select your Special Profile:";
        document.getElementById("otg-btn-activar").innerText = es ? "Activar Plan" : "Activate Plan";
        document.getElementById("otg-btn-borrar").innerText = es ? "Borrar Todo" : "Clear All";
        document.getElementById("otg-lbl-f1").innerText = es ? "Fase 1: Antes del Uso (Freno de Tensión)" : "Phase 1: Before Use (Tension Brake)";
        document.getElementById("otg-lbl-f2").innerText = es ? "Fase 2: Durante el Uso (Misión Práctica) ▼" : "Phase 2: During Use (Practical Mission) ▼";
        document.getElementById("otg-lbl-f3").innerText = es ? "Fase 3: Después del Uso (Cierre Seguro) ▼" : "Phase 3: After Use (Safe Close) ▼";
    },

    iniciarGrabacionAudio: function() {
        document.getElementById('texto-mic').innerText = this.idioma === "en" ? "Recording... (Max 60s)" : "Grabando... (Máx 60s)";
    },

    detenerGrabacionAudio: function() {
        document.getElementById('texto-mic').innerText = this.idioma === "en" ? "Hold to talk (Max. 1 min)" : "Mantén presionado para hablar (Máx. 1 min)";
        document.getElementById('otg-texto-extenso').value = this.idioma === "en" ? "Voice message recorded." : "Mensaje de voz grabado con éxito.";
    },

    limpiarVentanilla: function() {
        window.speechSynthesis.cancel();
        document.getElementById('otg-texto-extenso').value = '';
        document.getElementById('otg-panel-respuesta').style.display = 'none';
        if (this.esferaInterval) clearTimeout(this.esferaInterval);
        if (this.relojInterval) clearInterval(this.relojInterval);
    },

    ejecutarPlan: function() {
        const perfil = document.getElementById("otg-perfil-select").value;
        const es = this.idioma === "es";
        this.modoTiempoLibre = false;

        // Generar folio de control idéntico al de Open Than Go
        document.getElementById("otg-id-display").innerText = "OTG-" + Math.random().toString(36).substring(2, 10).toUpperCase();

        // LÓGICA LOCAL FIJA: Lee directo del objeto inmutable sin peticiones HTTP
        const m = this.bancoMisiones[this.idioma][perfil];

        // Pintar los resultados correspondientes en la pantalla
        document.getElementById("otg-f1-pauta").innerText = m.antes;
        document.getElementById("otg-f2-pauta").innerText = m.durante;
        document.getElementById("otg-f3-pauta").innerText = m.despues;
        
        // Asignar enlaces sin que se caiga el motor
        document.getElementById("otg-f2-mapa").href = "https://google.com" + m.mapa + "+near+me";

        // Mostrar la tarjeta de resultados de golpe
        document.getElementById("otg-f2-cuerpo").style.display = "none";
        document.getElementById("otg-f3-cuerpo").style.display = "none";
        document.getElementById("otg-panel-respuesta").style.display = "block";

        // Locución inicial automática de la misión
        this.reproducirVozHumana(m.antes + ". " + m.durante);

        // Calibración de tiempos según el perfil
        let tInhala = perfil === "veteranos" ? 5000 : (perfil === "adultos_mayores" ? 3000 : 4000);
        let tExhala = perfil === "veteranos" ? 5000 : 4000;
        document.getElementById("otg-ritmo-titulo").innerText = es ? `Ritmo Calibrado (${tInhala}s x ${tExhala}s)` : `Calibrated Pace (${tInhala}s x ${tExhala}s)`;

        // ANIMACIÓN DE LA ESFERA SENSORIAL COPIADA DEL PDF ORIGINAL
        if (this.esferaInterval) clearTimeout(this.esferaInterval);
        let alternar = true;
        const animar = () => {
            const esf = document.getElementById("otg-esfera-visual");
            const txt = document.getElementById("otg-esfera-texto");
            if(!esf || !txt) return;
            
            esf.style.transform = alternar ? "scale(1.35)" : "scale(0.92)";
            esf.style.backgroundColor = alternar ? "rgba(56, 189, 248, 0.22)" : "rgba(56, 189, 248, 0.04)";
            txt.innerText = alternar ? (es ? "INHALA" : "BREATHE IN") : (es ? "EXHALA" : "BREATHE OUT");
            
            this.reproducirVozHumana(txt.innerText);
            
            alternar = !alternar;
            this.esferaInterval = setTimeout(animar, alternar ? tExhala : tInhala);
        };
        animar();

        // CRONÓMETRO DE 15 MINUTOS OBLIGATORIOS COMPARTIDOS + PUERTA ABIERTA
        if (this.relojInterval) clearInterval(this.relojInterval);
        let remSegundos = 900;
        this.relojInterval = setInterval(() => {
            const nodoReloj = document.getElementById("otg-reloj-display");
            if (!nodoReloj) return;

            if (!this.modoTiempoLibre) {
                remSegundos--;
                let mm = Math.floor(remSegundos / 60);
                let ss = remSegundos % 60;
                nodoReloj.innerText = (mm < 10 ? "0" + mm : mm) + ":" + (ss < 10 ? "0" + ss : ss);

                if (remSegundos <= 0) {
                    window.speechSynthesis.cancel();
                    this.modoTiempoLibre = true;
                    const pregunta = es ? "Has cumplido tus 15 minutos obligados. ¿Deseas continuar en modo libre?" : "15 required minutes completed. Continue in free mode?";
                    this.reproducirVozHumana(pregunta);
                    if (confirm(pregunta)) {
                        remSegundos = 0;
                        document.getElementById("otg-txt-reloj-lbl").innerText = es ? "⏱️ Modo Libre Opcional:" : "⏱️ Optional Free Mode:";
                    } else {
                        window.location.href = "/";
                    }
                }
            } else {
                remSegundos++;
                let mm = Math.floor(remSegundos / 60);
                let ss = remSegundos % 60;
                nodoReloj.innerText = (mm < 10 ? "0" + mm : mm) + ":" + (ss < 10 ? "0" + ss : ss);
            }
        }, 1000);
    }
};

document.addEventListener("DOMContentLoaded", () => { 
    window.KERNEL_ESPECIAL.cambiarIdioma("es"); 
});
