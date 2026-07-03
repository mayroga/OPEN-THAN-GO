// ======================================================
// OPEN THAN GO SYSTEM - ENGINE vFINAL (CORE ADAPTIVE AI)
// May Roga LLC
// ONE STATE · TWO MODES · FULL ADAPTIVE FLOW
// ======================================================

let state = {
    mode: "salir",                // salir | casa
    language: "es",               // es | en
    budget: "cero",
    emotion: "neutral",
    userInput: "",
    
    // missions
    missions: [],
    missionIndex: 0,
    blockIndex: 0,
    
    // home mode
    homeActive: false,
    homeTimer: null,
    homeTimeLeft: 600,
    
    // voice
    voiceEnabled: true,
    voiceGender: "male",
    
    // recommendation memory
    places: [],
    selectedPlace: null
};

// ======================================================
// SAFE GET
// ======================================================
function get(id) {
    return document.getElementById(id);
}

// ======================================================
// TITLE SYSTEM (EMOTION DRIVEN)
// ======================================================
function setTitle(emotion = "neutral") {
    const el = get("interactive-title");
    if (!el) return;

    const map = {
        stress: "OPEN ◉ THAN GO",
        monotony: "OPEN — THAN GO",
        low: "OPEN ○ THAN GO",
        neutral: "OPEN ◯ THAN GO"
    };

    el.innerText = map[emotion] || map.neutral;
}

// ======================================================
// MODE CONTROL
// ======================================================
function setMode(mode) {
    state.mode = mode;

    const badge = get("mode-badge");

    if (mode === "casa") {
        badge.innerText = "Modo: Casa (Intervención interna)";
        badge.className = "mode-badge mode-casa";
        startHomeMode();
    } else {
        badge.innerText = "Modo: Salir (Exploración adaptativa)";
        badge.className = "mode-badge mode-salir";
        stopHomeMode();
    }
}

// ======================================================
// USER INPUT ANALYSIS (CORE ADAPTIVE ENGINE)
// ======================================================
function analyzeUser(text = "") {
    text = text.toLowerCase();

    state.userInput = text;

    const stressWords = ["estres", "presion", "ansiedad", "trabajo"];
    const monotonyWords = ["aburrido", "rutina", "igual"];
    const lowWords = ["cansado", "sin energia", "agotado"];

    if (stressWords.some(w => text.includes(w))) return "stress";
    if (monotonyWords.some(w => text.includes(w))) return "monotony";
    if (lowWords.some(w => text.includes(w))) return "low";

    return "neutral";
}

// ======================================================
// VOICE ENGINE (ALWAYS ACTIVE SPANISH MALE)
// ======================================================
function speak(text) {
    if (!state.voiceEnabled || !text) return;

    window.speechSynthesis.cancel();

    const u = new SpeechSynthesisUtterance(text);
    u.lang = state.language === "es" ? "es-ES" : "en-US";
    u.rate = 0.95;

    const voices = window.speechSynthesis.getVoices();
    const male = voices.find(v => v.lang.includes("es") || v.lang.includes("en"));
    if (male) u.voice = male;

    window.speechSynthesis.speak(u);
}

// ======================================================
// START REQUEST
// ======================================================
async function start() {

    const payload = {
        decision: state.mode,
        estado: get("inp-state").value,
        zip_code: get("inp-zip").value,
        budget_level: get("inp-budget").value,
        desahogo: get("inp-text").value
    };

    state.emotion = analyzeUser(payload.desahogo);

    get("form").style.display = "none";
    get("loader").style.display = "block";

    const res = await fetch("/api/open-than-go", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    const data = await res.json();

    get("loader").style.display = "none";

    state.missions = data.mision?.b || [];
    state.places = data.recommendations || [];

    setTitle(state.emotion);

    if (state.mode === "casa") {
        startHomeMode();
    } else {
        renderOutMode();
    }
}

// ======================================================
// OUT MODE (EXPLORATION + ADAPTIVE PLACES)
// ======================================================
function renderOutMode() {

    const result = get("result");

    let html = `<div class="card"><h3>Tu guía adaptada</h3></div>`;

    // recommendation ranking (hidden logic)
    const shuffled = [...state.places].sort(() => Math.random() - 0.5);

    shuffled.forEach((p, i) => {

        const autoSelected = i === 0 ? " (Recomendado)" : "";

        html += `
        <div class="card">
            <h3>${p.name}${autoSelected}</h3>
            <p>${p.why}</p>
            <p><b>${p.cost}</b></p>

            <a href="${p.gps_link}" target="_blank">
                IR AL LUGAR
            </a>
        </div>`;
    });

    result.innerHTML = html;

    speak("He encontrado opciones adaptadas a lo que necesitas. Puedes explorar libremente.");
}

// ======================================================
// HOME MODE (SILENT GUIDED INTERVENTION 10 MIN)
// ======================================================
function startHomeMode() {

    state.homeActive = true;
    state.homeTimeLeft = 600;

    const result = get("result");

    result.innerHTML = `
        <div class="card center">
            <h2> </h2>
            <div id="circle" class="breath-circle">●</div>
            <h3 id="breathText">INHALA</h3>
            <p id="timer">10:00</p>
        </div>
    `;

    speak("Comenzamos. Sigue el ritmo de respiración.");

    runBreathing();
    runHomeTimer();
}

// ======================================================
// BREATHING ENGINE
// ======================================================
function runBreathing() {

    let inhale = true;

    const circle = setInterval(() => {

        if (!state.homeActive) return clearInterval(circle);

        const c = get("circle");
        const t = get("breathText");

        if (!c || !t) return;

        if (inhale) {
            c.style.transform = "scale(1.4)";
            t.innerText = "INHALA";
            speak("inhala");
        } else {
            c.style.transform = "scale(0.8)";
            t.innerText = "EXHALA";
            speak("exhala");
        }

        inhale = !inhale;

    }, 4000);
}

// ======================================================
// 10 MIN TIMER (LOCKED FLOW)
// ======================================================
function runHomeTimer() {

    const timer = setInterval(() => {

        if (!state.homeActive) return clearInterval(timer);

        state.homeTimeLeft--;

        const m = Math.floor(state.homeTimeLeft / 60);
        const s = state.homeTimeLeft % 60;

        const el = get("timer");
        if (el) el.innerText = `${m}:${s < 10 ? "0" + s : s}`;

        if (state.homeTimeLeft <= 0) {
            clearInterval(timer);
            finishHomeMode();
        }

    }, 1000);
}

// ======================================================
// HOME END
// ======================================================
function finishHomeMode() {

    state.homeActive = false;

    get("result").innerHTML = `
        <div class="card center">
            <h2>Terminado</h2>
            <p>Vuelve cuando lo necesites.</p>
        </div>
    `;

    speak("Sesión completada. Puedes continuar tu día.");
}

// ======================================================
// STOP HOME
// ======================================================
function stopHomeMode() {
    state.homeActive = false;
}
