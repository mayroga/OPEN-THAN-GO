// OPEN THAN GO SYSTEM - Kernel Somatic Voice Engine V.4.0.0
// Company: May Roga LLC
// File: static/engine.js
// PARTE 1 Y 2 DE 4: Inicialización, Saludo de Choque Dopamínico, Motor de Voz y Localización Global
const KERNEL = {
    timer: null,
    timeLeft: 600,
    isLocked: false,
    idiomaActual: 'es',
    pasosMisiones: [],
    indiceMision: 0,
    datosLugarGlobal: null,
    tipoEscapeGlobal: "",
    stagnationFactor: 0.5, // Capturado por el backend de las Big Tech
    init() {
        const btnMando = document.getElementById('btn-mando') || document.getElementById('btn-main-trigger');
        if (btnMando) {
            btnMando.onclick = () => this.ejecutar();
        }        
        // Inicializa el disparador del botón de la pantalla negra de Render de forma manual si es necesario
        const triggerBienvenida = document.getElementById('init-trigger');
        if (triggerBienvenida) {
            triggerBienvenida.onclick = () => {
                this.despertarInicial();
            };
        }
    },
    despertarInicial() {
        // Quita la pantalla negra de golpe y revela el mando de control en Render
        const pantalla = document.getElementById('pantalla-bienvenida');
        const wrapper = document.getElementById('wrapper-form');
        if (pantalla) pantalla.style.display = 'none';
        if (wrapper) wrapper.classList.remove('hidden');
        // Catálogo de 10 entradas de choque dopamínico con palabras directas de acompañamiento
        const saludosSorpresa = [
            "Bienvenido a ópen dán go. Tu escape inteligente. Estoy contigo ahora. Pon tus datos en el mando y hazlo conmigo ya.",
            "ópen dán go está activo en este segundo. Olvida tus biles por un momento. Escucha mi voz. Activa el mando ahora mismo.",
            "Entraste a ópen dán go. El despertador está encendido. Vamos a sacarte de la rutina gris en este instante. Hazlo conmigo.",
            "ópen dán go tomó el control. Deja de dar vueltas en círculos. Mira el mando. Pon tu zona y comencemos ya.",
            "Ya estás dentro de ópen dán go. No mires los colores de la pantalla. Siente tu respiración. Activa el mando ahora.",
            "ópen dán go te saluda hoy. El sistema te quiere dormido, pero yo te voy a despertar. Usa el mando en este segundo.",
            "Frecuencias alineadas en ópen dán go. Estoy al lado tuyo ahora. Rompamos el piloto automático juntos. Activa el mando ya.",
            "ópen dán go inició ahora. La vida está afuera, no en tus preocupaciones. Pon tus datos en la pantalla en este instante.",
            "Bienvenido al despierto de ópen dán go. Una acción corta puede cambiar tu día entero hoy. Haz clic en activar ya.",
            "Mando listo en ópen dán go. Tu mente necesita un escape real ahora mismo. No lo pienses más. Pon tu zona y camina conmigo."
        ];
        // Algoritmo de selección aleatoria instantánea
        const saludoElegido = saludosSorpresa[Math.floor(Math.random() * saludosSorpresa.length)];       
        // Ejecuta el secuestro del altavoz del smartphone de inmediato
        this.hablar(saludoElegido);
    },
    hablar(texto) {
        if (!texto) return;
        window.speechSynthesis.cancel();
        // HACK DE MARCA NATIVO: Corrige la fonética para obligar al teléfono a pronunciar fluido
        let textoCorregido = texto.replace(/OPEN THAN GO/gi, "OPEN DAN GO");
        textoCorregido = textoCorregido.replace(/<[^>]*>/g, '');
        const msg = new SpeechSynthesisUtterance(textoCorregido);
        msg.lang = 'es-US';
        msg.rate = 1.15;  // Velocidad táctica y despierta para evitar la desconexión del usuario
        msg.pitch = 1.0;  // Tono firme y clínico
        window.speechSynthesis.speak(msg);
    },
    // PARTE 2: Conmutador de Localización de Idioma e Interceptación de Variables de Entrada
    cambiarIdioma(lang) {
        this.idiomaActual = lang;     
        const btnEs = document.getElementById('lang-es');
        const btnEn = document.getElementById('lang-en');
        if (btnEs) btnEs.classList.toggle('active', lang === 'es');
        if (btnEn) btnEn.classList.toggle('active', lang === 'en');
        const contenidos = {
            es: {
                title: "OPEN THAN GO",
                zip: "Código Postal",
                mode: "Modo de Operación",
                mente: "Estado Mental",
                budget: "Presupuesto",
                perfil: "Perfil",
                desahogo: "Desahogo",
                placeholder: "Escribe tu estado actual... (deudas, monotonía, biles, etc.)",
                btn: "ACTIVAR MANDO"
            },
            en: {
                title: "OPEN THAN GO",
                zip: "ZIP Code",
                mode: "Operation Mode",
                mente: "Mental State",
                budget: "Budget Available",
                perfil: "Profile",
                desahogo: "Venting Layer",
                placeholder: "Write freely about how you feel today... (debts, bills, stress)",
                btn: "ACTIVATE CONTROL"
            }
        };
        const traduccion = contenidos[lang];       
        // Inyección directa en los elementos del DOM de tu URL de Render
        if (document.getElementById('txt-app-title')) document.getElementById('txt-app-title').innerText = traduccion.title;
        if (document.getElementById('lbl-zip')) document.getElementById('lbl-zip').innerText = traduccion.zip;
        if (document.getElementById('lbl-mode')) document.getElementById('lbl-mode').innerText = traduccion.mode;
        if (document.getElementById('lbl-mente')) document.getElementById('lbl-mente').innerText = traduccion.mente;
        if (document.getElementById('lbl-budget')) document.getElementById('lbl-budget').innerText = traduccion.budget;
        if (document.getElementById('lbl-perfil')) document.getElementById('lbl-perfil').innerText = traduccion.perfil;
        if (document.getElementById('lbl-desahogo')) document.getElementById('lbl-desahogo').innerText = traduccion.desahogo;
        if (document.getElementById('inp-text')) document.getElementById('inp-text').placeholder = traduccion.placeholder;
        if (document.getElementById('btn-mando')) document.getElementById('btn-mando').innerText = traduccion.btn;
    }
};
// Autoejecución del listener global al cargar el script en el navegador
window.onload = () => { KERNEL.init(); };
// ======================================================
// MODO SALIR (ACCION_CAMPO)
// Algoritmo Predictivo Big Tech Desplegado
// ======================================================
if (this.tipoEscapeGlobal === "ACCION_CAMPO") {
    if (this.datosLugarGlobal) {
        if (statusText) {
            statusText.innerText = "ESCUCHA MI GUÍA DE ACCIÓN DIRECTA";
        }
        let textoMostrar =
            this.datosLugarGlobal.destino_instruccion.replace(/\n/g, "");
        if (instructionBox) {
            instructionBox.innerHTML = `
                <h3 style="color:#d84315; margin:0 0 10px 0; text-transform:uppercase;">
                    ${this.datosLugarGlobal.destino_titulo}
                </h3>
                <strong>ENTORNO:</strong>
                ${this.datosLugarGlobal.destino_entorno}
                <br><br>
                ${textoMostrar}
            `;
            instructionBox.classList.remove("hidden");
        }
        this.hablar(
            "Veredicto listo. " +
            this.datosLugarGlobal.destino_instruccion
        );
        let retencion = 35;
        if (lungBox) {
            lungBox.innerText = retencion;
        }
        if (blueButton) {
            blueButton.style.display = "block";
            blueButton.disabled = true;
            blueButton.style.background = "#222";
            blueButton.style.color = "#aaa";
            blueButton.innerText =
                `${retencion}S RETENCIÓN DE ENFOQUE`;
        }
        this.timer = setInterval(() => {
            retencion--;
            if (lungBox) {
                lungBox.innerText = retencion;
            }
            if (blueButton) {
                blueButton.innerText =
                    `${retencion}S RETENCIÓN DE ENFOQUE`;
            }
            if (retencion <= 0) {
                clearInterval(this.timer);
                if (lungBox) {
                    lungBox.innerText = "GO";
                }
                if (blueButton) {
                    blueButton.disabled = false;
                    blueButton.style.background =
                        "var(--secondary)";
                    blueButton.style.color = "#fff";
                    blueButton.innerText =
                        "ABRIR GOOGLE MAPS YA";
                    blueButton.onclick = () => {
                        window.open(
                            this.datosLugarGlobal
                                .destino_coordenadas_gps,
                            "_blank"
                        );
                        this.destruirYReiniciar();
                    };
                }
            }

        }, 1000);

        return;
    }
}
// ======================================================
// MODO CASA - FLUJO SECUENCIAL DE MISIONES INTERNAS
// ======================================================
if (this.indiceMision >= this.pasosMisiones.length) {
    this.iniciarRelojClinicoCasa(
        container,
        traduccion
    );
    return;
}
if (statusText) {
    statusText.innerText =
        "MISION INTERNA EN PROGRESO";
}
const paso =
    this.pasosMisiones[this.indiceMision];
if (instructionBox) {
    instructionBox.innerHTML = `
        <h3 style="
            color:var(--accent);
            margin:0 0 10px 0;
            text-transform:uppercase;
        ">
            ${paso.titulo}
        </h3>

        ${paso.descripcion}
    `;
    instructionBox.classList.remove("hidden");
}
if (lungBox) {
    lungBox.innerText = "!";
}
if (blueButton) {
    blueButton.style.display = "block";
    blueButton.disabled = false;
    blueButton.style.background =
        "var(--accent)";
    blueButton.style.color = "#fff";
    blueButton.innerText =
        "HAZLO CONMIGO AHORA";
    blueButton.onclick = () =>
        this.avanzarPaso();
}
this.hablar(
    paso.titulo + ". " +
    paso.descripcion
);
// ======================================================
// RELOJ CLÍNICO CASA
// ======================================================
},
iniciarRelojClinicoCasa(
    container,
    traduccion
) {
    this.hablar(
        "Fase de misiones terminada. " +
        "Iniciamos la sesión de limpieza " +
        "mental profunda de diez minutos. " +
        "Hazlo conmigo ahora. " +
        "Sincroniza tu respiración."
    );
    const statusText =
        document.getElementById(
            "retention-status"
        );
    const lungBox =
        document.getElementById(
            "pulmon-visual"
        );
    const instructionBox =
        document.getElementById(
            "texto-instruccion"
        );
    const blueButton =
        document.getElementById(
            "action-blue-button"
        );
    if (statusText) {
        statusText.innerText =
            "RECONFIGURACIÓN PULMONAR PROFUNDA (10 MIN)";
    }
    if (blueButton) {
        blueButton.style.display = "none";
    }
    if (instructionBox) {
        instructionBox.innerHTML =
            "Cierra los ojos si es necesario. " +
            "Permite que el audio de asistencia " +
            "estabilice tu ritmo cerebral. " +
            "Libera el control.";

        instructionBox.classList.remove(
            "hidden"
        );
    }
    this.timeLeft = 600;
    this.timer = setInterval(() => {
        this.timeLeft--;
        let m =
            Math.floor(this.timeLeft / 60);
        let s =
            this.timeLeft % 60;
        if (lungBox) {
            lungBox.innerText =
                `${m}:${s
                    .toString()
                    .padStart(2, "0")}`;
        }
        if (statusText) {
            let ciclo =
                this.timeLeft % 8;
            if (ciclo >= 4) {
                statusText.innerText =
                    traduccion.inspira.toUpperCase();
                statusText.style.color =
                    "#00bcd4";
            } else {
                statusText.innerText =
                    traduccion.expira.toUpperCase();
                statusText.style.color =
                    "#d84315";
            }
        }
        if (
            this.timeLeft > 0 &&
            this.timeLeft % 20 === 0
        ) {
            let recordatorios = [
                "Sigue el pulso azul ahora. Estás conmigo.",
                "No mires tus biles. Respira ya.",
                "Mantén el ritmo ahora. Estás ganando control.",
                "Siente el peso fuera de tus hombros en este segundo.",
                "Te estoy acompañando. No estás solo. Hazlo conmigo.",
                "Siente el aire limpiando tu pecho ahora mismo.",
                "El piloto automático está apagado. Continúa.",
                "Quédate en este instante. El presente es tuyo.",
                "Siente tus pies firmes. El suelo te sostiene gratis.",
                "Suelta la mandíbula ahora. Libera esa carga ya.",
                "Tu mente está despertando en este segundo. Sigue así.",
                "Eres más grande que tus deudas. Respira hondo.",
                "Rompe el zombi que llevas dentro en este instante.",
                "Escucha mi voz. Quédate en la sala conmigo ahora."
            ];
            KERNEL.hablar(
                recordatorios[
                    Math.floor(
                        Math.random() *
                        recordatorios.length
                    )
                ]
            );
        }
        if (this.timeLeft <= 0) {
            clearInterval(this.timer);
            this.hablar(
                traduccion.fin_casa
            );
            alert(
                traduccion.fin_casa
            );
            this.destruirYReiniciar();
        }
    }, 1000);
},
// ======================================================
// AVANZAR MISIÓN
// ======================================================
avanzarPaso() {
    this.indiceMision++;
    const container =
        document.getElementById(
            "wrapper-interactive"
        );
    this.procesarFlujoSecuencial(
        container
    );
},
// ======================================================
// REINICIO TOTAL DEL SISTEMA
// ======================================================
destruirYReiniciar() {
    clearInterval(this.timer);
    window.speechSynthesis.cancel();
    this.pasosMisiones = [];
    this.indiceMision = 0;
    this.isLocked = false;
    // Purga total de memoria local
    localStorage.clear();
    sessionStorage.clear();
    location.reload();
}
