// OPEN THAN GO SYSTEM - FRONTEND ENGINE v6 STABLE
// FIX: no freeze / no interval stacking / safe voice queue

let idiomaActual = "es";
let presupuestoActual = "cero";
let modalidadSalir = true;

let pasosMisionGlobal = [];
let indicePasoActual = 0;
let datosLugarGlobal = null;
let tipoEscapeGlobal = "";

let breathInterval = null;
let timerInterval = null;

let tiempoTotal = 0;
let tiempoRestante = 0;

let lockAvance = false;

// ---------------- SAFE GET ----------------
const get = (id) => document.getElementById(id);

// ---------------- VOZ (ANTI FREEZE QUEUE) ----------------
let voiceQueue = [];
let speaking = false;

function hablar(texto, delay = 0) {
    if (!("speechSynthesis" in window)) return;
    if (!texto) return;

    voiceQueue.push({ texto, delay });

    if (speaking) return;
    procesarVoz();
}

function procesarVoz() {
    if (voiceQueue.length === 0) {
        speaking = false;
        return;
    }

    speaking = true;
    const { texto, delay } = voiceQueue.shift();

    setTimeout(() => {
        const u = new SpeechSynthesisUtterance(texto);
        const voces = speechSynthesis.getVoices();

        let voice =
            (idiomaActual === "es"
                ? voces.find(v => v.lang?.startsWith("es"))
                : voces.find(v => v.lang?.startsWith("en")))
            || voces[0];

        u.voice = voice;
        u.lang = idiomaActual === "es" ? "es-ES" : "en-US";
        u.rate = 0.9;

        u.onend = () => {
            speaking = false;
            procesarVoz();
        };

        speechSynthesis.speak(u);

    }, delay);
}

// ---------------- INIT ----------------
document.addEventListener("DOMContentLoaded", () => {
    get("btn-start")?.addEventListener("click", solicitarEscape);
});

// ---------------- UI ----------------
function showLoader() {
    get("wrapper-form").style.display = "none";
    get("wrapper-loader").style.display = "flex";
    get("wrapper-interactive").style.display = "none";
}

function showApp() {
    get("wrapper-loader").style.display = "none";
    get("wrapper-interactive").style.display = "block";
}

// ---------------- FETCH ----------------
async function solicitarEscape() {

    showLoader();

    const payload = {
        decision: modalidadSalir ? "salir" : "casa",
        lang: idiomaActual,
        budget_level: presupuestoActual,
        zip_code: get("inp-zip")?.value || "",
        estado: get("inp-state")?.value || "",
        desahogo: get("inp-text")?.value || ""
    };

    try {
        const res = await fetch("/api/open-than-go", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!data?.mision) throw new Error("bad backend");

        pasosMisionGlobal = data.mision.b || [];
        datosLugarGlobal = data.lugar || null;
        tipoEscapeGlobal = data.tipo || "";

        indicePasoActual = 0;

        tiempoTotal = tipoEscapeGlobal === "Casa" ? 600 : 60;
        tiempoRestante = tiempoTotal;

        showApp();
        iniciarFlujo();

    } catch (e) {
        console.error(e);
        alert("Error servidor");
        get("wrapper-form").style.display = "block";
    }
}

// ---------------- FLOW CORE ----------------
function iniciarFlujo() {

    clearInterval(timerInterval);
    clearInterval(breathInterval);

    const cont = get("step-content");
    const btn = ensureNext();
    const map = ensureMap();

    if (tiempoRestante <= 0 || indicePasoActual >= pasosMisionGlobal.length) {
        finalizar(btn, map);
        return;
    }

    const paso = pasosMisionGlobal[indicePasoActual];

    btn.onclick = () => {
        if (lockAvance) return;
        indicePasoActual++;
        iniciarFlujo();
    };

    // BREATH MODE (ISOLATED)
    if (paso.t === "breath_auto") {
        iniciarRespiracion(paso.d || 10);
        return;
    }

    if (tipoEscapeGlobal === "Casa") iniciarTimer();

    const texto = paso.tx?.es || paso.story?.es || "";

    cont.innerHTML = `<div>${texto}</div>`;

    hablar(texto);

    tiempoRestante -= 5;
    btn.style.display = "block";
}

// ---------------- BREATH SAFE (NO UI BLOCK) ----------------
function iniciarRespiracion(seg) {

    const cont = get("step-content");
    let s = seg;

    lockAvance = true;

    cont.innerHTML = `
        <div>
            <div id="breathingCircle"></div>
            <h2 id="breathLabel">Inhala</h2>
        </div>
    `;

    const circle = get("breathingCircle");

    breathInterval = setInterval(() => {

        if (s <= 0) {
            clearInterval(breathInterval);
            lockAvance = false;
            indicePasoActual++;
            iniciarFlujo();
            return;
        }

        const phase = s % 2 === 0 ? "Inhala" : "Exhala";

        get("breathLabel").innerText = phase;

        if (circle) {
            circle.style.transform = phase === "Inhala"
                ? "scale(1.3)"
                : "scale(0.95)";
        }

        if (s % 3 === 0) hablar(phase);

        s--;
        tiempoRestante--;

    }, 1000);
}

// ---------------- TIMER SAFE ----------------
function iniciarTimer() {

    if (timerInterval) return;

    const t = get("timer");

    timerInterval = setInterval(() => {

        if (tiempoRestante <= 0) {
            clearInterval(timerInterval);
            return;
        }

        const m = Math.floor(tiempoRestante / 60);
        const s = tiempoRestante % 60;

        if (t) t.innerText = `${m}:${s.toString().padStart(2, "0")}`;

        tiempoRestante--;

    }, 1000);
}

// ---------------- FINAL ----------------
function finalizar(btn, map) {

    get("step-content").innerHTML =
        `<div><h2>Sesión lista</h2></div>`;

    if (tipoEscapeGlobal === "Salida") {
        map.style.display = "block";
        map.href = datosLugarGlobal?.gps_link || "#";
    } else {
        btn.innerText = "REINICIAR";
        btn.style.display = "block";
        btn.onclick = () => location.reload();
    }
}

// ---------------- SAFE BUTTONS ----------------
function ensureNext() {
    let b = get("btn-next");
    if (!b) {
        b = document.createElement("button");
        b.id = "btn-next";
        get("wrapper-interactive").appendChild(b);
    }
    b.innerText = "CONTINUAR";
    b.style.display = "none";
    return b;
}

function ensureMap() {
    let b = get("btn-maps-action");
    if (!b) {
        b = document.createElement("a");
        b.id = "btn-maps-action";
        get("wrapper-interactive").appendChild(b);
    }
    b.innerText = "MAPA";
    b.style.display = "none";
    return b;
}
