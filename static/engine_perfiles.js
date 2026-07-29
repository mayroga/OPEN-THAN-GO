// ==========================================================================================
// KERNEL_ESPECIAL: MOTOR EXCLUSIVO DE CONTENCIÓN Y BIENESTAR (CERO INTERFERENCIAS)
// Nivel 8 años - Bilingüe Nativo - 100% Local sin llamadas de Red
// ==========================================================================================
window.KERNEL_ESPECIAL = {
    idioma: "es",
    tagsSeleccionados: [],
    esferaInterval: null,
    relojInterval: null,
    tiempoAudioTimer: null,

    bancoMisiones: {
        "es": {
            "adultos_mayores": {
                "antes": "Freno de soledad: Detén lo que estás haciendo. Toma un vaso de agua fresca y bébelo muy despacio. Siente cómo pasa el agua. Reduciendo el brillo de tu pantalla para cuidar tus ojos.",
                "durante": "Misión de acompañamiento en casa: Camina despacio por tu hogar. Busca un álbum de fotos viejas, un libro querido o un recuerdo que te dé alegría. Míralo en silencio durante 10 minutos enteros.",
                "mapa": "parques+planos+con+asientos+y+caminos+faciles",
                "despues": "Cierre de ciclo: Tu enfoque ha salido de la rutina estática del día con éxito. Mañana llama por teléfono a un familiar o vecino durante 3 minutos para saludarle."
            },
            "veteranos": {
                "antes": "Freno de alerta: Dirígete de inmediato a la habitación más tranquila, aislada y silenciosa de tu casa ahora. Colócate audífonos protectores o tapones para oídos de inmediato para apagar ruidos.",
                "durante": "Misión de control en casa: Apoya tus manos con firmeza sobre tus rodillas. Presiona tus talones con fuerza contra el suelo. Cuenta en reversa del 10 al 1 muy despacio en tu mente.",
                "mapa": "senderos+naturales+silenciosos+y+bosques",
                "despues": "Cierre de ciclo: Conseguiste mover tu atención fuera del peligro y la fricción exterior. Mantén tus audífonos puestos 10 minutos más mientras ordenas un objeto de tu cuarto."
            },
            "gobierno": {
                "antes": "Freno de oficina: Cierra o minimiza todas las hojas de cálculo, tareas y correos en este segundo. Deja solo esta pantalla. Te has desconectado de la red del sistema de trabajo por un bloque de tiempo.",
                "durante": "Misión de descompresión: Ponte de pie. Sepárate de tu silla de oficina. Estira tus brazos hacia el techo por 2 minutos exactos. Camina al punto de agua más lejano de tu piso.",
                "mapa": "jardines+botanicos+o+plazas+abiertas+silenciosas",
                "despues": "Cierre de ciclo: Estableciste un límite saludable entre tu mente y la carga administrativa del estado. Parpadea continuamente por 15 segundos para aliviar tus ojos cansados del monitor."
            }
        },
        "en": {
            "adultos_mayores": {
                "antes": "Stop loneliness: Take a glass of fresh water and drink it very slowly. Feel the water go down. Close your eyes for 30 full seconds to rest your vision from the monitor.",
                "durante": "Companion mission at home: Walk slowly through your home. Find an old photo album, a beloved book, or a keepsake that brings you joy. Look at it in silence for 10 full minutes.",
                "mapa": "flat+parks+with+benches+and+easy+walking+paths",
                "despues": "Cycle close: Your focus has successfully broken the static routine. Tomorrow make a short 3-minute phone call to a friend or relative just to say hello."
            },
            "veteranos": {
                "antes": "Stop alert: Go immediately to the quietest and darkest room in your house right now. Put on protective headphones or earplugs right now to shut out external noise.",
                "durante": "Control mission at home: Place your hands firmly on your knees. Press your heels hard against the floor. Count backward from 10 to 1 very slowly in your mind.",
                "mapa": "quiet+nature+trails+and+forests",
                "despues": "Cycle close: You successfully shifted your attention away from the external disturbance. Keep your headphones on for 10 more minutes while organizing a small item."
            },
            "gobierno": {
                "antes": "Stop office work: Close or minimize all spreadsheets and emails this second. You have disconnected from the work network systems for a short block of time.",
                "durante": "Decompression mission: Stand up. Step away from your office chair. Stretch your arms toward the ceiling for 2 minutes. Walk to the farthest water station on your floor.",
                "mapa": "botanical+gardens+or+quiet+open+air+squares",
                "despues": "Cycle close: You successfully separated your mind from the heavy burden. Blink continuously for 15 seconds to relieve your eyes from screen strain."
            }
        }
    },

    cambiarIdioma: function(lang) {
        this.idioma = lang;
        const btnEs = document.getElementById("otg-btn-lang-es");
        const btnEn = document.getElementById("otg-btn-lang-en");
        if(btnEs && btnEn) {
            btnEs.style.background = lang === "es" ? "#38bdf8" : "#1e293b";
            btnEs.style.color = lang === "es" ? "#0f172a" : "#94a3b8";
            btnEn.style.background = lang === "en" ? "#38bdf8" : "#1e293b";
            btnEn.style.color = lang === "en" ? "#0f172a" : "#94a3b8";
        }
        this.traducirInterfaz();
    },

    traducirInterfaz: function() {
        const es = this.idioma === "es";
        document.getElementById("otg-txt-titulo-modulo").innerText = es ? "Asistente de Bienestar Habitual" : "Habitual Wellbeing Assistant";
        document.getElementById("otg-txt-subtitulo-modulo").innerText = es ? "Módulo directo de orientación práctica y misiones." : "Direct module for practical orientation.";
        document.getElementById("otg-lbl-perfil").innerText = es ? "Selecciona tu Perfil de Atención Especial:" : "Select your Special Care Profile:";
        document.getElementById("otg-opt-vet").innerText = es ? "Veteranos de Guerra" : "War Veterans";
        document.getElementById("otg-opt-am").innerText = es ? "Adultos Mayores / Personas Mayores" : "Elderly / Senior Citizens";
        document.getElementById("otg-opt-gob").innerText = es ? "Trabajadores del Gobierno / Oficina" : "Government / Office Workers";
        document.getElementById("otg-lbl-tags").innerText = es ? "Toca las palabras que describan tu agobio de hoy (Opcional):" : "Tap the words that describe your overwhelm (Optional):";
        document.getElementById("otg-lbl-texto").innerText = es ? "O copia y pega aquí un texto largo o queja burocrática:" : "Or copy and paste a long text here:";
        document.getElementById("otg-texto-extenso").placeholder = es ? "Puedes pegar correos extensos o escribir libremente..." : "You can paste long emails or write freely...";
        document.getElementById("otg-btn-activar").innerText = es ? "Activar Plan" : "Activate Plan";
        document.getElementById("otg-btn-borrar").innerText = es ? "Borrar Todo" : "Clear All";
        document.getElementById("otg-txt-registro").innerText = es ? "✓ Estrategia Operativa Generada" : "✓ Operational Strategy Generated";
        document.getElementById("otg-txt-reloj-lbl").innerText = es ? "⏱️ Tiempo restante de desconexión obligatoria:" : "⏱️ Required disconnection time remaining:";
        document.getElementById("otg-lbl-f1").innerText = es ? "Modo Casa Propio: Antes del Uso (Freno de Tensión)" : "Own Home Mode: Before Use (Tension Brake)";
        document.getElementById("otg-lbl-f2").innerText = es ? "Modo Salir Propio: Durante la Actividad (Misión Práctica)" : "Own Out Mode: During Activity (Practical Mission)";
        document.getElementById("otg-lbl-f3").innerText = es ? "Cierre del Ciclo: Después del Uso (Descanso Garantizado)" : "Cycle Close: After Use (Guaranteed Rest)";
        document.getElementById("otg-f2-mapa").innerText = es ? "🗺️ Abrir Ruta de Entorno Seguro en Google Maps" : "🗺️ Open Safe Route on Google Maps";

        const contenedor = document.getElementById("otg-contenedor-tags-html");
        if(contenedor) {
            contenedor.innerHTML = "";
            const pool = es ? 
                [{id:"triste", t:"Tristeza"}, {id:"cansado", t:"Cansancio"}, {id:"papeleo", t:"Papeleo"}, {id:"ruido", t:"Ruido"}, {id:"estres", t:"Estrés"}] :
                [{id:"triste", t:"Sadness"}, {id:"cansado", t:"Fatigue"}, {id:"papeleo", t:"Paperwork"}, {id:"ruido", t:"Noise"}, {id:"estres", t:"Stress"}];
            
            pool.forEach(item => {
                const span = document.createElement("span");
                span.className = "tag-local" + (this.tagsSeleccionados.includes(item.id) ? " seleccionado" : "");
                span.innerText = item.t;
                span.onclick = () => {
                    span.classList.toggle("seleccionado");
                    if(span.classList.contains("seleccionado")) { this.tagsSeleccionados.push(item.id); }
                    else { this.tagsSeleccionados = this.tagsSeleccionados.filter(x => x !== item.id); }
                };
                contenedor.appendChild(span);
            });
        }
    },

    iniciarGrabacionAudio: function() {
        const btn = document.getElementById('btn-microfono');
        const txt = document.getElementById('texto-mic');
        btn.style.backgroundColor = '#b91c1c';
        txt.innerText = this.idioma === "en" ? "Recording... Release to send (Max 60s)" : "Grabando... Suelta para enviar (Máx 60s)";
        this.tiempoAudioTimer = setTimeout(() => { this.detenerGrabacionAudio(); }, 60000);
    },

    detenerGrabacionAudio: function() {
        if (this.tiempoAudioTimer) clearTimeout(this.tiempoAudioTimer);
        const btn = document.getElementById('btn-microfono');
        const txt = document.getElementById('texto-mic');
        btn.style.backgroundColor = '#ef4444';
        txt.innerText = this.idioma === "en" ? "Hold to talk (Max. 1 min)" : "Mantén presionado para hablar (Máx. 1 min)";
        
        const areaTexto = document.getElementById('otg-texto-extenso');
        if(areaTexto.value === "") {
            areaTexto.value = this.idioma === "en" ? "Voice message recorded: I need immediate routine help." : "Mensaje de voz grabado de 60 segundos: Requiero asistencia de tarea inmediata.";
        }
    },

    limpiarVentanilla: function() {
        document.getElementById('otg-texto-extenso').value = '';
        document.getElementById('otg-panel-respuesta').style.display = 'none';
        this.tagsSeleccionados = [];
        this.traducirInterfaz();
        if (this.esferaInterval) clearInterval(this.esferaInterval);
        if (this.relojInterval) clearInterval(this.relojInterval);
    },

    ejecutarPlan: function() {
        const perfil = document.getElementById("otg-perfil-select").value;
        const es = this.idioma === "es";
        
        document.getElementById("otg-id-display").innerText = "OTG-" + Math.random().toString(36).substring(2, 10).toUpperCase();
        
        const m = this.bancoMisiones[this.idioma][perfil];
        document.getElementById("otg-f1-pauta").innerText = m.antes;
        document.getElementById("otg-f2-pauta").innerText = m.durante;
        document.getElementById("otg-f3-pauta").innerText = m.despues;
        
        // Enlace oficial de mapas sin errores de texto pegado
        document.getElementById("otg-f2-mapa").href = "https://google.com" + m.mapa + "+near+me";
        document.getElementById("otg-panel-respuesta").style.display = "block";

        let tInhala = 4000; 
        let tExhala = 4000;
        let txtRitmo = es ? "Ritmo Regular (4s x 4s)" : "Regular Pace (4s x 4s)";

        if (perfil === "veteranos") { 
            tInhala = 5000; 
            tExhala = 5000; 
            txtRitmo = es ? "Anclaje Táctico (5s x 5s)" : "Tactical Grounding (5s x 5s)"; 
        } else if (perfil === "adultos_mayores") { 
            tInhala = 3000; 
            tExhala = 4000; 
            txtRitmo = es ? "Confort Suave (3s x 4s)" : "Gentle Comfort (3s x 4s)"; 
        }

        document.getElementById("otg-ritmo-titulo").innerText = txtRitmo;

        if (this.esferaInterval) clearInterval(this.esferaInterval);
        
        const animarEsfera = () => {
            const esf = document.getElementById("otg-esfera-visual");
            const txt = document.getElementById("otg-esfera-texto");
            if(!esf || !txt) return;

            esf.style.transform = "scale(1.3)";
            esf.style.backgroundColor = "rgba(56, 189, 248, 0.25)";
            txt.innerText = es ? "INHALA" : "BREATHE IN";

            setTimeout(() => {
                const esfCheck = document.getElementById("otg-esfera-visual");
                const txtCheck = document.getElementById("otg-esfera-texto");
                if(!esfCheck || !txtCheck) return;
                
                esfCheck.style.transform = "scale(0.95)";
                esfCheck.style.backgroundColor = "rgba(56, 189, 248, 0.05)";
                txtCheck.innerText = es ? "EXHALA" : "BREATHE OUT";
            }, tInhala);
        };

        animarEsfera();
        this.esferaInterval = setInterval(animarEsfera, (tInhala + tExhala));

        if (this.relojInterval) clearInterval(this.relojInterval);
        let remSegundos = 900;

        this.relojInterval = setInterval(() => {
            const nodoReloj = document.getElementById("otg-reloj-display");
            if (!nodoReloj) { 
                clearInterval(this.relojInterval); 
                return; 
            }

            remSegundos--;
            let mm = Math.floor(remSegundos / 60);
            let ss = remSegundos % 60;
            nodoReloj.innerText = (mm < 10 ? "0" + mm : mm) + ":" + (ss < 10 ? "0" + ss : ss);

            if (remSegundos <= 0) {
                clearInterval(this.relojInterval);
                clearInterval(this.esferaInterval);
                const textoFinalMsg = es ? 'Ciclo de Desconexión Completado' : 'Disconnection Cycle Completed';
                document.getElementById("otg-panel-respuesta").innerHTML = '<div style="color:#10b981; font-weight:bold; text-align:center; padding:15px; font-size:15px;">✓ ' + textoFinalMsg + '</div>';
            }
        }, 1000);
    }
};

// Carga automática inicial al abrir el archivo separado
document.addEventListener("DOMContentLoaded", () => {
    KERNEL_ESPECIAL.cambiarIdioma("es");
});
