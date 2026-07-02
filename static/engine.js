// OPEN THAN GO SYSTEM - Frontend Engine v4 FINAL
// Company: May Roga LLC

let idiomaActual = "es";
let presupuestoActual = "cero";
let modalidadSalir = true;

let pasosMisionGlobal = [];
let indicePasoActual = 0;
let datosLugarGlobal = null;
let tipoEscapeGlobal = "";

let intervaloRespiracion = null;
let intervaloTimer = null;
let tiempoRestante = 0;

// ------------------------------
// SAFE GET
// ------------------------------
function get(id) {
    return document.getElementById(id);
}

// ------------------------------
// VOZ CONTROLADA (SIN MEZCLA)
// ------------------------------
function hablar(texto) {
    if (!("speechSynthesis" in window)) return;
    if (!texto) return;

    const u = new SpeechSynthesisUtterance(texto);
    const voces = speechSynthesis.getVoices();

    let voice = null;

    if (idiomaActual === "es") {
        voice =
            voces.find(v => v.lang === "es-ES") ||
            voces.find(v => v.lang.startsWith("es"));
    }

    if (idiomaActual === "en") {
        voice =
            voces.find(v => v.lang === "en-US") ||
            voces.find(v => v.lang.startsWith("en"));
    }

    if (!voice) voice = voces[0];

    u.voice = voice;
    u.lang = idiomaActual === "es" ? "es-ES" : "en-US";
    u.rate = 0.95;
    u.pitch = 1;

    speechSynthesis.cancel();
    speechSynthesis.speak(u);
}

// ------------------------------
// TRADUCCIÓN SEGURA
// ------------------------------
function t(p) {
    if (!p) return "";
    if (typeof p === "string") return p;
    return p[idiomaActual] || p.es || p.en || "";
}

// ------------------------------
// INIT
// ------------------------------
document.addEventListener("DOMContentLoaded", () => {
    const btn = get("btn-start");
    if (btn) btn.onclick = solicitarEscape;
});

// ------------------------------
// IDIOMA
// ------------------------------
function cambiarIdioma(lang) {
    idiomaActual = lang;

    get("lang-es")?.classList.toggle("active", lang === "es");
    get("lang-en")?.classList.toggle("active", lang === "en");
}

// ------------------------------
// PRESUPUESTO
// ------------------------------
function cambiarBolsillo(opcion) {
    presupuestoActual = opcion;

    ["cero", "minimo", "moderado", "libre"].forEach(v => {
        const el = get(`b-${v}`);
        if (el) el.classList.toggle("active", v === opcion);
    });
}

// ------------------------------
// MODALIDAD
// ------------------------------
function cambiarModalidad(esSalir) {
    modalidadSalir = esSalir;

    get("m-salir")?.classList.toggle("active", esSalir);
    get("m-casa")?.classList.toggle("active", !esSalir);
}

// ------------------------------
// MAIN REQUEST
// ------------------------------
async function solicitarEscape() {

    const payload = {
        decision: modalidadSalir ? "salir" : "casa",
        lang: idiomaActual,
        budget_level: presupuestoActual,
        zip_code: get("inp-zip")?.value || "",
        estado: get("inp-state")?.value || "",
        region: get("inp-region")?.value || "",
        desahogo: get("inp-text")?.value || ""
    };

    get("wrapper-form").style.display = "none";
    get("wrapper-loader").style.display = "flex";
    get("wrapper-interactive").style.display = "none";

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

        setTimeout(() => {

            get("wrapper-loader").style.display = "none";
            get("wrapper-interactive").style.display = "block";

            pasosMisionGlobal = data.mision?.b || [];
            datosLugarGlobal = data.lugar || null;
            tipoEscapeGlobal = data.tipo || "";

            indicePasoActual = 0;

            iniciarFlujo();

        }, 500);

    } catch (e) {
        console.error(e);
        alert("Error de conexión");
        get("wrapper-form").style.display = "block";
    }
}

// ------------------------------
// FLUJO PRINCIPAL
// ------------------------------
function iniciarFlujo() {

    clearInterval(intervaloRespiracion);
    clearInterval(intervaloTimer);
    window.speechSynthesis.cancel();

    const cont = get("step-content");
    const btnNext = ensureNext();
    const btnMap = ensureMap();

    if (indicePasoActual >= pasosMisionGlobal.length) {

        if (tipoEscapeGlobal === "Salida") {
            btnMap.style.display = "block";
            btnMap.href = datosLugarGlobal?.gps_link || "#";
        } else {
            btnNext.innerText = "FINALIZAR";
            btnNext.style.display = "block";
            btnNext.onclick = () => location.reload();
        }
        return;
    }

    const paso = pasosMisionGlobal[indicePasoActual];

    btnNext.onclick = () => {
        indicePasoActual++;
        iniciarFlujo();
    };

    // ---------------- BREATH ----------------
    if (paso.t === "breath_auto") {
        iniciarRespiracion(paso.d || 10);
        return;
    }

    // ---------------- TIMER CASA ----------------
    if (tipoEscapeGlobal === "Casa") {
        iniciarTimer(600);
    }

    const contenido = paso.tx || paso.story || paso;
    cont.innerHTML = `<div class="fade">${t(contenido)}</div>`;
    hablar(t(contenido));

    btnNext.style.display = "block";
}

// ------------------------------
// RESPIRACIÓN (GLOBO AZUL/PLATEADO)
// ------------------------------
function iniciarRespiracion(segundos) {

    const cont = get("step-content");
    let s = segundos;

    cont.innerHTML = `
        <div class="breath-ui">
            <canvas id="breathCanvas"></canvas>
            <h2 id="breathLabel">Inhala</h2>
            <div id="breathTime"></div>
        </div>
    `;

    const canvas = document.getElementById("breathCanvas");
    const ctx = canvas.getContext("2d");

    canvas.width = 220;
    canvas.height = 220;

    let r = 45;
    let grow = true;

    intervaloRespiracion = setInterval(() => {

        ctx.clearRect(0, 0, 220, 220);

        ctx.beginPath();
        ctx.arc(110, 110, r, 0, Math.PI * 2);

        ctx.fillStyle = "rgba(180,220,255,0.35)";
        ctx.strokeStyle = "rgba(200,220,255,0.9)";
        ctx.lineWidth = 2;

        ctx.fill();
        ctx.stroke();

        r += grow ? 1.3 : -1.3;
        if (r > 75) grow = false;
        if (r < 45) grow = true;

        get("breathLabel").innerText = grow ? "Inhala" : "Exhala";
        get("breathTime").innerText = s + "s";

        s--;

        if (s <= 0) {
            clearInterval(intervaloRespiracion);
            indicePasoActual++;
            iniciarFlujo();
        }

    }, 1000);
}

// ------------------------------
// TIMER CASA (10 MIN)
// ------------------------------
function iniciarTimer(segundos) {

    const cont = get("step-content");
    let t = segundos;

    cont.innerHTML = `
        <div class="timer-ui">
            <h2>Sesión en casa</h2>
            <div id="clock"></div>
        </div>
    `;

    intervaloTimer = setInterval(() => {

        let m = Math.floor(t / 60);
        let s = t % 60;

        get("clock").innerText = `${m}:${s.toString().padStart(2, "0")}`;

        t--;

        if (t <= 0) {
            clearInterval(intervaloTimer);
            get("step-content").innerHTML = "<h2>Sesión completada</h2>";
        }

    }, 1000);
}

// ------------------------------
// BOTONES SAFE
// ------------------------------
function ensureNext() {
    let b = get("btn-next");
    if (!b) {
        b = document.createElement("button");
        b.id = "btn-next";
        b.className = "btn-next-step";
        get("wrapper-interactive").appendChild(b);
    }
    b.style.display = "none";
    b.innerText = "CONTINUAR";
    return b;
}

function ensureMap() {
    let b = get("btn-maps-action");
    if (!b) {
        b = document.createElement("a");
        b.id = "btn-maps-action";
        b.className = "btn-maps-route";
        get("wrapper-interactive").appendChild(b);
    }
    b.style.display = "none";
    b.innerText = "ABRIR MAPA";
    return b;
}
