// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.3.3.0
// Company: May Roga LLC
// File: static/engine.js
// PARTE 1 DE 4: Inicialización, Sorpresa Inicial y Motor de Voz Activo

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
        // La sorpresa desde el clic cero en la URL usando palabras cortas de acción y acompañamiento directo
        document.getElementById('pantalla-bienvenida').style.display = 'none';
        document.getElementById('wrapper-form').classList.remove('hidden');
        this.hablar("O P E N  T H A N  G O. Estoy contigo ahora. Escucha mi voz. No mires los colores de la pantalla. No pienses en tus biles. Pon tus datos en el mando en este instante y hazlo conmigo. Vamos a romper tu piloto automático ya.");
    },

    hablar(texto) {
        if (!texto) return;
        // Corta rastros de voz previos únicamente al avanzar de fase secuencial, jamás por segundo
        window.speechSynthesis.cancel(); 
        
        const textoLimpio = texto.replace(/<[^>]*>/g, '');
        const msg = new SpeechSynthesisUtterance(textoLimpio);
        msg.lang = 'es-US';
        msg.rate = 0.88; // Ritmo pausado y firme de guía absoluta
        msg.pitch = 1.0;
        window.speechSynthesis.speak(msg);
    },
  
// PARTE 2 DE 4: Captura de Datos, Conexión Rápida y Memoria Local Global de 50 Misiones

    async ejecutar() {
        if (this.isLocked) return;
        this.isLocked = true;

        const payload = {
            zip: document.getElementById('inp-zip') ? document.getElementById('inp-zip').value.trim() : "",
            mente: document.getElementById('inp-mente') ? document.getElementById('inp-mente').value : "agotado",
            modo: document.getElementById('modo-selector') ? document.getElementById('modo-selector').value : "SALIR",
            budget: document.getElementById('inp-budget') ? document.getElementById('inp-budget').value : "0",
            perfil: document.getElementById('inp-perfil') ? document.getElementById('inp-perfil').value : "solo",
            desahogo: document.getElementById('inp-text') ? document.getElementById('inp-text').value.trim() : "",
            estado: document.getElementById('inp-state') ? document.getElementById('inp-state').value : "FL"
        };

        const container = document.getElementById('wrapper-interactive');
        document.getElementById('wrapper-form').classList.add('hidden');
        container.innerHTML = `<div style='text-align:center; padding:40px 0;'><h2 style='color:#fff; font-size:1.1rem; letter-spacing:1px;'>CONECTANDO CON TU ENTORNO REAL...</h2></div>`;
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
                // Algoritmo distribuido en el hardware del cliente para rotación de las 50 misiones directas
                let completadas = JSON.parse(localStorage.getItem('otg_completadas_50')) || [];
                let disponibles = data.misiones.filter(m => !completadas.includes(m.id));
                
                // Tope final alcanzado: Resetea el ciclo de reingreso diario automáticamente
                if (disponibles.length < 3) {
                    completadas = [];
                    localStorage.setItem('otg_completadas_50', JSON.stringify([]));
                    disponibles = data.misiones;
                }
                
                // Extrae un bloque continuo de 3 pasos para la sesión de hoy
                this.pasosMisiones = disponibles.slice(0, 3);
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
  
// PARTE 3 DE 4: Sesiones de Salida, Retención Somática Obligatoria de 35 segundos e Inyección de Destino

    procesarFlujoSecuencial(container) {
        clearInterval(this.timer);
        const traducciones = {
            es: { inspira: "Inhala / Inspira ahora", expira: "Exhala / Expira ahora", fin_casa: "Protocolo de diez minutos completado. Borrando rastro de sesión por tu paz mental." },
            en: { inspira: "Inhale now", expira: "Exhale now", fin_casa: "Protocol completed. Clearing tracks for your mental peace." }
        };
        const traduccion = traducciones[this.idiomaActual];

        if (this.indiceMision >= this.pasosMisiones.length) {
            if (this.tipoEscapeGlobal === "SALIR" && this.datosLugarGlobal) {
                container.innerHTML = `
                    <div class="mision-card" style="border: 1px solid #333; padding: 20px; text-align: center; background: #0a0a0a; border-radius: 12px;">
                        <h2 style="color:#d84315; font-weight:900; font-size:1.3rem;">${this.datosLugarGlobal.name}</h2>
                        <p style="font-size:13px; color:#aaa; margin:5px 0;">${this.datosLugarGlobal.address}</p>
                        <hr style="border:0; border-top:1px dashed #333; margin:15px 0;">
                        <p style="text-align:left; font-size:14px; line-height:1.45; background:#111; padding:12px; border-radius:6px; border-left:4px solid #2e7d32; color:#fff;">
                            <strong>GUÍA ABSOLUTA DE ACCIÓN:</strong><br>${this.datosLugarGlobal.analisis_sugerido}
                        </p>
                        <button id="btn-countdown-salida" style="width:100%; background:#222; color:#aaa; padding:16px; font-weight:bold; margin-top:15px;" disabled>35s ESCUCHA MI GUÍA</button>
                        <button id="btn-gps-action" class="hidden" style="width:100%; background:#4285f4; color:#fff; padding:16px; font-weight:bold; margin-top:15px;">ABRIR GOOGLE MAPS YA</button>
                    </div>`;

                // La voz te lo exige: Te lee el qué, cómo, cuándo, dónde y para qué de forma directa
                this.hablar("He tomado la decisión por ti. Tu destino es " + this.datosLugarGlobal.name + " . Escucha las indicaciones de acción obligatorias antes de marcharte: " + this.datosLugarGlobal.analisis_sugerido);

                let retencion = 35;
                const btnCount = document.getElementById('btn-countdown-salida');
                const btnGps = document.getElementById('btn-gps-action');

                let relojSalida = setInterval(() => {
                    retencion--;
                    if (btnCount) btnCount.innerText = `${retencion}s ESCUCHA MI GUÍA`;
                    if (retencion <= 0) {
                        clearInterval(relojSalida);
                        if (btnCount) btnCount.style.display = 'none';
                        if (btnGps) {
                            btnGps.classList.remove('hidden');
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
        let textoSesion = paso.sesion ? `<small style="color:#666; font-weight:bold; display:block; margin-bottom:5px;">${paso.sesion.toUpperCase()}</small>` : "";
        let textoParaQue = paso.para_que ? `<p style="font-size:12px; color:#00bcd4; font-weight:bold; margin-top:10px; text-transform:uppercase;">¿PARA QUÉ?: ${paso.para_que}</p>` : "";

        container.innerHTML = `
            <div class="mision-card" style="background:#0a0a0a; border:1px solid #333; padding:25px; border-radius:12px;">
                ${textoSesion}
                <h3 style="color:#2e7d32; font-size:1.25rem; font-weight:800; text-transform:uppercase; margin-top:0;">${paso.titulo}</h3>
                <p style="font-size:1.1rem; line-height:1.55; color:#eee; margin:15px 0; text-align:left; border-left:3px solid #2e7d32; padding-left:12px;">${paso.descripcion}</p>
                ${textoParaQue}
                <button id="btn-next" style="width:100%; background:#2e7d32; color:#fff; padding:15px; font-weight:bold; text-transform:uppercase; border-radius:6px; cursor:pointer; margin-top:15px;">HAZLO CONMIGO AHORA</button>
            </div>`;
        
        // El acompañamiento hablado incluye el propósito exacto en tiempo real
        this.hablar(paso.titulo + " . " + paso.descripcion + " . ¿Para qué lo haces?: " + (paso.para_que || "Para tomar el control."));
        document.getElementById('btn-next').onclick = () => this.avanzarPaso();
    },
   
// PARTE 4 DE 4: Reloj Clínico por Sesiones en Casa, Sincronización Pulmonar y Borrado Físico de Caché

    iniciarRelojClinicoCasa(container, traduccion) {
        // Explicación de los tiempos médicos: Por qué, para qué y cómo se va a lograr la limpieza mental
        this.hablar("Fase de entrenamiento terminada. Iniciamos la sesión de limpieza mental profunda de diez minutos. ¿Para qué lo hacemos?: Para bajar tus niveles de ansiedad de golpe y sacar a tu cerebro del bucle cotidiano. Hazlo conmigo ahora. Sincroniza tus costillas con el círculo azul en este instante. Inhala cuando crezca, exhala cuando se encoja. El conteo regresivo ha comenzado.");
        
        container.innerHTML = `
            <div id="breath-circle"></div>
            <div id="timer" style="font-weight:900; text-align:center; font-size:2.8rem; margin:15px 0;">10:00</div>
            <p id="txt-pulmon" style="font-size:13px; text-transform:uppercase; font-weight:bold; color:#00bcd4; text-align:center; letter-spacing:2px;">INHALA / INSPIRA AHORA</p>
            <p style="font-size:12px; color:#555; text-align:center; line-height:1.4; max-width:85%; margin:10px auto 0 auto;">TE ESTOY ACOMPAÑANDO. QUÉDATE EN LA SALA. NO ABRAZAS LAS PANTALLAS. EL MUNDO ESTÁ AFUERA.</p>
        `;
        
        this.timeLeft = 600;
        this.timer = setInterval(() => {
            this.timeLeft--;
            let m = Math.floor(this.timeLeft / 60);
            let s = this.timeLeft % 60;
            const timerDiv = document.getElementById('timer');
            const pulmonDiv = document.getElementById('txt-pulmon');
            
            if (timerDiv) timerDiv.innerText = `${m}:${s.toString().padStart(2, '0')}`;
            
            // Sincronización pulmonar puramente gráfica para móviles sin comandos Speech internos que pisoteen la voz anterior
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
            
            // Explicaciones dinámicas intercaladas de apoyo durante los 10 minutos fijos
            if (this.timeLeft === 450) this.hablar("Has completado la primera sesión de tres minutos. Tu pulso está bajando. Quédate conmigo ahora. Respira.");
            if (this.timeLeft === 300) this.hablar("Segunda sesión en marcha. Siente el peso fuera de tus hombros. Lo estás haciendo bien. Continúa.");
            if (this.timeLeft === 150) this.hablar("Última fase de estabilización. Tu mente ha despertado de la rutina gris. Sigue el pulso azul.");

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
        clearInterval(this.timer);
        window.speechSynthesis.cancel();
        this.pasosMisiones = [];
        this.indiceMision = 0;
        this.isLocked = false;
        location.reload(); // Borrado instantáneo de rastro en el hardware
    }
};

document.addEventListener('DOMContentLoaded', () => KERNEL.init());
