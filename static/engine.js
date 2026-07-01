let configuracion = {
    idioma: 'es',
    puedes_salir: true,
    bolsillo: 'cero',
    modo: null, // HOME / OUTSIDE
};

let comandosMision = [];
let indiceActual = 0;
let intervaloRespiracion = null;
let cuentaRegresiva = null;

/* =========================
   TEXTO UI
========================= */
const textos = {
    es: {
        subtitle: "Tu botón de escape inmediato para romper la monotonía urbana.",
        lblState: "Estado / State:",
        lblZip: "ZIP Code (5 dígitos):",
        lblPocket: "¿Cuál es tu presupuesto real para hoy?",
        pocketCero: "GASTO $0 HOY",
        pocketMod: "MODERADO",
        pocketLibre: "LIBRE",
        lblMode: "¿Puedes o quieres salir de casa hoy?",
        btnOut: "🟢 SÍ, SALIR",
        btnIn: "🏠 EN CASA",
        lblText: "Desahógate aquí:",
        placeholder: "Escribe cómo te sientes...",
        btnSubmit: "SÁCAME DE LA MONOTONÍA",
        alertZip: "ZIP inválido",
        alertError: "Error de conexión",
        btnMaps: "🗺️ ABRIR MAPA"
    },
    en: {
        subtitle: "Your instant escape from urban monotony.",
        lblState: "State:",
        lblZip: "ZIP (5 digits):",
        lblPocket: "Budget today:",
        pocketCero: "$0",
        pocketMod: "Moderate",
        pocketLibre: "Free",
        lblMode: "Can you leave home today?",
        btnOut: "YES, GO OUT",
        btnIn: "STAY HOME",
        lblText: "Vent here:",
        placeholder: "Write how you feel...",
        btnSubmit: "BREAK MONOTONY",
        alertZip: "Invalid ZIP",
        alertError: "Connection error",
        btnMaps: "OPEN MAP"
    }
};

/* =========================
   IDIOMA
========================= */
function cambiarIdioma(lang) {
    configuracion.idioma = lang;

    const t = textos[lang];

    document.getElementById('txt-subtitle').innerText = t.subtitle;
    document.getElementById('lbl-state').innerText = t.lblState;
    document.getElementById('lbl-zip').innerText = t.lblZip;
    document.getElementById('lbl-pocket').innerText = t.lblPocket;

    document.getElementById('pocket-cero').innerText = t.pocketCero;
    document.getElementById('pocket-mod').innerText = t.pocketMod;
    document.getElementById('pocket-libre').innerText = t.pocketLibre;

    document.getElementById('lbl-mode').innerText = t.lblMode;
    document.getElementById('mode-out').innerText = t.btnOut;
    document.getElementById('mode-in').innerText = t.btnIn;

    document.getElementById('lbl-text').innerText = t.lblText;
    document.getElementById('inp-text').placeholder = t.placeholder;
    document.getElementById('btn-submit').innerText = t.btnSubmit;
}

/* =========================
   BOLSILLO
========================= */
function cambiarBolsillo(tipo) {
    configuracion.bolsillo = tipo;

    document.querySelectorAll('.pocket').forEach(b => b.classList.remove('active'));
    document.getElementById(`pocket-${tipo}`).classList.add('active');
}

/* =========================
   MODO CASA / EXTERIOR
========================= */
function cambiarModalidad(salir) {
    configuracion.puedes_salir = salir;

    document.getElementById('mode-out').classList.toggle('active', salir);
    document.getElementById('mode-in').classList.toggle('active', !salir);

    const zip = document.getElementById('inp-zip');

    zip.disabled = !salir;
    zip.style.opacity = salir ? "1" : "0.4";

    configuracion.modo = salir ? "OUTSIDE" : "HOME";
}

/* =========================
   VOZ (MASCULINA GUIADA)
========================= */
function speak(text) {
    if (!window.speechSynthesis) return;

    const msg = new SpeechSynthesisUtterance(text);
    msg.lang = configuracion.idioma === 'es' ? 'es-ES' : 'en-US';
    msg.rate = 0.95;
    msg.pitch = 0.7; // más masculino
    msg.volume = 1;

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(msg);
}

/* =========================
   ENVÍO AL BACKEND
========================= */
function solicitarEscape() {

    const estado = document.getElementById('inp-state').value;
    const zip = document.getElementById('inp-zip').value.trim();
    const texto = document.getElementById('inp-text').value.trim();

    const t = textos[configuracion.idioma];

    if (configuracion.puedes_salir && zip.length !== 5) {
        alert(t.alertZip);
        return;
    }

    const payload = {
        puedes_salir: configuracion.puedes_salir,
        idioma: configuracion.idioma,
        zip_code: zip,
        estado,
        bolsillo: configuracion.bolsillo,
        texto_libre: texto
    };

    fetch('/diagnostico-kamizen', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {

        document.getElementById('wrapper-form').style.display = 'none';
        document.getElementById('wrapper-interactive').style.display = 'block';

        document.getElementById('interactive-title').innerText = data.titulo;
        document.getElementById('interactive-location').innerText = data.lugar;

        comandosMision = data.bloques_interactivos || [];
        indiceActual = 0;

        // MAPA SOLO OUTSIDE
        const btnMaps = document.getElementById('btn-maps-action');
        if (data.modalidad === 'outdoor' && data.url_maps) {
            btnMaps.href = data.url_maps;
            btnMaps.style.display = 'block';
        } else {
            btnMaps.style.display = 'none';
        }

        procesarComando();

        // VOZ INICIAL
        speak(data.titulo);

    })
    .catch(() => alert(t.alertError));
}

/* =========================
   MOTOR DE EJECUCIÓN
========================= */
function procesarComando() {

    clearInterval(intervaloRespiracion);
    clearInterval(cuentaRegresiva);

    const box = document.getElementById('step-content');
    const next = document.getElementById('btn-next');

    box.innerHTML = "";
    next.style.display = "none";

    if (indiceActual >= comandosMision.length) {
        box.innerHTML = "✔ Misión completada";
        speak(configuracion.idioma === 'es' ? "Misión completada" : "Mission completed");
        return;
    }

    const c = comandosMision[indiceActual];

    /* =========================
       STORY / TEXTO SIMPLE
    ========================= */
    if (c.t === 'v' || c.t === 'h' || c.t === 'c' || c.story) {
        const txt = c.tx || c.story || c.c || "";

        box.innerHTML = `<div class="screen-story">${txt}</div>`;
        next.style.display = "block";

        speak(typeof txt === "string" ? txt : JSON.stringify(txt));
        return;
    }

    /* =========================
       BREATH MODE
    ========================= */
    if (c.t === 'breath_auto') {

        let sec = c.d;

        box.innerHTML = `
            <div class="screen-story">${c.tx}</div>
            <div class="breath-circle" id="circle">INHALA</div>
            <div>${sec}s</div>
        `;

        const circle = document.getElementById('circle');

        intervaloRespiracion = setInterval(() => {
            circle.innerText = (circle.innerText === "INHALA") ? "EXHALA" : "INHALA";
            speak(circle.innerText);
        }, 4000);

        cuentaRegresiva = setInterval(() => {
            sec--;
            if (sec <= 0) {
                clearInterval(intervaloRespiracion);
                clearInterval(cuentaRegresiva);
                next.style.display = "block";
                speak("listo");
            }
        }, 1000);

        return;
    }

    /* =========================
       SILENCE MODE
    ========================= */
    if (c.t === 'sil') {

        let sec = c.d;

        box.innerHTML = `<div>${c.tx}</div><div>${sec}s</div>`;

        cuentaRegresiva = setInterval(() => {
            sec--;
            if (sec <= 0) {
                clearInterval(cuentaRegresiva);
                next.style.display = "block";
                speak("continuamos");
            }
        }, 1000);

        return;
    }

    /* =========================
       DECISION MODE
    ========================= */
    if (c.t === 'd') {

        let html = "";

        c.op.forEach((op, i) => {
            html += `<button onclick="validar(${i},${c.c},'${c.ex[i]}')">${op}</button>`;
        });

        box.innerHTML = `<div>${c.q}</div>${html}<div id="exp"></div>`;
        return;
    }

    indiceActual++;
    procesarComando();
}

/* =========================
   RESPUESTA DECISIÓN
========================= */
function validar(i, correct, exp) {

    const buttons = document.querySelectorAll('button');
    buttons.forEach(b => b.disabled = true);

    document.getElementById('exp').innerText = exp;

    speak(exp);

    document.getElementById('btn-next').style.display = "block";
}

/* =========================
   NEXT
========================= */
function siguienteComando() {
    indiceActual++;
    procesarComando();
}
