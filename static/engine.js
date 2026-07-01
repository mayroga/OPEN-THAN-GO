/* =========================================================
   OPEN THAN GO ENGINE vFINAL CLEAN
   SINGLE BRAIN • NO FREEZE • REAL FLOW • 10 MIN LOOP
========================================================= */

let state = {
    missions: [],
    stories: [],
    currentIndex: 0,
    currentBlock: 0,
    lang: "es",
    pocket: "cero",
    mode: "outdoor",
    speaking: false,

    // TIMER MASTER
    sessionActive: false,
    sessionTime: 600, // 10 min
    timer: null,

    // BREATH
    breathTimer: null,
    breathState: "inhale"
};

/* =========================
   INIT
========================= */
window.addEventListener("load", async () => {
    await loadData();
    renderForm();
});

/* =========================
   LOAD DATA
========================= */
async function loadData() {
    const res = await fetch("/api/missions");
    const data = await res.json();
    state.missions = data.missions || [];
}

/* =========================
   UI FORM
========================= */
function renderForm() {
    document.getElementById("wrapper-form").style.display = "block";
    document.getElementById("wrapper-interactive").style.display = "none";
}

/* =========================
   START FLOW
========================= */
function solicitarEscape() {
    state.lang = getLang();
    state.pocket = getPocket();
    state.mode = getMode();

    startSession();
}

/* =========================
   SESSION START (ONLY ONE LOOP)
========================= */
function startSession() {
    state.sessionActive = true;
    state.sessionTime = 600;

    document.getElementById("wrapper-form").style.display = "none";
    document.getElementById("wrapper-interactive").style.display = "block";

    startTimer();
    startFlow();
}

/* =========================
   MASTER TIMER (10 MIN EXACT)
========================= */
function startTimer() {
    clearInterval(state.timer);

    state.timer = setInterval(() => {
        state.sessionTime--;

        if (state.sessionTime <= 0) {
            finishSession();
        }
    }, 1000);
}

function finishSession() {
    clearInterval(state.timer);
    clearInterval(state.breathTimer);

    state.sessionActive = false;

    document.getElementById("wrapper-interactive").innerHTML = `
        <div class="screen-title">SESSION COMPLETE</div>
        <p>Respiración, enfoque y control finalizados.</p>
        <button onclick="location.reload()">RESTART</button>
    `;
}

/* =========================
   FLOW ENGINE (SEQUENTIAL 1→N LOOP)
========================= */
function startFlow() {
    state.currentIndex = 0;
    nextStep();
}

function nextStep() {
    const mission = state.missions[state.currentIndex];

    if (!mission) {
        state.currentIndex = 0;
        return nextStep();
    }

    renderMission(mission);
}

/* =========================
   RENDER MISSION
========================= */
function renderMission(mission) {
    let html = `
        <div class="screen-title">
            STEP ${mission.id}
        </div>

        <div class="screen-story">
            ${mission.t?.[state.lang] || mission.t?.es || ""}
        </div>
    `;

    document.getElementById("interactive-title").innerHTML = "";
    document.getElementById("interactive-location").innerHTML = "";

    document.getElementById("step-content").innerHTML = html;

    speak(mission.t?.[state.lang] || mission.t?.es || "", () => {
        runMission(mission);
    });
}

/* =========================
   EXECUTE MISSION LOGIC
========================= */
function runMission(mission) {

    // BREATH STEP
    if (mission.type === "breath") {
        startBreathing();
        setTimeout(() => nextMission(), 8000);
        return;
    }

    // SILENCE STEP
    if (mission.type === "silence") {
        setTimeout(() => nextMission(), 5000);
        return;
    }

    // DECISION STEP
    if (mission.type === "decision") {
        renderDecision(mission);
        return;
    }

    // DEFAULT STEP
    setTimeout(() => nextMission(), 2000);
}

/* =========================
   BREATHING REAL (NATURAL FLOW)
========================= */
function startBreathing() {
    clearInterval(state.breathTimer);

    const circle = document.getElementById("breathCircle");
    if (!circle) return;

    let inhale = true;

    state.breathTimer = setInterval(() => {
        if (!state.sessionActive) return;

        if (inhale) {
            circle.style.transform = "scale(1.4)";
            circle.innerText = "INHALE";
        } else {
            circle.style.transform = "scale(0.8)";
            circle.innerText = "EXHALE";
        }

        inhale = !inhale;

    }, 3000);
}

/* =========================
   DECISION BLOCK
========================= */
function renderDecision(mission) {
    let html = `<div class="screen-story">${mission.q?.[state.lang] || ""}</div>`;

    mission.op.forEach((op, i) => {
        html += `
            <button onclick="selectOption(${i})">${op[state.lang] || op.es}</button>
        `;
    });

    document.getElementById("step-content").innerHTML = html;
}

function selectOption(i) {
    nextMission();
}

/* =========================
   NAVIGATION SEQUENTIAL ONLY
========================= */
function nextMission() {
    state.currentIndex++;

    if (state.currentIndex >= state.missions.length) {
        state.currentIndex = 0;
    }

    nextStep();
}

/* =========================
   SPEECH ENGINE
========================= */
function speak(text, cb) {
    if (!text) {
        cb && cb();
        return;
    }

    window.speechSynthesis.cancel();

    const msg = new SpeechSynthesisUtterance(text);
    msg.lang = state.lang === "es" ? "es-ES" : "en-US";
    msg.rate = 0.95;

    msg.onend = () => cb && cb();

    window.speechSynthesis.speak(msg);
}

/* =========================
   HELPERS
========================= */
function getLang() {
    const es = document.getElementById("lang-es").classList.contains("active");
    return es ? "es" : "en";
}

function getPocket() {
    return "cero";
}

function getMode() {
    return true;
}
