window.KERNEL_ESPECIAL = {
    idioma: "es",
    tagsSeleccionados: [],
    esferaInterval: null,
    relojInterval: null,
    tiempoAudioTimer: null,
    modoTiempoLibre: false,

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

    ejecutarPlan: async function() {
        const perfil = document.getElementById("otg-perfil-select").value;
        const es = this.idioma === "es";
        this.modoTiempoLibre = false;
        
        let textoEscrito = document.getElementById('otg-texto-extenso').value.trim();
        if (!textoEscrito) {
            textoEscrito = es ? "Asistencia rutinaria general." : "General routine assistance.";
        }

        const API_URL = window.location.origin + "/api/v1/perfiles-especiales/procesar";
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                // Enlace corregido enviando el parámetro exacto que main.py espera leer
                body: JSON.stringify({ categoria: perfil, lang: this.idioma, parametro: textoEscrito })
            });
            const rep = await response.json();

            document.getElementById("otg-id-display").innerText = rep.id_caso;
            document.getElementById("otg-f1-pauta").innerText = rep.antes;
            document.getElementById("otg-f2-pauta").innerText = rep.durante;
            document.getElementById("otg-f3-pauta").innerText = rep.despues;
            
            document.getElementById("otg-f2-mapa").href = rep.mapa_url;
            document.getElementById("otg-f2-youtube").href = rep.youtube_url;
            document.getElementById("otg-f2-spotify").href = rep.spotify_url;

            document.getElementById("otg-f2-cuerpo").style.display = "none";
            document.getElementById("otg-f3-cuerpo").style.display = "none";
            document.getElementById("otg-panel-respuesta").style.display = "block";

            this.reproducirVozHumana(rep.antes + ". " + rep.durante);

            let tInhala = perfil === "veteranos" ? 5000 : (perfil === "adultos_mayores" ? 3000 : 4000);
            let tExhala = perfil === "veteranos" ? 5000 : 4000;
            document.getElementById("otg-ritmo-titulo").innerText = es ? `Ritmo Calibrado (${tInhala}s x ${tExhala}s)` : `Calibrated Pace (${tInhala}s x ${tExhala}s)`;

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

        } catch (e) {
            alert(es ? "Fallo de conexión." : "Connection error.");
        }
    }
};

document.addEventListener("DOMContentLoaded", () => { window.KERNEL_ESPECIAL.cambiarIdioma("es"); });
