// ===============================
// SAFE LOOP ENGINE vFINAL
// CLIENT ONLY (NO LOGIC DECISION)
// ===============================

let sessionId = null;
let mission = null;
let state = null;

let stepIndex = 1;
let maxSteps = 27;

let timer = null;
let breathingTimer = null;
let secondsLeft = 600;

let currentLanguage = "es";
let bolsillo = "cero";
let canGo = true;

// ===============================
// UI ELEMENTS
// ===============================
const form = document.getElementById("wrapper-form");
const interactive = document.getElementById("wrapper-interactive");

const titleEl = document.getElementById("interactive-title");
const locationEl = document.getElementById("interactive-location");
const stepContent = document.getElementById("step-content");

const btnNext = document.getElementById("btn-next");
const btnMaps = document.getElementById("btn-maps-action");

// ===============================
// LANGUAGE
// ===============================
function cambiarIdioma(lang) {
    currentLanguage = lang;

    document.getElementById("lang-es").classList.remove("active");
    document.getElementById("lang-en").classList.remove("active");

    document.getElementById("lang-" + lang).classList.add("active");
}

// ===============================
// BOLSILLO
// ===============================
function cambiarBolsillo(v) {
    bolsillo = v;
}

// ===============================
// MODALIDAD
// ===============================
let salirCasa = true;

function cambiarModalidad(v) {
    salirCasa = v;
}

// ===============================
// START
// ===============================
async function solicitarEscape() {

    const payload = {
        session_id: sessionId,
        texto_libre: document.getElementById("inp-text").value,
        zip_code: document.getElementById("inp-zip").value,
        estado: document.getElementById("inp-state").value,
        bolsillo: bolsillo,
        idioma: currentLanguage,
        action: "next"
    };

    const res = await fetch("/safe-loop", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    const data = await res.json();

    sessionId = data.session_id;
    mission = data.mission;
    state = data.state;
    maxSteps = data.max_steps;

    renderScreen(data);
}

// ===============================
// RENDER
// ===============================
function renderScreen(data) {

    form.style.display = "none";
    interactive.style.display = "block";

    titleEl.innerText = mission.title;
    locationEl.innerText = `Step ${state.step} / ${maxSteps} | Emotion: ${state.emotion}`;

    stepContent.innerHTML = "";

    // RESET UI
    stopTimers();

    // BREATHING
    startBreathing(mission.breathing);

    // TIMER 10 MIN
    startTimer(mission.loop_duration_seconds);

    // CONTENT
    stepContent.innerHTML = `
        <div class="screen-story">
            ${mission.instruction}
        </div>
    `;

    btnNext.style.display = "block";

    if (data.url_maps) {
        btnMaps.style.display = "block";
        btnMaps.href = data.url_maps;
    } else {
        btnMaps.style.display = "none";
    }

    speak(mission.instruction);
}

// ===============================
// NEXT STEP
// ===============================
async function siguienteComando() {

    const res = await fetch("/safe-loop", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            session_id: sessionId,
            texto_libre: "",
            action: "next"
        })
    });

    const data = await res.json();

    mission = data.mission;
    state = data.state;

    renderScreen(data);
}

// ===============================
// BREATHING ENGINE (REALISTIC)
// ===============================
function startBreathing(cfg) {

    const circle = createBreathCircle();

    let inhale = cfg?.inhale || 4;
    let hold = cfg?.hold || 2;
    let exhale = cfg?.exhale || 6;

    let phase = "inhale";
    let time = inhale;

    breathingTimer = setInterval(() => {

        if (phase === "inhale") {
            circle.style.transform = "scale(1.4)";
            time--;

            if (time <= 0) {
                phase = "hold";
                time = hold;
            }

        } else if (phase === "hold") {
            circle.style.transform = "scale(1.4)";
            time--;

            if (time <= 0) {
                phase = "exhale";
                time = exhale;
            }

        } else if (phase === "exhale") {
            circle.style.transform = "scale(0.8)";
            time--;

            if (time <= 0) {
                phase = "inhale";
                time = inhale;
            }
        }

    }, 1000);
}

// ===============================
// TIMER 10 MIN EXACT
// ===============================
function startTimer(seconds) {

    secondsLeft = seconds || 600;

    timer = setInterval(() => {

        secondsLeft--;

        if (secondsLeft <= 0) {
            clearInterval(timer);
            clearInterval(breathingTimer);

            finishLoop();
        }

    }, 1000);
}

// ===============================
// END LOOP
// ===============================
function finishLoop() {

    stepContent.innerHTML = `
        <div class="screen-title">
            LOOP COMPLETED
        </div>
        <button onclick="solicitarEscape()" class="btn-trigger">
            RESTART 10 MIN LOOP
        </button>
    `;
}

// ===============================
// STOP TIMERS
// ===============================
function stopTimers() {
    if (timer) clearInterval(timer);
    if (breathingTimer) clearInterval(breathingTimer);
}

// ===============================
// SPEECH (VOICE GUIDE)
// ===============================
function speak(text) {

    if (!("speechSynthesis" in window)) return;

    let msg = new SpeechSynthesisUtterance(text);
    msg.lang = currentLanguage === "es" ? "es-ES" : "en-US";
    msg.rate = 1;

    speechSynthesis.cancel();
    speechSynthesis.speak(msg);
}

// ===============================
// BREATH CIRCLE CREATOR
// ===============================
function createBreathCircle() {

    let old = document.querySelector(".breath-circle");
    if (old) old.remove();

    const wrapper = document.createElement("div");
    wrapper.className = "wrapper-circle";

    const circle = document.createElement("div");
    circle.className = "breath-circle";

    wrapper.appendChild(circle);
    stepContent.appendChild(wrapper);

    return circle;
}
