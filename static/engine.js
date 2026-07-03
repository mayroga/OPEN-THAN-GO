// OPEN THAN GO SYSTEM - ENGINE v7 STABLE CORE
// FIX: NO FREEZE / NO BLOCK UI / SAFE VOICE + SAFE FLOW

let idiomaActual = "es";
let presupuestoActual = "cero";
let modalidadSalir = true;

let pasos = [];
let i = 0;

let lugar = null;
let tipo = "";

let breath = null;
let timer = null;

let tiempo = 0;
let bloqueo = false;

// ---------------- DOM ----------------
const get = (id) => document.getElementById(id);

// ---------------- VOZ ULTRA SAFE (NO CANCEL LOOP) ----------------
function hablar(texto) {
    if (!texto || !("speechSynthesis" in window)) return;

    // NO cancelamos constantemente (esto era el freeze)
    const u = new SpeechSynthesisUtterance(texto);

    const voces = speechSynthesis.getVoices();
    const v =
        (idiomaActual === "es"
            ? voces.find(x => x.lang?.startsWith("es"))
            : voces.find(x => x.lang?.startsWith("en")))
        || voces[0];

    u.voice = v;
    u.lang = idiomaActual === "es" ? "es-ES" : "en-US";
    u.rate = 0.92;

    // pequeño delay natural evita saturación
    setTimeout(() => speechSynthesis.speak(u), 120);
}

// ---------------- INIT ----------------
document.addEventListener("DOMContentLoaded", () => {
    get("btn-start")?.addEventListener("click", start);
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
async function start() {

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
        const r = await fetch("/api/open-than-go", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const d = await r.json();

        if (!d?.mision) throw new Error("bad backend");

        pasos = d.mision.b || [];
        lugar = d.lugar;
        tipo = d.tipo;

        i = 0;
        tiempo = tipo === "Casa" ? 600 : 60;

        showApp();
        loop();

    } catch (e) {
        console.error(e);
        alert("Error servidor");
        get("wrapper-form").style.display = "block";
    }
}

// ---------------- CORE FLOW (NO BLOCKING) ----------------
function loop() {

    clearInterval(breath);
    clearInterval(timer);

    const cont = get("step-content");
    const next = ensureNext();
    const map = ensureMap();

    if (tiempo <= 0 || i >= pasos.length) return end(next, map);

    const p = pasos[i];

    next.onclick = () => {
        if (bloqueo) return;
        i++;
        loop();
    };

    // BREATH MODE
    if (p.t === "breath_auto") {
        breathMode(p.d || 10);
        return;
    }

    if (tipo === "Casa") timerMode();

    const txt = p.tx?.es || p.story?.es || "";

    cont.innerHTML = `<div>${txt}</div>`;

    hablar(txt);

    tiempo -= 4;

    next.style.display = "block";
}

// ---------------- BREATH (ISOLATED SAFE LOOP) ----------------
function breathMode(sec) {

    const cont = get("step-content");
    let s = sec;

    bloqueo = true;

    cont.innerHTML = `
        <div>
            <div id="breathingCircle"></div>
            <h2 id="breathLabel">Inhala</h2>
        </div>
    `;

    const circle = get("breathingCircle");

    breath = setInterval(() => {

        if (s <= 0) {
            clearInterval(breath);
            bloqueo = false;
            i++;
            loop();
            return;
        }

        const phase = s % 2 === 0 ? "Inhala" : "Exhala";

        get("breathLabel").innerText = phase;

        if (circle) {
            circle.style.transform = phase === "Inhala"
                ? "scale(1.25)"
                : "scale(0.95)";
        }

        if (s % 4 === 0) hablar(phase);

        s--;
        tiempo--;

    }, 1000);
}

// ---------------- TIMER (SINGLE INSTANCE) ----------------
function timerMode() {

    if (timer) return;

    const t = get("timer");

    timer = setInterval(() => {

        const m = Math.floor(tiempo / 60);
        const s = tiempo % 60;

        if (t) t.innerText = `${m}:${s.toString().padStart(2, "0")}`;

        tiempo--;

        if (tiempo <= 0) clearInterval(timer);

    }, 1000);
}

// ---------------- END ----------------
function end(next, map) {

    get("step-content").innerHTML = `<h2>Sesión completada</h2>`;

    if (tipo === "Salida") {
        map.style.display = "block";
        map.href = lugar?.gps_link || "#";
    } else {
        next.innerText = "REINICIAR";
        next.style.display = "block";
        next.onclick = () => location.reload();
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
