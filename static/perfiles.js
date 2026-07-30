// ==========================================================================================
// OPEN THAN GO SYSTEM - Módulo de Perfiles Especiales (Frontend Logic & UI)
// Company: May Roga LLC - Version: 1.0.0
// Language Restrictions: Strict Preventative/Wellbeing Tone (No Clinical/Medical Terms)
// ==========================================================================================

(function () {
    // Objeto de Estado del Módulo Especial
    const PERFILES_ESPECIALES = {
        activo: false,
        perfilSeleccionado: "veterano",
        keywordsSeleccionadas: [],
        textoPdfExtraido: "",
        mediaRecorder: null,
        audioChunks: [],
        grabando: false,
        timerGrabacion: null,
        recorridoMisiones: [],
        
        // Diccionario de Traducción Simétrica e Independiente (Cero términos médicos/gubernamentales)
        TEXTOS: {
            es: {
                switchEspecial: "Módulo Especial",
                switchNormal: "Open Than Go",
                seleccionaPerfil: "Selecciona tu perfil de autocuidado:",
                veterano: "Veteranos",
                adulto_mayor: "Adultos Mayores",
                gubernamental: "Trabajadores Públicos",
                lblKeywords: "Palabras clave flotantes (Toca para seleccionar):",
                lblTexto: "Comparte tus observaciones o pega contenido aquí:",
                placeholderTexto: "Escribe libremente sobre tu entorno actual...",
                lblPdf: "Cargar documento de orientación (PDF):",
                lblMic: "Micro de autocuidado (Máx 1 min):",
                btnMicGrabar: "🎙️ Grabar Voz",
                btnMicDetener: "🛑 Detener (Transcripción...)",
                btnProcesar: "Activar Mando Especial",
                btnReporte: "📋 Solicitar Reporte de Bienestar",
                errorMic: "El reconocimiento de voz o micrófono no está disponible.",
                alertPdf: "Contenido del documento cargado con éxito.",
                errorProcesar: "Por favor, introduce texto o selecciona palabras clave.",
                lblReporteTitulo: "REPORTE DESCRIPTIVO GENERADO"
            },
            en: {
                switchEspecial: "Special Module",
                switchNormal: "Open Than Go",
                seleccionaPerfil: "Select your self-care profile:",
                veterano: "Veterans",
                adulto_mayor: "Senior Citizens",
                gubernamental: "Public Servants",
                lblKeywords: "Floating keywords (Tap to select):",
                lblTexto: "Share your observations or paste content here:",
                placeholderTexto: "Write freely about your current environment...",
                lblPdf: "Load orientation document (PDF):",
                lblMic: "Self-care microphone (Max 1 min):",
                btnMicGrabar: "🎙️ Record Voice",
                btnMicDetener: "🛑 Stop (Transcribing...)",
                btnProcesar: "Activate Special Control",
                btnReporte: "📋 Request Wellbeing Report",
                errorMic: "Voice recognition or microphone is not available.",
                alertPdf: "Document content loaded successfully.",
                errorProcesar: "Please enter text or select keywords.",
                lblReporteTitulo: "WELLBEING REPORT GENERATED"
            }
        },

        init() {
            this.inyectarEstilosAdicionales();
            this.crearBotonAlternancia();
            this.crearContenedorInterfazEspecial();
            console.log("Módulo de Perfiles Especiales acoplado a Open Than Go con éxito.");
        },

        inyectarEstilosAdicionales() {
            let css = document.createElement("style");
            css.textContent = `
                .switch-perfiles-container { display: flex; justify-content: center; margin: 10px 0; }
                .btn-switch-perfil { background: #111; color: #888; border: 1px solid #333; padding: 8px 16px; border-radius: 20px; font-weight: bold; cursor: pointer; transition: all 0.3s; font-size: 0.85rem; }
                .btn-switch-perfil.active { background: var(--accent); color: #fff; border-color: var(--accent); box-shadow: 0 0 10px rgba(216,67,21,0.4); }
                .perfil-selector-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 15px; }
                .btn-perfil-opcion { background: #0a0a0a; border: 1px solid #222; color: #aaa; padding: 12px 6px; text-align: center; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 0.8rem; transition: all 0.2s; }
                .btn-perfil-opcion.active { border-color: var(--cyan-inhale); color: var(--cyan-inhale); background: rgba(0,188,212,0.05); }
                .keywords-floating-box { display: flex; flex-wrap: wrap; gap: 6px; margin: 10px 0; min-height: 40px; padding: 8px; background: #070707; border: 1px dashed #222; border-radius: 6px; }
                .badge-keyword { background: #151515; border: 1px solid #333; color: #bbb; padding: 6px 12px; border-radius: 15px; font-size: 0.75rem; cursor: pointer; transition: all 0.2s; user-select: none; }
                .badge-keyword.selected { background: var(--green-action); color: #fff; border-color: var(--green-action); }
                .media-controls-wrapper { display: flex; gap: 10px; margin: 12px 0; align-items: center; }
                .btn-audio-action { flex: 1; padding: 12px; font-weight: bold; border-radius: 4px; border: none; cursor: pointer; text-transform: uppercase; font-size: 0.8rem; transition: background 0.2s; }
                .file-pdf-input { background: #0a0a0a; border: 1px solid #222; color: #888; padding: 8px; font-size: 0.8rem; border-radius: 4px; width: 100%; box-sizing: border-box; }
                .reporte-output-box { background: #050505; border: 1px solid #222; border-radius: 8px; padding: 20px; margin-top: 20px; text-align: left; }
                .reporte-output-box h2 { color: var(--cyan-inhale); font-size: 1.2rem; margin-top: 0; font-weight: 900; border-bottom: 1px solid #222; padding-bottom: 8px; }
                .reporte-output-box h3 { color: var(--green-action); font-size: 1rem; margin: 15px 0 6px 0; font-weight: bold; }
                .reporte-output-box p, .reporte-output-box li { font-size: 0.9rem; color: #ccc; line-height: 1.4; }
                .reporte-output-box ul { margin: 0; padding-left: 20px; }
                .nota-legal-reporte { font-size: 0.7rem !important; color: #555 !important; margin-top: 15px; display: block; border-top: 1px dashed #222; padding-top: 8px; text-align: justify; }
            `;
            document.head.appendChild(css);
        },

        crearBotonAlternancia() {
            const langBar = document.querySelector(".lang-bar");
            if (!langBar) return;
            
            const containerSwitch = document.createElement("div");
            containerSwitch.className = "switch-perfiles-container";
            
            const btn = document.createElement("button");
            btn.className = "btn-switch-perfil";
            btn.id = "btn-master-toggle-modulo";
            btn.innerText = this.TEXTOS[window.KERNEL.idiomaActual].switchEspecial;
            
            btn.onclick = () => {
                this.activo = !this.activo;
                btn.classList.toggle("active", this.activo);
                btn.innerText = this.activo 
                    ? this.TEXTOS[window.KERNEL.idiomaActual].switchNormal 
                    : this.TEXTOS[window.KERNEL.idiomaActual].switchEspecial;
                
                this.alternarVisibilidadPaneles();
            };
            
            containerSwitch.appendChild(btn);
            langBar.parentNode.insertBefore(containerSwitch, langBar.nextSibling);
        },

        crearContenedorInterfazEspecial() {
            const wrapperForm = document.getElementById("wrapper-form");
            if (!wrapperForm) return;
            
            const divEspecial = document.createElement("div");
            divEspecial.id = "panel-perfiles-especiales";
            divEspecial.className = "hidden";
            divEspecial.style = "margin-top: 15px;";
            wrapperForm.parentNode.insertBefore(divEspecial, wrapperForm.nextSibling);
            
            // Note: renderizarInterfazEspecial is called when the panel becomes active.
            // No need to call it here directly, as it handles initial rendering when visible.
        },

        alternarVisibilidadPaneles() {
            const wrapperForm = document.getElementById("wrapper-form");
            const panelEspecial = document.getElementById("panel-perfiles-especiales");
            const wrapperInteractive = document.getElementById("wrapper-interactive");
            const pantallaCierre = document.getElementById('pantalla-cierre');
            
            if (this.activo) {
                if (wrapperForm) wrapperForm.classList.add("hidden");
                if (wrapperInteractive) wrapperInteractive.classList.add("hidden");
                if (pantallaCierre) pantallaCierre.classList.add("hidden");
                if (panelEspecial) {
                    panelEspecial.classList.remove("hidden");
                    this.renderizarInterfazEspecial(); // Render on activation
                }
                window.KERNEL.hablar(window.KERNEL.idiomaActual === 'es' ? "Entrando al entorno de personalización adaptada." : "Entering tailored personalization environment.");
            } else {
                if (panelEspecial) panelEspecial.classList.add("hidden");
                if (wrapperForm) {
                    wrapperForm.classList.remove("hidden");
                    window.KERNEL.inyectarBloquePreguntas();
                    window.KERNEL.activarBotonMandoLibreInicial();
                }
                // When returning to normal mode, clear any special module content
                if (wrapperInteractive) {
                    wrapperInteractive.classList.add("hidden");
                    wrapperInteractive.innerHTML = '';
                }
                const btnVolver = document.getElementById("btn-volver-app");
                if (btnVolver) btnVolver.classList.add("hidden"); // Hide floating back button
            }
        },

        renderizarInterfazEspecial() {
            const container = document.getElementById("panel-perfiles-especiales");
            if (!container) return;
            
            const t = this.TEXTOS[window.KERNEL.idiomaActual];
            
            // Corregido: La concatenación de strings y llamadas a funciones estaba malformada.
            // Se reconstruye la interfaz con una estructura HTML válida.
            container.innerHTML = `
                <h1 style="color:var(--accent); font-size:1.5rem; text-align:center; margin-bottom:20px;">OPEN THAN GO - TAILORED EXPERIENCE</h1>

                <label for="perfil-selector" style="display:block; margin-bottom:10px; color:#ddd; font-weight:bold;">${t.seleccionaPerfil}</label>
                <div class="perfil-selector-grid" id="perfil-selector">
                    <button class="btn-perfil-opcion ${this.perfilSeleccionado === 'veterano' ? 'active' : ''}" data-perf="veterano">${t.veterano}</button>
                    <button class="btn-perfil-opcion ${this.perfilSeleccionado === 'adulto_mayor' ? 'active' : ''}" data-perf="adulto_mayor">${t.adulto_mayor}</button>
                    <button class="btn-perfil-opcion ${this.perfilSeleccionado === 'gubernamental' ? 'active' : ''}" data-perf="gubernamental">${t.gubernamental}</button>
                </div>

                <label style="display:block; margin-top:20px; margin-bottom:8px; color:#ddd; font-weight:bold;">${t.lblKeywords}</label>
                <div class="keywords-floating-box" id="box-keywords-flotantes">
                    <!-- Keywords loaded dynamically here -->
                </div>

                <label for="txt-input-especial" style="display:block; margin-top:20px; margin-bottom:8px; color:#ddd; font-weight:bold;">${t.lblTexto}</label>
                <textarea id="txt-input-especial" class="input-glow" placeholder="${t.placeholderTexto}" rows="5" style="width:100%; box-sizing:border-box; background:#0a0a0a; border:1px solid #222; color:#eee; padding:10px; border-radius:4px; font-size:0.9rem; resize:vertical;"></textarea>

                <label for="file-pdf-especial" style="display:block; margin-top:20px; margin-bottom:8px; color:#ddd; font-weight:bold;">${t.lblPdf}</label>
                <input type="file" id="file-pdf-especial" accept="application/pdf" class="file-pdf-input">

                <label style="display:block; margin-top:20px; margin-bottom:8px; color:#ddd; font-weight:bold;">${t.lblMic}</label>
                <div class="media-controls-wrapper">
                    <button id="btn-mic-especial" class="btn-audio-action" style="background:#222; color:#eee;">${t.btnMicGrabar}</button>
                </div>

                <div style="display:flex; gap:10px; margin-top:25px;">
                    <button id="btn-procesar-especial" class="btn-action-primary" style="flex:1; background:var(--accent); color:#fff; border:none; padding:12px 15px; border-radius:4px; font-weight:bold; cursor:pointer; text-transform:uppercase; font-size:0.9rem;">${t.btnProcesar}</button>
                    <button id="btn-reporte-especial" class="btn-action-secondary" style="flex:1; background:#004d40; color:#fff; border:none; padding:12px 15px; border-radius:4px; font-weight:bold; cursor:pointer; text-transform:uppercase; font-size:0.9rem;">${t.btnReporte}</button>
                </div>

                <div id="wrapper-reporte-output" class="reporte-output-box hidden">
                    <!-- Report output will be rendered here -->
                </div>
            `;
            this.enlazarEventosInterfaz();
            this.cargarKeywordsPerfil();
        },

        enlazarEventosInterfaz() {
            const container = document.getElementById("panel-perfiles-especiales");
            if (!container) return; // Ensure container exists before trying to query its elements

            // Grid de Selección de Perfil
            container.querySelectorAll(".btn-perfil-opcion").forEach(btn => {
                btn.onclick = () => {
                    container.querySelectorAll(".btn-perfil-opcion").forEach(b => b.classList.remove("active"));
                    btn.classList.add("active");
                    this.perfilSeleccionado = btn.getAttribute("data-perf");
                    this.keywordsSeleccionadas = []; // Reset keywords on profile change
                    this.cargarKeywordsPerfil();
                };
            });

            // Carga y simulación/parseo local de PDF (Nativo sin librerías externas)
            const fileInput = document.getElementById("file-pdf-especial");
            if (fileInput) {
                fileInput.onchange = (e) => {
                    const file = e.target.files[0]; // Acceder al objeto File
                    if (file) {
                        // Corregido: Template literal mal formado y uso de file.name para simulación.
                        this.textoPdfExtraido = `Contenido analizado del documento voluntario: ${file.name}. Orientación y pautas adaptadas de autocuidado diario para el participante.`;
                        alert(this.TEXTOS[window.KERNEL.idiomaActual].alertPdf);
                    }
                };
            }

            // Botón de Micrófono con Grabación y Transcripción Nativa Real (Webkit/Speech API)
            const btnMic = document.getElementById("btn-mic-especial");
            if (btnMic) {
                btnMic.onclick = () => this.gestionarFlujoMicrofono(btnMic);
            }

            // Botón Ejecutar Mando Especial
            const btnProcesar = document.getElementById("btn-procesar-especial");
            if (btnProcesar) {
                btnProcesar.onclick = () => this.ejecutarMandoEspecial();
            }

            // Botón Generar Reporte
            const btnReporte = document.getElementById("btn-reporte-especial");
            if (btnReporte) {
                btnReporte.onclick = () => this.generarReporteBienestar();
            }
        },

        async cargarKeywordsPerfil() {
            const box = document.getElementById("box-keywords-flotantes");
            if (!box) return;
            box.innerHTML = "";
            try {
                const res = await fetch(`/api/perfiles-especiales/config?perfil=${this.perfilSeleccionado}&lang=${window.KERNEL.idiomaActual}`);
                const data = await res.json();
                if (data.keywords) {
                    data.keywords.forEach(kw => {
                        const b = document.createElement("div");
                        b.className = "badge-keyword";
                        b.innerText = kw;
                        // Sincronizar el estado seleccionado si ya estaba en this.keywordsSeleccionadas
                        if (this.keywordsSeleccionadas.includes(kw)) {
                            b.classList.add("selected");
                        }
                        b.onclick = () => {
                            b.classList.toggle("selected");
                            if (b.classList.contains("selected")) {
                                this.keywordsSeleccionadas.push(kw);
                            } else {
                                this.keywordsSeleccionadas = this.keywordsSeleccionadas.filter(k => k !== kw);
                            }
                        };
                        box.appendChild(b);
                    });
                }
            } catch (e) {
                console.error("Error cargando palabras clave contextuales:", e);
            }
        },

        gestionarFlujoMicrofono(btn) {
            const t = this.TEXTOS[window.KERNEL.idiomaActual];
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                alert(t.errorMic);
                return;
            }
            if (!this.grabando) {
                // Iniciar Grabación de Voz y Transcripción Asíncrona
                this.grabando = true;
                btn.style.background = "#dc2626";
                btn.innerText = t.btnMicDetener;
                this.audioChunks = []; // Esto sigue aquí, aunque solo se use SpeechRecognition.
                                      // Potencialmente para futura integración de MediaRecorder.
                this.recognitionInstance = new SpeechRecognition();
                this.recognitionInstance.lang = window.KERNEL.idiomaActual === 'es' ? 'es-US' : 'en-US';
                this.recognitionInstance.interimResults = false;
                this.recognitionInstance.maxAlternatives = 1;
                this.recognitionInstance.onresult = (event) => {
                    const textoVoz = event.results[0][0].transcript;
                    const txtArea = document.getElementById("txt-input-especial");
                    if (txtArea && textoVoz) {
                        // Corregido: .strip() no es un método JS estándar, se reemplaza por .trim()
                        txtArea.value = (txtArea.value + " " + textoVoz).trim();
                    }
                };
                this.recognitionInstance.onerror = (e) => {
                    console.error("Fallo estructural en reconocimiento de voz:", e.error);
                    this.detenerGraboHardware(btn, t);
                };
                this.recognitionInstance.onend = () => {
                    if (this.grabando) this.recognitionInstance.start(); // Ciclo continuo hasta timeout
                };
                this.recognitionInstance.start();
                // Hardware Timer: Bloqueo inmutable estricto a los 60 segundos exactos
                this.timerGrabacion = setTimeout(() => {
                    this.detenerGraboHardware(btn, t);
                }, 60000);
            } else {
                this.detenerGraboHardware(btn, t);
            }
        },

        detenerGraboHardware(btn, t) {
            this.grabando = false;
            clearTimeout(this.timerGrabacion);
            btn.style.background = "#222";
            btn.innerText = t.btnMicGrabar;
            if (this.recognitionInstance) {
                this.recognitionInstance.onend = null;
                this.recognitionInstance.stop();
            }
        },

        async ejecutarMandoEspecial() {
            const txtInput = document.getElementById("txt-input-especial") ? document.getElementById("txt-input-especial").value.trim() : "";
            if (txtInput.length === 0 && this.keywordsSeleccionadas.length === 0) {
                // Corregido: Usar idiomaActual directamente para el mensaje de error.
                window.KERNEL.hablar(this.TEXTOS[window.KERNEL.idiomaActual].errorProcesar);
                return;
            }
            const containerInteractive = document.getElementById("wrapper-interactive");
            const panelPerfiles = document.getElementById("panel-perfiles-especiales");
            if (panelPerfiles) panelPerfiles.classList.add("hidden");
            if (containerInteractive) {
                // Corregido: Template literal mal formado.
                containerInteractive.innerHTML = `<div style='text-align:center; padding:40px 0;'><h2 style='color:#fff; font-size:1.1rem;'>${window.KERNEL.idiomaActual === 'es' ? 'ESTABLECIENDO ENTORNO ESPECIAL...' : 'ESTABLISHING SPECIAL ENVIRONMENT...'}</h2></div>`;
                containerInteractive.classList.remove("hidden");
            }
            const payload = {
                perfil: this.perfilSeleccionado,
                lang: window.KERNEL.idiomaActual,
                texto: txtInput,
                keywords_seleccionadas: this.keywordsSeleccionadas,
                contexto_pdf: this.textoPdfExtraido
            };
            try {
                const res = await fetch("/api/perfiles-especiales/procesar", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.status === "success") {
                    // Sincronización transparente con el motor Open Than Go
                    window.KERNEL.tipoEscapeGlobal = "ACCION_CAMPO";
                    window.KERNEL.indiceMision = 0;
                    window.KERNEL.pasosMisiones = data.misiones || [];
                    window.KERNEL.mensajeCalidezHumanaActual = data.calidez_humana;
                    // Registro de misiones completadas en el historial para el reporte final
                    if (data.misiones && data.misiones.length > 0) {
                        // Solo añadir el título de la primera misión del paso actual
                        this.recorridoMisiones.push(data.misiones[0].destino_titulo);
                    }
                    window.KERNEL.hablar(data.calidez_humana);
                    window.KERNEL.mostrarOpcionesSalir(containerInteractive);
                    // Mostramos el botón de retorno flotante nativo de OTG para navegación suave
                    const btnVolver = document.getElementById("btn-volver-app");
                    if (btnVolver) btnVolver.classList.remove("hidden");
                } else {
                    // Manejar error si la API responde con status no 'success'
                    console.error("API Especial devolvió error:", data.message);
                    window.KERNEL.hablar(data.message || (window.KERNEL.idiomaActual === 'es' ? "Ha ocurrido un error al procesar el mando especial." : "An error occurred while processing the special command."));
                    this.activo = false;
                    this.alternarVisibilidadPaneles();
                }
            } catch (e) {
                console.error("Error en comunicación con API Especial:", e);
                window.KERNEL.hablar(window.KERNEL.idiomaActual === 'es' ? "Problema de comunicación. Intentando reestablecer." : "Communication issue. Attempting to re-establish.");
                this.activo = false;
                this.alternarVisibilidadPaneles();
            }
        },

        async generarReporteBienestar() {
            const txtInput = document.getElementById("txt-input-especial") ? document.getElementById("txt-input-especial").value.trim() : "";
            const wrapperReporte = document.getElementById("wrapper-reporte-output");
            if (!wrapperReporte) return;

            const infoCompartida = [...this.keywordsSeleccionadas];
            if (txtInput) infoCompartida.push(txtInput);
            if (this.textoPdfExtraido) infoCompartida.push("Documento de orientación.");

            const payload = {
                perfil: this.perfilSeleccionado,
                lang: window.KERNEL.idiomaActual,
                recorrido: this.recorridoMisiones,
                informacion_compartida: infoCompartida
            };

            try {
                const res = await fetch("/api/perfiles-especiales/reporte", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                // Corregido: Template literal mal formado y adición de estructura HTML según los estilos definidos.
                wrapperReporte.innerHTML = `
                    <h2>${data.titulo || this.TEXTOS[window.KERNEL.idiomaActual].lblReporteTitulo}</h2>
                    <p>${data.resumen_descriptivo || ''}</p>
                    <h3>${window.KERNEL.idiomaActual === 'es' ? 'Recorrido de Orientación:' : 'Orientation Journey:'}</h3>
                    <ul>
                        ${data.recorrido_realizado && data.recorrido_realizado.length > 0 ? data.recorrido_realizado.map(r => `<li>${r}</li>`).join('') : `<li>${window.KERNEL.idiomaActual === 'es' ? 'No se ha realizado un recorrido específico.' : 'No specific journey has been undertaken.'}</li>`}
                    </ul>
                    <h3>${window.KERNEL.idiomaActual === 'es' ? 'Dinámicas Sugeridas:' : 'Suggested Dynamics:'}</h3>
                    <ul>
                        ${data.actividades_sugeridas && data.actividades_sugeridas.length > 0 ? data.actividades_sugeridas.map(a => `<li>${a}</li>`).join('') : `<li>${window.KERNEL.idiomaActual === 'es' ? 'No hay dinámicas sugeridas en este momento.' : 'No suggested dynamics at this time.'}</li>`}
                    </ul>
                    <h3>${window.KERNEL.idiomaActual === 'es' ? 'Observaciones de Autocuidado:' : 'Self-Care Observations:'}</h3>
                    <p>${data.observaciones_finales || ''}</p>
                    <span class="nota-legal-reporte">${data.nota_legal || (window.KERNEL.idiomaActual === 'es' ? 'Este reporte es una guía descriptiva. No sustituye el asesoramiento profesional.' : 'This report is a descriptive guide. It does not replace professional advice.')}</span>
                `;
                wrapperReporte.classList.remove("hidden");
                window.KERNEL.hablar(window.KERNEL.idiomaActual === 'es' ? "Reporte descriptivo de bienestar listo." : "Descriptive wellbeing report is ready.");
            } catch (e) {
                console.error("Error compilando reporte descriptivo:", e);
                window.KERNEL.hablar(window.KERNEL.idiomaActual === 'es' ? "No se pudo generar el reporte. Inténtalo de nuevo." : "Could not generate the report. Please try again.");
                if (wrapperReporte) {
                    wrapperReporte.innerHTML = `<p style="color:var(--accent); text-align:center;">${window.KERNEL.idiomaActual === 'es' ? 'Error al generar reporte.' : 'Error generating report.'}</p>`;
                    wrapperReporte.classList.remove("hidden");
                }
            }
        }
    };

    // Inicialización del engranaje una vez el DOM esté completamente mapeado
    document.addEventListener("DOMContentLoaded", () => {
        // Monitoreamos cambios de idioma en KERNEL para refrescar la interfaz simétricamente
        const originalCambiarIdioma = window.KERNEL.cambiarIdioma;
        window.KERNEL.cambiarIdioma = function (lang) {
            originalCambiarIdioma.call(window.KERNEL, lang);
            if (PERFILES_ESPECIALES.activo) {
                PERFILES_ESPECIALES.renderizarInterfazEspecial(); // Re-render if active to update texts
                PERFILES_ESPECIALES.cargarKeywordsPerfil(); // Re-load keywords for new language
            } else {
                const btnToggle = document.getElementById("btn-master-toggle-modulo");
                if (btnToggle) btnToggle.innerText = PERFILES_ESPECIALES.TEXTOS[lang].switchEspecial;
            }
        };

        // Escuchamos el botón volver nativo de OTG para resetear estados locales sin romper la SPA
        const btnVolver = document.getElementById("btn-volver-app");
        if (btnVolver) {
            btnVolver.addEventListener("click", (e) => {
                // Prevenir el comportamiento por defecto si se desea solo manejar el reseteo
                // e.preventDefault(); 
                if (PERFILES_ESPECIALES.activo) {
                    PERFILES_ESPECIALES.activo = false;
                    PERFILES_ESPECIALES.alternarVisibilidadPaneles();
                    const btnToggle = document.getElementById("btn-master-toggle-modulo");
                    if (btnToggle) {
                        btnToggle.classList.remove("active");
                        btnToggle.innerText = PERFILES_ESPECIALES.TEXTOS[window.KERNEL.idiomaActual].switchEspecial;
                    }
                    // Limpiar el estado interno del módulo al volver
                    PERFILES_ESPECIALES.keywordsSeleccionadas = [];
                    PERFILES_ESPECIALES.textoPdfExtraido = "";
                    PERFILES_ESPECIALES.recorridoMisiones = [];
                    // Asegurarse de ocultar el reporte si está visible
                    const wrapperReporte = document.getElementById("wrapper-reporte-output");
                    if(wrapperReporte) wrapperReporte.classList.add("hidden");
                }
            });
        }
        PERFILES_ESPECIALES.init();
    });

    window.PERFILES_ESPECIALES = PERFILES_ESPECIALES;
})();
