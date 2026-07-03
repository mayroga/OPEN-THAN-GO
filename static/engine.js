// =========================================================
// OPEN THAN GO - ENGINE.JS v4 (STABLE CORE)
// SAFE FLOW - NO FREEZES - NO CRASH ON NULL DATA
// =========================================================

let currentMission = null;
let steps = [];
let stepIndex = 0;

let timer = null;
let timeLeft = 600;

// =========================================================
// START SYSTEM
// =========================================================
function startOpenThanGo() {

    const payload = collectInput();

    showLoader(true);

    fetch("/api/open-than-go", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {

        showLoader(false);

        if (!data) return;

        loadMission(data.mission, data.ui);

    })
    .catch(err => {
        showLoader(false);
        console.error("API ERROR:", err);
    });
}

// =========================================================
// INPUT
// =========================================================
function collectInput() {
    return {
        decision: window.currentMode || "salir",
        desahogo: document.getElementById("inp-text")?.value || "",
        estado: document.getElementById("inp-state")?.value || "FL",
        zip_code: document.getElementById("inp-zip")?.value || "",
        budget_level: document.getElementById("inp-budget")?.value || "cero"
    };
}

// =========================================================
// LOAD MISSION
// =========================================================
function loadMission(mission, ui) {

    currentMission = mission || {};
    steps = Array.isArray(currentMission.b) ? currentMission.b : [];
    stepIndex = 0;

    document.getElementById("result").innerHTML = "";

    resetTimer();
    nextStep();
}

// =========================================================
// SAFE FLOW ENGINE
// =========================================================
function nextStep() {

    if (!steps || stepIndex >= steps.length) {
        showContinueButton();
        return;
    }

    const step = steps[stepIndex++];
    if (!step) {
        showContinueButton();
        return;
    }

    switch (step.t || "story") {

        case "v":
        case "h":
            if (step.tx?.es) {
                renderText(step.tx.es);
                speak(step.tx.es);
            }
            break;

        case "story":
            if (step.story?.es) {
                renderText(step.story.es);
                speak(step.story.es);
            }
            break;

        case "breath_auto":
            runBreathing(step);
            break;

        case "d":
            if (step.q?.es && Array.isArray(step.op)) {
                renderDecision(step);
            } else {
                nextStep();
            }
            break;

        case "sil":
            runSilence(step);
            break;

        case "r":
            if (step.tx?.es) renderText(step.tx.es);
            setTimeout(nextStep, 600);
            break;

        case "c":
            if (step.tx?.es) renderText("💡 " + step.tx.es);
            break;

        default:
            nextStep();
            break;
    }
}

// =========================================================
// TEXT
// =========================================================
function renderText(text) {
    if (!text) return;

    const div = document.getElementById("result");

    div.innerHTML += `
        <div class="card">
            <p>${text}</p>
        </div>
    `;
}

// =========================================================
// VOICE (SAFE ESPAÑOL)
// =========================================================
function speak(text) {

    if (!text || !window.speechSynthesis) return;

    const utter = new SpeechSynthesisUtterance(text);

    utter.lang = "es-ES";
    utter.rate = 0.95;
    utter.pitch = 1;

    const voices = speechSynthesis.getVoices?.() || [];
    const esVoice = voices.find(v => v.lang?.includes("es"));

    if (esVoice) utter.voice = esVoice;

    speechSynthesis.cancel();
    speechSynthesis.speak(utter);
}

// =========================================================
// BREATHING
// =========================================================
function runBreathing(step) {

    const div = document.getElementById("result");

    div.innerHTML += `
        <div class="card center">
            <div id="circle" class="breath-circle">RESPIRA</div>
        </div>
    `;

    const circle = document.getElementById("circle");

    let cycles = 5;
    let i = 0;
    let expand = true;

    const interval = setInterval(() => {

        circle.style.transform = expand ? "scale(1.3)" : "scale(1)";
        circle.innerText = expand ? "INHALA" : "EXHALA";

        expand = !expand;
        i++;

        if (i >= cycles * 2) {
            clearInterval(interval);
            nextStep();
        }

    }, 2000);
}

// =========================================================
// DECISION
// =========================================================
function renderDecision(step) {

    const div = document.getElementById("result");

    let html = `<div class="card"><p>${step.q?.es || ""}</p>`;

    (step.op || []).forEach((op, index) => {

        html += `
            <button onclick="selectOption(${index}, ${step.c || 0})">
                ${op.es || ""}
            </button>
        `;
    });

    html += `</div>`;

    div.innerHTML += html;
}

// =========================================================
// OPTION SELECT
// =========================================================
function selectOption(index, correct) {

    renderText(index === correct ? "✔ Correcto" : "✖ Reflexiona");

    setTimeout(nextStep, 700);
}

// =========================================================
// SILENCE
// =========================================================
function runSilence(step) {

    if (step.tx?.es) renderText(step.tx.es);

    const seconds = step.d || 20;

    const div = document.getElementById("result");

    div.innerHTML += `
        <div class="card center">
            <p>⏳ ${seconds} segundos</p>
        </div>
    `;

    setTimeout(nextStep, seconds * 1000);
}

// =========================================================
// TIMER RESET (FIX REAL)
// =========================================================
function resetTimer() {

    clearInterval(timer);
    timer = null;

    timeLeft = 600;

    timer = setInterval(() => {

        timeLeft--;

        if (timeLeft <= 0) {
            clearInterval(timer);
            timer = null;
            showContinueButton();
        }

    }, 1000);
}

// =========================================================
// CONTINUE FLOW (FIXED)
// =========================================================
function showContinueButton() {

    const div = document.getElementById("result");

    div.innerHTML += `
        <div class="card center">
            <button onclick="continueMission()">CONTINUAR</button>
        </div>
    `;
}

function continueMission() {

    clearInterval(timer);
    timer = null;

    stepIndex = 0;
    steps = [];

    document.getElementById("result").innerHTML = "";

    startOpenThanGo();
}

// =========================================================
// MODE
// =========================================================
function setMode(mode) {

    window.currentMode = mode;

    const badge = document.getElementById("mode-badge");

    if (!badge) return;

    badge.innerText = mode === "casa" ? "Modo Casa" : "Modo Salir";
}

// =========================================================
// LOADER
// =========================================================
function showLoader(show) {
    const el = document.getElementById("loader");
    if (el) el.style.display = show ? "block" : "none";
}
