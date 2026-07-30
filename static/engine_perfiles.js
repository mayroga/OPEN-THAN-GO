// ==========================================================================================
// FILE: static/engine_perfiles.js - BLOQUE 1 DE 3: VARIABLES Y CONTROL DE BOTONES TÁCTILES
// ==========================================================================================
window.KERNEL_ESPECIAL = {
    idioma: "es",
    perfilSeleccionado: "veteranos",
    modoSeleccionado: "salir",
    menteSeleccionada: "aburrido",
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
        if (window.speechSynthesis) window.speechSynthesis.cancel(); // Silenciar Spanglish de golpe
        this.traducirInterfaz();
    },

    alternarCortina: function(idCortina) {
        const elemento = document.getElementById(idCortina);
        if (elemento) {
            const estaAbierto = elemento.style.display === "block";
            elemento.style.display = estaAbierto ? "none" : "block";
        }
    },

    // CONTROL TÁCTIL: Enciende el perfil seleccionado y apaga los otros dos
    seleccionarPerfil: function(perfilId) {
        this.perfilSeleccionado = perfilId;
        const IDs = ["veteranos", "adultos_mayores", "gobierno"];
        IDs.forEach(id => {
            const nodo = document.getElementById("perfil-" + id);
            if (nodo) nodo.classList.remove("seleccionado");
        });
        document.getElementById("perfil-" + perfilId).classList.add("seleccionado");
    },

    // CONTROL TÁCTIL: Alterna entre entorno SALIR o CASA
    seleccionarModo: function(modoId) {
        this.modoSeleccionado = modoId;
        document.getElementById("modo-salir").classList.remove("seleccionado");
        document.getElementById("modo-casa").classList.remove("seleccionado");
        document.getElementById("modo-" + modoId).classList.add("seleccionado");
    },

    // CONTROL TÁCTIL: Enciende el estado de agobio de un toque y apaga el resto
    seleccionarMente: function(menteId) {
        this.menteSeleccionada = menteId;
        const mentes = ["aburrido", "agotado", "estresado", "cansado", "ansioso"];
        mentes.forEach(id => {
            const nodo = document.getElementById("mente-" + id);
            if (nodo) nodo.classList.remove("seleccionado");
        });
        document.getElementById("mente-" + menteId).classList.add("seleccionado");
    },
    // ==========================================================================================
    // FILE: static/engine_perfiles.js - BLOQUE 2 DE 3: TRADUCCIÓN NATIVA Y MICROFONO
    // ==========================================================================================
    traducirInterfaz: function() {
        const es = this.idioma === "es";
        
        // Traducción de Títulos Principales y Secciones Estilo Open Than Go
        document.getElementById("otg-txt-titulo-modulo").innerText = es ? "OPEN THAN GO" : "OPEN THAN GO";
        document.getElementById("otg-txt-subtitulo-modulo").innerText = es ? "Módulo Premium: Perfiles Especiales" : "Premium Module: Special Profiles";
        document.getElementById("otg-lbl-perfil").innerText = es ? "Perfil de Contención Especial" : "Special Containment Profile";
        document.getElementById("otg-lbl-modo").innerText = es ? "Modo Operativo de Entorno" : "Environment Operational Mode";
        document.getElementById("otg-lbl-mente").innerText = es ? "Mente / Diagnóstico de Agobio Existencial" : "Mind / Existential Overwhelm Diagnosis";
        document.getElementById("otg-lbl-texto").innerText = es ? "O escribe aquí tu propio agobio si no aparece arriba:" : "Or write your own overwhelm here if it does not appear above:";
        document.getElementById("otg-texto-extenso").placeholder = es ? "Copia correos extensos o escribe lo que sature tu mente hoy..." : "Copy long emails or write what saturates your mind today...";
        
        // Botones de Mente Individuales
        document.getElementById("mente-aburrido").innerText = es ? "Aburrido" : "Bored";
        document.getElementById("mente-agotado").innerText = es ? "Agotado" : "Exhausted";
        document.getElementById("mente-estresado").innerText = es ? "Estresado" : "Stressed";
        document.getElementById("mente-cansado").innerText = es ? "Cansado" : "Tired";
        document.getElementById("mente-ansioso").innerText = es ? "Ansioso" : "Anxious";
        
        // Nombres de Perfiles en Botones Táctiles
        document.getElementById("perfil-veteranos").innerText = es ? "Veteranos" : "Veterans";
        document.getElementById("perfil-adultos_mayores").innerText = es ? "Mayor" : "Senior";
        document.getElementById("perfil-gobierno").innerText = es ? "Gobierno" : "Government";

        // Botones de Acción de Fondo
        document.getElementById("otg-btn-activar").innerText = es ? "Activar Mando Especial" : "Activate Special Command";
        document.getElementById("otg-btn-borrar").innerText = es ? "Borrar Todo" : "Clear All";
        
        // Elementos Dinámicos de las Cortinas Plegables Inmersivas
        document.getElementById("otg-txt-reloj-lbl").innerText = es ? "⏱️ Desconexión Somática:" : "⏱️ Somatic Disconnection:";
        document.getElementById("otg-lbl-f1").innerText = es ? "Fase 1: Preparación Analógica" : "Phase 1: Analog Preparation";
        document.getElementById("otg-lbl-f2").innerText = es ? "Fase 2: Misión Somática en Curso" : "Phase 2: Active Somatic Mission";
        document.getElementById("otg-lbl-f3").innerText = es ? "Fase 3: Cierre de Vector Soberano" : "Phase 3: Sovereign Vector Close";
        document.getElementById("otg-reporte-titulo").innerText = es ? "Síntesis de Equilibrio Somático" : "Somatic Balance Synthesis";

        // Forzar el encendido visual de los botones configurados por defecto
        this.seleccionarPerfil(this.perfilSeleccionado);
        this.seleccionarModo(this.modoSeleccionado);
        this.seleccionarMente(this.menteSeleccionada);
    },

    iniciarGrabacionAudio: function() {
        const btn = document.getElementById('btn-microfono');
        const txt = document.getElementById('texto-mic');
        if (btn && txt) {
            btn.style.backgroundColor = '#b91c1c';
            txt.innerText = this.idioma === "en" ? "Recording... Release to process" : "Grabando... Suelta para procesar";
        }
        this.tiempoAudioTimer = setTimeout(() => { this.detenerGrabacionAudio(); }, 60000);
    },

    detenerGrabacionAudio: function() {
        if (this.tiempoAudioTimer) clearTimeout(this.tiempoAudioTimer);
        const btn = document.getElementById('btn-microfono');
        const txt = document.getElementById('texto-mic');
        if (btn && txt) {
            btn.style.backgroundColor = 'var(--accent-red)';
            txt.innerText = this.idioma === "en" ? "Hold to talk" : "Mantén presionado para hablar";
        }
        const areaTexto = document.getElementById('otg-texto-extenso');
        if (areaTexto && areaTexto.value === "") {
            areaTexto.value = this.idioma === "en" ? "Voice entry registered." : "Entrada de desahogo procesada de forma analógica.";
        }
    },

    limpiarVentanilla: function() {
        document.getElementById('otg-texto-extenso').value = '';
        document.getElementById('otg-panel-respuesta').style.display = 'none';
        document.getElementById('otg-bloque-configuracion').style.display = 'block';
        document.getElementById('otg-contenedor-master').classList.remove('compacto');
        document.body.classList.remove('modo-servicio');
        
        this.perfilSeleccionado = "veteranos";
        this.modoSeleccionado = "salir";
        this.menteSeleccionada = "aburrido";
        
        this.traducirInterfaz();
        
        if (this.esferaInterval) clearInterval(this.esferaInterval);
        if (this.relojInterval) clearInterval(this.relojInterval);
        if (this.bucleIntervalVoz) clearInterval(this.bucleIntervalVoz);
        if (window.speechSynthesis) window.speechSynthesis.cancel();
    },
    // ==========================================================================================
    // FILE: static/engine_perfiles.js - BLOQUE 3 DE 3: PROCESAMIENTO DINÁMICO PRIME
    // ==========================================================================================
    emitirVozHumana: function(textoALeer) {
        if (!textoALeer || !window.speechSynthesis) return;
        
        window.speechSynthesis.cancel(); // Detener de golpe cualquier residuo acústico anterior
        
        const enunciado = new SpeechSynthesisUtterance(textoALeer);
        enunciado.lang = this.idioma === "en" ? "en-US" : "es-ES";
        
        // CALIBRACIÓN CORPORATIVA PRIME: Voz fuerte, firme, pausada y antiestrés (cero prisa robot)
        enunciado.rate = 0.82; 
        enunciado.pitch = 0.95; 
        
        // Imprimir de inmediato en la pantalla limpia las letras de la instrucción en curso
        document.getElementById("otg-subtitulado-voz").innerText = textoALeer;
        
        window.speechSynthesis.speak(enuncique);
    },

    ejecutarPlan: function() {
        const es = this.idioma === "es";
        const entradaManual = document.getElementById("otg-texto-extenso").value.trim();
        const factorAgobio = entradaManual !== "" ? entradaManual : this.menteSeleccionada;
        
        // Captura del cargamento multi-vectorial para el servidor
        const payloadMaster = {
            categoria: this.perfilSeleccionado,
            entorno: this.modoSeleccionado,
            lang: this.idioma,
            tag_agobio: factorAgobio
        };

        fetch("/api/v1/perfiles-especiales/procesar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payloadMaster)
        })
        .then(res => res.json())
        .then(datos => {
            if (datos.status !== "success") return;
            
            // LIMPIEZA RADICAL DE INTERFAZ PRIME: Ocultar dashboard, aclarar fondo, compactar panel
            document.body.classList.add('modo-servicio');
            document.getElementById('otg-bloque-configuracion').style.display = 'none';
            document.getElementById('otg-contenedor-master').classList.add('compacto');
            
            // Asignación de identificador único de caso generado por entropía
            document.getElementById("otg-id-display").innerText = datos.id_caso;
            
            // Cargar cortinas (Repliegan todo el contenido para evitar el agobio visual de golpe)
            document.getElementById("cortina-f1").innerText = datos.antes;
            document.getElementById("otg-html-mision-texto").innerText = datos.durante;
            document.getElementById("cortina-f3").innerText = datos.despues;
            
            // Direccionamiento absoluto y directo a recursos de APIs externas Big Tech
            document.getElementById("otg-f2-mapa").href = datos.mapa_url;
            document.getElementById("otg-f2-youtube").href = datos.youtube_url;
            document.getElementById("otg-f2-spotify").href = datos.spotify_url;
            
            document.getElementById("otg-panel-respuesta").style.display = "block";
            document.getElementById("otg-bloque-reporte-acordeon").style.display = "none";
            
            // Primer impacto acústico inmersivo: Freno de tensión inicial
            this.emitirVozHumana(datos.antes_voz);
            
            this.bucleAudiosCortos = datos.bucle_audios_cortos || [];
            this.indiceAudioActual = 0;
            
            // Configurar el gran pulmón responsivo real (30% más grande) según perfil
            let tInhala = 4000, tExhala = 4000;
            let txtRitmo = es ? "Ritmo Regular (4s x 4s)" : "Regular Pace (4s x 4s)";
            
            if (this.perfilSeleccionado === "veteranos") { 
                tInhala = 5000; tExhala = 5000; 
                txtRitmo = es ? "Anclaje Táctico (5s x 5s)" : "Tactical Grounding (5s x 5s)"; 
            } else if (this.perfilSeleccionado === "adultos_mayores") { 
                tInhala = 3000; tExhala = 4000; 
                txtRitmo = es ? "Confort Suave (3s x 4s)" : "Gentle Comfort (3s x 4s)"; 
            }
            
            document.getElementById("otg-ritmo-titulo").innerText = txtRitmo;
            
            if (this.esferaInterval) clearInterval(this.esferaInterval);
            const animarEsfera = () => {
                const esf = document.getElementById("otg-esfera-visual");
                if (!esf) return;
                esf.style.transform = "scale(1.25)";
                esf.style.borderColor = "#10b981";
                document.getElementById("otg-esfera-texto").innerText = es ? "INHALA" : "BREATHE IN";
                
                setTimeout(() => {
                    const esfCheck = document.getElementById("otg-esfera-visual");
                    if (!esfCheck) return;
                    esfCheck.style.transform = "scale(0.9)";
                    esfCheck.style.borderColor = "var(--secondary)";
                    document.getElementById("otg-esfera-texto").innerText = es ? "EXHALA" : "BREATHE OUT";
                }, tInhala);
            };
            animarEsfera();
            this.esferaInterval = setInterval(animarEsfera, (tInhala + tExhala));
            
            // Activar cronómetro maestro y el hacedor de variedad cada 20 segundos
            this.iniciarCicloVidaSomatica(datos.durante_voz, datos.despues_voz, datos.reporte_anonimo, datos.reporte_nota);
        });
    },

    iniciarCicloVidaSomatica: function(duranteVoz, despuesVoz, reporteCuerpo, reporteNota) {
        if (this.relojInterval) clearInterval(this.relojInterval);
        if (this.bucleIntervalVoz) clearInterval(this.bucleIntervalVoz);
        
        const es = this.idioma === "es";
        let remSegundos = 900; // 15 minutos exactos de sesión
        
        // Pauta intermedia inyectada al segundo 35
        setTimeout(() => {
            if (document.getElementById("otg-panel-respuesta").style.display === "block") {
                this.emitirVozHumana(duranteVoz);
            }
        }, 35000);

        // GUIADO SEGURO DINÁMICO CADA 20 SEGUNDOS EXACTOS (Cero monotonía, cero robots)
        this.bucleIntervalVoz = setInterval(() => {
            if (remSegundos <= 15) return;
            if (this.bucleAudiosCortos && this.bucleAudiosCortos.length > 0) {
                const fraseActual = this.bucleAudiosCortos[this.indiceAudioActual];
                this.emitirVozHumana(fraseActual);
                this.indiceAudioActual = (this.indiceAudioActual + 1) % this.bucleAudiosCortos.length;
            }
        }, 20000);

        // Cronómetro maestro en tiempo real
        this.relojInterval = setInterval(() => {
            remSegundos--;
            let mm = Math.floor(remSegundos / 60);
            let ss = remSegundos % 60;
            document.getElementById("otg-reloj-display").innerText = (mm < 10 ? "0" + mm : mm) + ":" + (ss < 10 ? "0" + ss : ss);
            
            // Al segundo 10, romper acompañamientos periódicos y dictar reto lógico final en voz alta
            if (remSegundos === 10) {
                clearInterval(this.bucleIntervalVoz);
                const retoLector = document.getElementById("otg-html-mision-texto").innerText;
                this.emitirVozHumana(es ? "Atención se activa el reto de desfragmentación mental final " + retoLector : "Attention final de-escalation mind challenge activated " + retoLector);
            }
            
            // CONCLUSIÓN DEL SERVICIO COMPLETO (Cero resultados antes de finalizar)
            if (remSegundos <= 0) {
                clearInterval(this.relojInterval);
                clearInterval(this.esferaInterval);
                clearInterval(this.bucleIntervalVoz);
                
                document.getElementById("otg-esfera-visual").style.transform = "scale(1.0)";
                document.getElementById("otg-esfera-texto").innerText = es ? "CONCLUIDO" : "DONE";
                
                // Emisión acústica de cierre soberano largo de 60 segundos
                this.emitirVozHumana(despuesVoz);
                
                // REVELAR RESULTADOS PSICOMÉTRICOS CALCULADOS INVISIBLEMENTE POR LA TÉCNICA (OCULTOS BAJO CORTINA)
                document.getElementById("otg-reporte-cuerpo").innerText = reporteCuerpo;
                document.getElementById("otg-reporte-nota").innerText = reporteNota;
                document.getElementById("otg-bloque-reporte-acordeon").style.display = "block";
            }
        }, 1000);
    }
};

// Inicialización automática del entorno
document.addEventListener("DOMContentLoaded", () => {
    window.KERNEL_ESPECIAL.cambiarIdioma("es");
});
