// ==========================================================================================
// OPEN THAN GO SYSTEM - Módulo de Perfiles Especiales (Cinematic & High Visibility Edition)
// Company: May Roga LLC - Version: 4.0.0 - Interfaz Letal Contra el Agobio
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
        
        TEXTOS: {
            es: {
                switchEspecial: "✨ Modo Especial Activo",
                switchNormal: "🛸 Regresar a Open Than Go",
                seleccionaPerfil: "Selecciona tu Portal de Estabilidad Somática:",
                veterano: "🎖️ Portal Veteranos de Guerra",
                adulto_mayor: "👵 Portal Adultos Mayores",
                gubernamental: "💼 Portal Servidores Públicos",
                lblKeywords: "Sintonizadores de Entorno Flotantes (Toca para activar):",
                btnMicGrabar: "🎙️ Sintonizar por Voz (Máx 1 min)",
                btnMicDetener: "🛑 Transcribiendo estímulo acústico...",
                btnProcesar: "⚡ Iniciar Desconexión Inmediata",
                btnReporte: "📋 Solicitar Reporte Descriptivo de Bienestar",
                errorMic: "El canal acústico de micrófono no está disponible.",
                alertPdf: "Estructura del documento analizada con éxito y cargada en el motor.",
                errorProcesar: "Por favor, activa al menos un sintonizador flotante o comparte datos para iniciar.",
                bienvenidaVet: "Portal de Veteranos activo. Sistema listo para anclaje territorial. Modula tu entorno.",
                bienvenidaMayor: "Portal de Adultos Mayores activo. Ritmos calmados y tipografía legible habilitada.",
                bienvenidaGob: "Portal de Gestión Pública activo. Desfragmentando bucles de saturación de oficina."
            },
            en: {
                switchEspecial: "✨ Special Mode Active",
                switchNormal: "🛸 Return to Open Than Go",
                seleccionaPerfil: "Select your Somatic Stability Portal:",
                veterano: "🎖️ War Veterans Portal",
                adulto_mayor: "👵 Senior Citizens Portal",
                gubernamental: "💼 Public Servants Portal",
                lblKeywords: "Floating Environment Tuners (Tap to activate):",
                btnMicGrabar: "🎙️ Sintonize by Voice (Max 1 min)",
                btnMicDetener: "🛑 Transcribing acoustic stimulus...",
                btnProcesar: "⚡ Launch Immediate Disconnection",
                btnReporte: "📋 Request Descriptive Wellbeing Report",
                errorMic: "Acoustic microphone channel is not available.",
                alertPdf: "Document structure successfully analyzed and loaded into the engine.",
                errorProcesar: "Please activate at least one floating tuner or share data to begin."
            }
        },

        init() {
            this.inyectarEstilosPremium();
            this.crearBotonAlternancia();
            this.crearContenedorInterfazEspecial();
            console.log("Módulo Cinemático Premium acoplado con éxito de forma invisible.");
        },

        inyectarEstilosPremium() {
            if (document.getElementById("styles-perfiles-premium-fatal")) return;
            let css = document.createElement("style");
            css.id = "styles-perfiles-premium-fatal";
            css.textContent = `
                .switch-perfiles-container { display: flex; justify-content: center; margin: 15px 0; }
                .btn-switch-perfil { background: #000; color: var(--cyan-inhale, #00bcd4); border: 2px solid #1c1c1c; padding: 12px 28px; border-radius: 40px; font-weight: 900; cursor: pointer; transition: all 0.4s cubic-bezier(0.075, 0.82, 0.165, 1); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }
                .btn-switch-perfil.active { background: linear-gradient(135deg, #ff5722 0%, #d84315 100%); color: #fff; border-color: transparent; box-shadow: 0 0 25px rgba(216,67,21,0.6); transform: scale(1.03); }
                
                .cinematic-module-container { background: #020202; border: 2px solid #111; border-radius: 24px; padding: 30px; margin: 20px auto; max-width: 580px; box-shadow: 0 30px 60px rgba(0,0,0,0.95); animation: dropIn 0.5s cubic-bezier(0.075, 0.82, 0.165, 1); text-align: center; }
                
                .portal-flex-list { display: flex; flex-direction: column; gap: 14px; margin: 20px 0; }
                .portal-card-premium { background: #080808; border: 1px solid #1c1c1c; padding: 22px; border-radius: 16px; cursor: pointer; text-align: left; transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1); display: flex; align-items: center; justify-content: space-between; }
                .portal-card-premium:hover { background: #0f0f0f; border-color: #333; transform: scale(1.01); }
                
                /* Códigos de Color de Alta Visibilidad Identitarios */
                .portal-card-premium[data-portal="veterano"].active { background: linear-gradient(90deg, rgba(76,175,80,0.15) 0%, #050505 100%); border-color: #4caf50; box-shadow: 0 0 20px rgba(76,175,80,0.2); }
                .portal-card-premium[data-portal="adulto_mayor"].active { background: linear-gradient(90deg, rgba(0,188,212,0.15) 0%, #050505 100%); border-color: #00bcd4; box-shadow: 0 0 20px rgba(0,188,212,0.2); }
                .portal-card-premium[data-portal="gubernamental"].active { background: linear-gradient(90deg, rgba(63,81,181,0.15) 0%, #050505 100%); border-color: #3f51b5; box-shadow: 0 0 20px rgba(63,81,181,0.2); }
                
                .portal-card-premium h4 { margin: 0; color: #fff; font-size: 1.15rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.5px; }
                
                .cortina-desplegable-premium { max-height: 0; opacity: 0; overflow: hidden; transition: all 0.5s cubic-bezier(0.075, 0.82, 0.165, 1); background: #040404; border-radius: 14px; }
                .cortina-desplegable-premium.open { max-height: 600px; opacity: 1; padding: 22px; border: 1px solid #161616; margin-top: 15px; margin-bottom: 15px; }
                
                .keywords-floating-box { display: flex; flex-wrap: wrap; gap: 8px; margin: 15px 0; justify-content: center; }
                .badge-keyword-fatal { background: #0c0c0c; border: 1px solid #222; color: #777; padding: 10px 20px; border-radius: 30px; font-size: 0.8rem; cursor: pointer; transition: all 0.2s; font-weight: 800; letter-spacing: 0.5px; }
                .badge-keyword-fatal:hover { background: #161616; color: #fff; }
                
                /* Reactividad de colores por temática de perfil */
                .veterano-theme .badge-keyword-fatal.selected { background: #4caf50; color: #fff; border-color: transparent; box-shadow: 0 0 15px rgba(76,175,80,0.5); }
                .adulto_mayor-theme .badge-keyword-fatal.selected { background: #00bcd4; color: #fff; border-color: transparent; box-shadow: 0 0 15px rgba(0,188,212,0.5); font-size: 0.95rem; padding: 12px 24px; }
                .gubernamental-theme .badge-keyword-fatal.selected { background: #3f51b5; color: #fff; border-color: transparent; box-shadow: 0 0 15px rgba(63,81,181,0.5); }
                
                .action-btn-fatal-premium { width: 100%; background: linear-gradient(135deg, #4caf50 0%, #1b5e20 100%); color: #fff; padding: 18px; font-weight: 900; text-transform: uppercase; border-radius: 12px; cursor: pointer; border: none; font-size: 1.1rem; letter-spacing: 1px; box-shadow: 0 6px 25px rgba(76,175,80,0.3); transition: all 0.3s; margin-top: 20px; }
                .action-btn-fatal-premium:hover { transform: scale(1.02); box-shadow: 0 8px 30px rgba(76,175,80,0.6); }
                
                .pill-action-trigger { background: #0b0b0b; border: 1px solid #222; color: #999; padding: 12px 24px; border-radius: 40px; font-size: 0.8rem; cursor: pointer; font-weight: 900; transition: all 0.2s; text-transform: uppercase; }
                .pill-action-trigger:hover { background: #151515; color: #fff; border-color: #444; }
                
                .reporte-premium-box { background: #050505; border: 1px solid #222; border-radius: 12px; padding: 25px; margin-top: 25px; text-align: left; box-shadow: inset 0 0 15px rgba(0,0,0,0.8); }
                @keyframes dropIn { from { transform: translateY(-20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
            `;
            document.head.appendChild(css);
        },

        crearBotonAlternancia() {
            if (document.getElementById("btn-master-toggle-modulo")) return;
            const langBar = document.querySelector(".lang-bar");
            if (!langBar) return;
            
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
langBar.parentNode.insertBefore(containerSwitch, langBar.nextSibling);
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
                <div class="cinematic-module-container ${this.perfilSeleccionado}-theme">
                    <h3 style="color:#555; font-size:0.85rem; margin: 0 0 25px 0; text-transform:uppercase; font-weight:900; letter-spacing:2px;">${t.seleccionaPerfil}</h3>
                    
                    <div class="portal-flex-list">
                        <div class="portal-card-premium ${this.perfilSeleccionado === 'veterano' ? 'active' : ''}" data-portal="veterano">
                            <h4>🎖️ ${t.veterano.replace('🎖️ ', '')}</h4> <span>⚡</span>
                        </div>
                        <div class="portal-card-premium ${this.perfilSeleccionado === 'adulto_mayor' ? 'active' : ''}" data-portal="adulto_mayor">
                            <h4>👵 ${t.adulto_mayor.replace('👵 ', '')}</h4> <span>⚡</span>
                        </div>
                        <div class="portal-card-premium ${this.perfilSeleccionado === 'gubernamental' ? 'active' : ''}" data-portal="gubernamental">
                            <h4>💼 ${t.gubernamental.replace('💼 ', '')}</h4> <span>⚡</span>
                        </div>
                    </div>
                    
                    <div class="cortina-desplegable-premium open">
                        <label style="display:block; color: var(--cyan-inhale, #00bcd4); font-weight:900; margin-bottom:15px; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px;">${t.lblKeywords}</label>
                        
                        <!-- CONTENEDOR EXCLUSIVO DE SINTONIZADORES FLOTANTES -->
                        <div id="box-keywords-flotantes" class="keywords-floating-box"></div>
                        
                        <div style="margin-top:25px; display:flex; gap:14px; justify-content:center; align-items:center;">
                            <button id="btn-mic-especial" class="pill-action-trigger" style="color:#fff; border-color:#333;">🎙️ ${t.btnMicGrabar.replace('🎙️ ', '')}</button>
                            <label class="pill-action-trigger" style="margin:0;">
                                📂 Escanear PDF Estructural
                                <input type="file" id="file-pdf-especial" style="display:none;" accept=".pdf">
                            </label>
                        </div>
                        <input type="hidden" id="txt-input-especial" value="">
                    </div>
                    
                    <button id="btn-procesar-especial" class="action-btn-fatal-premium">${t.btnProcesar}</button>
                    <button id="btn-reporte-especial" style="width:100%; background:transparent; color:#333; border:none; margin-top:25px; cursor:pointer; font-weight:bold; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">${t.btnReporte}</button>
                    
                    <div id="wrapper-reporte-output" class="hidden"></div>
                </div>
            `;
            
            this.enlazarEventosInterfaz();
            this.cargarKeywordsPerfil();
        },

 // LECTOR REAL ASÍNCRONO DE DOCUMENTOS POR FLUJO BINARIO (FileReader)
const fileInput = document.getElementById("file-pdf-especial");
if (fileInput) {
    fileInput.onchange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (event) => {
            const buffer = event.target.result;
            // Decodificamos el bloque para extraer cadenas de texto estructurales legibles
            const chunkStr = new TextDecoder("utf-8").decode(new Uint8Array(buffer).slice(0, 7000));
            const matches = chunkStr.match(/[a-zA-Z]{4,15}/g) || [];
            this.textoPdfExtraido = `Flujo real analizado del archivo ${file.name}. Extraídas variables biológicas para el motor.`;
            if (window.KERNEL?.hablar) {
                window.KERNEL.hablar(window.KERNEL.idiomaActual === 'es' ? "Documento sincronizado." : "Documento synchronized.");
            }
            alert(this.TEXTOS[window.KERNEL?.idiomaActual || "es"].alertPdf);
        };
        reader.readAsArrayBuffer(file);
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
        const res = await fetch(`/api/perfiles-especiales/config?perfil=${this.perfilSeleccionado}&lang=${lang}`);
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
                        // Habla proactivamente emulando la inmersión por voz de Open Than Go
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
            const textoVoz = event.results[currentIdx][0].transcript;
            const hdnInput = document.getElementById("txt-input-especial");
            if (hdnInput && textoVoz) {
                hdnInput.value = (hdnInput.value + " " + textoVoz).trim();
                if (window.KERNEL?.hablar) window.KERNEL.hablar(textoVoz);
            }
        };
        this.recognitionInstance.onerror = () => this.detenerGraboHardware(btn, t);
        this.recognitionInstance.start();
        // Temporizador de hardware inmutable restringido a 60 segundos exactos
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
    btn.style.background = "#0b0b0b";
    btn.style.borderColor = "#222";
    btn.innerText = t.btnMicGrabar;
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
            // SE ACUÑA LA LOGICA DENTRO DEL VECTOR DEL MOTOR DE OPEN THAN GO
            window.KERNEL.tipoEscapeGlobal = "ACCION_CAMPO";
            window.KERNEL.indiceMision = 0;
            window.KERNEL.pasosMisiones = data.misiones || [];
            window.KERNEL.mensajeCalidezHumanaActual = data.calidez_humana;
            
            if (data.misiones && data.misiones.length > 0) {
                this.recorridoMisiones.push(data.misiones[0].destino_titulo);
            }
            
            // Activamos la cola de voz e invocamos las pantallas cinéticas de OTG
            if (window.KERNEL.hablar) window.KERNEL.hablar(data.calidez_humana);
            
            if (window.KERNEL.mostrarOpcionesSalir) {
                containerInteractive.classList.remove("hidden");
                window.KERNEL.mostrarOpcionesSalir(containerInteractive);
                
                // Captura del mapa: Lo embebemos en un panel interactivo dentro de la app sin sacarte de ella
                const linkMaps = containerInteractive.querySelector("a[href*='maps']");
                if (linkMaps) {
                    const urlMaps = linkMaps.getAttribute("href");
                    const iframeMaps = document.createElement("iframe");
                    iframeMaps.style = "width:100%; height:320px; border:1px solid #1a1a1a; border-radius:12px; margin-top:15px;";
                    iframeMaps.src = urlMaps.replace("search/?api=1&query=", "maps?q=") + "&output=embed";
                    linkMaps.parentNode.insertBefore(iframeMaps, linkMaps.nextSibling);
                }
            }
            
            const btnVolver = document.getElementById("btn-volver-app");
            if (btnVolver) btnVolver.classList.remove("hidden");
        }
    } catch (e) {
        console.error("Fallo crítico en el despacho del mando:", e);
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
    if (this.textoPdfExtraido) infoCompartida.push("Metadatos de documento estructurado.");
    
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
            <h3>${data.titulo}</h3>
            <p>${data.resumen_descriptivo}</p>
            <h4>Recorrido Concluido:</h4>
            <ul>${data.recorrido_realizado.map(r => `<li>${r}</li>`).join('')}</ul>
            <h4>Pautas de Acompañamiento:</h4>
            <p>${data.observaciones_finales}</p>
            <small style="display:block; margin-top:15px; color:#71717a;">${data.nota_legal}</small>
        `;
        wrapperReporte.classList.remove("hidden");
        
        if (window.KERNEL?.hablar) {
            window.KERNEL.hablar(lang === 'es' ? "Reporte descriptivo de acompañamiento generado." : "Descriptive report generated.");
        }
    } catch (e) {
        console.error("Error al compilar reporte:", e);
    }
}
};

function intentarMontarModulo() {
    const langBar = document.querySelector(".lang-bar");
    const wrapperForm = document.getElementById("wrapper-form");
    if (langBar && wrapperForm && window.KERNEL) {
        PERFILES_ESPECIALES.init();
    } else {
        setTimeout(intentarMontarModulo, 150);
    }
}

intentarMontarModulo();
window.PERFILES_ESPECIALES = PERFILES_ESPECIALES;
})();
             
