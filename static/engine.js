// OPEN THAN GO SYSTEM - Frontend Engine v5 PRO
// May Roga LLC

// =========================
// STATE GLOBAL
// =========================
let idiomaActual = "es";
let presupuestoActual = "cero";
let modalidadSalir = true;

let pasosMisionGlobal = [];
let indicePasoActual = 0;

let datosLugarGlobal = null;
let tipoEscapeGlobal = "";

let intervaloRespiracion = null;
let intervaloTimer = null;

// control de voz
let vozLista = [];
let vozReady = false;

// =========================
// SAFE DOM
// =========================
const $ = (id) => document.getElementById(id);

// =========================
// INIT VOZ
// =========================
function initVoz() {
    if (!("speechSynthesis" in window)) return;

    const cargar = () => {
        vozLista = speechSynthesis.getVoices();
        vozReady = true;
    };

    cargar();
    speechSynthesis.onvoiceschanged = cargar;
}

// =========================
// VOZ PROFESIONAL (CONSISTENTE)
// =========================
function hablar(texto) {
    if (!texto || !("speechSynthesis" in window)) return;

    speechSynthesis.cancel();

    const u = new SpeechSynthesisUtterance(texto);

    let v = null;

    if (idiomaActual === "es") {
        v =
            vozLista.find(x => x.lang === "es-ES") ||
            vozLista.find(x => x.lang?.startsWith("es"));
    } else {
        v =
            vozLista.find(x => x.lang === "en-US") ||
            vozLista.find(x => x.lang?.startsWith("en"));
    }

    u.voice = v || vozLista[0];
    u.lang = idiomaActual === "es" ? "es-ES" : "en-US";
    u.rate = 0.92;
    u.pitch = 1;

    speechSynthesis.speak(u);
}

// =========================
// TRADUCCIÓN SEGURA
// =========================
function t(obj) {
    if (!obj) return "";
    if (typeof obj === "string") return obj;
    return obj[idiomaActual] || obj.es || obj.en || "";
}

// =========================
// INIT APP
// =========================
document.addEventListener("DOMContentLoaded", () => {
    initVoz();

    const btn = $("btn-start");
    if (btn) btn.onclick = solicitarEscape;
});

// =========================
// UI HELPERS
// =========================
function setScreen(mode) {
    const form = $("wrapper-form");
    const load = $("wrapper-loader");
    const app = $("wrapper-interactive");

    if (form) form.style.display = mode === "form" ? "block" : "none";
    if (load) load.style.display = mode === "loading" ? "flex" : "none";
    if (app) app.style.display = mode === "app" ? "block" : "none";
}

// =========================
// CONFIG UI
// =========================
function cambiarIdioma(lang) {
    idiomaActual = lang;
    $("lang-es")?.classList.toggle("active", lang === "es");
    $("lang-en")?.classList.toggle("active", lang === "en");
}

function cambiarBolsillo(opcion) {
    presupuestoActual = opcion;

    ["cero", "minimo", "moderado", "libre"].forEach(v => {
        $("b-" + v)?.classList.toggle("active", v === opcion);
    });
}

function cambiarModalidad(val) {
    modalidadSalir = val;
    $("m-salir")?.classList.toggle("active", val);
    $("m-casa")?.classList.toggle("active", !val);
}

// =========================
// REQUEST BACKEND
// =========================
async function solicitarEscape() {

    setScreen("loading");

    const payload = {
        decision: modalidadSalir ? "salir" : "casa",
        lang: idiomaActual,
        budget_level: presupuestoActual,
        zip_code: $("inp-zip")?.value || "",
        estado: $("inp-state")?.value || "",
        region: $("inp-region")?.value || "",
        desahogo: $("inp-text")?.value || ""
    };

    try {
        const res = await fetch("/api/open-than-go", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!data || data.status !== "success") {
            throw new Error("backend error");
        }

        pasosMisionGlobal = data.mision?.b || [];
        datosLugarGlobal = data.lugar || null;
        tipoEscapeGlobal = data.tipo || "";

        indicePasoActual = 0;

        setTimeout(() => {
            setScreen("app");
            iniciarFlujo();
        }, 400);

    } catch (err) {
        console.error(err);
        alert("Error de conexión");
        setScreen("form");
    }
}

// =========================
// FLOW CORE
// =========================
function iniciarFlujo() {

    clearInterval(intervaloRespiracion);
    clearInterval(intervaloTimer);
    speechSynthesis.cancel();

    const cont = $("step-content");
    const btn = ensureNext();
    const map = ensureMap();

    if (indicePasoActual >= pasosMisionGlobal.length) {
        finalizarFlujo(btn, map);
        return;
    }

    const paso = pasosMisionGlobal[indicePasoActual];

    btn.onclick = () => {
        indicePasoActual++;
        iniciarFlujo();
    };

    btn.style.display = "none";
    map.style.display = "none";

    // ================= BREATH STEP
    if (paso.t === "breath_auto") {
        iniciarRespiracion(paso.d || 10);
        return;
    }

    // ================= TIMER CASA
    if (tipoEscapeGlobal === "Casa") {
        iniciarTimer(600);
    }

    const contenido = paso.tx || paso.story || paso;
    const texto = t(contenido);

    cont.innerHTML = `<div class="fade">${texto}</div>`;
    hablar(texto);

    btn.style.display = "block";
}

// =========================
// FINAL FLOW
// =========================
function finalizarFlujo(btn, map) {

    const cont = $("step-content");

    if (tipoEscapeGlobal === "salir" || tipoEscapeGlobal === "Salida") {
        map.style.display = "block";
        map.href = datosLugarGlobal?.gps_link || "#";
        map.innerText = idiomaActual === "es" ? "ABRIR MAPA" : "OPEN MAP";
        return;
    }

    btn.innerText = idiomaActual === "es" ? "FINALIZAR" : "FINISH";
    btn.style.display = "block";
    btn.onclick = () => location.reload();

    cont.innerHTML = `<h2>${idiomaActual === "es" ? "Sesión completada" : "Session completed"}</h2>`;
}

// =========================
// RESPIRACIÓN PRO (UI MÁS VIVA)
// =========================
function iniciarRespiracion(segundos) {

    const cont = $("step-content");
    let s = segundos;
    let r = 50;
    let grow = true;

    cont.innerHTML = `
        <div class="breath-ui">
            <canvas id="breathCanvas"></canvas>
            <h2 id="breathLabel">Inhala</h2>
            <div id="breathTime"></div>
        </div>
    `;

    const canvas = $("breathCanvas");
    const ctx = canvas.getContext("2d");

    canvas.width = 240;
    canvas.height = 240;

    intervaloRespiracion = setInterval(() => {

        ctx.clearRect(0, 0, 240, 240);

        ctx.beginPath();
        ctx.arc(120, 120, r, 0, Math.PI * 2);

        ctx.fillStyle = "rgba(160,210,255,0.35)";
        ctx.strokeStyle = "rgba(200,230,255,0.9)";
        ctx.lineWidth = 2;

        ctx.fill();
        ctx.stroke();

        r += grow ? 1.6 : -1.6;

        if (r > 80) grow = false;
        if (r < 50) grow = true;

        $("breathLabel").innerText = grow ? "Inhala" : "Exhala";
        $("breathTime").innerText = s + "s";

        s--;

        if (s <= 0) {
            clearInterval(intervaloRespiracion);
            indicePasoActual++;
            iniciarFlujo();
        }

    }, 1000);
}

// =========================
// TIMER CASA
// =========================
function iniciarTimer(segundos) {

    const cont = $("step-content");
    let t = segundos;

    cont.innerHTML = `
        <div class="timer-ui">
            <h2>Sesión en casa</h2>
            <div id="clock"></div>
        </div>
    `;

    intervaloTimer = setInterval(() => {

        const m = Math.floor(t / 60);
        const s = t % 60;

        $("clock").innerText = `${m}:${s.toString().padStart(2, "0")}`;

        t--;

        if (t <= 0) {
            clearInterval(intervaloTimer);
            $("step-content").innerHTML = "<h2>OK</h2>";
        }

    }, 1000);
}

// =========================
// SAFE BUTTONS
// =========================
function ensureNext() {
    let b = $("btn-next");

    if (!b) {
        b = document.createElement("button");
        b.id = "btn-next";
        b.className = "btn-next-step";
        $("wrapper-interactive").appendChild(b);
    }

    b.innerText = "CONTINUAR";
    b.style.display = "none";
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
    return b;
}
