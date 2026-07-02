// OPEN THAN GO SYSTEM - EMOTIONAL STATE MACHINE v2
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
// SAFE GET
// ------------------------------
const $ = (id) => document.getElementById(id);

// ------------------------------
// INIT
// ------------------------------
document.addEventListener("DOMContentLoaded", () => {
    $("btn-start").onclick = startFlow;
});

// ------------------------------
// EMOTION PARSER
// ------------------------------
function parseEmotion(text) {
    if (!text) return;

    const t = text.toLowerCase();

    state.emotion.stress = ["estres", "trabajo", "ansiedad", "presión"].some(w => t.includes(w));
    state.emotion.monotony = ["aburrido", "rutina", "igual", "monotonía"].some(w => t.includes(w));
    state.emotion.lowEnergy = ["cansado", "agotado", "sin energia", "fatiga"].some(w => t.includes(w));
    state.emotion.desireToBeGuided = ["decidir", "elige", "no quiero pensar", "guíame"].some(w => t.includes(w));
}

// ------------------------------
// TITLE SYSTEM (VIVO)
// ------------------------------
function updateTitle() {

    const el = $("app-title");
    if (!el) return;

    let base = "OPEN THAN GO";

    // ESTADO EMOCIONAL
    if (state.emotion.stress) {
        base = "OPEN ◉ THAN GO";
    }

    if (state.emotion.monotony) {
        base = "OPEN — THAN GO";
    }

    if (state.emotion.lowEnergy) {
        base = "OPEN ○ THAN GO";
    }

    // MODO CASA = INTERIOR (RECOGIMIENTO / REGULACIÓN)
    if (state.mode === "casa") {
        base = "OPEN ◯ THAN GO";
    }

    // MODO SALIR = EXPANSIÓN / DECISIÓN EXTERNA
    if (state.mode === "salir") {
        base = "OPEN ◎ THAN GO";
    }

    el.innerText = base;

    animateTitle(el);
}

// ------------------------------
// TITLE ANIMATION (SENSACIÓN VIVA)
// ------------------------------
function animateTitle(el) {

    el.style.transition = "all 0.6s ease";

    // expansión vs interior
    if (state.mode === "salir") {
        el.style.letterSpacing = "2px";
        el.style.transform = "scale(1.02)";
    } else {
        el.style.letterSpacing = "0px";
        el.style.transform = "scale(0.98)";
    }

    // color emocional
    if (state.emotion.stress) {
        el.style.color = "#d84315";
    } else if (state.emotion.monotony) {
        el.style.color = "#6ec6ff";
    } else if (state.emotion.lowEnergy) {
        el.style.color = "#90a4ae";
    } else {
        el.style.color = "#1e3a1e";
    }
}

// ------------------------------
// MODE CONTROL (SIGNIFICADO REAL)
// ------------------------------
function setMode(isOut) {

    state.mode = isOut ? "salir" : "casa";

    $("m-salir")?.classList.toggle("active", isOut);
    $("m-casa")?.classList.toggle("active", !isOut);

    // SIGNIFICADO PROFUNDO:

    // CASA:
    // - reducción de estímulo
    // - respiración + regulación
    // - no decisiones externas
    // - reordenamiento interno

    // SALIR:
    // - expansión cognitiva
    // - decisiones guiadas
    // - 3 opciones externas siempre
    // - movimiento + acción

    updateTitle();
}

// ------------------------------
// POCKET CONTROL
// ------------------------------
function setPocket(p) {
    state.pocket = p;

    ["cero", "minimo", "moderado", "libre"].forEach(v => {
        $("b-" + v)?.classList.toggle("active", v === p);
    });
}

// ------------------------------
// LANGUAGE
// ------------------------------
function setLang(l) {
    state.lang = l;

    $("lang-es")?.classList.toggle("active", l === "es");
    $("lang-en")?.classList.toggle("active", l === "en");
}

// ------------------------------
// MAIN START
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

    updateTitle();

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

            updateTitle();
            runState();

        }, 400);

    } catch (e) {
        console.error(e);
        alert("Error de conexión");
        $("wrapper-form").style.display = "block";
    }
}

// ------------------------------
// STATE ENGINE CORE
// ------------------------------
function runState() {

    clearTimers();
    speechSynthesis.cancel();

    const container = $("step-content");
    const nextBtn = ensureNext();
    const mapBtn = ensureMap();

    updateTitle();

    if (state.stepIndex >= state.mission.length) {
        handleEnd(nextBtn, mapBtn);
        return;
    }

    const step = state.mission[state.stepIndex];

    nextBtn.onclick = () => {
        state.stepIndex++;
        runState();
    };

    if (step.t === "breath_auto") {
        runBreathing(step.d || 10);
        return;
    }

    if (state.mode === "casa") {
        runHomeMode();
    }

    const content = step.tx || step.story || step;
    container.innerHTML = `<div class="fade">${t(content)}</div>`;

    speak(t(content));

    nextBtn.style.display = "block";
}

// ------------------------------
// HOME MODE (REGULACIÓN INTERNA)
// ------------------------------
function runHomeMode() {
    if (!state.timers.session) {
        state.timers.session = setInterval(() => {
            // espacio futuro: micro-instrucciones de regulación
        }, 10000);
    }
}

// ------------------------------
// BREATH STATE
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

function clearTimers() {
    if (state.timers.breath) clearInterval(state.timers.breath);
    if (state.timers.session) clearInterval(state.timers.session);
}
