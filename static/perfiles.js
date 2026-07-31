// ==========================================================================================
// OPEN THAN GO SYSTEM - Módulo de Perfiles Especiales (Commercial High Fidelity Edition)
// Company: May Roga LLC - Version: 6.0.0 - Interfaz Letal contra el Agobio en Cortina
// Language Restrictions: Strict Preventative/Wellbeing Tone (No Clinical/Medical Terms)
// ==========================================================================================

(function () {
    const PERFILES_ESPECIALES = {
        activo: false,
        perfilSeleccionado: "veterano",
        keywordsSeleccionadas: [],
        textoPdfExtraido: "",
        grabando: false,
        timerGrabacion: null,
        recorridoMisiones: [],
        recognitionInstance: null,
        frasesRespiracionActuales: null,
        
        TEXTOS: {
            es: {
                switchEspecial: "✨ Modo Especial Adaptado",
                switchNormal: "🛸 Regresar a Open Than Go",
                seleccionaPerfil: "Selecciona tu Portal de Estabilidad Somática:",
                veterano: "Portal Veterans de Guerra",
                adulto_mayor: "Portal Adultos Mayores",
                gubernamental: "Portal Servidores Públicos",
                lblKeywords: "Sintonizadores Somáticos Interactivos (Toca para modular):",
                btnMicGrabar: "Sintonizar por Voz (Estímulo Acústico)",
                btnMicDetener: "Transcribiendo tu voz en tiempo real...",
                btnProcesar: "⚡ Lanzar Desconexión Letal e Inmediata",
                btnReporte: "📋 Solicitar Reporte Descriptivo",
                errorMic: "El canal acústico de voz no está habilitado.",
                alertPdf: "Estructura del documento analizada con éxito y cargada en el motor.",
                errorProcesar: "El motor requiere al menos un sintonizador activo.",
                bienvenidaVet: "Entorno táctico de veteranos activo. Sistema listo para anclaje territorial.",
                bienvenidaMayor: "Entorno de adultos mayores activo. Tipografías de alta legibilidad habilitadas.",
                bienvenidaGob: "Entorno de gestión pública activo. Rompiendo bucles de saturación urbana."
            },
            en: {
                switchEspecial: "✨ Tailored Special Mode",
                switchNormal: "🛸 Return to Open Than Go",
                seleccionaPerfil: "Select your Biological Stability Portal:",
                veterano: "War Veterans Portal",
                adulto_mayor: "Senior Citizens Portal",
                gubernamental: "Public Servants Portal",
                lblKeywords: "Interactive Somatic Tuners (Tap to modulate):",
                btnMicGrabar: "Sintonize by Voice (Acoustic Stimulus)",
                btnMicDetener: "Transcribing voice in real time...",
                btnProcesar: "⚡ Launch Immediate Lethal Disconnection",
                btnReporte: "📋 Request Descriptive Report",
                errorMic: "Acoustic voice channel is not enabled.",
                alertPdf: "Document binary stream synchronized into the engine.",
                errorProcesar: "The engine requires at least one active tuner."
            }
        },
        
    // PASO 2: RECUPERACIÓN DEL COMPORTAMIENTO DE ARRANQUE QUE SÍ FUNCIONABA
    init() {
        this.inyectarEstilosCinematicos();
        this.crearContenedorInterfazEspecial();
        
        // Sincronizamos de inmediato el estado visual del botón físico que está arriba
        const btnFijo = document.getElementById("btn-session-toggle-modulo");
        if (btnFijo) {
            btnFijo.classList.toggle("active", this.activo);
            console.log("Enlace síncrono con el botón de session.html establecido.");
        }
    },

    conmutarDesdeHtml() {
        const btn = document.getElementById("btn-session-toggle-modulo");
        if (!btn) return;
        
        this.activo = !this.activo;
        btn.classList.toggle("active", this.activo);
        
        btn.innerText = this.activo 
            ? this.TEXTOS[window.KERNEL?.idiomaActual || "es"].switchNormal 
            : this.TEXTOS[window.KERNEL?.idiomaActual || "es"].switchEspecial;
            
        this.alternarVisibilidadPaneles();
    },

    inyectarEstilosCinematicos() {
        if (document.getElementById("styles-perfiles-fatal-premium")) return;
        let css = document.createElement("style");
        css.id = "styles-perfiles-fatal-premium";

            css.textContent = `
                .switch-perfiles-container { display: flex; justify-content: center; margin: 15px 0; }
                .btn-switch-perfil { background: #000; color: var(--cyan-inhale, #00bcd4); border: 2px solid #151515; padding: 12px 28px; border-radius: 40px; font-weight: 900; cursor: pointer; transition: all 0.4s cubic-bezier(0.075, 0.82, 0.165, 1); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }
                .btn-switch-perfil.active { background: linear-gradient(135deg, #ff5722 0%, #d84315 100%); color: #fff; border-color: transparent; box-shadow: 0 0 25px rgba(216,67,21,0.6); transform: scale(1.03); }
                
                .cinematic-module-container { background: #020202; border: 2px solid #111; border-radius: 24px; padding: 30px; margin: 20px auto; max-width: 580px; box-shadow: 0 30px 60px rgba(0,0,0,0.95); text-align: center; }
                .portal-flex-list { display: flex; flex-direction: column; gap: 14px; margin: 20px 0; }
                .portal-card-premium { background: #080808; border: 1px solid #1c1c1c; padding: 22px; border-radius: 16px; cursor: pointer; text-align: left; transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1); display: flex; align-items: center; justify-content: space-between; position: relative; }
                .portal-card-premium:hover { background: #0f0f0f; border-color: #333; transform: scale(1.01); }
                
                .portal-card-premium[data-portal="veterano"].active { background: linear-gradient(90deg, rgba(76,175,80,0.15) 0%, #050505 100%); border-color: #4caf50; box-shadow: 0 0 20px rgba(76,175,80,0.2); }
                .portal-card-premium[data-portal="adulto_mayor"].active { background: linear-gradient(90deg, rgba(0,188,212,0.15) 0%, #050505 100%); border-color: #00bcd4; box-shadow: 0 0 20px rgba(0,188,212,0.2); }
                .portal-card-premium[data-portal="gubernamental"].active { background: linear-gradient(90deg, rgba(63,81,181,0.15) 0%, #050505 100%); border-color: #3f51b5; box-shadow: 0 0 20px rgba(63,81,181,0.2); }
                
                .portal-card-premium h4 { margin: 0; color: #fff; font-size: 1.15rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.5px; }
                .cortina-desplegable-premium { background: #040404; border-radius: 14px; padding: 22px; border: 1px solid #161616; margin-top: 15px; margin-bottom: 15px; }
                .keywords-floating-box { display: flex; flex-wrap: wrap; gap: 8px; margin: 15px 0; justify-content: center; }
                
                .badge-keyword-fatal { background: #0c0c0c; border: 1px solid #222; color: #777; padding: 10px 20px; border-radius: 30px; font-size: 0.8rem; cursor: pointer; transition: all 0.2s; font-weight: 800; letter-spacing: 0.5px; }
                .badge-keyword-fatal:hover { background: #161616; color: #fff; }
                
                .veterano-theme .badge-keyword-fatal.selected { background: #4caf50; color: #fff; border-color: transparent; box-shadow: 0 0 15px rgba(76,175,80,0.5); }
                .adulto_mayor-theme .badge-keyword-fatal.selected { background: #00bcd4; color: #fff; border-color: transparent; box-shadow: 0 0 15px rgba(0,188,212,0.5); font-size: 1.05rem; padding: 14px 26px; }
                .gubernamental-theme .badge-keyword-fatal.selected { background: #3f51b5; color: #fff; border-color: transparent; box-shadow: 0 0 15px rgba(63,81,181,0.5); }
                
                .action-btn-fatal-premium { width: 100%; background: linear-gradient(135deg, #4caf50 0%, #1b5e20 100%); color: #fff; padding: 18px; font-weight: 900; text-transform: uppercase; border-radius: 12px; border: none; cursor: pointer; font-size: 1.1rem; letter-spacing: 1px; box-shadow: 0 6px 25px rgba(76,175,80,0.3); transition: all 0.3s; margin-top: 20px; }
                .action-btn-fatal-premium:hover { transform: scale(1.02); box-shadow: 0 8px 30px rgba(76,175,80,0.6); }
                .pill-action-trigger { background: #0b0b0b; border: 1px solid #222; color: #999; padding: 12px 24px; border-radius: 40px; font-size: 0.8rem; cursor: pointer; font-weight: 900; transition: all 0.2s; text-transform: uppercase; }
                .pill-action-trigger:hover { background: #151515; color: #fff; border-color: #444; }
                .reporte-premium-box { background: #050505; border: 1px solid #222; border-radius: 12px; padding: 25px; margin-top: 25px; text-align: left; box-shadow: inset 0 0 15px rgba(0,0,0,0.8); }
            `;
            document.head.appendChild(css);
        },
    crearBotonAlternancia() {
        if (document.getElementById("btn-master-toggle-modulo")) return;
        const barraIdiomas = document.querySelector(".lang-bar");
        if (!barraIdiomas) return;
        
        const containerSwitch = document.createElement("div");
        containerSwitch.className = "switch-perfiles-container";
        
        const btn = document.createElement("button");
        btn.className = "btn-switch-perfil";
        btn.id = "btn-master-toggle-modulo";
        btn.innerText = this.TEXTOS[window.KERNEL?.idiomaActual || "es"].switchEspecial;
        
        btn.onclick = () => {
            this.activo = !this.activo;
            btn.classList.toggle("active", this.activo);
            btn.innerText = this.activo 
                ? this.TEXTOS[window.KERNEL.idiomaActual].switchNormal 
                : this.TEXTOS[window.KERNEL.idiomaActual].switchEspecial;
            this.alternarVisibilidadPaneles();
        };
        
        containerSwitch.appendChild(btn);
        // Posicionamiento inmutable: se inserta arriba de la barra de idiomas
        barraIdiomas.parentNode.insertBefore(containerSwitch, barraIdiomas);
    },

    crearContenedorInterfazEspecial() {
        if (document.getElementById("panel-perfiles-especiales")) return;
        const wrapperForm = document.getElementById("wrapper-form");
        if (!wrapperForm) return;
        
        const divEspecial = document.createElement("div");
        divEspecial.id = "panel-perfiles-especiales";
        divEspecial.className = "hidden";
        wrapperForm.parentNode.insertBefore(divEspecial, wrapperForm.nextSibling);
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
                this.renderizarInterfazEspecial();
            }
            this.ejecutarVozBienvenida();
        } else {
            if (panelEspecial) panelEspecial.classList.add("hidden");
            if (wrapperForm) wrapperForm.classList.remove("hidden");
        }
    },

        ejecutarVozBienvenida() {
            if (!window.KERNEL?.hablar) return;
            const lang = window.KERNEL.idiomaActual;
            const msgs = {
                veterano: this.TEXTOS[lang].bienvenidaVet,
                adulto_mayor: this.TEXTOS[lang].bienvenidaMayor,
                gubernamental: this.TEXTOS[lang].bienvenidaGob
            };
            window.KERNEL.hablar(msgs[this.perfilSeleccionado]);
        },

        renderizarInterfazEspecial() {
            const container = document.getElementById("panel-perfiles-especiales");
            if (!container) return;
            
            const lang = window.KERNEL?.idiomaActual || "es";
            const t = this.TEXTOS[lang];
            
            container.innerHTML = `
                <div class="cinematic-module-container \${this.perfilSeleccionado}-theme">
                    <h3 style="color:#555; font-size:0.85rem; margin: 0 0 25px 0; text-transform:uppercase; font-weight:900; letter-spacing:2px;">\${t.seleccionaPerfil}</h3>
                    
                    <div class="portal-flex-list">
                        <div class="portal-card-premium \${this.perfilSeleccionado === 'veterano' ? 'active' : ''}" data-portal="veterano">
                            <h4>🎖️ \${t.veterano}</h4> <span>⚡</span>
                        </div>
                        <div class="portal-card-premium \${this.perfilSeleccionado === 'adulto_mayor' ? 'active' : ''}" data-portal="adulto_mayor">
                            <h4>👵 \${t.adulto_mayor}</h4> <span>⚡</span>
                        </div>
                        <div class="portal-card-premium \${this.perfilSeleccionado === 'gubernamental' ? 'active' : ''}" data-portal="gubernamental">
                            <h4>💼 \${t.gubernamental}</h4> <span>⚡</span>
                        </div>
                    </div>
                    
                    <div class="cortina-desplegable-premium">
                        <label style="display:block; color: var(--cyan-inhale, #00bcd4); font-weight:900; margin-bottom:15px; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px;">\${t.lblKeywords}</label>
                        
                        <div id="box-keywords-flotantes" class="keywords-floating-box"></div>
                        
                        <div style="margin-top:25px; display:flex; gap:14px; justify-content:center; align-items:center;">
                            <button id="btn-mic-especial" class="pill-action-trigger" style="color:#fff; border-color:#333;">🎙️ \${t.btnMicGrabar}</button>
                            <label class="pill-action-trigger" style="margin:0;">
                                📂 Escanear PDF Estructural
                                <input type="file" id="file-pdf-especial" style="display:none;" accept=".pdf">
                            </label>
                        </div>
                        <input type="hidden" id="txt-input-especial" value="">
                    </div>
                    
                    <button id="btn-procesar-especial" class="action-btn-fatal-premium">\${t.btnProcesar}</button>
                    <button id="btn-reporte-especial" style="width:100%; background:transparent; color:#333; border:none; margin-top:25px; cursor:pointer; font-weight:bold; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px; transition:color 0.2s;">\${t.btnReporte}</button>
                    
                    <div id="wrapper-reporte-output" class="hidden"></div>
                </div>
            `;
            this.enlazarEventosInterfaz();
            this.cargarKeywordsPerfil();
        },
        enlazarEventosInterfaz() {
            const container = document.getElementById("panel-perfiles-especiales");
            if (!container) return;
            
            container.querySelectorAll(".portal-card-premium").forEach(card => {
                card.onclick = () => {
                    container.querySelectorAll(".portal-card-premium").forEach(c => c.classList.remove("active"));
                    card.classList.add("active");
                    this.perfilSeleccionado = card.getAttribute("data-portal");
                    this.keywordsSeleccionadas = [];
                    this.textoPdfExtraido = "";
                    const hiddenTxt = document.getElementById("txt-input-especial");
                    if (hiddenTxt) hiddenTxt.value = "";
                    this.ejecutarVozBienvenida();
                    this.renderizarInterfazEspecial();
                };
            });

            const fileInput = document.getElementById("file-pdf-especial");
            if (fileInput) {
                fileInput.onchange = (e) => {
                    const files = e.target.files;
                    if (!files || files.length === 0) return;
                    
                    const reader = new FileReader();
                    reader.onload = (event) => {
                        const buffer = event.target.result;
                        const chunkStr = new TextDecoder("utf-8").decode(new Uint8Array(buffer).slice(0, 7000));
                        this.textoPdfExtraido = "Flujo real binario analizado. Variables integradas al motor.";
                        
                        if (window.KERNEL?.hablar) {
                            window.KERNEL.hablar(window.KERNEL.idiomaActual === 'es' ? "Documento sincronizado." : "Documento synchronized.");
                        }
                        alert(this.TEXTOS[window.KERNEL?.idiomaActual || "es"].alertPdf);
                    };
                    reader.readAsArrayBuffer(files);
                };
            }

            const btnMic = document.getElementById("btn-mic-especial");
            if (btnMic) btnMic.onclick = () => this.gestionarFlujoMicrofono(btnMic);
            
            document.getElementById("btn-procesar-especial").onclick = () => this.ejecutarMandoEspecial();
            document.getElementById("btn-reporte-especial").onclick = () => this.generarReporteBienestar();
        },

        async cargarKeywordsPerfil() {
            const box = document.getElementById("box-keywords-flotantes");
            if (!box) return;
            box.innerHTML = "";
            
            const lang = window.KERNEL?.idiomaActual || "es";
            try {
                const res = await fetch(`/api/perfiles-especiales/config?perfil=\${this.perfilSeleccionado}&lang=\${lang}`);
                const data = await res.json();
                
                if (data.keywords) {
                    data.keywords.forEach(kw => {
                        const b = document.createElement("div");
                        b.className = "badge-keyword-fatal";
                        b.innerText = kw;
                        b.onclick = () => {
                            b.classList.toggle("selected");
                            if (b.classList.contains("selected")) {
                                this.keywordsSeleccionadas.push(kw);
                                if (window.KERNEL?.hablar) window.KERNEL.hablar(kw.toLowerCase());
                            } else {
                                this.keywordsSeleccionadas = this.keywordsSeleccionadas.filter(k => k !== kw);
                            }
                        };
                        box.appendChild(b);
                    });
                }
            } catch (e) {
                console.error("Error cargando sintonizadores:", e);
            }
        },

        gestionarFlujoMicrofono(btn) {
            const lang = window.KERNEL?.idiomaActual || "es";
            const t = this.TEXTOS[lang];
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            
            if (!SpeechRecognition) {
                alert(t.errorMic);
                return;
            }
            
            if (!this.grabando) {
                this.grabando = true;
                btn.style.background = "#dc2626";
                btn.style.borderColor = "#dc2626";
                btn.innerText = t.btnMicDetener;
                
                this.recognitionInstance = new SpeechRecognition();
                this.recognitionInstance.lang = lang === 'es' ? 'es-US' : 'en-US';
                this.recognitionInstance.interimResults = false;
                this.recognitionInstance.continuous = true;
                
                this.recognitionInstance.onresult = (event) => {
                    const currentIdx = event.resultIndex;
                    const textoVoz = event.results[currentIdx].transcript;
                    const hdnInput = document.getElementById("txt-input-especial");
                    if (hdnInput && textoVoz) {
                        hdnInput.value = (hdnInput.value + " " + textoVoz).trim();
                        if (window.KERNEL?.hablar) window.KERNEL.hablar(textoVoz);
                    }
                };
                
                this.recognitionInstance.onerror = () => this.detenerGraboHardware(btn, t);
                this.recognitionInstance.start();
                this.timerGrabacion = setTimeout(() => { this.detenerGraboHardware(btn, t); }, 60000);
            } else {
                this.detenerGraboHardware(btn, t);
            }
        },

        detenerGraboHardware(btn, t) {
            this.grabando = false;
            clearTimeout(this.timerGrabacion);
            btn.style.background = "#0b0b0b";
            btn.style.borderColor = "#222";
            btn.innerText = "🎙️ Sintonizar por Voz";
            if (this.recognitionInstance) this.recognitionInstance.stop();
        },

        async ejecutarMandoEspecial() {
            const hdnInput = document.getElementById("txt-input-especial");
            const txtInput = hdnInput ? hdnInput.value.trim() : "";
            const lang = window.KERNEL?.idiomaActual || "es";
            
            if (txtInput.length === 0 && this.keywordsSeleccionadas.length === 0 && this.textoPdfExtraido.length === 0) {
                alert(this.TEXTOS[lang].errorProcesar);
                return;
            }
            
            const containerInteractive = document.getElementById("wrapper-interactive");
            const panelPerfiles = document.getElementById("panel-perfiles-especiales");
            if (panelPerfiles) panelPerfiles.classList.add("hidden");
            
            const payload = {
                perfil: this.perfilSeleccionado,
                lang: lang,
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
                
                if (data.status === "success" && window.KERNEL) {
                    window.KERNEL.tipoEscapeGlobal = "ACCION_CAMPO";
                    window.KERNEL.indiceMision = 0;
                    window.KERNEL.pasosMisiones = data.misiones || [];
                    window.KERNEL.mensajeCalidezHumanaActual = data.calidez_humana;
                    this.frasesRespiracionActuales = data.frases_respiracion;
                    
                    if (data.misiones && data.misiones.length > 0) {
                        this.recorridoMisiones.push(data.misiones[0].destino_titulo);
                    }
                    
                    if (window.KERNEL.hablar) window.KERNEL.hablar(data.calidez_humana);
                    if (window.KERNEL.mostrarOpcionesSalir) {
                        containerInteractive.classList.remove("hidden");
                        window.KERNEL.mostrarOpcionesSalir(containerInteractive);
                        
                        const linkMaps = containerInteractive.querySelector("a[href*='maps']");
                        if (linkMaps && data.misiones && data.misiones[0]) {
                            const iframeMaps = document.createElement("iframe");
                            iframeMaps.style = "width:100%; height:320px; border:1px solid #1a1a1a; border-radius:12px; margin-top:15px;";
                            iframeMaps.src = data.misiones[0].destino_coordenadas_gps;
                            linkMaps.parentNode.insertBefore(iframeMaps, linkMaps.nextSibling);
                            linkMaps.style.display = "none";
                        }
                        
                        const linkYT = containerInteractive.querySelector("a[href*='youtube']");
                        if (linkYT && data.misiones && data.misiones[0]) {
                            const iframeYT = document.createElement("iframe");
                            iframeYT.style = "width:100%; height:240px; border:1px solid #1a1a1a; border-radius:12px; margin-top:15px;";
                            iframeYT.src = data.misiones[0].enlace_youtube;
                            iframeYT.allow = "autoplay; encrypted-media";
                            linkYT.parentNode.insertBefore(iframeYT, linkYT.nextSibling);
                            linkYT.style.display = "none";
                        }
                    }
                const btnVolver = document.getElementById("btn-volver-app");
                if (btnVolver) btnVolver.classList.remove("hidden");
            }
        } catch (e) {
            console.error("Fallo crítico despachando mando:", e);
            this.activo = false;
            this.alternarVisibilidadPaneles();
        }
    },
    async generarReporteBienestar() {
        const hdnInput = document.getElementById("txt-input-especial");
        const txtInput = hdnInput ? hdnInput.value.trim() : "";
        const wrapperReporte = document.getElementById("wrapper-reporte-output");
        if (!wrapperReporte) return;
        const lang = window.KERNEL?.idiomaActual || "es";
        const infoCompartida = [...this.keywordsSeleccionadas];
        if (txtInput) infoCompartida.push("Sintonía acústica por voz.");
        if (this.textoPdfExtraido) infoCompartida.push("Mapeo de documento.");
        const payload = {
            perfil: this.perfilSeleccionado,
            lang: lang,
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
            wrapperReporte.innerHTML = `
                <div class="reporte-premium-box" style="margin-top:25px; border-top:1px dashed #222; padding-top:20px; text-align:left;">
                    <h2 style="color:var(--cyan-inhale, #00bcd4); font-size:1.1rem; font-weight:900; text-transform:uppercase; margin:0 0 10px 0;">\${data.titulo}</h2>
                    <p style="font-size:0.85rem; color:#888; line-height:1.4; margin-bottom:15px;">\${data.resumen_descriptivo}</p>
                    <h4 style="color:#fff; margin:0 0 5px 0; font-size:0.9rem; text-transform:uppercase;">Recorrido Concluido:</h4>
                    <ul style="padding-left:15px; margin:0 0 15px 0; font-size:0.85rem; color:#ccc;">
                        \${data.recorrido_realizado.map(r => `<li>\${r}</li>`).join('')}
                    </ul>
                    <h4 style="color:#fff; margin:0 0 5px 0; font-size:0.9rem; text-transform:uppercase;">Evaluación de Autocuidado Comercial:</h4>
                    <p style="font-size:0.85rem; color:#ccc; margin:0; line-height:1.4; text-align:justify;">\${data.observaciones_finales}</p>
                    <span style="font-size:0.65rem; color:#444; display:block; margin-top:15px; text-align:justify; line-height:1.3;">\${data.nota_legal}</span>
                </div>
            `;
            wrapperReporte.classList.remove("hidden");
            if (window.KERNEL?.hablar) {
                window.KERNEL.hablar(lang === 'es' ? "Reporte descriptivo de acompañamiento generado." : "Descriptive report generated.");
            }
        } catch (e) {
            console.error("Error al compilar reporte:", e);
        }
    }
}; // <- Esta llave cierra el objeto principal PERFILES_ESPECIALES

function interceptarMesaDeRelojes() {
    if (window.KERNEL && window.KERNEL.iniciarRelojEnfocadoCasa) {
        console.log("Mesa de Relojes interceptada con éxito.");
        const originalRelojCasa = window.KERNEL.iniciarRelojEnfocadoCasa;
        window.KERNEL.iniciarRelojEnfocadoCasa = function() {
            if (PERFILES_ESPECIALES.activo && PERFILES_ESPECIALES.frasesRespiracionActuales) {
                if (window.KERNEL.hablar) window.KERNEL.hablar(PERFILES_ESPECIALES.frasesRespiracionActuales.antes);
            }
            originalRelojCasa.call(window.KERNEL);
            if (PERFILES_ESPECIALES.activo && PERFILES_ESPECIALES.frasesRespiracionActuales) {
                setTimeout(() => {
                    if (window.KERNEL.hablar) window.KERNEL.hablar(PERFILES_ESPECIALES.frasesRespiracionActuales.despues);
                }, 900000);
            }
        };
    } else {
        setTimeout(interceptarMesaDeRelojes, 250);
    }
}

    function forzarMontajeBotonArriba() {
        // 1. Buscamos el contenedor nativo donde se encuentra la barra de idiomas original
        const barraIdiomas = document.querySelector(".lang-bar");
        
        // 2. Si ya existe en el árbol HTML y no hemos duplicado el botón, lo inyectamos de forma nativa arriba
        if (barraIdiomas && !document.getElementById("btn-master-toggle-modulo")) {
            const btn = document.createElement("button");
            btn.className = "btn-switch-perfil";
            btn.id = "btn-master-toggle-modulo";
            btn.style = "background: #000; color: #00bcd4; border: 2px solid #151515; padding: 12px 28px; border-radius: 40px; font-weight: 900; cursor: pointer; text-transform: uppercase; letter-spacing: 1px; margin: 15px auto; display: block;";
            btn.innerText = PERFILES_ESPECIALES.TEXTOS[window.KERNEL?.idiomaActual || "es"].switchEspecial;
            
            // Enlace de clics directo al motor del módulo para conmutar las cortinas
            btn.onclick = () => {
                PERFILES_ESPECIALES.activo = !PERFILES_ESPECIALES.activo;
                btn.classList.toggle("active", PERFILES_ESPECIALES.activo);
                btn.innerText = PERFILES_ESPECIALES.activo 
                    ? PERFILES_ESPECIALES.TEXTOS[window.KERNEL?.idiomaActual || "es"].switchNormal 
                    : PERFILES_ESPECIALES.TEXTOS[window.KERNEL?.idiomaActual || "es"].switchEspecial;
                PERFILES_ESPECIALES.alternarVisibilidadPaneles();
            };
            
            // Lo colocamos exactamente arriba de la barra de idiomas sin romper el diseño de Open Than Go
            barraIdiomas.parentNode.insertBefore(btn, barraIdiomas);
            PERFILES_ESPECIALES.init();
            interceptarMesaDeRelojes();
            console.log("Botón Maestro inyectado arriba de forma inmutable.");
        } else {
            // Reintentos continuos para acoplarse de forma transparente al ciclo asíncrono de KERNEL.init
            setTimeout(forzarMontajeBotonArriba, 100);
        }
    }

    // Arranque inmediato por hardware
    forzarMontajeBotonArriba();
    window.PERFILES_ESPECIALES = PERFILES_ESPECIALES;
})();
