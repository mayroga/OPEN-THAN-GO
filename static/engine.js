// static/engine.js
// OPEN THAN GO SYSTEM - Frontend Engine v6 (STABLE ORCHESTRATOR UI)
// Company: May Roga LLC

let idiomaActual = "es";

let sessionMode = null;
let missions = [];
let stepIndex = 0;

let totalTime = 0;
let remainingTime = 0;

let breathInterval = null;
let timerInterval = null;

let voiceEnabled = true;
let lock = false;

// ----------------------------
// SAFE GET
// ----------------------------
function get(id) {
    return document.getElementById(id);
}

// ----------------------------
// SAFE TEXT
// ----------------------------
function t(obj) {
    if (!obj) return "";
    if (typeof obj === "string") return obj;
    return obj[idiomaActual] || obj.es || obj.en || "";
}

// ----------------------------
// VOICE ENGINE (SAFE)
// ----------------------------
function speak(text) {
    if (!voiceEnabled || !("speechSynthesis" in window)) return;
    if (!text) return;

    const u = new SpeechSynthesisUtterance(text);
    const voices = speechSynthesis.getVoices();

    let v =
        voices.find(v => v.lang.startsWith(idiomaActual)) ||
        voices[0];

    u.voice = v;
    u.rate = 0.95;
    u.pitch = 1;

    speechSynthesis.cancel();
    speechSynthesis.speak(u);
}

// ----------------------------
// UI STATE
// ----------------------------
function showLoader() {
    get("wrapper-form").style.display = "none";
    get("wrapper-loader").style.display = "flex";
    get("wrapper-interactive").style.display = "none";
}

function showApp() {
    get("wrapper-loader").style.display = "none";
    get("wrapper-interactive").style.display = "block";
}

// ----------------------------
// START
// ----------------------------
document.addEventListener("DOMContentLoaded", () => {
    get("btn-start").onclick = startSession;
});

// ----------------------------
// MAIN REQUEST
// ----------------------------
async function startSession() {

    const payload = {
        decision: document.querySelector("#inp-mode")?.value || "salir",
        lang: idiomaActual,
        budget_level: get("inp-budget")?.value || "cero",
        zip_code: get("inp-zip")?.value || "",
        estado: get("inp-state")?.value || "",
        desahogo: get("inp-text")?.value || ""
    };

    showLoader();

    try {
        const res = await fetch("/api/open-than-go", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (data.status !== "success") throw new Error("backend error");

        sessionMode = data.mode;

        // ---------------- HOME ----------------
        if (sessionMode === "home") {
            missions = data.missions || [];
            totalTime = data.duration || 600;
            remainingTime = totalTime;
        }

        // ---------------- OUT ----------------
        if (sessionMode === "out") {
            missions = [];
            totalTime = data.duration || 60;
            remainingTime = totalTime;

            renderOut(data);
        }

        stepIndex = 0;
        showApp();

        if (sessionMode === "home") {
            runHome();
        } else {
            runOutTimer();
        }

    } catch (e) {
        console.error(e);
        alert("Error backend");
        location.reload();
    }
}

// ----------------------------
// OUT MODE (SALIR)
// ----------------------------
function renderOut(data) {

    const cont = get("step-content");

    cont.innerHTML = `
        <div class="card-box">
            <h2>${data.place.name}</h2>
            <p>${data.why}</p>
            <p>${data.psych_logic?.es || ""}</p>
        </div>
    `;

    const mapBtn = get("btn-maps-action");
    mapBtn.style.display = "block";
    mapBtn.href = "#";
}

// ----------------------------
// HOME MODE (CASA)
// ----------------------------
function runHome() {
    clearAll();

    renderStep();
    runTimerHome();
}

// ----------------------------
// STEP RENDER
// ----------------------------
function renderStep() {

    const cont = get("step-content");
    const step = missions[stepIndex];

    if (!step) {
        finishSession();
        return;
    }

    cont.innerHTML = `<div class="card-box">${t(step.text)}</div>`;
    speak(t(step.text));

    if (step.type === "breath") {
        runBreath(step.duration || 60);
        return;
    }

    setTimeout(() => {
        stepIndex++;
        renderStep();
    }, step.duration * 1000);
}

// ----------------------------
// BREATH ENGINE (FIXED)
// ----------------------------
function runBreath(seconds) {

    const cont = get("step-content");

    let s = seconds;

    cont.innerHTML = `
        <div class="card-box">
            <div id="breathingCircle"></div>
            <h2 id="breathText">Inhala</h2>
            <div id="breathTimer"></div>
        </div>
    `;

    const circle = get("breathingCircle");

    lock = true;

    clearInterval(breathInterval);

    breathInterval = setInterval(() => {

        if (s <= 0) {
            clearInterval(breathInterval);
            lock = false;
            stepIndex++;
            renderStep();
            return;
        }

        const inhale = s % 2 === 0;

        get("breathText").innerText = inhale ? "Inhala" : "Exhala";

        if (circle) {
            circle.style.transform = inhale ? "scale(1.4)" : "scale(1)";
        }

        if (s % 4 === 0) speak(inhale ? "Inhala" : "Exhala");

        get("breathTimer").innerText = s + "s";

        s--;
        remainingTime--;

    }, 1000);
}

// ----------------------------
// HOME TIMER (10 MIN CONTROL)
// ----------------------------
function runTimerHome() {

    const t = get("timer");

    clearInterval(timerInterval);

    timerInterval = setInterval(() => {

        let m = Math.floor(remainingTime / 60);
        let s = remainingTime % 60;

        if (t) t.innerText = `${m}:${s.toString().padStart(2, "0")}`;

        remainingTime--;

        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            finishSession();
        }

    }, 1000);
}

// ----------------------------
// OUT TIMER (60s SIMPLE)
// ----------------------------
function runOutTimer() {

    const t = get("timer");

    const i = setInterval(() => {

        let s = remainingTime % 60;

        if (t) t.innerText = `0:${s.toString().padStart(2, "0")}`;

        remainingTime--;

        if (remainingTime <= 0) {
            clearInterval(i);
            finishSession();
        }

    }, 1000);
}

// ----------------------------
// FINISH
// ----------------------------
function finishSession() {

    const cont = get("step-content");

    cont.innerHTML = `
        <div class="card-box">
            <h2>Sesión completada</h2>
        </div>
    `;

    const btn = get("btn-next");
    btn.style.display = "block";
    btn.innerText = "REINICIAR";
    btn.onclick = () => location.reload();
}

// ----------------------------
// CLEAN SYSTEM
// ----------------------------
function clearAll() {
    clearInterval(timerInterval);
    clearInterval(breathInterval);
    speechSynthesis.cancel();
}
