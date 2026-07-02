// OPEN THAN GO SYSTEM - ENGINE v6 (USA 50 STATES READY)
// May Roga LLC

let state = {
    mode: "salir",
    emotion: {
        stress: false,
        monotony: false,
        lowEnergy: false
    }
};

let idiomaActual = "es";
let presupuestoActual = "cero";

let pasos = [];
let index = 0;
let lugar = null;

// ------------------ SAFE GET ------------------
function $(id) {
    return document.getElementById(id);
}

// ------------------ EMOTION SYNC ------------------
function syncEmotion(text) {
    const t = (text || "").toLowerCase();

    state.emotion.stress =
        t.includes("estres") || t.includes("trabajo") || t.includes("presion");

    state.emotion.monotony =
        t.includes("aburrido") || t.includes("rutina") || t.includes("igual");

    state.emotion.lowEnergy =
        t.includes("cansado") || t.includes("sin energia") || t.includes("agotado");

    updateTitle();
}

// ------------------ TITLE EMOTION CORE ------------------
function updateTitle() {
    const el = $("interactive-title") || $("txt-subtitle");
    if (!el) return;

    let base = "OPEN THAN GO";

    if (state.emotion.stress) base = "OPEN ◉ THAN GO";
    else if (state.emotion.monotony) base = "OPEN — THAN GO";
    else if (state.emotion.lowEnergy) base = "OPEN ○ THAN GO";

    if (state.mode === "casa") base = "OPEN ◯ THAN GO";
    if (state.mode === "salir") base = "OPEN ◎ THAN GO";

    el.innerText = base;
    animateTitle(el);
}

// ------------------ TITLE ANIMATION ------------------
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

// ------------------ BREATHING (CASA VS SALIR) ------------------
function breathingCycle() {
    const circle = $("breathingCircle");
    const label = $("breathLabel");

    if (!circle) return;

    let inhale = true;

    setInterval(() => {

        // CASA = terapia real
        if (state.mode === "casa") {
            circle.style.transform = inhale ? "scale(1.4)" : "scale(0.85)";
            label.innerText = inhale ? "Inhala" : "Exhala";
        }

        // SALIR = micro-calma
        else {
            circle.style.transform = "scale(1.08)";
            label.innerText = "Observa y suelta";
        }

        inhale = !inhale;

    }, 2000);
}

// ------------------ BUDGET VISUAL ------------------
function showBudget(level) {
    const map = {
        cero: "$0 - $40 (Base USA Low Cost)",
        minimo: "$20 - $60",
        moderado: "$40 - $70",
        libre: "Sin límite"
    };
    return map[level] || "$0 - $40";
}

// ------------------ GOOGLE MAP FIX (USA REAL + ZIP + STATE) ------------------
function buildMap(place, stateCode, zip) {

    let query = "";

    if (place) query += place + " ";
    if (stateCode) query += stateCode + " USA ";
    if (zip) query += zip;

    return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(query)}`;
}

// ------------------ INIT ------------------
document.addEventListener("DOMContentLoaded", () => {

    $("btn-start").onclick = start;

    // default mode sync
    window.cambiarModalidad = function(isOut) {
        state.mode = isOut ? "salir" : "casa";
        updateTitle();
    };

    breathingCycle();
    updateTitle();
});

// ------------------ START FLOW ------------------
async function start() {

    const payload = {
        decision: state.mode,
        budget_level: presupuestoActual,
        desahogo: $("inp-text").value,
        zip_code: $("inp-zip").value,
        estado: $("inp-state").value,
        region: $("inp-region").value
    };

    $("wrapper-form").style.display = "none";
    $("wrapper-loader").style.display = "block";

    const res = await fetch("/api/open-than-go", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const data = await res.json();

    syncEmotion(payload.desahogo);

    $("wrapper-loader").style.display = "none";
    $("wrapper-interactive").style.display = "block";

    pasos = data.mission?.b || [];

    // FIX: ahora usa recommendations reales del backend
    lugar = data.recommendations || null;

    index = 0;

    render();
}

// ------------------ RENDER FLOW ------------------
function render() {

    updateTitle();

    const btn = $("btn-next");
    const mapBtn = $("btn-maps-action");

    // ---------------- CASA MODE ----------------
    if (state.mode === "casa") {

        $("step-content").innerHTML = `
            <h3>Modo Casa (Reset emocional)</h3>
            <p>Respiración + enfoque mental</p>
            <p>Duración: 10 min</p>
        `;

        btn.style.display = "block";
        btn.innerText = "INICIAR RESPIRACIÓN";

        btn.onclick = () => {
            $("breathingCircle").scrollIntoView({ behavior: "smooth" });
        };

        return;
    }

    // ---------------- SALIR MODE ----------------
    if (index >= pasos.length) {

        const zip = $("inp-zip").value;
        const st = $("inp-state").value;

        if (lugar && Array.isArray(lugar)) {

            // FIX USA: SIEMPRE 3 OPCIONES REALES
            $("step-content").innerHTML = lugar.map((l, i) => `
                <div style="margin-bottom:12px;">
                    <h3>${l}</h3>
                    <p>💵 ${showBudget(presupuestoActual)}</p>
                    <button onclick="window.open('${buildMap(l, st, zip)}','_blank')">
                        IR AQUÍ
                    </button>
                </div>
            `).join("");

            btn.style.display = "none";
        }

        return;
    }

    const step = pasos[index];

    $("step-content").innerHTML =
        step.story?.es || step.tx || "..."

    speak(step.story?.es || "");

    btn.style.display = "block";
    btn.innerText = "CONTINUAR";

    btn.onclick = () => {
        index++;
        render();
    };
}

// ------------------ SPEAK ------------------
function speak(text) {
    if (!("speechSynthesis" in window)) return;
    const u = new SpeechSynthesisUtterance(text || "");
    speechSynthesis.cancel();
    speechSynthesis.speak(u);
}
