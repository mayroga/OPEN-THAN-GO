(() => {
"use strict";

// ===============================
// SAFE LOOP ENGINE v6 (STABLE UI + REAL BREATH + NO FREEZE)
// SINGLE FLOW CONTROLLER
// ===============================

let state = {
    lang: "es",
    bloques: [],
    index: 0,
    used: new Set(),

    loopDuration: 600000,
    loopStart: 0,

    breathing: null,
    silence: null,

    speaking: false
};

// ===============================
// INIT
// ===============================
window.addEventListener("load", () => {
    window.speechSynthesis.onvoiceschanged = () => {};
});

// ===============================
// HELPERS
// ===============================
function el(id) {
    return document.getElementById(id);
}

function safeText(v) {
    if (!v) return "";
    if (typeof v === "string") return v;
    return v.es || v.en || "";
}

// ===============================
// VOICE
// ===============================
function speak(text) {
    if (!text) return;

    window.speechSynthesis.cancel();

    const u = new SpeechSynthesisUtterance(text);
    u.lang = state.lang;

    u.onend = () => state.speaking = false;

    state.speaking = true;
    window.speechSynthesis.speak(u);
}

// ===============================
// START FLOW
// ===============================
async function solicitarEscape() {

    const payload = {
        estado: el("inp-state").value,
        zip_code: el("inp-zip").value,
        bolsillo: getBolsillo(),
        puedes_salir: getModalidad(),
        texto_libre: el("inp-text").value,
        idioma: state.lang
    };

    const res = await fetch("/diagnostico-kamizen", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const data = await res.json();

    state.bloques = data.bloques_interactivos || data.blocks || [];

    el("wrapper-form").style.display = "none";
    el("wrapper-interactive").style.display = "block";

    el("interactive-title").innerText = data.titulo || data.title || "";
    el("interactive-location").innerText = data.lugar || data.location || "";

    if (data.url_maps || data.map) {
        const btn = el("btn-maps-action");
        btn.href = data.url_maps || data.map;
        btn.style.display = "block";
    }

    state.loopStart = Date.now();

    startLoop();
    nextStep();
}

// ===============================
// LOOP CONTROL (10 MIN EXACT)
// ===============================
function startLoop() {
    clearTimeout(state.loopTimeout);

    state.loopTimeout = setTimeout(() => {
        endLoop();
    }, state.loopDuration);
}

function endLoop() {
    speak(state.lang === "es"
        ? "Ejercicio terminado. Puedes reiniciar cuando quieras."
        : "Session completed. You may restart anytime."
    );

    reset();
}

// ===============================
// RESET
// ===============================
function reset() {
    state.index = 0;
    state.used.clear();
    clearInterval(state.breathing);
    clearInterval(state.silence);
}

// ===============================
// STEP ENGINE (NO FREEZE SAFE)
// ===============================
function nextStep() {

    if (!state.bloques.length) return;

    if (state.used.size >= state.bloques.length) {
        state.used.clear();
    }

    let available = state.bloques
        .map((_, i) => i)
        .filter(i => !state.used.has(i));

    let idx = available[Math.floor(Math.random() * available.length)];

    state.used.add(idx);
    state.index = idx;

    render(state.bloques[idx]);
}

// ===============================
// RENDER BLOCK
// ===============================
function render(block) {

    const container = el("step-content");
    container.innerHTML = "";

    // TEXT
    if (block.tx) {
        const t = safeText(block.tx);
        const div = document.createElement("div");
        div.innerText = t;
        container.appendChild(div);
        speak(t);
    }

    // QUESTION
    if (block.q) {
        const q = document.createElement("h3");
        q.innerText = safeText(block.q);
        container.appendChild(q);
    }

    // OPTIONS (FIXED CLICK ISSUE)
    if (block.op && Array.isArray(block.op)) {

        block.op.forEach((o, i) => {
            const btn = document.createElement("button");

            btn.innerText = safeText(o);
            btn.style.display = "block";
            btn.style.width = "100%";
            btn.style.margin = "6px 0";
            btn.style.padding = "12px";

            btn.onclick = () => {
                speak(state.lang === "es" ? "Continuando" : "Continuing");
                nextStep();
            };

            container.appendChild(btn);
        });
    }

    // BREATHING FIX (REAL SMOOTH ANIMATION)
    if (block.t === "breath_auto") {
        startBreathing(block.d || 20);
    }

    // SILENCE TIMER (FIXED)
    if (block.t === "sil") {
        startSilence(block.d || 30);
    }

    el("btn-next").style.display = "block";
}

// ===============================
// BREATHING (REAL PULSE SMOOTH)
// ===============================
function startBreathing(seconds) {

    clearInterval(state.breathing);

    const container = el("step-content");

    let circle = document.createElement("div");
    circle.className = "breath-circle";
    circle.style.transition = "transform 4s ease-in-out";
    circle.style.margin = "20px auto";

    container.appendChild(circle);

    let inhale = true;
    let count = 0;

    state.breathing = setInterval(() => {

        if (inhale) {
            circle.style.transform = "scale(1.8)";
            circle.innerText = state.lang === "es" ? "INHALA" : "IN";
        } else {
            circle.style.transform = "scale(1)";
            circle.innerText = state.lang === "es" ? "EXHALA" : "OUT";
        }

        inhale = !inhale;
        count++;

        if (count >= seconds * 2) {
            clearInterval(state.breathing);
        }

    }, 2000);
}

// ===============================
// SILENCE TIMER (REAL COUNTDOWN FIX)
// ===============================
function startSilence(seconds) {

    clearInterval(state.silence);

    const container = el("step-content");

    let timer = document.createElement("div");
    timer.style.fontSize = "20px";
    timer.style.marginTop = "10px";

    container.appendChild(timer);

    let t = seconds;

    timer.innerText = `⏳ ${t}`;

    state.silence = setInterval(() => {

        t--;
        timer.innerText = `⏳ ${t}`;

        if (t <= 0) {
            clearInterval(state.silence);
            nextStep();
        }

    }, 1000);
}

// ===============================
// UI STATE
// ===============================
function cambiarIdioma(l) {
    state.lang = l;

    el("lang-es").classList.toggle("active", l === "es");
    el("lang-en").classList.toggle("active", l === "en");
}

function cambiarBolsillo(v) {
    window._bolsillo = v;
}

function getBolsillo() {
    return window._bolsillo || "cero";
}

function cambiarModalidad(v) {
    window._modalidad = v;
}

function getModalidad() {
    return window._modalidad ?? true;
}

// ===============================
// NEXT BUTTON
// ===============================
function siguienteComando() {
    nextStep();
}

// ===============================
// EXPORT GLOBAL
// ===============================
window.solicitarEscape = solicitarEscape;
window.siguienteComando = siguienteComando;
window.cambiarIdioma = cambiarIdioma;
window.cambiarBolsillo = cambiarBolsillo;
window.cambiarModalidad = cambiarModalidad;

})();
