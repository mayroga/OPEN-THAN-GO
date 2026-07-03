// =========================================================
// OPEN THAN GO - ENGINE.JS v3 (MISSION EXECUTOR)
// FRONTEND BRAIN SYSTEM
// =========================================================

let currentMission = null;
let stepIndex = 0;
let steps = [];
let timer = null;
let timeLeft = 600; // 10 min por misión
let speaking = false;


// =========================================================
// INIT
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
        loadMission(data.mission, data.ui);
    })
    .catch(err => {
        showLoader(false);
        console.log(err);
    });
}


// =========================================================
// COLLECT INPUT
// =========================================================
function collectInput() {
    return {
        decision: window.currentMode || "salir",
        desahogo: document.getElementById("inp-text").value,
        estado: document.getElementById("inp-state").value,
        zip_code: document.getElementById("inp-zip").value,
        budget_level: document.getElementById("inp-budget").value
    };
}


// =========================================================
// LOAD MISSION
// =========================================================
function loadMission(mission, ui) {

    currentMission = mission;
    stepIndex = 0;
    steps = mission.b || [];

    document.getElementById("result").innerHTML = "";

    startTimer();
    nextStep();
}


// =========================================================
// STEP ENGINE (CORE)
// =========================================================
function nextStep() {

    if (!steps || stepIndex >= steps.length) {
        showContinueButton();
        return;
    }

    const step = steps[stepIndex];
    stepIndex++;

    switch(step.t || "story") {

        case "v":
        case "h":
            renderText(step.tx.es);
            speak(step.tx.es);
            break;

        case "story":
            renderText(step.story.es);
            speak(step.story.es);
            break;

        case "breath_auto":
            runBreathing(step);
            break;

        case "d":
            renderDecision(step);
            break;

        case "sil":
            runSilence(step);
            break;

        case "r":
            renderReward(step);
            break;

        case "c":
            renderText("💡 " + step.tx.es);
            break;

        default:
            nextStep();
            break;
    }
}


// =========================================================
// TEXT RENDER
// =========================================================
function renderText(text) {
    const div = document.getElementById("result");
    div.innerHTML += `
        <div class="card">
            <p>${text}</p>
        </div>
    `;
}


// =========================================================
// VOICE (SPANISH ONLY FIX)
// =========================================================
function speak(text) {
    if (!window.speechSynthesis) return;

    const utter = new SpeechSynthesisUtterance(text);

    utter.lang = "es-ES";
    utter.rate = 0.95;
    utter.pitch = 1;

    // FORZAR VOZ ESPAÑOLA SI EXISTE
    const voices = speechSynthesis.getVoices();
    const spanishVoice = voices.find(v =>
        v.lang.includes("es")
    );

    if (spanishVoice) {
        utter.voice = spanishVoice;
    }

    speechSynthesis.cancel();
    speechSynthesis.speak(utter);
}


// =========================================================
// BREATHING ENGINE (CIRCLE)
// =========================================================
function runBreathing(step) {

    const div = document.getElementById("result");

    div.innerHTML += `
        <div class="card center">
            <div class="breath-circle" id="circle">
                RESPIRA
            </div>
        </div>
    `;

    let circle = document.getElementById("circle");
    let expand = true;

    let cycles = 6;
    let i = 0;

    let breathInterval = setInterval(() => {

        if (expand) {
            circle.style.transform = "scale(1.4)";
            circle.innerText = "INHALA";
        } else {
            circle.style.transform = "scale(1)";
            circle.innerText = "EXHALA";
        }

        expand = !expand;

        i++;
        if (i >= cycles * 2) {
            clearInterval(breathInterval);
            nextStep();
        }

    }, 2000);
}


// =========================================================
// DECISION STEP
// =========================================================
function renderDecision(step) {

    const div = document.getElementById("result");

    let html = `
        <div class="card">
            <p>${step.q.es}</p>
    `;

    step.op.forEach((op, index) => {
        html += `
            <button onclick="selectOption(${index}, ${step.c})">
                ${op.es}
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

    const div = document.getElementById("result");

    let msg = index === correct
        ? "✔ Correcto"
        : "✖ Reflexiona";

    renderText(msg);

    setTimeout(nextStep, 800);
}


// =========================================================
// SILENCE / MINDFUL STEP
// =========================================================
function runSilence(step) {

    renderText(step.tx.es);

    let div = document.getElementById("result");

    div.innerHTML += `
        <div class="card center">
            <p>⏳ ${step.d} segundos de enfoque</p>
        </div>
    `;

    setTimeout(() => {
        nextStep();
    }, step.d * 1000);
}


// =========================================================
// REWARD STEP
// =========================================================
function renderReward(step) {
    renderText(step.tx.es);
    setTimeout(nextStep, 1000);
}


// =========================================================
// TIMER (10 MIN GLOBAL MISSION)
// =========================================================
function startTimer() {

    clearInterval(timer);
    timeLeft = 600;

    timer = setInterval(() => {

        timeLeft--;

        if (timeLeft <= 0) {
            clearInterval(timer);
            showContinueButton();
        }

    }, 1000);
}


// =========================================================
// CONTINUE BUTTON (MISSION FLOW)
// =========================================================
function showContinueButton() {

    const div = document.getElementById("result");

    div.innerHTML += `
        <div class="card center">
            <button onclick="continueMission()">
                CONTINUAR MISIÓN
            </button>
        </div>
    `;
}


// =========================================================
// CONTINUE FLOW (NEXT MISSION STEP OR NEW MISSION)
// =========================================================
function continueMission() {
    stepIndex++;
    nextStep();
}


// =========================================================
// MODE CONTROL
// =========================================================
function setMode(mode) {
    window.currentMode = mode;

    const badge = document.getElementById("mode-badge");

    badge.innerText =
        mode === "casa"
        ? "Modo: Casa"
        : "Modo: Salir";

    badge.className =
        mode === "casa"
        ? "mode-badge mode-casa"
        : "mode-badge mode-salir";
}


// =========================================================
// LOADER
// =========================================================
function showLoader(show) {
    document.getElementById("loader").style.display =
        show ? "block" : "none";
}
