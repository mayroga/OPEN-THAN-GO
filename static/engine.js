// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.3.2.0
// Company: May Roga LLC
// File: static/engine.js
// PARTE 1 DE 4: Inicialización, Sorpresa Inicial y Motor de Voz

const KERNEL = {
    timer: null,
    timeLeft: 600,
    isLocked: false,
    idiomaActual: 'es',
    pasosMisiones: [],
    indiceMision: 0,
    datosLugarGlobal: null,
    tipoEscapeGlobal: "",

    init() {
        const btnMando = document.getElementById('btn-mando') || document.getElementById('btn-main-trigger');
        if (btnMando) {
            btnMando.onclick = () => this.ejecutar();
        }
    },

    despertarInicial() {
        // La gran sorpresa: El usuario da un clic y la app le habla directo al oído con palabras simples
        document.getElementById('pantalla-bienvenida').style.display = 'none';
        document.getElementById('wrapper-form').classList.remove('hidden');
        this.hablar("Bienvenido a O P E N  T H A N  G O. Tu escape inteligente. Estamos listos para sacarte de la rutina diaria. Activa el mando para comenzar.");
    },

    hablar(texto) {
        if (!texto) return;
        // Corta de raíz audios viejos al cambiar de fase, evitando que se trabe la memoria del teléfono
        window.speechSynthesis.cancel(); 
        
        const textoLimpio = texto.replace(/<[^>]*>/g, '');
        const msg = new SpeechSynthesisUtterance(textoLimpio);
        msg.lang = this.idiomaActual === 'es' ? 'es-US' : 'en-US';
        msg.rate = 0.88; // Velocidad pausada y clara para guiar los sentidos
        msg.pitch = 1.0;
        window.speechSynthesis.speak(msg);
    },
    
// PARTE 2 DE 4: Captura de Datos, Conexión Rápida y Memoria Local Global

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;

        const payload = {
            zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
            mente: document.getElementById('inp-mente') ? document.getElementById('inp-mente').value : "aburrido",
            modo: document.getElementById('modo-selector') ? document.getElementById('modo-selector').value : "SALIR",
            budget: document.getElementById('inp-budget') ? document.getElementById('inp-budget').value : "0",
            perfil: document.getElementById('inp-perfil') ? document.getElementById('inp-perfil').value : "solo",
            desahogo: document.getElementById('inp-text') ? document.getElementById('inp-text').value.trim() : "",
            estado: document.getElementById('inp-state') ? document.getElementById('inp-state').value : "FL"
        };

        const container = document.getElementById('wrapper-interactive');
        document.getElementById('wrapper-form').classList.add('hidden');
        container.innerHTML = `<div style='text-align:center; padding:40px 0;'><h2 style='color:#fff;'>Sincronizando frecuencias de bienestar...</h2></div>`;
        container.classList.remove('hidden');

        try {
            const respuesta = await fetch("/api/mando-integral", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await respuesta.json();
            
            this.datosLugarGlobal = data.lugar || null;
            this.tipoEscapeGlobal = data.modo || data.tipo;
            this.indiceMision = 0;

            if (this.tipoEscapeGlobal === "CASA") {
                // ALGORITMO INTEGRAL ANTI-REPETICIÓN A COSTO CERO PARA MILLONES
                // El teléfono del cliente recuerda individualmente qué misiones completó
                let completadas = JSON.parse(localStorage.getItem('otg_completadas_50')) || [];
                
                // Filtramos del catálogo de 50 misiones cuáles quedan libres
                let disponibles = data.misiones.filter(m => !completadas.includes(m.id));
                
                // TOPE FINAL LOGRADO: Si completó las 50 misiones, el historial se limpia solo y empieza de nuevo
                if (disponibles.length < 3) {
                    completadas = [];
                    localStorage.setItem('otg_completadas_50', JSON.stringify([]));
                    disponibles = data.misiones;
                }
                
                // Selecciona las próximas 3 misiones fijas secuenciales sin repetir
                this.pasosMisiones = disponibles.slice(0, 3);
                
                // Guarda de inmediato los IDs en el hardware del cliente para bloquear repeticiones en el próximo reingreso
                this.pasosMisiones.forEach(m => completadas.push(m.id));
                localStorage.setItem('otg_completadas_50', JSON.stringify(completadas));
            } else {
                this.pasosMisiones = data.misiones || [];
            }

            this.procesarFlujoSecuencial(container);
        } catch (error) {
            alert("Error de enlace satelital con el servidor.");
            document.getElementById('wrapper-form').classList.remove('hidden');
            container.classList.add('hidden');
            this.isLocked = false;
        }
    },

    procesarRespuesta(res) {
        this.isLocked = false;
    },
    
// PARTE 3 DE 4: Procesador Secuencial y Reloj de Retención de 35 Segundos

    procesarFlujoSecuencial(container) {
        clearInterval(this.timer);
        const traducciones = {
            es: { inspira: "Inhala / Inspira", expira: "Exhala / Expira", txt_correcto: "<strong>¡RESPUESTA VERDADERA!</strong><br>", txt_incorrecto: "<strong>ANÁLISIS DE FALLO:</strong><br>", alerta_35s: "Preparación de campo activa por 35 segundos. Escucha atentamente antes de abrir la ruta.", fin_casa: "Protocolo completado. Borrando rastro de sesión." },
            en: { inspira: "Inhale", expira: "Exhale", txt_correcto: "<strong>TRUE ANSWER!</strong><br>", txt_incorrecto: "<strong>FAILURE ANALYSIS:</strong><br>", alerta_35s: "Field preparation active for 35 seconds. Listen carefully before opening route.", fin_casa: "Protocol completed. Clearing session tracks." }
        };
        const traduccion = traducciones[this.idiomaActual];

        // REGLA DE CIERRE: Al completar los 3 pasos asignados del catálogo
        if (this.indiceMision >= this.pasosMisiones.length) {
            if (this.tipoEscapeGlobal === "SALIR" && this.datosLugarGlobal) {
                container.innerHTML = `
                    <div class="mision-card" style="border: 1px solid #333; padding: 20px; text-align: center; background: #0a0a0a; border-radius: 12px;">
                        <h2 style="color:#d84315; font-weight:900;">${this.datosLugarGlobal.name}</h2>
                        <p style="font-size:13px; color:#aaa; margin:5px 0;">${this.datosLugarGlobal.address}</p>
                        <hr style="border:0; border-top:1px dashed #333; margin:15px 0;">
                        <p style="text-align:left; font-size:14px; line-height:1.45; background:#111; padding:12px; border-radius:6px; border-left:4px solid #2e7d32; color:#fff;">
                            <strong>GUÍA ABSOLUTA DE ACCIÓN:</strong><br>${this.datosLugarGlobal.analisis_sugerido}
                        </p>
                        <button id="btn-countdown-salida" style="width:100%; background:#222; color:#aaa; padding:16px; font-weight:bold; margin-top:15px;" disabled>35s ANCLAJE SOMÁTICO</button>
                        <button id="btn-gps-action" class="hidden" style="width:100%; background:#4285f4; color:#fff; padding:16px; font-weight:bold; margin-top:15px;">ABRIR ENLACE DE MAPA</button>
                    </div>`;

                this.hablar(this.datosLugarGlobal.name + " . Escucha las indicaciones de campo: " + this.datosLugarGlobal.analisis_sugerido);

                let retencion = 35;
                const btnCount = document.getElementById('btn-countdown-salida');
                const btnGps = document.getElementById('btn-gps-action');

                let relojSalida = setInterval(() => {
                    retencion--;
                    if (btnCount) btnCount.innerText = `${retencion}s PREPARACIÓN DE ENTORNO`;
                    if (retencion <= 0) {
                        clearInterval(relojSalida);
                        if (btnCount) btnCount.style.display = 'none';
                        if (btnGps) {
                            btnGps.classList.remove('hidden');
                            // Clic voluntario inmune al bloqueo de Pop-Ups
                            btnGps.onclick = () => { window.open(this.datosLugarGlobal.gps, '_blank'); };
                        }
                    }
                }, 1000);
            } else {
                this.iniciarRelojClinicoCasa(container, traduccion);
            }
            return;
        }

        const paso = this.pasosMisiones[this.indiceMision];

        // Renderizado e inyección limpia de la misión en el lienzo interactivo
        let textoTitulo = paso.titulo;
        let textoDetalle = paso.descripcion;

        container.innerHTML = `
            <div class="mision-card" style="background:#0a0a0a; border:1px solid #333; padding:25px; border-radius:12px;">
                <h3 style="color:#2e7d32; font-size:1.3rem; font-weight:800; text-transform:uppercase; margin-top:0;">${textoTitulo}</h3>
                <p style="font-size:1.1rem; line-height:1.5; color:#ccc; margin:20px 0;">${textoDetalle}</p>
                <button id="btn-next" style="width:100%; background:#2e7d32; color:#fff; padding:15px; font-weight:bold; text-transform:uppercase; border-radius:6px; cursor:pointer;">CONTINUAR</button>
            </div>`;
        
        this.hablar(textoTitulo + " . " + textoDetalle);
        document.getElementById('btn-next').onclick = () => this.avanzarPaso();
    },
    
// PARTE 4 DE 4: Reloj Clínico de Casa, Sincronización Pulmonar y Autodestrucción de Rastro

    iniciarRelojClinicoCasa(container, traduccion) {
        this.hablar("Fase educativa completada. Iniciando reloj clínico de diez minutos. Sincroniza tu respiración con el pulmón.");
        container.innerHTML = `
            <div id="breath-circle"></div>
            <div id="timer" style="font-weight:900; text-align:center; font-size:2.8rem; margin:15px 0;">10:00</div>
            <p id="txt-pulmon" style="font-size:14px; text-transform:uppercase; font-weight:bold; color:#00bcd4; text-align:center; letter-spacing:2px;">INHALA / INSPIRA</p>
        `;
        this.timeLeft = 600;
        this.timer = setInterval(() => {
            this.timeLeft--;
            let m = Math.floor(this.timeLeft / 60);
            let s = this.timeLeft % 60;
            const timerDiv = document.getElementById('timer');
            const pulmonDiv = document.getElementById('txt-pulmon');
            if (timerDiv) timerDiv.innerText = `${m}:${s.toString().padStart(2, '0')}`;
            
            // Control visual del pulmón en pantalla (In/Out) sin invocar SpeechSynthesis interno que corte el audio anterior
            if (pulmonDiv) {
                let ciclo = this.timeLeft % 8;
                if (ciclo >= 4) { 
                    pulmonDiv.innerText = traduccion.inspira; 
                    pulmonDiv.style.color = "#00bcd4"; 
                } else { 
                    pulmonDiv.innerText = traduccion.expira; 
                    pulmonDiv.style.color = "#d84315"; 
                }
            }
            if (this.timeLeft <= 0) {
                clearInterval(this.timer);
                this.hablar(traduccion.fin_casa);
                alert(traduccion.fin_casa);
                this.destruirYReiniciar();
            }
        }, 1000);
    },

    avanzarPaso() {
        this.indiceMision++;
        const container = document.getElementById('wrapper-interactive');
        this.procesarFlujoSecuencial(container);
    },

    destruirYReiniciar() {
        // Borrado definitivo de variables y rastros para evitar acumulaciones que traben el teléfono
        clearInterval(this.timer);
        window.speechSynthesis.cancel();
        this.pasosMisiones = [];
        this.indiceMision = 0;
        this.isLocked = false;
        location.reload(); // Borra la caché visual del navegador de forma instantánea
    }
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());
