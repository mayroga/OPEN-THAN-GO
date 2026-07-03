// OPEN THAN GO SYSTEM - Frontend Engine v5 (ORCHESTRATOR)
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

let flujoTiempoTotal = 0;
let flujoTiempoRestante = 0;

let lockAvance = false;

// ------------------------------
// SAFE GET
// ------------------------------
function get(id) {
    return document.getElementById(id);
}

// ------------------------------
// VOZ ORQUESTADA
// ------------------------------
function hablar(texto, delay = 0) {
    if (!("speechSynthesis" in window)) return;
    if (!texto) return;

    setTimeout(() => {
        const u = new SpeechSynthesisUtterance(texto);
        const voces = speechSynthesis.getVoices();

        let voice = null;

        if (idiomaActual === "es") {
            voice =
                voces.find(v => v.lang === "es-ES") ||
                voces.find(v => v.lang.startsWith("es"));
        } else {
            voice =
                voces.find(v => v.lang === "en-US") ||
                voces.find(v => v.lang.startsWith("en"));
        }

        if (!voice) voice = voces[0];

        u.voice = voice;
        u.lang = idiomaActual === "es" ? "es-ES" : "en-US";
        u.rate = 0.92;
        u.pitch = 1;

        speechSynthesis.cancel();
        speechSynthesis.speak(u);

    }, delay);
}

// ------------------------------
// SAFE TRANSLATE
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
// UI STATE CONTROL
// ------------------------------
function mostrarLoader() {
    get("wrapper-form").style.display = "none";
    get("wrapper-loader").style.display = "flex";
    get("wrapper-interactive").style.display = "none";
}

function mostrarFlujo() {
    get("wrapper-loader").style.display = "none";
    get("wrapper-interactive").style.display = "block";
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

    mostrarLoader();

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

            pasosMisionGlobal = data.mision?.b || [];
            datosLugarGlobal = data.lugar || null;
            tipoEscapeGlobal = data.tipo || "";

            indicePasoActual = 0;

            flujoTiempoTotal = tipoEscapeGlobal === "Casa" ? 600 : 60;
            flujoTiempoRestante = flujoTiempoTotal;

            mostrarFlujo();
            iniciarFlujo();

        }, 400);

    } catch (e) {
        console.error(e);
        alert("Error de conexión");
        get("wrapper-form").style.display = "block";
    }
}

// ------------------------------
// FLUJO PRINCIPAL ORQUESTADO
// ------------------------------
function iniciarFlujo() {

    clearInterval(intervaloRespiracion);
    clearInterval(intervaloTimer);
    window.speechSynthesis.cancel();

    const cont = get("step-content");
    const btnNext = ensureNext();
    const btnMap = ensureMap();

    // ---------------- FINAL ----------------
    if (flujoTiempoRestante <= 0 || indicePasoActual >= pasosMisionGlobal.length) {

        finalizarFlujo(btnNext, btnMap);
        return;
    }

    const paso = pasosMisionGlobal[indicePasoActual];

    btnNext.onclick = () => {
        if (lockAvance) return;
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
        iniciarTimerGlobal();
    }

    const contenido = paso.tx || paso.story || paso;
    const texto = t(contenido);

    cont.innerHTML = `<div class="fade">${texto}</div>`;

    hablar(texto, 300);

    flujoTiempoRestante -= 8;

    btnNext.style.display = "block";
}

// ------------------------------
// FINAL FLOW
// ------------------------------
function finalizarFlujo(btnNext, btnMap) {

    const cont = get("step-content");

    cont.innerHTML = `
        <div class="fade">
            <h2>Sesión completada</h2>
            <p>${tipoEscapeGlobal === "Casa"
                ? "Has completado tu regulación interna."
                : "Has completado tu micro-escape externo."}
            </p>
        </div>
    `;

    if (tipoEscapeGlobal === "Salida") {
        btnMap.style.display = "block";
        btnMap.href = datosLugarGlobal?.gps_link || "#";
    } else {
        btnNext.innerText = "REINICIAR";
        btnNext.style.display = "block";
        btnNext.onclick = () => location.reload();
    }
}

// ------------------------------
// BREATHING ENGINE (SYNC VOICE)
// ------------------------------
function iniciarRespiracion(segundos) {

    const cont = get("step-content");
    let s = segundos;

    cont.innerHTML = `
        <div class="breath-ui">
            <div id="breathingCircle"></div>
            <h2 id="breathLabel">Inhala</h2>
            <div id="breathTime"></div>
        </div>
    `;

    const circle = get("breathingCircle");

    lockAvance = true;

    intervaloRespiracion = setInterval(() => {

        if (s <= 0) {
            clearInterval(intervaloRespiracion);
            lockAvance = false;
            indicePasoActual++;
            iniciarFlujo();
            return;
        }

        const phase = s % 2 === 0 ? "Inhala" : "Exhala";

        get("breathLabel").innerText = phase;
        get("breathTime").innerText = `${s}s`;

        if (circle) {
            circle.style.transform =
                phase === "Inhala"
                    ? "scale(1.4)"
                    : "scale(0.9)";
        }

        if (s % 4 === 0) {
            hablar(phase, 0);
        }

        s--;
        flujoTiempoRestante--;

    }, 1000);
}

// ------------------------------
// TIMER GLOBAL CASA (10 MIN CONTROL)
// ------------------------------
function iniciarTimerGlobal() {

    if (intervaloTimer) return;

    const t = get("timer");

    intervaloTimer = setInterval(() => {

        let m = Math.floor(flujoTiempoRestante / 60);
        let s = flujoTiempoRestante % 60;

        if (t) {
            t.innerText = `${m}:${s.toString().padStart(2, "0")}`;
        }

        flujoTiempoRestante--;

        if (flujoTiempoRestante <= 0) {
            clearInterval(intervaloTimer);
        }

    }, 1000);
}

// ------------------------------
// BUTTON SAFE
// ------------------------------
function ensureNext() {
    let b = get("btn-next");
    if (!b) {
        b = document.createElement("button");
        b.id = "btn-next";
        b.className = "btn-next-step";
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
        b.className = "btn-maps-route";
        b.target = "_blank";
        get("wrapper-interactive").appendChild(b);
    }
    b.innerText = "ABRIR MAPA";
    b.style.display = "none";
    return b;
}
