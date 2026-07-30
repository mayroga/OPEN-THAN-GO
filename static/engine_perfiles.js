// ==========================================================================================
// FILE: static/engine_perfiles.js - BLOQUE 1 DE 4: INICIALIZACIÓN Y IDIOMA
// ==========================================================================================
window.KERNEL_ESPECIAL = {
    idioma: "es",
    tagsSeleccionados: [],
    esferaInterval: null,
    relojInterval: null,
    bucleIntervalVoz: null,
    tiempoAudioTimer: null,
    bucleAudiosCortos: [],
    indiceAudioActual: 0,

    cambiarIdioma: function(lang) {
        this.idioma = lang;
        const btnEs = document.getElementById("otg-btn-lang-es");
        const btnEn = document.getElementById("otg-btn-lang-en");
        if (btnEs && btnEn) {
            btnEs.style.background = lang === "es" ? "#38bdf8" : "#1e293b";
            btnEs.style.color = lang === "es" ? "#0f172a" : "#94a3b8";
            btnEn.style.background = lang === "en" ? "#38bdf8" : "#1e293b";
            btnEn.style.color = lang === "en" ? "#0f172a" : "#94a3b8";
        }
        this.traducirInterfaz();
    },
    // ==========================================================================================
    // FILE: static/engine_perfiles.js - BLOQUE 2 DE 4: TRADUCCIÓN DE INTERFAZ
    // ==========================================================================================
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
        document.getElementById("otg-txt-reloj-lbl").innerText = es ? "⏱️ Tiempo de desconexión obligatoria:" : "⏱️ Required disconnection time remaining:";
        document.getElementById("otg-lbl-f1").innerText = es ? "Fase 1: Antes del Uso (Freno de Tensión)" : "Phase 1: Before Use (Tension Brake)";
        document.getElementById("otg-lbl-f2").innerText = es ? "Fase 2: Durante la Actividad (Misión Práctica)" : "Phase 2: During Activity (Practical Mission)";
        document.getElementById("otg-lbl-f3").innerText = es ? "Fase 3: Al Finalizar (Cierre y Descanso)" : "Phase 3: Cycle Close (Guaranteed Rest)";
        document.getElementById("otg-f2-mapa").innerText = es ? "Abrir Ruta de Entorno Seguro en Google Maps" : "Open Safe Route on Google Maps";
        document.getElementById("otg-reporte-titulo").innerText = es ? "Síntesis de Equilibrio Rutinario" : "Routine Balance Synthesis";
        document.getElementById("otg-reporte-nota").innerText = es ? "*Este reporte no es obligatorio ni oficial; constituye una guía práctica de bienestar habitual." : "*This report is neither mandatory nor official; it constitutes a practical guide for habitual well-being.";

        const contenedor = document.getElementById("otg-contenedor-tags-html");
        if (contenedor) {
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
                    if (span.classList.contains("seleccionado")) { 
                        this.tagsSeleccionados.push(item.id); 
                    } else { 
                        this.tagsSeleccionados = this.tagsSeleccionados.filter(x => x !== item.id); 
                    }
                };
                contenedor.appendChild(span);
            });
        }
    },
    // ==========================================================================================
    // FILE: static/engine_perfiles.js - BLOQUE 3 DE 4: COMPONENTES TÁCTILES Y FETCH
    // ==========================================================================================
    iniciarGrabacionAudio: function() {
        const btn = document.getElementById('btn-microfono');
        const txt = document.getElementById('texto-mic');
        if (btn && txt) {
            btn.style.backgroundColor = '#b91c1c';
            txt.innerText = this.idioma === "en" ? "Recording... Release to send (Max 60s)" : "Grabando... Suelta para enviar (Máx 60s)";
        }
        this.tiempoAudioTimer = setTimeout(() => { this.detenerGrabacionAudio(); }, 60000);
    },

    detenerGrabacionAudio: function() {
        if (this.tiempoAudioTimer) clearTimeout(this.tiempoAudioTimer);
        const btn = document.getElementById('btn-microfono');
        const txt = document.getElementById('texto-mic');
        if (btn && txt) {
            btn.style.backgroundColor = '#ef4444';
            txt.innerText = this.idioma === "en" ? "Hold to talk (Max. 1 min)" : "Mantén presionado para hablar (Máx. 1 min)";
        }
        const areaTexto = document.getElementById('otg-texto-extenso');
        if (areaTexto && areaTexto.value === "") {
            areaTexto.value = this.idioma === "en" ? "Voice message recorded: I need immediate routine help." : "Mensaje de voz grabado de 60 segundos: Requiero asistencia de tarea inmediata.";
        }
    },

    limpiarVentanilla: function() {
        const areaTexto = document.getElementById('otg-texto-extenso');
        const panelRespuesta = document.getElementById('otg-panel-respuesta');
        const contenedorReporte = document.getElementById('otg-contenedor-reporte');
        
        if (areaTexto) areaTexto.value = '';
        if (panelRespuesta) panelRespuesta.style.display = 'none';
        if (contenedorReporte) contenedorReporte.style.display = 'none';
        
        this.tagsSeleccionados = [];
        this.traducirInterfaz();
        
        if (this.esferaInterval) clearInterval(this.esferaInterval);
        if (this.relojInterval) clearInterval(this.relojInterval);
        if (this.bucleIntervalVoz) clearInterval(this.bucleIntervalVoz);
    },

    emitirVozHumana: function(textoALeer) {
        if (!textoALeer) return;
        if (window.speechSynthesis) {
            window.speechSynthesis.cancel();
        }
        const enunciado = new SpeechSynthesisUtterance(textoALeer);
        enunciado.lang = this.idioma === "en" ? "en-US" : "es-ES";
        enunciado.rate = 0.95; 
        enunciado.pitch = 1.0;
        window.speechSynthesis.speak(enunciado);
    },

    ejecutarPlan: function() {
        const perfilSeleccionado = document.getElementById("otg-perfil-select").value;
        const es = this.idioma === "es";
        
        const payloadMaster = {
            categoria: perfilSeleccionado,
            lang: this.idioma
        };

        fetch("/api/v1/perfiles-especiales/procesar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payloadMaster)
        })
        .then(res => {
            if (!res.ok) throw new Error("Fallo de respuesta del servidor");
            return res.json();
        })
        .then(datos => {
            if (datos.status !== "success") return;
            
            document.getElementById("otg-id-display").innerText = datos.id_caso;
            document.getElementById("otg-f1-pauta").innerText = datos.antes;
            document.getElementById("otg-f2-pauta").innerText = datos.durante;
            document.getElementById("otg-f3-pauta").innerText = datos.despues;
            document.getElementById("otg-f2-mapa").href = datos.mapa_url;
            
            document.getElementById("otg-panel-respuesta").style.display = "block";
            document.getElementById("otg-contenedor-reporte").style.display = "none";
            
            this.emitirVozHumana(datos.antes_voz);
            
            this.bucleAudiosCortos = datos.bucle_audios_cortos || [];
            this.indiceAudioActual = 0;
            
            let tInhala = 4000;
            let tExhala = 4000;
            let txtRitmo = es ? "Ritmo Regular (4s x 4s)" : "Regular Pace (4s x 4s)";
            
            if (perfilSeleccionado === "veteranos") {
                tInhala = 5000;
                tExhala = 5000;
                txtRitmo = es ? "Anclaje Táctico (5s x 5s)" : "Tactical Grounding (5s x 5s)";
            } else if (perfilSeleccionado === "adultos_mayores") {
                tInhala = 3000;
                tExhala = 4000;
                txtRitmo = es ? "Confort Suave (3s x 4s)" : "Gentle Comfort (3s x 4s)";
            }
            
            document.getElementById("otg-ritmo-titulo").innerText = txtRitmo;
            
            if (this.esferaInterval) clearInterval(this.esferaInterval);
            
            const animarEsfera = () => {
                const esf = document.getElementById("otg-esfera-visual");
                const txt = document.getElementById("otg-esfera-texto");
                if (!esf || !txt) return;
                
                esf.style.transform = "scale(1.3)";
                esf.style.backgroundColor = "rgba(56, 189, 248, 0.25)";
                txt.innerText = es ? "INHALA" : "BREATHE IN";
                
                setTimeout(() => {
                    const esfCheck = document.getElementById("otg-esfera-visual");
                    const txtCheck = document.getElementById("otg-esfera-texto");
                    if (!esfCheck || !txtCheck) return;
                    
                    esfCheck.style.transform = "scale(0.95)";
                    esfCheck.style.backgroundColor = "rgba(56, 189, 248, 0.05)";
                    txtCheck.innerText = es ? "EXHALA" : "BREATHE OUT";
                }, tInhala);
            };
            
            animarEsfera();
            this.esferaInterval = setInterval(animarEsfera, (tInhala + tExhala));
            
            this.iniciarCicloVidaSomatica(perfilSeleccionado, datos.durante_voz, datos.despues_voz);
        })
        .catch(err => {
            console.error("Error en el canal de red: ", err);
        });
    },
    // ==========================================================================================
    // FILE: static/engine_perfiles.js - BLOQUE 4 DE 4: TEMPORIZADOR DE AUDIO Y ARRANQUE
    // ==========================================================================================
    iniciarCicloVidaSomatica: function(perfil, duranteVoz, despuesVoz) {
        if (this.relojInterval) clearInterval(this.relojInterval);
        if (this.bucleIntervalVoz) clearInterval(this.bucleIntervalVoz);
        
        const es = this.idioma === "es";
        let remSegundos = 900; 
        
        // Disparador a los 35 segundos para la pauta central
        setTimeout(() => {
            const panel = document.getElementById("otg-panel-respuesta");
            if (panel && panel.style.display === "block") {
                this.emitirVozHumana(duranteVoz);
            }
        }, 35000);

        // Bucle periódico de voz conversacional de acompañamiento cada 15 segundos
        this.bucleIntervalVoz = setInterval(() => {
            const panel = document.getElementById("otg-panel-respuesta");
            if (!panel || panel.style.display !== "block" || remSegundos <= 10) return;

            if (this.bucleAudiosCortos && this.bucleAudiosCortos.length > 0) {
                const fraseActual = this.bucleAudiosCortos[this.indiceAudioActual];
                this.emitirVozHumana(fraseActual);
                this.indiceAudioActual = (this.indiceAudioActual + 1) % this.bucleAudiosCortos.length;
            }
        }, 15000);

        // Cronómetro maestro en tiempo real
        this.relojInterval = setInterval(() => {
            const nodoReloj = document.getElementById("otg-reloj-display");
            if (!nodoReloj) {
                clearInterval(this.relojInterval);
                if (this.bucleIntervalVoz) clearInterval(this.bucleIntervalVoz);
                return;
            }
            
            remSegundos--;
            let mm = Math.floor(remSegundos / 60);
            let ss = remSegundos % 60;
            nodoReloj.innerText = (mm < 10 ? "0" + mm : mm) + ":" + (ss < 10 ? "0" + ss : ss);
            
            // Inyectar el Reto de Atención en el segundo 10
            if (remSegundos === 10) {
                if (this.bucleIntervalVoz) clearInterval(this.bucleIntervalVoz); 
                const textoDuranteConReto = document.getElementById("otg-f2-pauta").innerText;
                this.emitirVozHumana(es ? "Atención llega un reto especial de diez segundos " + textoDuranteConReto : "Attention special ten second challenge incoming " + textoDuranteConReto);
            }
            
            // Cierre definitivo con la frase larga de 60 segundos
            if (remSegundos <= 0) {
                clearInterval(this.relojInterval);
                clearInterval(this.esferaInterval);
                if (this.bucleIntervalVoz) clearInterval(this.bucleIntervalVoz);
                
                const textoFinalMsg = es ? 'Ciclo de Desconexión Completado' : 'Disconnection Cycle Completed';
                document.getElementById("otg-panel-respuesta").innerHTML = '<div style="color: #10b981; font-weight: bold; text-align: center; padding: 15px; font-size: 15px;">✓ ' + textoFinalMsg + '</div>';
                
                this.emitirVozHumana(despuesVoz);
                
                const contenedorReporte = document.getElementById("otg-contenedor-reporte");
                if (contenedorReporte) {
                    contenedorReporte.style.display = "block";
                    contenedorReporte.scrollIntoView({ behavior: 'smooth' });
                }
            }
        }, 1000);
    }
};

// Disparador de carga inicial limpia del documento
document.addEventListener("DOMContentLoaded", () => {
    window.KERNEL_ESPECIAL.cambiarIdioma("es");
});
