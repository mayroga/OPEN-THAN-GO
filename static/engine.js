// OPEN THAN GO SYSTEM - EMOTION STATE MACHINE v1
// May Roga LLC

// ----------------------------
// GLOBAL STATE (CEREBRO DEL SISTEMA)
// ----------------------------
const state = {
    lang: "es",
    mode: "salir", // casa | salir
    budget: "cero",
    emotion: {
        stress: false,
        monotony: false,
        lowEnergy: false
    },
    step: 0,
    steps: [],
    location: null,
    recommendations: [],
    speaking: false
};

// ----------------------------
// HELPERS
// ----------------------------
function $(id) {
    return document.getElementById(id);
}

// ----------------------------
// VOZ NATURAL
// ----------------------------
function speak(text) {
    if (!("speechSynthesis" in window)) return;
    if (!text) return;

    const u = new SpeechSynthesisUtterance(text);
    const voices = speechSynthesis.getVoices();

    let voice =
        state.lang === "es"
            ? voices.find(v => v.lang?.startsWith("es")) || voices[0]
            : voices.find(v => v.lang?.startsWith("en")) || voices[0];

    u.voice = voice;
    u.lang = state.lang === "es" ? "es-ES" : "en-US";
    u.rate = 0.95;
    u.pitch = 1;

    speechSynthesis.cancel();
    speechSynthesis.speak(u);
}

// ----------------------------
// SAFE TEXT
// ----------------------------
function t(v) {
    if (!v) return "";
    if (typeof v === "string") return v;
    return v[state.lang] || v.es || v.en || "";
}

// ----------------------------
// TITLE STATE ENGINE (OPEN THAN GO FEELING)
// ----------------------------
function updateTitle() {

    const el = $("app-title") || document.querySelector("h1");
    if (!el) return;

    let base = "OPEN THAN GO";

    if (state.emotion.stress) base = "OPEN ◉ THAN GO";
    if (state.emotion.monotony) base = "OPEN — THAN GO";
    if (state.emotion.lowEnergy) base = "OPEN ○ THAN GO";

    if (state.mode === "casa") base = "OPEN ◯ THAN GO";
    if (state.mode === "salir") base = "OPEN ◎ THAN GO";

    el.innerText = base;
    animateTitle(el);
}

// ----------------------------
// TITLE ANIMATION (SENSACIÓN VIVA)
// ----------------------------
function animateTitle(el) {

    el.style.transition = "all 0.6s ease";

    if (state.mode === "salir") {
        el.style.transform = "scale(1.03)";
        el.style.letterSpacing = "2px";
    } else {
        el.style.transform = "scale(0.98)";
        el.style.letterSpacing = "0px";
    }

    if (state.emotion.stress) el.style.color = "#d84315";
    else if (state.emotion.monotony) el.style.color = "#6ec6ff";
    else el.style.color = "#1e3a1e";
}

// ----------------------------
// INIT
// ----------------------------
document.addEventListener("DOMContentLoaded", () => {
    $("btn-start").onclick = requestEmotionRoute;
    updateTitle();
});

// ----------------------------
// UI CONTROLS
// ----------------------------
function changeLang(lang) {
    state.lang = lang;
    $("lang-es")?.classList.toggle("active", lang === "es");
    $("lang-en")?.classList.toggle("active", lang === "en");
}

function setBudget(v) {
    state.budget = v;

    ["cero", "minimo", "moderado", "libre"].forEach(x => {
        $("b-" + x)?.classList.toggle("active", x === v);
    });
}

function setMode(isOut) {
    state.mode = isOut ? "salir" : "casa";

    $("m-salir")?.classList.toggle("active", isOut);
    $("m-casa")?.classList.toggle("active", !isOut);

    updateTitle();
}

// ----------------------------
// EMOTION PARSER (FRONT LAYER)
// ----------------------------
function parseEmotion(text) {
    const t = (text || "").toLowerCase();

    state.emotion.stress =
        t.includes("trabajo") || t.includes("estres") || t.includes("ansiedad");

    state.emotion.monotony =
        t.includes("aburrido") || t.includes("rutina") || t.includes("igual");

    state.emotion.lowEnergy =
        t.includes("cansado") || t.includes("agotado") || t.includes("sin energia");
}

// ----------------------------
// MAIN REQUEST (EMOTION ROUTER CALL)
// ----------------------------
async function requestEmotionRoute() {

    const payload = {
        decision: state.mode,
        budget_level: state.budget,
        lang: state.lang,
        desahogo: $("inp-text")?.value || "",
        zip_code: $("inp-zip")?.value || "",
        estado: $("inp-state")?.value || "",
        region: $("inp-region")?.value || ""
    };

    parseEmotion(payload.desahogo);
    updateTitle();

    $("wrapper-form").style.display = "none";
    $("wrapper-loader").style.display = "flex";

    try {

        const res = await fetch("/api/open-than-go", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!data || data.status !== "success") throw new Error("API error");

        setTimeout(() => {

            $("wrapper-loader").style.display = "none";
            $("wrapper-interactive").style.display = "block";

            state.steps = data.mission?.b || [];
            state.recommendations = data.recommendations || [];
            state.location = data.lugar || null;
            state.step = 0;

            runFlow();

        }, 400);

    } catch (e) {
        console.error(e);
        alert("Error de conexión");
        $("wrapper-form").style.display = "block";
    }
}

// ----------------------------
// FLOW ENGINE (CASA vs SALIR)
// ----------------------------
function runFlow() {

    speechSynthesis.cancel();

    const container = $("step-content");
    const btnNext = ensureNext();

    // END
    if (state.step >= state.steps.length) {

        if (state.mode === "salir") {
            showExitOptions();
        } else {
            btnNext.innerText = "FINALIZAR";
            btnNext.style.display = "block";
            btnNext.onclick = () => location.reload();
        }
        return;
    }

    const step = state.steps[state.step];

    btnNext.onclick = () => {
        state.step++;
        runFlow();
    };

    // CASA MODE = simple + respiración
    if (state.mode === "casa") {
        if (step.t === "breath_auto") {
            startBreathing(step.d || 10);
            return;
        }
    }

    const text = step.tx || step.story || step;

    container.innerHTML = `<div>${t(text)}</div>`;
    speak(t(text));

    btnNext.style.display = "block";
    updateTitle();
}

// ----------------------------
// BREATHING (CASA RESET)
// ----------------------------
function startBreathing(seconds) {

    const container = $("step-content");
    let s = seconds;

    container.innerHTML = `
        <div style="text-align:center;">
            <div id="breathingCircle"></div>
            <h3 id="breathText">Inhala</h3>
            <p id="breathTime"></p>
        </div>
    `;

    let grow = true;
    let r = 1;

    const interval = setInterval(() => {

        const circle = $("breathingCircle");

        if (circle) {
            r += grow ? 0.02 : -0.02;
            if (r > 1.3) grow = false;
            if (r < 0.9) grow = true;

            circle.style.transform = `scale(${r})`;
        }

        $("breathText").innerText = grow ? "Inhala" : "Exhala";
        $("breathTime").innerText = s + "s";

        s--;

        if (s <= 0) {
            clearInterval(interval);
            state.step++;
            runFlow();
        }

    }, 1000);
}

// ----------------------------
// EXIT MODE (SALIR = GUIADO)
// ----------------------------
function showExitOptions() {

    const container = $("step-content");
    container.innerHTML = "";

    const list = state.recommendations || [];

    let html = `<h3>Tu ruta recomendada</h3>`;

    list.slice(0, 3).forEach(r => {
        html += `
            <div class="card-box">
                <strong>${r}</strong>
            </div>
        `;
    });

    if (state.location?.gps_link) {
        html += `
            <a href="${state.location.gps_link}" target="_blank" class="btn-maps-route" style="display:block">
                ABRIR RUTA
            </a>
        `;
    }

    container.innerHTML = html;

    updateTitle();
}

// ----------------------------
// SAFE BUTTONS
// ----------------------------
function ensureNext() {
    let b = $("btn-next");
    if (!b) {
        b = document.createElement("button");
        b.id = "btn-next";
        b.className = "btn-next-step";
        $("wrapper-interactive").appendChild(b);
    }
    return b;
}
