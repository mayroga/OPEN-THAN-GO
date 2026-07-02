// OPEN THAN GO SYSTEM - EMOTIONAL STATE MACHINE v1
// May Roga LLC

// ------------------------------
// GLOBAL STATE
// ------------------------------
let state = {
    lang: "es",
    pocket: "cero",
    mode: "salir", // salir | casa

    stepIndex: 0,
    mission: [],
    place: null,
    escapeType: "",

    emotion: {
        stress: false,
        monotony: false,
        lowEnergy: false,
        desireToBeGuided: false
    },

    timers: {
        breath: null,
        session: null
    }
};

// ------------------------------
// SAFE DOM
// ------------------------------
const $ = (id) => document.getElementById(id);

// ------------------------------
// EMOTION PARSER (CLIENT SIDE MIRROR)
// ------------------------------
function parseEmotion(text) {
    if (!text) return;

    const t = text.toLowerCase();

    state.emotion.stress = ["estres", "trabajo", "ansiedad", "presión"].some(w => t.includes(w));
    state.emotion.monotony = ["aburrido", "rutina", "igual"].some(w => t.includes(w));
    state.emotion.lowEnergy = ["cansado", "agotado", "sin energia"].some(w => t.includes(w));
    state.emotion.desireToBeGuided = ["decidir", "elige", "no quiero pensar"].some(w => t.includes(w));
}

// ------------------------------
// SPEECH (GUIDED VOICE)
// ------------------------------
function speak(text) {
    if (!("speechSynthesis" in window)) return;

    const u = new SpeechSynthesisUtterance(text);
    const voices = speechSynthesis.getVoices();

    let voice =
        state.lang === "es"
            ? voices.find(v => v.lang?.startsWith("es"))
            : voices.find(v => v.lang?.startsWith("en"));

    u.voice = voice || voices[0];
    u.lang = state.lang === "es" ? "es-ES" : "en-US";
    u.rate = state.emotion.stress ? 0.9 : 0.95;
    u.pitch = 1;

    speechSynthesis.cancel();
    speechSynthesis.speak(u);
}

// ------------------------------
// TEXT SAFE
// ------------------------------
function t(p) {
    if (!p) return "";
    if (typeof p === "string") return p;
    return p[state.lang] || p.es || p.en || "";
}

// ------------------------------
// INIT
// ------------------------------
document.addEventListener("DOMContentLoaded", () => {
    $("btn-start").onclick = startFlow;
});

// ------------------------------
// UPDATE SETTINGS
// ------------------------------
function setLang(l) {
    state.lang = l;
    $("lang-es")?.classList.toggle("active", l === "es");
    $("lang-en")?.classList.toggle("active", l === "en");
}

function setPocket(p) {
    state.pocket = p;
    ["cero", "minimo", "moderado", "libre"].forEach(v => {
        $("b-" + v)?.classList.toggle("active", v === p);
    });
}

function setMode(isOut) {
    state.mode = isOut ? "salir" : "casa";
    $("m-salir")?.classList.toggle("active", isOut);
    $("m-casa")?.classList.toggle("active", !isOut);
}

// ------------------------------
// MAIN REQUEST
// ------------------------------
async function startFlow() {

    const payload = {
        decision: state.mode,
        lang: state.lang,
        budget_level: state.pocket,
        zip_code: $("inp-zip")?.value || "",
        estado: $("inp-state")?.value || "",
        region: $("inp-region")?.value || "",
        desahogo: $("inp-text")?.value || ""
    };

    parseEmotion(payload.desahogo);

    $("wrapper-form").style.display = "none";
    $("wrapper-loader").style.display = "flex";
    $("wrapper-interactive").style.display = "none";

    try {
        const res = await fetch("/api/open-than-go", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!data || data.status !== "success") throw new Error("backend error");

        setTimeout(() => {

            $("wrapper-loader").style.display = "none";
            $("wrapper-interactive").style.display = "block";

            state.mission = data.mission?.b || [];
            state.place = data.place || null;
            state.escapeType = data.type || "";

            state.stepIndex = 0;

            runState();

        }, 400);

    } catch (e) {
        console.error(e);
        alert("Error de conexión");
        $("wrapper-form").style.display = "block";
    }
}

// ------------------------------
// STATE MACHINE CORE
// ------------------------------
function runState() {

    clearAllTimers();
    speechSynthesis.cancel();

    const container = $("step-content");
    const nextBtn = ensureNext();
    const mapBtn = ensureMap();

    // END
    if (state.stepIndex >= state.mission.length) {
        handleEnd(nextBtn, mapBtn);
        return;
    }

    const step = state.mission[state.stepIndex];

    nextBtn.onclick = () => {
        state.stepIndex++;
        runState();
    };

    // -------------------------
    // BREATH STATE
    // -------------------------
    if (step.t === "breath_auto") {
        runBreathing(step.d || 10);
        return;
    }

    // -------------------------
    // HOME MODE = SIMPLE LOOP
    // -------------------------
    if (state.mode === "casa") {
        runHomeSession();
    }

    const content = t(step.tx || step.story || step);
    container.innerHTML = `<div class="fade">${content}</div>`;

    speak(content);

    nextBtn.style.display = "block";
}

// ------------------------------
// HOME FLOW (LOW LOAD)
// ------------------------------
function runHomeSession() {
    if (!state.timers.session) {
        state.timers.session = setInterval(() => {
            // passive grounding loop (future extension)
        }, 10000);
    }
}

// ------------------------------
// BREATH STATE (ADAPTIVE)
// ------------------------------
function runBreathing(seconds) {

    const c = $("step-content");
    let s = seconds;

    c.innerHTML = `
        <div class="breath-ui">
            <div id="breathCircle"></div>
            <h2 id="breathText">Inhala</h2>
            <div id="breathTime"></div>
        </div>
    `;

    const circle = $("breathCircle");

    let grow = true;
    let scale = 1;

    state.timers.breath = setInterval(() => {

        scale += grow ? 0.03 : -0.03;
        if (scale > 1.4) grow = false;
        if (scale < 0.9) grow = true;

        circle.style.transform = `scale(${scale})`;

        $("breathText").innerText = grow ? "Inhala" : "Exhala";
        $("breathTime").innerText = s + "s";

        s--;

        if (s <= 0) {
            clearInterval(state.timers.breath);
            state.stepIndex++;
            runState();
        }

    }, 1000);
}

// ------------------------------
// END STATE
// ------------------------------
function handleEnd(nextBtn, mapBtn) {

    if (state.escapeType === "Salida") {
        mapBtn.style.display = "block";
        mapBtn.href = state.place?.gps_link || "#";
        return;
    }

    nextBtn.style.display = "block";
    nextBtn.innerText = "FINALIZAR";
    nextBtn.onclick = () => location.reload();
}

// ------------------------------
// HELPERS
// ------------------------------
function ensureNext() {
    let b = $("btn-next");
    if (!b) {
        b = document.createElement("button");
        b.id = "btn-next";
        b.className = "btn-next-step";
        $("wrapper-interactive").appendChild(b);
    }
    b.style.display = "none";
    b.innerText = "CONTINUAR";
    return b;
}

function ensureMap() {
    let b = $("btn-maps-action");
    if (!b) {
        b = document.createElement("a");
        b.id = "btn-maps-action";
        b.className = "btn-maps-route";
        $("wrapper-interactive").appendChild(b);
    }
    b.style.display = "none";
    b.innerText = "ABRIR MAPA";
    return b;
}

function clearAllTimers() {
    if (state.timers.breath) clearInterval(state.timers.breath);
    if (state.timers.session) clearInterval(state.timers.session);
}
