// ===============================
// SAFE LOOP ENGINE v1
// OPEN THAN GO SYSTEM
// ===============================

let state = {
    session_id: null,
    bloques: [],
    index: 0,
    timer: null,
    breathTimer: null,
    silenceTimer: null,
    loopEnd: 0,
    running: false,
    maps: null,
    idioma: "es"
};

const circle = () => document.querySelector(".breath-circle");
const stepContent = () => document.getElementById("step-content");
const title = () => document.getElementById("interactive-title");
const locationBox = () => document.getElementById("interactive-location");
const btnNext = () => document.getElementById("btn-next");
const mapsBtn = () => document.getElementById("btn-maps-action");

// ===============================
// INIT REQUEST
// ===============================
async function solicitarEscape() {

    const data = {
        session_id: Date.now().toString(),
        estado: document.getElementById("inp-state").value,
        zip_code: document.getElementById("inp-zip").value,
        bolsillo: getBolsillo(),
        puedes_salir: getModalidad(),
        texto_libre: document.getElementById("inp-text").value,
        idioma: state.idioma
    };

    const res = await fetch("/diagnostico-kamizen", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const json = await res.json();

    if (json.error) {
        alert("No hay misiones disponibles");
        return;
    }

    startEngine(json);
}

// ===============================
// START ENGINE
// ===============================
function startEngine(data) {

    state.session_id = data.session_id;
    state.bloques = data.bloques;
    state.index = 0;
    state.maps = data.maps || null;
    state.running = true;

    state.loopEnd = Date.now() + (data.loop_seconds * 1000);

    document.getElementById("wrapper-form").style.display = "none";
    document.getElementById("wrapper-interactive").style.display = "block";

    title().innerText = data.title || "OPEN THAN GO";

    if (data.location) {
        locationBox().innerText = data.location;
    }

    if (state.maps) {
        mapsBtn().style.display = "block";
        mapsBtn().href = state.maps;
    }

    renderStep();

    startLoopTimer();
    startBreathing();
}

// ===============================
// STEP ENGINE
// ===============================
function renderStep() {

    if (!state.bloques[state.index]) {
        finishLoop();
        return;
    }

    const b = state.bloques[state.index];

    let html = "";

    if (b.t === "v") {
        html = `<h3>${b.tx}</h3>`;
    }

    if (b.t === "h") {
        html = `<div class="screen-story">${b.tx}</div>`;
    }

    if (b.t === "story") {
        html = `<div class="screen-story">${b.tx}</div>`;
    }

    if (b.t === "breath_auto") {
        startBreathingCycle(b.d || 5);
        html = `<p>${b.tx}</p>`;
    }

    if (b.t === "d") {
        html = `
            <div class="screen-story">
                <p><b>${b.q}</b></p>
                ${b.op.map((o, i) =>
                    `<button class="btn-choice" onclick="selectOption(${i})">${o}</button>`
                ).join("")}
            </div>
        `;
    }

    if (b.t === "sil") {
        startSilenceTimer(b.d || 10);
        html = `<p><b>SILENCE CHALLENGE</b></p><p>${b.tx}</p>`;
    }

    stepContent().innerHTML = html;

    btnNext().style.display = "block";
}

// ===============================
// NEXT STEP
// ===============================
function siguienteComando() {
    state.index++;
    renderStep();
}

// ===============================
// BREATHING ENGINE (REAL ANIMATION)
// ===============================
function startBreathing() {

    const c = circle();
    if (!c) return;

    let grow = true;
    let size = 90;

    clearInterval(state.breathTimer);

    state.breathTimer = setInterval(() => {

        if (!state.running) return;

        if (grow) {
            size += 1;
            if (size >= 130) grow = false;
        } else {
            size -= 1;
            if (size <= 80) grow = true;
        }

        c.style.width = size + "px";
        c.style.height = size + "px";

    }, 50);
}

// ===============================
// BREATH CYCLE CONTROLLED
// ===============================
function startBreathingCycle(seconds) {

    const c = circle();
    if (!c) return;

    let t = seconds * 2;
    let size = 90;

    clearInterval(state.breathTimer);

    state.breathTimer = setInterval(() => {

        if (!state.running) return;

        size = size === 90 ? 120 : 90;

        c.style.width = size + "px";
        c.style.height = size + "px";

        t--;

        if (t <= 0) {
            clearInterval(state.breathTimer);
            startBreathing();
        }

    }, 1000);
}

// ===============================
// SILENCE TIMER (CRITICAL)
// ===============================
function startSilenceTimer(seconds) {

    let remaining = seconds;

    clearInterval(state.silenceTimer);

    state.silenceTimer = setInterval(() => {

        if (!state.running) return;

        remaining--;

        if (remaining <= 0) {
            clearInterval(state.silenceTimer);
            siguienteComando();
        }

    }, 1000);
}

// ===============================
// MAIN LOOP TIMER 10 MIN
// ===============================
function startLoopTimer() {

    clearInterval(state.timer);

    state.timer = setInterval(() => {

        const left = state.loopEnd - Date.now();

        if (left <= 0) {
            finishLoop();
        }

    }, 1000);
}

// ===============================
// FINISH LOOP
// ===============================
function finishLoop() {

    state.running = false;

    clearInterval(state.timer);
    clearInterval(state.breathTimer);
    clearInterval(state.silenceTimer);

    stepContent().innerHTML = `
        <div class="screen-story">
            <h3>LOOP COMPLETED</h3>
            <p>You can restart your 10-minute reset cycle.</p>
        </div>
    `;

    btnNext().style.display = "none";
}

// ===============================
// UI HELPERS
// ===============================
function getBolsillo() {
    return document.querySelector(".btn-choice.active")?.textContent === "$0"
        ? "cero"
        : "moderado";
}

function getModalidad() {
    return true;
}

function cambiarIdioma(l) {
    state.idioma = l;
}

// placeholder for option click
function selectOption(i) {
    siguienteComando();
}
