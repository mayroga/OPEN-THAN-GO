//////////////////////////////////////////////////////////
// OPEN THAN GO - ENGINE JS v2 (BIOSOCIAL CORE FRONTEND)
// CASA + SALIR + MISSIONS 1–21 + VOICE + BREATH + TIMER
//////////////////////////////////////////////////////////

// ===============================
// GLOBAL STATE
// ===============================
const state = {
    mode: "salir",
    missions: [],
    currentIndex: 0,
    currentMission: null,
    timer: null,
    secondsLeft: 600,
    speaking: false
};

// ===============================
// INIT
// ===============================
window.addEventListener("load", async () => {
    await loadMissions();
    requestWakeLockSafe();
});

// ===============================
// LOAD MISSIONS FROM BACKEND
// ===============================
async function loadMissions() {
    try {
        const res = await fetch("/api/open-than-go", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                decision: "salir",
                estado: "FL",
                zip_code: "",
                budget_level: "cero",
                desahogo: ""
            })
        });

        const data = await res.json();

        // Simulamos pool estable de misiones (fallback robusto)
        state.missions = Array.from({ length: 21 }, (_, i) => ({
            id: i + 1,
            text: `Misión ${i + 1}`
        }));

    } catch (e) {
        console.log("Mission load fallback activated");
        state.missions = Array.from({ length: 21 }, (_, i) => ({
            id: i + 1,
            text: `Misión ${i + 1}`
        }));
    }
}

// ===============================
// MODE SWITCH
// ===============================
function setMode(mode) {
    state.mode = mode;

    const badge = document.getElementById("mode-badge");
    const title = document.getElementById("interactive-title");

    if (mode === "casa") {
        badge.innerText = "Modo: Casa (Reset)";
        badge.className = "mode-badge mode-casa";
        title.innerText = "OPEN ◯ THAN GO";
    } else {
        badge.innerText = "Modo: Salir (Exploración)";
        badge.className = "mode-badge mode-salir";
        title.innerText = "OPEN ◎ THAN GO";
    }
}

// ===============================
// START SYSTEM
// ===============================
async function startOpenThanGo() {

    document.getElementById("form").style.display = "none";
    document.getElementById("loader").style.display = "block";

    const payload = {
        decision: state.mode,
        estado: document.getElementById("inp-state").value,
        zip_code: document.getElementById("inp-zip").value,
        budget_level: document.getElementById("inp-budget").value,
        desahogo: document.getElementById("inp-text").value
    };

    const res = await fetch("/api/open-than-go", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    const data = await res.json();

    document.getElementById("loader").style.display = "none";

    state.currentIndex = 0;

    renderMission(data);
}

// ===============================
// RENDER SYSTEM
// ===============================
function renderMission(data) {

    const result = document.getElementById("result");
    result.innerHTML = "";

    const mission = data.mission;

    const card = document.createElement("div");
    card.className = "card";

    card.innerHTML = `
        <h2>${data.type}</h2>
        <h3>OPEN THAN GO</h3>

        <div class="breath-circle" id="breathCircle">
            RESPIRA
        </div>

        <div class="small">
            Estado emocional: ${data.emotion}
        </div>

        <div style="margin-top:20px;">
            <h3>Misión ${mission?.id || "?"}</h3>
            <p>${mission?.b?.[0]?.story?.es || "Respira y continúa"}</p>
        </div>

        <div id="timerDisplay">10:00</div>

        <button onclick="nextMission()">
            CONTINUAR
        </button>
    `;

    result.appendChild(card);

    speakSpanish(mission?.b?.[0]?.story?.es || "Respira");

    startBreathing();
    startTimer();
}

// ===============================
// BREATHING CIRCLE CONTROL
// ===============================
function startBreathing() {

    const circle = document.getElementById("breathCircle");
    if (!circle) return;

    let scale = 1;

    setInterval(() => {
        if (scale === 1) {
            scale = 1.4;
            circle.style.transform = "scale(1.4)";
        } else {
            scale = 1;
            circle.style.transform = "scale(1)";
        }
    }, 4000);
}

// ===============================
// TIMER PER MISSION (FIXED 10 MIN FLOW)
// ===============================
function startTimer() {

    clearInterval(state.timer);
    state.secondsLeft = 600;

    state.timer = setInterval(() => {

        state.secondsLeft--;

        const min = Math.floor(state.secondsLeft / 60);
        const sec = state.secondsLeft % 60;

        const display = document.getElementById("timerDisplay");
        if (display) {
            display.innerText =
                `${String(min).padStart(2,"0")}:${String(sec).padStart(2,"0")}`;
        }

        if (state.secondsLeft <= 0) {
            nextMission();
        }

    }, 1000);
}

// ===============================
// NEXT MISSION FLOW (1–21 AUTO)
// ===============================
function nextMission() {

    if (state.currentIndex < 20) {
        state.currentIndex++;

        startTimer();

        speakSpanish("Continuamos");

    } else {
        speakSpanish("Has completado el recorrido");
        showEnd();
    }
}

// ===============================
// END SCREEN
// ===============================
function showEnd() {

    const result = document.getElementById("result");

    result.innerHTML = `
        <div class="card center">
            <h2>OPEN THAN GO</h2>
            <p>Sesión completada</p>
            <button onclick="location.reload()">
                Reiniciar
            </button>
        </div>
    `;
}

// ===============================
// VOICE SYSTEM (SPANISH FIXED)
// ===============================
function speakSpanish(text) {

    if (!window.speechSynthesis) return;

    window.speechSynthesis.cancel();

    const utter = new SpeechSynthesisUtterance(text);

    utter.lang = "es-ES";
    utter.rate = 0.95;
    utter.pitch = 1;

    // fuerza voz española si existe
    const voices = speechSynthesis.getVoices();
    const spanishVoice = voices.find(v =>
        v.lang.includes("es")
    );

    if (spanishVoice) {
        utter.voice = spanishVoice;
    }

    speechSynthesis.speak(utter);
}

// ===============================
// WAKE LOCK SAFE
// ===============================
async function requestWakeLockSafe() {
    try {
        if ('wakeLock' in navigator) {
            await navigator.wakeLock.request('screen');
        }
    } catch (e) {
        console.log("WakeLock error");
    }
}
def select_places(profile):
    scored = []

    for place in PLACES_DB:
        score = 0

        if profile["stress"] and "stress" in place["mood"]:
            score += 3

        if profile["fatigue"] and "fatigue" in place["mood"]:
            score += 3

        if profile["monotony"] and "monotony" in place["mood"]:
            score += 3

        if profile["social_need"] and "social_need" in place["mood"]:
            score += 3

        if profile["low_budget"] and place["cost"] == "free":
            score += 2

        scored.append((score, place))

    scored.sort(key=lambda x: x[0], reverse=True)

    # 🔥 IMPORTANTE:
    # 1 destino principal (oculto como “decisión del sistema”)
    main = scored[0][1]

    # + 3 visibles alternativos (no abrumar)
    alternatives = [p[1] for p in scored[1:4]]

    return {
        "selected": main,
        "alternatives": alternatives
    }
