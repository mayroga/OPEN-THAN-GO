// ==========================================================================================
// OPEN THAN GO SYSTEM - Módulo de Perfiles Especiales (Premium Cinematic & Voice Edition)
// Company: May Roga LLC - Version: 5.0.0 - Control de Homeostasis de Alta Velocidad
// OPEN THAN GO SYSTEM - Módulo de Perfiles Especiales (Commercial High Fidelity Edition)
// Company: May Roga LLC - Version: 5.1.0 - Interfaz Letal contra el Agobio en Cortina
// Language Restrictions: Strict Preventative/Wellbeing Tone (No Clinical/Medical Terms)
// ==========================================================================================

@@ -14,6 +14,7 @@
        timerGrabacion: null,
        recorridoMisiones: [],
        recognitionInstance: null,
        frasesRespiracionActuales: null,

        TEXTOS: {
            es: {
@@ -29,10 +30,10 @@
                btnProcesar: "⚡ Lanzar Desconexión Letal e Inmediata",
                btnReporte: "📋 Solicitar Reporte Descriptivo",
                errorMic: "El canal acústico de voz no está habilitado.",
                alertPdf: "Chorro binario del documento sincronizado al motor.",
                alertPdf: "Estructura del documento analizada con éxito y cargada en el motor.",
                errorProcesar: "El motor requiere al menos un sintonizador activo.",
                bienvenidaVet: "Entorno táctico de veteranos activo. Sistema listo para anclaje territorial.",
                bienvenidaMayor: "Entorno de adultos mayores activo. Tipografías y ritmos biológicos habilitados.",
                bienvenidaMayor: "Entorno de adultos mayores activo. Tipografías de alta legibilidad habilitadas.",
                bienvenidaGob: "Entorno de gestión pública activo. Rompiendo bucles de saturación urbana."
            },
            en: {
@@ -52,11 +53,12 @@
                errorProcesar: "The engine requires at least one active tuner."
            }
        },

        init() {
            this.inyectarEstilosCinematicos();
            this.crearBotonAlternancia();
            this.crearContenedorInterfazEspecial();
            console.log("Módulo Cinemático Premium cargado en memoria.");
            console.log("Módulo Comercial de Perfiles Especiales inicializado.");
        },

        inyectarEstilosCinematicos() {
@@ -67,36 +69,26 @@
                .switch-perfiles-container { display: flex; justify-content: center; margin: 15px 0; }
                .btn-switch-perfil { background: #000; color: var(--cyan-inhale, #00bcd4); border: 2px solid #151515; padding: 12px 28px; border-radius: 40px; font-weight: 900; cursor: pointer; transition: all 0.4s cubic-bezier(0.075, 0.82, 0.165, 1); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }
                .btn-switch-perfil.active { background: linear-gradient(135deg, #ff5722 0%, #d84315 100%); color: #fff; border-color: transparent; box-shadow: 0 0 25px rgba(216,67,21,0.6); transform: scale(1.03); }
                
                .cinematic-module-container { background: #020202; border: 2px solid #111; border-radius: 24px; padding: 30px; margin: 20px auto; max-width: 580px; box-shadow: 0 30px 60px rgba(0,0,0,0.95); animation: dropAnim 0.5s cubic-bezier(0.075, 0.82, 0.165, 1); text-align: center; }
                
                .cinematic-module-container { background: #020202; border: 2px solid #111; border-radius: 24px; padding: 30px; margin: 20px auto; max-width: 580px; box-shadow: 0 30px 60px rgba(0,0,0,0.95); text-align: center; }
                .portal-flex-list { display: flex; flex-direction: column; gap: 14px; margin: 20px 0; }
                .portal-card-premium { background: #080808; border: 1px solid #1c1c1c; padding: 22px; border-radius: 16px; cursor: pointer; text-align: left; transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1); display: flex; align-items: center; justify-content: space-between; }
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
                .adulto_mayor-theme .badge-keyword-fatal.selected { background: #00bcd4; color: #fff; border-color: transparent; box-shadow: 0 0 15px rgba(0,188,212,0.5); font-size: 0.95rem; padding: 12px 24px; }
                .adulto_mayor-theme .badge-keyword-fatal.selected { background: #00bcd4; color: #fff; border-color: transparent; box-shadow: 0 0 15px rgba(0,188,212,0.5); font-size: 1.05rem; padding: 14px 26px; }
                .gubernamental-theme .badge-keyword-fatal.selected { background: #3f51b5; color: #fff; border-color: transparent; box-shadow: 0 0 15px rgba(63,81,181,0.5); }
                
                .action-btn-fatal-premium { width: 100%; background: linear-gradient(135deg, #4caf50 0%, #1b5e20 100%); color: #fff; padding: 18px; font-weight: 900; text-transform: uppercase; border-radius: 12px; cursor: pointer; border: none; font-size: 1.1rem; letter-spacing: 1px; box-shadow: 0 6px 25px rgba(76,175,80,0.3); transition: all 0.3s; margin-top: 20px; }
                .action-btn-fatal-premium:hover { transform: scale(1.02); box-shadow: 0 8px 30px rgba(76,175,80,0.6); }
                
                .pill-action-trigger { background: #0b0b0b; border: 1px solid #222; color: #999; padding: 12px 24px; border-radius: 40px; font-size: 0.8rem; cursor: pointer; font-weight: 900; transition: all 0.2s; text-transform: uppercase; }
                .pill-action-trigger:hover { background: #151515; color: #fff; border-color: #444; }
                
                .reporte-premium-box { background: #050505; border: 1px solid #222; border-radius: 12px; padding: 25px; margin-top: 25px; text-align: left; box-shadow: inset 0 0 15px rgba(0,0,0,0.8); }
                @keyframes dropAnim { from { transform: translateY(-20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
            `;
            document.head.appendChild(css);
        },
@@ -105,25 +97,18 @@
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
                
                btn.innerText = this.activo ? this.TEXTOS[window.KERNEL.idiomaActual].switchNormal : this.TEXTOS[window.KERNEL.idiomaActual].switchEspecial;
                this.alternarVisibilidadPaneles();
            };
            
            containerSwitch.appendChild(btn);
            langBar.parentNode.insertBefore(containerSwitch, langBar.nextSibling);
        },
@@ -132,7 +117,6 @@
            if (document.getElementById("panel-perfiles-especiales")) return;
            const wrapperForm = document.getElementById("wrapper-form");
            if (!wrapperForm) return;
            
            const divEspecial = document.createElement("div");
            divEspecial.id = "panel-perfiles-especiales";
            divEspecial.className = "hidden";
@@ -142,82 +126,84 @@
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
        },
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
                            <h4>🎖️ ${t.veterano}</h4> <span>⚡</span>
                        </div>
                        <div class="portal-card-premium ${this.perfilSeleccionado === 'adulto_mayor' ? 'active' : ''}" data-portal="adulto_mayor">
                            <h4>👵 ${t.adulto_mayor}</h4> <span>⚡</span>
                        </div>
                        <div class="portal-card-premium ${this.perfilSeleccionado === 'gubernamental' ? 'active' : ''}" data-portal="gubernamental">
                            <h4>💼 ${t.gubernamental}</h4> <span>⚡</span>
                        </div>
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
                        <h4>🎖️ ${t.veterano}</h4> <span>⚡</span>
                    </div>
                    
                    <div class="cortina-desplegable-premium">
                        <label style="display:block; color: var(--cyan-inhale, #00bcd4); font-weight:900; margin-bottom:15px; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px;">${t.lblKeywords}</label>
                        
                        <div id="box-keywords-flotantes" class="keywords-floating-box"></div>
                        
                        <div style="margin-top:25px; display:flex; gap:14px; justify-content:center; align-items:center;">
                            <button id="btn-mic-especial" class="pill-action-trigger" style="color:#fff; border-color:#333;">🎙️ ${t.btnMicGrabar}</button>
                            <label class="pill-action-trigger" style="margin:0;">
                                📂 Escanear PDF Estructural
                                <input type="file" id="file-pdf-especial" style="display:none;" accept=".pdf">
                            </label>
                        </div>
                        <input type="hidden" id="txt-input-especial" value="">
                    <div class="portal-card-premium ${this.perfilSeleccionado === 'adulto_mayor' ? 'active' : ''}" data-portal="adulto_mayor">
                        <h4>👵 ${t.adulto_mayor}</h4> <span>⚡</span>
                    </div>
                    <div class="portal-card-premium ${this.perfilSeleccionado === 'gubernamental' ? 'active' : ''}" data-portal="gubernamental">
                        <h4>💼 ${t.gubernamental}</h4> <span>⚡</span>
                    </div>
                </div>
                
                <div class="cortina-desplegable-premium">
                    <label style="display:block; color: var(--cyan-inhale, #00bcd4); font-weight:900; margin-bottom:15px; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px;">${t.lblKeywords}</label>
                    
                    <button id="btn-procesar-especial" class="action-btn-fatal-premium">${t.btnProcesar}</button>
                    <button id="btn-reporte-especial" style="width:100%; background:transparent; color:#333; border:none; margin-top:25px; cursor:pointer; font-weight:bold; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px; transition:color 0.2s;">${t.btnReporte}</button>
                    <!-- Inyección crítica del contenedor de palabras flotantes -->
                    <div id="box-keywords-flotantes" class="keywords-floating-box"></div>
                    
                    <div id="wrapper-reporte-output" class="hidden"></div>
                    <div style="margin-top:25px; display:flex; gap:14px; justify-content:center; align-items:center;">
                        <button id="btn-mic-especial" class="pill-action-trigger" style="color:#fff; border-color:#333;">🎙️ ${t.btnMicGrabar}</button>
                        <label class="pill-action-trigger" style="margin:0;">
                            📂 Escanear PDF Estructural
                            <input type="file" id="file-pdf-especial" style="display:none;" accept=".pdf">
                        </label>
                    </div>
                    <input type="hidden" id="txt-input-especial" value="">
                </div>
            `;
            
            this.enlazarEventosInterfaz();
            this.cargarKeywordsPerfil();
        },
                
                <button id="btn-procesar-especial" class="action-btn-fatal-premium">${t.btnProcesar}</button>
                <button id="btn-reporte-especial" style="width:100%; background:transparent; color:#333; border:none; margin-top:25px; cursor:pointer; font-weight:bold; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">${t.btnReporte}</button>
                
                <div id="wrapper-reporte-output" class="hidden"></div>
            </div>
        `;
        
        this.enlazarEventosInterfaz();
        this.cargarKeywordsPerfil();
    },

        enlazarEventosInterfaz() {
            const container = document.getElementById("panel-perfiles-especiales");
