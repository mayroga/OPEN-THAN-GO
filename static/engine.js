// OPEN THAN GO SYSTEM - ENGINE v5 (EMOTION CORE)

let state = {
    function syncEmotion(text){

    const t = (text || "").toLowerCase();

    state.emotion.stress =
        t.includes("estres") || t.includes("trabajo");

    state.emotion.monotony =
        t.includes("aburrido") || t.includes("rutina");

    state.emotion.lowEnergy =
        t.includes("cansado") || t.includes("energia");

    updateTitle();
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

// ------------------ TITLE EMOTION ------------------
function updateTitle() {
    const el = $("interactive-title");
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

// ------------------ BREATHING REAL ------------------
function breathingCycle() {
    const circle = $("breathingCircle");
    const label = $("breathLabel");

    if (!circle) return;

    let inhale = true;

    setInterval(() => {
        if (state.mode === "casa") {
            circle.style.transform = inhale ? "scale(1.35)" : "scale(0.9)";
            label.innerText = inhale ? "Inhala" : "Exhala";
        } else {
            circle.style.transform = "scale(1.05)";
            label.innerText = "Observa";
        }
        inhale = !inhale;
    }, 2200);
}

// ------------------ PRESUPUESTO ------------------
function showBudget(level) {
    const map = {
        cero: "$0 - $40",
        minimo: "$20 - $60",
        moderado: "$40 - $70",
        libre: "Sin límite"
    };
    return map[level] || "$0 - $40";
}

// ------------------ MAP LINK REAL ------------------
function buildMap(place) {
    return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(place)}`;
}

// ------------------ START ------------------
document.addEventListener("DOMContentLoaded", () => {
    $("btn-start").onclick = start;
    breathingCycle();
    updateTitle();
});

// ------------------ MAIN FLOW ------------------
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
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    const data = await res.json();
    syncEmotion(payload.desahogo);

    $("wrapper-loader").style.display = "none";
    $("wrapper-interactive").style.display = "block";

    pasos = data.mission?.b || [];
    lugar = data.lugar || null;
    index = 0;

    render();
}

// ------------------ RENDER ------------------
function render() {

    updateTitle();

    if (index >= pasos.length) {

        if (state.mode === "salir" && lugar) {

            const mapBtn = $("btn-maps-action");
            mapBtn.style.display = "block";
            mapBtn.href = buildMap(lugar.name);

            $("step-content").innerHTML =
                `<div>
                    <h3>Tu destino</h3>
                    <p>${lugar.name}</p>
                    <p>💵 ${showBudget(presupuestoActual)}</p>
                 </div>`;
        }

        return;
    }

    const step = pasos[index];

    $("step-content").innerHTML = step.story?.es || step.tx || "";

    speak(step.story?.es || "");

    $("btn-next").style.display = "block";
    $("btn-next").onclick = () => {
        index++;
        render();
    };
}

// ------------------ SPEAK ------------------
function speak(text) {
    if (!("speechSynthesis" in window)) return;
    const u = new SpeechSynthesisUtterance(text);
    speechSynthesis.cancel();
    speechSynthesis.speak(u);
}

// ------------------ MODE ------------------
function cambiarModalidad(isOut) {
    state.mode = isOut ? "salir" : "casa";
    updateTitle();
}

// ------------------ EMOTION SIMPLE ------------------
function detectEmotion(text) {

    text = (text || "").toLowerCase();

    state.emotion.stress = text.includes("estres") || text.includes("trabajo");
    state.emotion.monotony = text.includes("aburrido") || text.includes("rutina");
    state.emotion.lowEnergy = text.includes("cansado") || text.includes("energia baja");

    updateTitle();
}
