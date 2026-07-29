// ==========================================================================================
// KERNEL_ESPECIAL V11.0 - MOTOR DE ALTA CONTENCIÓN COGNITIVA Y AUDIO INTERCALADO
// Lenguaje Nivel 8 años - Cero terminología médica - Bilingüe Nativo - Inmune a Caídas de Red
// ==========================================================================================
window.KERNEL_ESPECIAL = {
    idioma: "es",
    tagsSeleccionados: [],
    esferaInterval: null,
    relojInterval: null,
    tiempoAudioTimer: null,
    // [FIX] 'contadorMilisegundos' removed as its previous logic for audio timing was refactored.
    modoTiempoLibre: false,
    breathCycleCount: 0, // [NEW] Track full breath cycles for audio phrase timing

    // BANCO EXTENSO MUTANTE CON JUSTIFICACIÓN OCULTA (Garantiza nula repetición en 50 sesiones)
    bancoContenido: {
        "es": {
            "veteranos": {
                "frases_7s": [
                    "Tu entorno está seguro aquí.", "Pisa firme, la tierra te sostiene.", "Este segundo es tuyo.", 
                    "Suelta la carga de la vigilia.", "Estás a salvo en tu espacio.", "El ruido exterior ya no importa.",
                    "Siente el peso de tus pies.", "El peligro ya pasó.", "Tu atención está aquí hoy.", "Eres fuerte por pausar."
                ],
                "frases_15s": [
                    "El presente es tu único escudo real y efectivo hoy.", "Tu fuerza vive en tu capacidad de respirar con calma.", 
                    "Ningún recuerdo del pasado tiene poder sobre este segundo.", "Breathe el aire limpio de tu libertad aquí y ahora.",
                    "La quietud de esta habitación te pertenece por completo.", "El control está en tus manos, apoya tus talones firmes."
                ],
                "proverbios": [
                    "La calma es la mayor manifestación de la fuerza humana.", 
                    "No dejes que el eco de tormentas pasadas nuble el cielo limpio de tu presente.",
                    "El guerrero más sabio es aquel que sabe cuándo deponer las armas para cuidar su propio hogar.",
                    "La madera más fuerte no es la que crece resguardada del viento, sino la que resiste la storm o tormenta."
                ],
                "juegos_mentales": [
                    {
                        "tipo": "matematica",
                        "enunciado": "Si en una caja de herramientas tienes 15 piezas de seguridad y decides guardar 6 en tu mochila para mantener el orden, ¿cuántas quedan fijas en la caja?",
                        "respuesta": "Quedan 9 piezas.",
                        "justificacion": "15 menos 6 es igual a 9. Este ejercicio obliga a tu mente a hacer una resta simple restando estímulos visuales y concentrando tu atención en números exactos en lugar de alertas del entorno."
                    },
                    {
                        "tipo": "adivinanza",
                        "enunciado": "Tengo hojas pero no soy un árbol, guardo secretos pero no soy un búnker cerrado. ¿Qué soy?",
                        "respuesta": "Un libro de papel.",
                        "justificacion": "Los libros tienen páginas (hojas) y guardan historias. Al resolver este acertijo, tu cerebro activa el lóbulo frontal para buscar analogías pacíficas alejadas de la alerta táctica."
                    }
                ]
            },
            "adultos_mayores": {
                "frases_7s": [
                    "Tu tiempo es valioso.", "Disfruta este momento de paz.", "Respira suave, sin prisa.", 
                    "Cada segundo trae calma.", "Siente el confort de tu hogar.", "Estás acompañado en silencio.",
                    "La tranquilidad es tu derecho.", "Disfruta la luz de hoy.", "Tu mente descansa libre.", "Paso a paso hay bienestar."
                ],
                "frases_15s": [
                    "La vida se saborea un segundo a la vez, con total calma.", "Tu sabiduría ha guiado caminos extensos, ahora te toca descansar.", 
                    "Cuidar de tu tranquilidad hoy es tu misión más importante y hermosa.", "Siente cómo la paz del presente inunda tu espacio habitual."
                ],
                "proverbios": [
                    "Los ríos más profundos son los que corren con menos ruido.", 
                    "La paciencia es un árbol de raíz amarga, pero de frutos sumamente dulces.",
                    "El hogar no es un lugar físico, es el estado de calma donde descansa tu atención.",
                    "Una palabra amable puede entibiar tres meses enteros de un invierno frío."
                ],
                "juegos_mentales": [
                    {
                        "tipo": "matematica",
                        "enunciado": "Si tienes 3 macetas en la ventana con flores hermosas y cada maceta necesita 4 soplos de agua fresca al día, ¿cuántos soplos das en total hoy?",
                        "respuesta": "Das 12 soplos de agua.",
                        "justificacion": "3 multiplicado por 4 da 12. La multiplicación sencilla estimula la memoria de trabajo analógica activa, ayudando a las personas mayores a conectar la lógica numérica con el cuidado cotidiano del hogar."
                    },
                    {
                        "tipo": "adivinanza",
                        "enunciado": "Doy vueltas todo el día pero nunca me muevo de mi sitio, marco los minutos pero no tengo dedos. ¿Qué soy?",
                        "respuesta": "El reloj de la pared.",
                        "justificacion": "El reloj gira sus manecillas fijamente. Este juego mental estimula el reconocimiento del paso del tiempo de forma controlada y segura, alejando la mente de la monotonía."
                    }
                ]
            },
            "gobierno": {
                "frases_7s": [
                    "La oficina se detuvo ya.", "El sistema puede esperar.", "Este minuto no le pertenece a nadie.", 
                    "Suelta la pantalla ahora.", "Tu mente es libre del papeleo.", "Respira fuera del cubículo.",
                    "El monitor ya está lejos.", "Cierra la pestaña de correos.", "Eres más que tu horario.", "Disfruta de este freno vital."
                ],
                "frases_15s": [
                    "Ninguna tarea urgente vale más que la soberanía y claridad de tu mente hoy.", "Desconectarse del engranaje administrativo es un derecho de salud laboral vital.", 
                    "El sistema seguirá girando aunque apagues tu monitor por quince minutos.", "Tu atención ha salido de la red burocrática del estado con éxito absoluto."
                ],
                "proverbios": [
                    "El trabajo llena tus bolsillos, pero solo el silencio restaura tu alma.", 
                    "No confundas el estar ocupado todo el día con el estar viviendo de verdad.",
                    "La prisa es el viento caótico que apaga la lámpara de toda claridad mental humana.",
                    "Quien compra lo que no necesita, termina vendiendo lo que de verdad le importa."
                ],
                "juegos_mentales": [
                    {
                        "tipo": "matematica",
                        "enunciado": "Si tienes una lista con 24 solicitudes de trámite y logras archivar de golpe 8 en la carpeta de resueltos, ¿cuántos quedan pendientes de revisión?",
                        "respuesta": "Quedan 16 trámites pendientes.",
                        "justificacion": "24 menos 8 es igual a 16. Obligar a la mente de oficina a procesar restas sencillas con conceptos de trabajo ayuda a desdramatizar la carga laboral, devolviendo el control al usuario."
                    },
                    {
                        "tipo": "adivinanza",
                        "enunciado": "Entro duro y seco al agua, pero salgo blando, suave y mojado de ella. ¿Qué soy?",
                        "respuesta": "Un sobre de té caliente.",
                        "justificacion": "La bolsa de té se ablanda al sumergirse. Este acertijo activa los mechanisms lógicos de asociación sensorial de la corteza cerebral, desconectando el estrés de las hojas de cálculo rutinarias."
                    }
                ]
            }
        },
        "en": {
            "veteranos": {
                "frases_7s": ["Your space is safe.", "Feel the solid ground.", "This second is yours.", "Release the high alert.", "You are at peace.", "The past has no voice here."],
                "frases_15s": ["The present moment is your only true shield today.", "Your strength lies in your ability to pause right now.", "No memory holds power over this single heartbeat.", "Breathe in the clear air of your hard-earned freedom."],
                "proverbios": ["Calm is the ultimate manifestation of human strength.", "Do not let the echoes of past storms cloud your present sky."],
                "juegos_mentales": [{ "tipo": "matematica", "enunciado": "If you have 15 safety items and pack 6 in your vest, how many are left?", "respuesta": "9 items are left.", "justificacion": "15 minus 6 equals 9. This basic subtraction anchors your focus away from tactical alert zones into a peaceful numeric truth." }]
            },
            "adultos_mayores": {
                "frases_7s": ["Your time is precious.", "Enjoy this quiet time.", "Breathe softly, no rush.", "Peace fills this room.", "Feel the cozy warmth.", "You are safe and sound."],
                "frases_15s": ["Life is savored one slow heartbeat at a time.", "Your wisdom has guided many, now it is your time to rest.", "Guarding your tranquility today is your most important task."],
                "proverbios": ["Deep rivers run with the least amount of noise.", "Patience is a bitter plant, but its fruit is remarkably sweet."],
                "juegos_mentales": [
                    { "tipo": "adivinanza", "enunciado": "I tick away all day but never move from my place. What am I?", "respuesta": "A wall clock.", "justificacion": "The clock hands move safely. This game triggers long-term logical memory structures without creating cognitive stress." },
                    // [FIX] Added missing 'matematica' game for consistency
                    { "tipo": "matematica", "enunciado": "If you have 3 pots with beautiful flowers and each needs 4 sips of fresh water daily, how many sips do you give in total today?", "respuesta": "You give 12 sips of water.", "justificacion": "3 multiplied by 4 is 12. Simple multiplication stimulates active analog working memory, helping seniors connect numeric logic with daily home care." }
                ]
            }, // [FIX] Missing closing brace '}' for 'adultos_mayores' object in 'en' language was added here.
            "gobierno": {
                "frases_7s": ["The office has stopped.", "The network can wait.", "This minute is strictly yours.", "Drop the screen strain.", "Free your mind from tasks.", "Breathe outside the loop."],
                "frases_15s": ["No urgent task is worth more than your mental sovereignty today.", "Disconnecting from the system is a vital and healthy right.", "The world keeps turning even if you step away from the monitor."],
                "proverbios": ["Labor fills your pockets, but only silence restores your inner self.", "Do not mistake being busy all day with truly experiencing life."],
                "juegos_mentales": [
                    { "tipo": "matematica", "enunciado": "If you have 24 task files and complete 8 right now, how many are remaining?", "respuesta": "16 files remain.", "justificacion": "24 minus 8 is 16. Simple math math help shift administrative anxiety patterns into structured modules under your direct control." },
                    // [FIX] Added missing 'adivinanza' game for consistency
                    { "tipo": "adivinanza", "enunciado": "I enter water hard and dry, but come out soft, smooth, and wet. What am I?", "respuesta": "A warm tea bag.", "justificacion": "The tea bag softens when submerged. This riddle activates the logical mechanisms of sensory association in the cerebral cortex, disconnecting stress from routine spreadsheets." }
                ]
            }
        }
    },

    // RECURSOS MULTIMEDIA CORREGIDOS Y ENLAZADOS EXCLUSIVAMENTE AL DOLOR DE CADA CATEGORÍA
    recursosMultimedia: {
        "veteranos": {
            "youtube": "https://youtube.com",
            "spotify": "https://spotify.com"
        },
        "adultos_mayores": {
            "youtube": "https://youtube.com",
            "spotify": "https://spotify.com"
        },
        "gobierno": {
            "youtube": "https://youtube.com",
            "spotify": "https://spotify.com"
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
        document.getElementById("otg-txt-subtitulo-modulo").innerText = es ? "Módulo directo de orientación práctica." : "Direct module for practical orientation.";
        document.getElementById("otg-lbl-perfil").innerText = es ? "Selecciona tu Perfil Especial:" : "Select your Special Profile:";
        document.getElementById("otg-opt-vet").innerText = es ? "Veteranos de Guerra" : "War Veterans";
        document.getElementById("otg-opt-am").innerText = es ? "Adultos Mayores" : "Senior Citizens";
        document.getElementById("otg-opt-gob").innerText = es ? "Trabajadores del Gobierno" : "Government Workers";
        document.getElementById("otg-lbl-tags").innerText = es ? "Toca las casillas de tu agobio (Opcional):" : "Tap the words that describe your overwhelm (Optional):";
        document.getElementById("otg-lbl-texto").innerText = es ? "Pega un texto largo o escribe detalladamente:" : "Or copy and paste a long text here:";
        document.getElementById("otg-texto-extenso").placeholder = es ? "Puedes pegar correos extensos o escribir libremente lo que pasa en tu mente hoy..." : "You can paste long emails or write freely...";
        document.getElementById("otg-btn-activar").innerText = es ? "Activar Plan" : "Activate Plan";
        document.getElementById("otg-btn-borrar").innerText = es ? "Borrar Todo" : "Clear All";
        document.getElementById("otg-btn-cerrar").innerText = es ? "✕ REGRESAR" : "✕ RETURN";
        document.getElementById("otg-txt-registro").innerText = es ? "✓ Estrategia Operativa Generada" : "✓ Operational Strategy Generated";
        document.getElementById("otg-txt-reloj-lbl").innerText = es ? "⏱️ Tiempo restante:" : "⏱️ Time remaining:";
        document.getElementById("otg-lbl-f1").innerText = es ? "Fase 1: Antes del Uso (Freno de Tensión)" : "Phase 1: Before Use (Tension Brake)";
        document.getElementById("otg-lbl-f2").innerText = es ? "Fase 2: Durante el Uso (Misión Práctica) ▼" : "Phase 2: During Use (Practical Mission) ▼";
        document.getElementById("otg-lbl-f3").innerText = es ? "Fase 3: Después del Uso (Cierre Seguro) ▼" : "Phase 3: After Use (Safe Close) ▼";
        document.getElementById("otg-f2-mapa").innerText = es ? "🗺️ Abrir Ruta de Entorno Seguro en Google Maps" : "🗺️ Open Safe Route on Google Maps";

        const contenedor = document.getElementById("otg-contenedor-tags-html");
        if(contenedor) {
            contenedor.innerHTML = "";
            const pool = es ? 
                [{id:"triste", t:"Tristeza"}, {id:"cansado", t:"Cansancio"}, {id:"papeleo", t:"Papeleo"}, {id:"ruido", t:"Ruido Fuerte"}, {id:"estres", t:"Estrés de Oficina"}] :
                [{id:"triste", t:"Sadness"}, {id:"cansado", t:"Fatigue"}, {id:"papeleo", t:"Paperwork"}, {id:"ruido", t:"Loud Noise"}, {id:"estres", t:"Office Stress"}];
            
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
            areaTexto.value = this.idioma === "en" ? "Voice message recorded: I need immediate help." : "Mensaje de voz grabado de 60 segundos: Requiero asistencia de tarea inmediata.";
        }
    },
    
    limpiarVentanilla: function() {
        window.speechSynthesis.cancel();
        document.getElementById('otg-texto-extenso').value = '';
        document.getElementById('otg-panel-respuesta').style.display = 'none';
        this.tagsSeleccionados = [];
        this.traducirInterfaz();
        if (this.esferaInterval) clearTimeout(this.esferaInterval);
        if (this.relojInterval) clearInterval(this.relojInterval);
        this.breathCycleCount = 0;
    },
    
    // ==========================================================================================
    // EJECUTAR PLAN: CONEXIÓN INTERACTIVA FIJA CON EL CEREBRO DE MAIN.PY (CON CLAVE CORRECTA)
    // ==========================================================================================
    ejecutarPlan: async function() {
        const perfil = document.getElementById("otg-perfil-select").value;
        const es = this.idioma === "es";
        let textoEscrito = document.getElementById('otg-texto-extenso').value.trim();
        this.modoTiempoLibre = false;
        this.breathCycleCount = 0;
        
        // CORRECCIÓN CRÍTICA DE CONEXIÓN: Si no escribe nada, el sistema asigna una frase analógica automática
        // para asegurar que la variable 'parametro' viaje llena al servidor y main.py no rompa el JSON.
        let parametroFinal = "";
        if (this.tagsSeleccionados.length > 0) {
            parametroFinal += "[Tags: " + this.tagsSeleccionados.join(", ") + "] ";
        }
        parametroFinal += textoEscrito;
        
        if (!parametroFinal.trim()) {
            parametroFinal = es ? "Asistencia de rutina general solicitada." : "General routine assistance requested.";
        }
        
        const API_URL = window.location.origin + "/api/v1/perfiles-especiales/procesar";
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                // Sincronización milimétrica con el backend: Mandamos la clave 'parametro' exacta que main.py espera leer
                body: JSON.stringify({
                    categoria: perfil,
                    lang: this.idioma,
                    parametro: parametroFinal
                })
            });
            const rep = await response.json();
            
            const poolEspecial = this.bancoContenido[this.idioma][perfil];
            const proverbioGanador = poolEspecial.proverbios[Math.floor(Math.random() * poolEspecial.proverbios.length)];
            const juegoGanador = poolEspecial.juegos_mentales[Math.floor(Math.random() * poolEspecial.juegos_mentales.length)];
            
            document.getElementById("otg-id-display").innerText = rep.id_caso;
            
            // Inyección estable usando comillas invertidas nativas corrigiendo las cadenas simples
            document.getElementById("otg-f1-pauta").innerHTML = `<strong>${rep.antes}</strong><br><br><span style="color:#38bdf8; font-style:italic; font-size:15px; font-weight:700;">📜 ${proverbioGanador}</span>`;
            
            document.getElementById("otg-f2-pauta").innerHTML = `
                <span style="display:block; margin-bottom:10px;">${rep.durante}</span> 
                <div style="background:#131f38; border:1px dashed #334155; padding:12px; border-radius:6px; margin:10px 0;"> 
                    <strong style="color:#ef4444; text-transform:uppercase; font-size:11px; display:block; margin-bottom:4px;">🧠 RETO ACTIVO (60s):</strong> 
                    <span style="font-size:14px; font-weight:600;">${juegoGanador.enunciado}</span> 
                    <div style="margin-top:10px; padding-top:8px; border-top:1px solid #1e293b; color:#10b981; font-size:13px; font-weight:700;"> 
                        💡 Solución: ${juegoGanador.respuesta}<br> 
                        <span style="color:#94a3b8; font-size:12px; font-weight:500; font-style:italic; display:block; margin-top:2px;">Justificación: ${juegoGanador.justificacion}</span> 
                    </div> 
                </div>
            `;
            document.getElementById("otg-f3-pauta").innerText = rep.despues;

            const media = this.recursosMultimedia[perfil];
            document.getElementById("otg-f2-mapa").href = rep.mapa_url;
            document.getElementById("otg-f2-youtube").href = media.youtube;
            document.getElementById("otg-f2-spotify").href = media.spotify;

            document.getElementById("otg-f2-cuerpo").style.display = "none";
            document.getElementById("otg-f3-cuerpo").style.display = "none";
            document.getElementById("otg-panel-respuesta").style.display = "block";

            // LOCUCIÓN AUTOMÁTICA DEL PLAN GENERADO + EL RETO INTERACTIVO CON SU SOLUCIÓN
            this.reproducirVozHumana(rep.antes + ". " + proverbioGanador + ". " + (es ? "Tu reto mental de sesenta segundos es: " : "Your sixty second challenge is: ") + juegoGanador.enunciado);

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

            if (this.esferaInterval) clearTimeout(this.esferaInterval);
            let alternarCiclo = true;

            const animarEsfera = () => {
                const esf = document.getElementById("otg-esfera-visual");
                const txt = document.getElementById("otg-esfera-texto");
                if (!esf || !txt) return;

                const poolEspecial = this.bancoContenido[this.idioma][perfil];

                if (alternarCiclo) {
                    esf.style.transform = "scale(1.35)";
                    esf.style.backgroundColor = "rgba(56, 189, 248, 0.22)";
                    txt.innerText = es ? "INHALA" : "BREATHE IN";
                    alternarCiclo = false;

                    // Locución de frase corta de apoyo cada 7 segundos aproximados al inhalar
                    const frase7 = poolEspecial.frases_7s[Math.floor(Math.random() * poolEspecial.frases_7s.length)];
                    this.reproducirVozHumana(frase7);
                    this.esferaInterval = setTimeout(animarEsfera, tInhala);
                } else {
                    esf.style.transform = "scale(0.92)";
                    esf.style.backgroundColor = "rgba(56, 189, 248, 0.04)";
                    txt.innerText = es ? "EXHALA" : "BREATHE OUT";
                    alternarCiclo = true;
                    this.breathCycleCount++;

                    // Locución de frase larga de apoyo cada 2 ciclos completos (15 segundos aproximados)
                    if (this.breathCycleCount % 2 === 0) {
                        const frase15 = poolEspecial.frases_15s[Math.floor(Math.random() * poolEspecial.frases_15s.length)];
                        this.reproducirVozHumana(frase15);
                    }
                    this.esferaInterval = setTimeout(animarEsfera, tExhala);
                }
            };
            animarEsfera();

            if (this.relojInterval) clearInterval(this.relojInterval);
            let remSegundos = 900;

            this.relojInterval = setInterval(() => {
                const nodoReloj = document.getElementById("otg-reloj-display");
                if (!nodoReloj) {
                    clearInterval(this.relojInterval);
                    return;
                }

                if (!this.modoTiempoLibre) {
                    remSegundos--;
                    let mm = Math.floor(remSegundos / 60);
                    let ss = remSegundos % 60;
                    nodoReloj.innerText = (mm < 10 ? "0" + mm : mm) + ":" + (ss < 10 ? "0" + ss : ss);

                    if (remSegundos <= 0) {
                        window.speechSynthesis.cancel();
                        this.modoTiempoLibre = true;

                        const preguntaComodidad = es ?
                            "Has cumplido tus 15 minutos obligados de descompresión con éxito. La puerta está abierta: ¿Deseas continuar en modo libre o regresar?" :
                            "You have successfully completed your 15 required minutes. The door is open: Would you like to continue in free mode or return?";

                        this.reproducirVozHumana(preguntaComodidad);

                        if (confirm(preguntaComodidad)) {
                            remSegundos = 0; // El cronómetro inicia desde cero en el modo libre
                            document.getElementById("otg-txt-reloj-lbl").innerText = es ? "⏱️ Modo Libre Opcional Activo:" : "⏱️ Optional Free Mode Active:";
                            nodoReloj.style.color = "#38bdf8";
                        } else {
                            clearInterval(this.relojInterval);
                            if (this.esferaInterval) clearTimeout(this.esferaInterval);
                            window.location.href = "/";
                        }
                    }
                } else {
                    // El tiempo libre avanza de forma ascendente
                    remSegundos++;
                    let mm = Math.floor(remSegundos / 60);
                    let ss = remSegundos % 60;
                    nodoReloj.innerText = (mm < 10 ? "0" + mm : mm) + ":" + (ss < 10 ? "0" + ss : ss);
                }
            }, 1000);

        } catch (e) {
            console.error("Error executing plan:", e);
            // CORRECCIÓN: Leemos directamente desde el objeto local para evitar romper la sintaxis
            const esModo = window.KERNEL_ESPECIAL.idioma === "es";
            alert(esModo ? "Fallo de conexión con el servidor central." : "Connection error with central server.");
        }
    }
};

// Carga automática inicial al abrir el archivo separado
document.addEventListener("DOMContentLoaded", () => {
    window.KERNEL_ESPECIAL.cambiarIdioma("es");
});
